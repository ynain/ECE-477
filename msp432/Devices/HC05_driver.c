/*
 * HC05_pins.c
 *
 *  Created on: Mar 22, 2019
 *      Author: 477grp2
 */

#include <Headers/HC05_driver.h>
#include <Headers/LOCK_handler.h>
#include <Headers/LED_driver.h>
#include <Headers/MSPIO.h>
#include <C:/ti/simplelink_msp432p4_sdk_2_40_00_10/source/ti/devices/msp432p4xx/driverlib/gpio.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int pswVerified = False;


void setup_bluetooth_state(void) {
    printf("Bluetooth state init\n");
    MAP_GPIO_setAsInputPin(GPIO_PORT_P4, GPIO_PIN1);
    setHC05State(DISCONNECTED);

}
void reset_temp_buffer(char* buffer){
    int i=0;
    for(i=0; i<BUFFER_SIZE; ++i) buffer[i] = 0x00;
}

int get_status_pin_val(void) {
    return GPIO_getInputPinValue(GPIO_PORT_P4, GPIO_PIN1);
}

void connect_bluetooth(char* password){
    char c = 0x00;
    int x = 0;
    static char bt_pwd[8];



    if(!get_status_pin_val()){
        setHC05State(DISCONNECTED);
        red_off();
        green_off();
        return;
    }
    if(getHC05State() == READY) return;
    if(get_status_pin_val()) setHC05State(CONNECTED);

    if(getHC05State() == CONNECTED){
        green_off();
        setHC05State(PASSWORD);
    }

    if(getHC05State() == PASSWORD){ //keep trying to fetch the password
        MSPrintf(EUSCI_A2_BASE, "pswd\n", BUFFER_SIZE);

        while(x < 8){
            x = getUARTRecieved();


        }
        UART_Read(EUSCI_A2_BASE,(uint8_t*)&bt_pwd, 8);
        setUARTRecieved(0);
        x = 0;

        setHC05State(VERIFIED);
    }

    if(getHC05State() == VERIFIED){
        MSPrintf(EUSCI_A2_BASE, "boot\n", BUFFER_SIZE);
        while(x < 1){
            x = getUARTRecieved();
        }
        UART_Read(EUSCI_A2_BASE,(uint8_t*)&c, 1);
        setUARTRecieved(0);
        x=0;

        if(c == 'c') {
            setHC05State(READY);
            red_on();
        }
    }

}

int look_for_char(char* buffer, char c){
    int i;
    for(i=0; i<BUFFER_SIZE; i++){
        if(buffer[i] == c || buffer[i] == (c+0x20)) return True;
    }
    return False;
}

char start_recognition(){
    char c = 0x00;
    if(getHC05State() != READY) return 0x00;
    MSPrintf(EUSCI_A2_BASE, "start\n", BUFFER_SIZE);
    if(UART_Read(EUSCI_A2_BASE, (uint8_t*)&c, 1) != 0){
        if(c == 'p' || c == 'P') return 'p';
        else if(c == 'f' || c == 'F') return 'f';
        else if(c == 'l' || c == 'L') {
            setHC05State(DISCONNECTED);
            return 'l';
        }
        else return 0x00;
    }
    return 0x00;
}

int verify_password(char * password){
    int numComp;
    int i;

    if((numComp = strncmp(pswrd_comp, password, strlen(pswrd_comp) - 2)) == 0) {
        reset_temp_buffer(pswrd_comp);
        return True;
    }
    else {
        reset_temp_buffer(pswrd_comp);
        return False;
    }
}


int get_hc05_count(){
    return hc05_count;
}
void set_hc05_count(int count){
    hc05_count = count;
}


State_HC05 getHC05State(){
    return curr_state;
}

void setHC05State(State_HC05 s){
    curr_state = s;
}


