/*
 * aKEYPAD_driver.c
 *
 *  Created on: Apr 1, 2019
 *      Author: 477grp2
 */
#include <Headers/KEYPAD_driver.h>

char keys_pressed[20]; // array holding button pressed, used for testing
int period = 2*24000000; // number of ticks per period, aligns with master clock operating at 24Mhz
int threshold = 120000;
int last_time_pressed = -1; // last press detected time stamp
int verifying = 0;

typedef struct _KeypadGPIO {
    uint_fast8_t port;
    uint_fast16_t pin;
}KeypadGPIO;


//GPIO OUT (PORT 2)
// 2.4, 2.5, 2.6, 2.7

//GPIO IN (PORT 6)
// 6.4, 6.5, 6.6, 6.7

extern KeypadGPIO ButtonKeys[8] = {
                                   //Columns
                 {.port = GPIO_PORT_P2, .pin = GPIO_PIN4},
                 {.port = GPIO_PORT_P2, .pin = GPIO_PIN5},
                 {.port = GPIO_PORT_P2, .pin = GPIO_PIN6},
                 {.port = GPIO_PORT_P2, .pin = GPIO_PIN7},
                                    //Rows
                 {.port = GPIO_PORT_P6, .pin = GPIO_PIN4},
                 {.port = GPIO_PORT_P6, .pin = GPIO_PIN5},
                 {.port = GPIO_PORT_P6, .pin = GPIO_PIN6},
                 {.port = GPIO_PORT_P6, .pin = GPIO_PIN7}};

extern char Buttons [ROW][COL] = {{'1', '2', '3', 'A'},
                                  {'4', '5', '6', 'B'},
                                  {'7', '8', '9', 'C'},
                                  {'0', 'F', 'E', 'D'}};

void keypad_init(void) {

    int i;


    for (i=0; i<COL; i++){
        MAP_GPIO_setAsOutputPin(ButtonKeys[i].port, ButtonKeys[i].pin);
        MAP_GPIO_setOutputHighOnPin(ButtonKeys[i].port, ButtonKeys[i].pin);
    }

    for (i=4; i<ROW+4; i++) {
        MAP_GPIO_setAsInputPinWithPullDownResistor(ButtonKeys[i].port, ButtonKeys[i].pin);
        MAP_GPIO_clearInterruptFlag(ButtonKeys[i].port, ButtonKeys[i].pin);
        MAP_GPIO_interruptEdgeSelect(ButtonKeys[i].port, ButtonKeys[i].pin, GPIO_LOW_TO_HIGH_TRANSITION);
        MAP_GPIO_enableInterrupt(ButtonKeys[i].port, ButtonKeys[i].pin);
    }

    MAP_Interrupt_enableInterrupt(INT_PORT6);

    printf("Keypad Init \n");
    return;

}

void PORT6_IRQHandler(void){

    // get the port status and clear the interrupt
    uint32_t status = GPIO_getEnabledInterruptStatus(GPIO_PORT_P6);

    int current_time;
    char button_pressed;
    int was_button_pressed;
    char password[5] = {'1', '2', '3', '4', '5'};
    //int incorrect = 0;
    int pin_value;
    int i;
    int j;

    current_time = SysTick_getValue();

    if(lockIsBusy() == 1){
        //printf("locking & unlocking are both True\n");
        return;
    }
    //Threshold conditions...
    if(last_time_pressed != -1 && current_time < last_time_pressed && last_time_pressed - current_time < threshold ){
        //GPIO_toggleOutputOnPin(GPIO_PORT_P2, GPIO_PIN3);
        //toggle_yellow();
        return;
    }
    if(last_time_pressed != -1 && last_time_pressed < current_time && period - last_time_pressed + current_time < threshold){
        //GPIO_toggleOutputOnPin(GPIO_PORT_P2, GPIO_PIN3);
        //printf("lol nah\n");
        return;
    }

    last_time_pressed = current_time;
    was_button_pressed = False;

    // Toggle off
    for (i=0; i<4; i++) {
        GPIO_setOutputLowOnPin(ButtonKeys[i].port, ButtonKeys[i].pin);
    }

    //Toggle individual
    for (i=0; i<4; i++) {

        GPIO_setOutputHighOnPin(ButtonKeys[i].port, ButtonKeys[i].pin); //toggle col
        for(j = 0; j < 4; j ++){
            pin_value = GPIO_getInputPinValue(6, ButtonKeys[j + 4].pin); //check row

            if(pin_value){
                button_pressed = Buttons[j][i]; //todo: was [j][i]
                was_button_pressed = True;

                //send the button pressed to the lock handler
                lock_button_pressed(button_pressed);
                GPIO_setOutputLowOnPin(ButtonKeys[i].port, ButtonKeys[i].pin);
                break;
            }
        }
        if(was_button_pressed){
            keys_pressed[get_kp_count()] = button_pressed;
            set_kp_count(get_kp_count()+1);//kp_count++;
            break;
        }
        GPIO_setOutputLowOnPin(ButtonKeys[i].port, ButtonKeys[i].pin);
    }

    //Logic handled in the lock handler now
    /*
    if(get_kp_count() % 5 == 0 && get_kp_count() > 0){
        for(i=get_kp_count()-5; i<get_kp_count(); i++){
                if(keys_pressed[i] != password[i % 5]){
                    incorrect--;
                    printf("last_time_pressed: %d\n", last_time_pressed);
                    printf("kp_count: %d, button pressed: %c is not %c \n", get_kp_count(), keys_pressed[i], password[i % 5]);
                }
                else{
                    printf("button pressed: %c \n", keys_pressed[i]);
                }
         }

        // Logic in the lock handler now
        if(incorrect == 0){
            green_on();
            yellow_off();
            set_overflow_count(0);
            //overflow_count = 0;
            set_unlocking(1);
            printf("Unlocking...\n");
        }
        else {

            set_locking(1);
            red_on();
            yellow_off();
            set_overflow_count(0);
            //overflow_count = 0;
            printf("Remain locked\n");
        }

        incorrect = 0;
    }*/


    //Toggle back on to be able to go back to the interrupt

    for (i=0; i<4; i++) {
        GPIO_setOutputHighOnPin(ButtonKeys[i].port, ButtonKeys[i].pin);
    }

    MAP_GPIO_clearInterruptFlag(GPIO_PORT_P6, status);
}
/*
void SysTick_Handler(void)
{


    if(overflow_count > 5 && locking){
        locking = 0;
        red_off();
    }

    if(overflow_count > 5 && unlocking){
        unlocking = 0;
        green_off();
    }
    if(kp_count % 5 == 0 && locking == 1 || unlocking == 1){
        yellow_off();
    }
    if(kp_count % 5 == 0 && locking == 0 && unlocking == 0){
        //toggle_yellow();
    }
    if(kp_count % 5 != 0 && locking == 0 && unlocking == 0){
        //yellow_on();
    }
    overflow_count++;
    //GPIO_toggleOutputOnPin(GPIO_PORT_P3, GPIO_PIN7);

}*/

/*void yellow_on(void){
    GPIO_setOutputHighOnPin(GPIO_PORT_P2, GPIO_PIN3);
}
void yellow_off(void){
    GPIO_setOutputLowOnPin(GPIO_PORT_P2, GPIO_PIN3);
}
void toggle_yellow(void){
    GPIO_toggleOutputOnPin(GPIO_PORT_P2, GPIO_PIN3);
}
void red_on(void){
    GPIO_setOutputHighOnPin(GPIO_PORT_P3, GPIO_PIN7);
}
void red_off(void){
    GPIO_setOutputLowOnPin(GPIO_PORT_P3, GPIO_PIN7);
}
void green_on(void){
    GPIO_setOutputHighOnPin(GPIO_PORT_P3, GPIO_PIN5);
}
void green_off(void){
    GPIO_setOutputLowOnPin(GPIO_PORT_P3, GPIO_PIN5);
}*/


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



