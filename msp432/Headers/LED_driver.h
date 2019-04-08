/*
 * Leds.h
 *
 *  Created on: Apr 8, 2019
 *      Author: 477grp2
 */

#ifndef HEADERS_LED_DRIVER_H_
#define HEADERS_LED_DRIVER_H_

#include <ti/devices/msp432p4xx/driverlib/gpio.h>
#include <ti/devices/msp432p4xx/driverlib/driverlib.h>

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
