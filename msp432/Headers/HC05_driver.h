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
#include <Headers/MSPIO.h>

#define True  1
#define False 0
#define BUFFER_SIZE 128

char pswrd_comp[BUFFER_SIZE];

int get_password(char* password);
void setup_bluetooth_state(void);
int get_state_status(void);
void connect_bluetooth(int* connected, int* pswdVerified, char* password);
void start_recognition(int* connected, int DPressed);


#endif /* DEVICES_HC05_PINS_H_ */
