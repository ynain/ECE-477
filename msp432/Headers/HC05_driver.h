/*
 * HC05_pins.h
 *
 *  Created on: Mar 22, 2019
 *      Author: 477grp2
 */

#ifndef DEVICES_HC05_PINS_H_
#define DEVICES_HC05_PINS_H_

#include <stdlib.h>
#include <ti/devices/msp432p4xx/driverlib/gpio.h>
#include <ti/devices/msp432p4xx/driverlib/interrupt.h>
#include <ti/devices/msp432p4xx/driverlib/driverlib.h>
#include <inttypes.h>

#define True  1
#define False 0

char c = 0x00;

void setup_bluetooth_state(void);
int get_state_status(void);
void connect_bluetooth(int* connected);
void start_recognition(int* connected);


#endif /* DEVICES_HC05_PINS_H_ */
