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
char resp[BUFFER_SIZE];

typedef enum state_hc05 {DISCONNECTED, CONNECTED, PASSWORD, VERIFIED, READY} State_HC05;

State_HC05 curr_state;

static int hc05_count;

int verify_password(char*);
void setup_bluetooth_state(void);
int get_status_pin_val(void);
void connect_bluetooth(char*);
char start_recognition(void);
void reset_temp_buffer(char* buffer);
int look_for_char(char*, char);

State_HC05 getHC05State(); // get the current state
void setHC05State(State_HC05 s); // set the state

int get_hc05_count(void);
void set_hc05_count(int count);

#endif /* DEVICES_HC05_PINS_H_ */
