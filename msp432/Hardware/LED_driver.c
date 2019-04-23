/*
 * Leds.c
 *
 *  Created on: Apr 8, 2019
 *      Author: 477grp2
 */
#include <Headers/LED_driver.h>
#include <stdio.h>

#define GREEN  0
#define RED    1
#define YELLOW 2

typedef struct _LEDGPIO {
    uint_fast8_t port;
    uint_fast16_t pin;
}LEDGPIO;

extern LEDGPIO LEDs[3] = {{.port = GPIO_PORT_P5, .pin = GPIO_PIN6}, //green
                          {.port = GPIO_PORT_P5, .pin = GPIO_PIN4}, //red
                          {.port = GPIO_PORT_P5, .pin = GPIO_PIN5}}; //yellow


void leds_init(){

    MAP_GPIO_setAsOutputPin(LEDs[GREEN].port, LEDs[GREEN].pin); // green
    MAP_GPIO_setAsOutputPin(LEDs[RED].port, LEDs[RED].pin); // red
    MAP_GPIO_setAsOutputPin(LEDs[YELLOW].port, LEDs[YELLOW].pin); // yellow

    yellow_on();
    green_off();
    red_off();
    printf("LEDs init\n");

}

void yellow_on(void){
    GPIO_setOutputHighOnPin(LEDs[YELLOW].port, LEDs[YELLOW].pin);
}
void yellow_off(void){
    GPIO_setOutputLowOnPin(LEDs[YELLOW].port, LEDs[YELLOW].pin);
}
void toggle_yellow(void){
    GPIO_toggleOutputOnPin(LEDs[YELLOW].port, LEDs[YELLOW].pin);
}

void red_on(void){
    GPIO_setOutputHighOnPin(LEDs[RED].port, LEDs[RED].pin);
}
void red_off(void){
    GPIO_setOutputLowOnPin(LEDs[RED].port, LEDs[RED].pin);
}
void toggle_red(void){
    GPIO_toggleOutputOnPin(LEDs[RED].port, LEDs[RED].pin);
}

void green_on(void){
    GPIO_setOutputHighOnPin(LEDs[GREEN].port, LEDs[GREEN].pin);
}
void green_off(void){
    GPIO_setOutputLowOnPin(LEDs[GREEN].port, LEDs[GREEN].pin);
}
void toggle_green(void){
    GPIO_toggleOutputOnPin(LEDs[GREEN].port, LEDs[GREEN].pin);
}
