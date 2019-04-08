/*
 * Leds.c
 *
 *  Created on: Apr 8, 2019
 *      Author: 477grp2
 */
#include <Headers/LED_driver.h>
#include <stdio.h>

void leds_init(){

    MAP_GPIO_setAsOutputPin(GPIO_PORT_P2, GPIO_PIN3); // yellow
    MAP_GPIO_setAsOutputPin(GPIO_PORT_P3, GPIO_PIN7); // red
    MAP_GPIO_setAsOutputPin(GPIO_PORT_P3, GPIO_PIN5); // green

    yellow_off();
    green_off();
    red_off();
    printf("LEDs init\n");

}

void yellow_on(void){
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
void toggle_red(void){
    GPIO_toggleOutputOnPin(GPIO_PORT_P3, GPIO_PIN7);
}

void green_on(void){
    GPIO_setOutputHighOnPin(GPIO_PORT_P3, GPIO_PIN5);
}
void green_off(void){
    GPIO_setOutputLowOnPin(GPIO_PORT_P3, GPIO_PIN5);
}
void toggle_green(void){
    GPIO_toggleOutputOnPin(GPIO_PORT_P3, GPIO_PIN5);
}
