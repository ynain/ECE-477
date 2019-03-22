#include "KEYPAD_driver.h"
#include <stdio.h>
#include <ti/devices/msp432p4xx/driverlib/driverlib.h>
#include <inttypes.h>

#define ROW 4
#define COL 4

typedef struct _KeypadGPIO {
    uint_fast8_t port;
    uint_fast16_t pin;
}KeypadGPIO;


//GPIO OUT (PORT 2)
// 2.4, 2.5, 2.6, 2.7

//GPIO IN (PORT 6)
// 6.4, 6.5, 6.6, 6.7

extern KeypadGPIO ButtonKeys[8] = {
                 {.port = GPIO_PORT_P2, .pin = GPIO_PIN4},
                 {.port = GPIO_PORT_P2, .pin = GPIO_PIN5},
                 {.port = GPIO_PORT_P2, .pin = GPIO_PIN6},
                 {.port = GPIO_PORT_P2, .pin = GPIO_PIN7},

                 {.port = GPIO_PORT_P6, .pin = GPIO_PIN4},
                 {.port = GPIO_PORT_P6, .pin = GPIO_PIN5},
                 {.port = GPIO_PORT_P6, .pin = GPIO_PIN6},
                 {.port = GPIO_PORT_P6, .pin = GPIO_PIN7},

};

extern char Buttons [ROW][COL] = {{'1', '2', '3', 'A'},
                                  {'4', '5', '6', 'B'},
                                  {'7', '8', '9', 'C'},
                                  {'0', 'F', 'E', 'D'}};


void GPIO_Init(void) {

    int i;

    for (i = 0; i < ROW; i++){
        MAP_GPIO_setAsOutputPin(ButtonKeys[i].port, ButtonKeys[i].pin);
        MAP_GPIO_clearInterruptFlag(ButtonKeys[i].port, ButtonKeys[i].pin);
        MAP_GPIO_enableInterrupt(ButtonKeys[i].port, ButtonKeys[i].pin);
        GPIO_setOutputHighOnPin(ButtonKeys[i].port, ButtonKeys[i].pin);
    }

    for (i=4; i<COL+4; i++) {
        MAP_GPIO_setAsInputPin(ButtonKeys[i].port, ButtonKeys[i].pin);
        MAP_GPIO_clearInterruptFlag(ButtonKeys[i].port, ButtonKeys[i].pin);
        MAP_GPIO_enableInterrupt(ButtonKeys[i].port, ButtonKeys[i].pin);

    }

    //MAP_Interrupt_enableInterrupt(INT_PORT2);
    //MAP_Interrupt_enableInterrupt(INT_PORT5);
    MAP_Interrupt_enableInterrupt(INT_PORT6);

    printf("GPIO Init \n");

}

void PORT6_IRQHandler(void){

    // get the port status
    uint32_t status = GPIO_getEnabledInterruptStatus(GPIO_PORT_P6);
    if(status != -0){
        printf("port 6 %x \n", status);
    }

    int i;
    int j;
    // Toggle off
    for (i=0; i< 4; i++) {
        GPIO_setOutputLowOnPin(ButtonKeys[i].port, ButtonKeys[i].pin);
    }

    //Toggle individual
    for (i=0; i< 4; i++) {

        GPIO_setOutputHighOnPin(ButtonKeys[i].port, ButtonKeys[i].pin);
        for(j = 0; j < 4; j ++){
            int pin_value;
            pin_value = GPIO_getInputPinValue(6, ButtonKeys[j + 4].pin);
            printf("pin value %d %d %d\n", i,j,pin_value);

            if(pin_value){
                printf(ButtonKeys[i].pin);
            }
        }

    }

    //Toggle back on
    for (i=0; i< 4; i++) {
        GPIO_setOutputHighOnPin(ButtonKeys[i].port, ButtonKeys[i].pin);
    }

    MAP_GPIO_clearInterruptFlag(GPIO_PORT_P2, status);
}


void GPIO_status(void) {

    int i;
    int j;
    int pin_value;

    for (i = 0; i < ROW; i++){

        // Set column Pin high
        GPIO_setOutputHighOnPin(ButtonKeys[i].port, ButtonKeys[i].pin);

        //Check each row
        for(j = 4; j < 8; j ++){

            pin_value = GPIO_getInputPinValue(ButtonKeys[j].port, ButtonKeys[j].pin);
            if(pin_value){
                printf("Row, Col pressed: %x, %x\n", j-4, i);
            }
        }
        // Set the column Pin Low
        GPIO_setOutputLowOnPin(ButtonKeys[i].port, ButtonKeys[i].pin);
    }

}
