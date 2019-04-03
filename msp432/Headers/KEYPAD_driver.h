#ifndef HARDWARE_KEYPAD_DRIVER_H_
#define HARDWARE_KEYPAD_DRIVER_H_

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ti/devices/msp432p4xx/driverlib/gpio.h>
#include <ti/devices/msp432p4xx/driverlib/interrupt.h>


void Keypad_Init(void);
void GPIO_status(void);


void red_on(void);
void red_off(void);
void yellow_on(void);
void yellow_off(void);
void toggle_yellow(void);
void green_on(void);
void green_off(void);

#endif // HARDWARE_KEYPAD_DRIVER_H_
