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

void setup_bluetooth_state(void) {
    MAP_GPIO_setAsInputPin(GPIO_PORT_P4, GPIO_PIN1);
}

int get_state_status(void) {
    return GPIO_getInputPinValue(GPIO_PORT_P4, GPIO_PIN1);
}

void connect_bluetooth(int* connected){
    char c = 0x00;
    if(!(*connected)){
        printf("not connected yet\n");
        if(get_state_status()){
            MSPrintf(EUSCI_A2_BASE, "boot\n", BUFFER_SIZE);
            printf("sending boot signal...\n");
        }


        if(UART_Read(EUSCI_A2_BASE, (uint8_t*)&c, 1) != 0){
            if(c == 'c' || c == 'C') {
                printf("connected successfully\n");
                (*connected) = True;
            } else printf("pi is responding, still trying to connect...\n");
        } else printf("waiting for response from pi...\n");

    }
}

void start_recognition(int *connected, int DPressed){
    char c = 0x00;
    if(DPressed && (*connected)) {
        MSPrintf(EUSCI_A2_BASE, " start\n", BUFFER_SIZE);
        UART_Read(EUSCI_A2_BASE, (uint8_t*)&c, 1);
        if(c == 'l' || c == 'L') {
            printf("lost connection to server...\n");
            (*connected) = False;
        }
        else if(c == 'p' || c == 'P') {
            printf("face PASSED!\n");
        }
        else if(c == 'f' || c == 'F') {
            printf("face FAILED!\n");
        } else printf("unrecognized input...\n");
    }
}
