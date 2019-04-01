#ifndef HARDWARE_KEYPAD_DRIVER_H_
#define HARDWARE_KEYPAD_DRIVER_H_

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ti/devices/msp432p4xx/driverlib/gpio.h>
#include <ti/devices/msp432p4xx/driverlib/interrupt.h>


void GPIO_Init(void);
void GPIO_status(void);

#endif // HARDWARE_KEYPAD_DRIVER_H_
