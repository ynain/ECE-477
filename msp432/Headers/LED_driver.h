/*
 * Leds.h
 *
 *  Created on: Apr 8, 2019
 *      Author: 477grp2
 */

#ifndef HEADERS_LED_DRIVER_H_
#define HEADERS_LED_DRIVER_H_

#include <C:/ti/simplelink_msp432p4_sdk_2_40_00_10/source/ti/devices/msp432p4xx/driverlib/gpio.h>
#include <C:/ti/simplelink_msp432p4_sdk_2_40_00_10/source/ti/devices/msp432p4xx/driverlib/driverlib.h>

#include <Headers/LED_driver.h>

void leds_init();

void yellow_on(void);
void yellow_off(void);
void toggle_yellow(void);

void red_on(void);
void red_off(void);
void toggle_red(void);

void green_on(void);
void green_off(void);
void toggle_green(void);


#endif /* HEADERS_LED_DRIVER_H_ */
