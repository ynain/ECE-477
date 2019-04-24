/*
 * HC05_pins.c
 *
 *  Created on: Mar 22, 2019
 *      Author: 477grp2
 */

#include <Headers/HC05_driver.h>
#include <Headers/LOCK_handler.h>
#include <Headers/MSPIO.h>
#include <C:/ti/simplelink_msp432p4_sdk_2_40_00_10/source/ti/devices/msp432p4xx/driverlib/gpio.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int pswVerified = False;

void setup_bluetooth_state(void) {
    printf("Bluetooth state init\n");
    MAP_GPIO_setAsInputPin(GPIO_PORT_P4, GPIO_PIN1);
}
void reset_temp_buffer(void){
    int i=0;
    for(i=0; i<BUFFER_SIZE; ++i) pswrd_comp[i] = 0x00;
}

int get_state_status(void) {
    return GPIO_getInputPinValue(GPIO_PORT_P4, GPIO_PIN1);
}

void connect_bluetooth(char* password){
    char c = 0x00;
    if(!get_state_status()){
        //printf("not connected to pi through BT...\n");
        connected = False;
        return;
    }
    if(connected && get_state_status()) return;
    if(get_state_status() && !connected){
        if(!get_password(password)) {
           // printf("wrong password\n");
            return;
        }
        reset_temp_buffer();

        //printf("correct password\n");
        MSPrintf(EUSCI_A2_BASE, "boot\n", BUFFER_SIZE);
        //printf("sending boot signal...\n");

        if(UART_Read(EUSCI_A2_BASE, (uint8_t*)&c, 1) != 0){
            if(c == 'c' || c == 'C') {
                printf("connected successfully\n");
                connected = True;
            } else printf("pi is responding, still trying to connect...\n");
        }
    }
    return;
}

char get_char(char c){
    if(c == 'l' || c == 'L') {
        printf("lost connection to server...\n");
        (connected) = False;
        return 'l';
    }
    else if(c == 'p' || c == 'P') {
        printf("face PASSED!\n");
        return 'p';
    }
    else if(c == 'f' || c == 'F') {
        printf("face FAILED!\n");
        return 'f';
    } else return 0x00;
}

int start_recognition(){
    char c = 0x00;
    int i;
    set_hc05_count(0);
    if(connected && get_state_status()) {
        MSPrintf(EUSCI_A2_BASE, " start\n", BUFFER_SIZE);
        return True;
     } else return False;

    return 0x00;
}

int get_password(char* password){
    int numComp = 0;
    MSPrintf(EUSCI_A2_BASE, "pswd\n", BUFFER_SIZE);
    //printf("sending pswd signal...\n");

    MSPgets(EUSCI_A2_BASE, pswrd_comp, BUFFER_SIZE);
    if((numComp = strncmp(pswrd_comp, password, strlen(pswrd_comp) - 2)) == 0) {
        reset_temp_buffer();
        return True;
    }
    else {
        reset_temp_buffer();
        return False;
    }

}

int get_hc05_count(){
    return hc05_count;
}
void set_hc05_count(int count){
    hc05_count = count;

}


