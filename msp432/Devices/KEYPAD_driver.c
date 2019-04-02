/*
 * aKEYPAD_driver.c
 *
 *  Created on: Apr 1, 2019
 *      Author: 477grp2
 */
#include <Headers/KEYPAD_driver.h>
#include <stdio.h>
#include <ti/devices/msp432p4xx/driverlib/driverlib.h>
#include <inttypes.h>

#define ROW 4
#define COL 4
#define True 1
#define False 0

typedef struct _KeypadGPIO {
    uint_fast8_t port;
    uint_fast16_t pin;
}KeypadGPIO;


//GPIO OUT (PORT 2)
// 2.4, 2.5, 2.6, 2.7

//GPIO IN (PORT 6)
// 6.4, 6.5, 6.6, 6.7

int overflow_count = 0; // count the number of SysTick overflows that occur between presses
char keys_pressed[100]; // array holding button pressed, used for testing
int kp_count = 0; // count the key presses
int period = 24000000; // number of ticks per period, aligns with master clock operating at 24Mhz
int threshold = 3*240000;
int last_time_pressed = -1; // last press detected time stamp

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

void Keypad_Init(void) {

    int i;

    MAP_GPIO_setAsOutputPin(GPIO_PORT_P2, GPIO_PIN3);
    MAP_GPIO_setAsOutputPin(GPIO_PORT_P3, GPIO_PIN7);
    GPIO_setOutputHighOnPin(GPIO_PORT_P2, GPIO_PIN3);



    MAP_SysTick_enableModule();
    MAP_SysTick_setPeriod(period);
    MAP_Interrupt_enableSleepOnIsrExit();
    MAP_SysTick_enableInterrupt();

    for (i = 0; i < ROW; i++){
        MAP_GPIO_setAsOutputPin(ButtonKeys[i].port, ButtonKeys[i].pin);
        //MAP_GPIO_clearInterruptFlag(ButtonKeys[i].port, ButtonKeys[i].pin);
        //MAP_GPIO_enableInterrupt(ButtonKeys[i].port, ButtonKeys[i].pin);
        MAP_GPIO_setOutputHighOnPin(ButtonKeys[i].port, ButtonKeys[i].pin);
    }

    for (i=4; i<COL+4; i++) {
        MAP_GPIO_setAsInputPinWithPullUpResistor(ButtonKeys[i].port, ButtonKeys[i].pin);
        MAP_GPIO_clearInterruptFlag(ButtonKeys[i].port, ButtonKeys[i].pin);
        MAP_GPIO_interruptEdgeSelect(ButtonKeys[i].port, ButtonKeys[i].pin, GPIO_LOW_TO_HIGH_TRANSITION);
        MAP_GPIO_enableInterrupt(ButtonKeys[i].port, ButtonKeys[i].pin);

    }

    //MAP_Interrupt_enableInterrupt(INT_PORT2);
    //MAP_Interrupt_enableInterrupt(INT_PORT5);
    MAP_Interrupt_enableInterrupt(INT_PORT6);

    printf("GPIO Init \n");

}

void PORT6_IRQHandler(void){

    // get the port status and clear the interrupt
    uint32_t status = GPIO_getEnabledInterruptStatus(GPIO_PORT_P6);

    int current_time;
    char button_pressed;
    int was_button_pressed;
    char password[5] = {'1', 'A', '2', 'B', 'C'};
    int incorrect = 0;
    int pin_value;
    int i;
    int j;

    current_time = SysTick_getValue();


    //Threshold conditions...
    if(last_time_pressed != -1 && current_time < last_time_pressed && last_time_pressed - current_time < threshold ){
        //GPIO_toggleOutputOnPin(GPIO_PORT_P2, GPIO_PIN3);
        //printf("lol\n");
        return;
    }
    if(last_time_pressed != -1 && last_time_pressed < current_time && period - last_time_pressed + current_time < threshold){
        //GPIO_toggleOutputOnPin(GPIO_PORT_P2, GPIO_PIN3);
        //printf("lol nah\n");
        return;
    }

    last_time_pressed = current_time;
    overflow_count = 0;
    was_button_pressed = False;

    // Toggle off
    for (i=0; i< 4; i++) {
        GPIO_setOutputLowOnPin(ButtonKeys[i].port, ButtonKeys[i].pin);
    }

    //Toggle individual
    for (i=0; i< 4; i++) {

        GPIO_setOutputHighOnPin(ButtonKeys[i].port, ButtonKeys[i].pin);
        for(j = 0; j < 4; j ++){
            pin_value = GPIO_getInputPinValue(6, ButtonKeys[j + 4].pin);

            if(pin_value){
                button_pressed = Buttons[j][i];
                was_button_pressed = True;
                GPIO_toggleOutputOnPin(GPIO_PORT_P2, GPIO_PIN3);
                break;
            }
        }
        if(was_button_pressed){
            keys_pressed[kp_count] = button_pressed;
            kp_count++;
            break;
        }
    }

    if(kp_count % 5 == 0 && kp_count > 0){
        for(i=kp_count-5; i<kp_count; i++){
                if(keys_pressed[i] != password[i % 5]){
                    incorrect--;
                    printf("button pressed: %c is not %c \n", keys_pressed[i], password[i % 5]);
                }
                else{
                    printf("button pressed: %c \n", keys_pressed[i]);
                }
         }

        if(incorrect == 0){
            printf("Unlocking...\n");
        }
        else {
            printf("Remain locked, incorrect == %d \n", incorrect);
        }

        incorrect = 0;
    }


    //Toggle back on
    for (i=0; i< 4; i++) {
        GPIO_setOutputHighOnPin(ButtonKeys[i].port, ButtonKeys[i].pin);
    }

    MAP_GPIO_clearInterruptFlag(GPIO_PORT_P6, status);
}

void SysTick_Handler(void)
{
    GPIO_toggleOutputOnPin(GPIO_PORT_P3, GPIO_PIN7);
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



