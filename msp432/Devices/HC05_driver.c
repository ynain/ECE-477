/*
 * HC05_pins.c
 *
 *  Created on: Mar 22, 2019
 *      Author: 477grp2
 */

#include <Headers/HC05_driver.h>
#include <Headers/MSPIO.h>
#include <ti/devices/msp432p4xx/driverlib/gpio.h>
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
    if(!connected){

        if(get_state_status()){
            //if(pswVerified) return;
            if(True){ //was else before
                if(!get_password(password)) {
                    printf("wrong password\n");
                    reset_temp_buffer();
                    return;
                } else {
                    reset_temp_buffer();
                }
            }
            reset_temp_buffer();
            printf("correct password\n");
            printf("not connected yet\n");
            MSPrintf(EUSCI_A2_BASE, "boot\n", BUFFER_SIZE);
            printf("sending boot signal...\n");
        }


        if(UART_Read(EUSCI_A2_BASE, (uint8_t*)&c, 1) != 0){
            if(c == 'c' || c == 'C') {
                printf("connected successfully\n");
                (connected) = True;
            } else printf("pi is responding, still trying to connect...\n");
        } //else printf("waiting for response from pi...\n");

    }
}

char start_recognition(){
    char c = 0x00;
    if(connected && get_state_status()) {
        MSPrintf(EUSCI_A2_BASE, " start\n", BUFFER_SIZE);
        UART_Read(EUSCI_A2_BASE, (uint8_t*)&c, 1);
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
        } else printf("unrecognized input...\n");
    } else printf("Pi is not connected...\n");
    return 0x00;
}

int get_password(char* password){
    int numComp = 0;
    MSPrintf(EUSCI_A2_BASE, " pswd\n", BUFFER_SIZE);
    printf("sending pswd signal...\n");

    MSPgets(EUSCI_A2_BASE, pswrd_comp, BUFFER_SIZE);
    if((numComp = strncmp(pswrd_comp, password, strlen(pswrd_comp) - 2)) == 0) {
        reset_temp_buffer();
        pswVerified = True;
        return True;
    }
    else {
        reset_temp_buffer();
        return False;
    }

}