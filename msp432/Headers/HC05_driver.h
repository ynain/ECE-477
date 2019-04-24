/*
 * HC05_pins.h
 *
 *  Created on: Mar 22, 2019
 *      Author: 477grp2
 */

#ifndef DEVICES_HC05_PINS_H_
#define DEVICES_HC05_PINS_H_

#include <stdlib.h>
#include <C:/ti/simplelink_msp432p4_sdk_2_40_00_10/source/ti/devices/msp432p4xx/driverlib/gpio.h>
#include <C:/ti/simplelink_msp432p4_sdk_2_40_00_10/source/ti/devices/msp432p4xx/driverlib/interrupt.h>
#include <C:/ti/simplelink_msp432p4_sdk_2_40_00_10/source/ti/devices/msp432p4xx/driverlib/driverlib.h>
#include <inttypes.h>
#include <Headers/MSPIO.h>

#define True  1
#define False 0
#define BUFFER_SIZE 128

int connected; // should refer to the extern variable
char pswrd_comp[BUFFER_SIZE];


static int hc05_count;

int get_password(char* password);
void setup_bluetooth_state(void);
int get_state_status(void);
void connect_bluetooth(char* password);
int start_recognition(void);
void reset_temp_buffer(void);
char get_char(char c);

int get_hc05_count(void);
void set_hc05_count(int count);

#endif /* DEVICES_HC05_PINS_H_ */
