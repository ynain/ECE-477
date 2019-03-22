/*
 * HC05_pins.c
 *
 *  Created on: Mar 22, 2019
 *      Author: 477grp2
 */

#include "HC05_pins.h"

void setup_bluetooth_state(void) {
    MAP_GPIO_setAsInputPin(GPIO_PORT_P4, GPIO_PIN1);
}

int get_state_status(void) {
    return GPIO_getInputPinValue(GPIO_PORT_P4, GPIO_PIN1);
}
