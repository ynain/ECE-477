#ifndef HARDWARE_KEYPAD_DRIVER_H_
#define HARDWARE_KEYPAD_DRIVER_H_

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ti/devices/msp432p4xx/driverlib/gpio.h>
#include <ti/devices/msp432p4xx/driverlib/interrupt.h>
#include <ti/devices/msp432p4xx/driverlib/driverlib.h>
//
#include <Headers/TIMER_handle.h>
#include <Headers/HC05_driver.h>


#include <inttypes.h>

#define ROW 4
#define COL 4
#define True 1
#define False 0

extern int connected; //from main

void Keypad_Init(void);
void GPIO_status(void);


#endif // HARDWARE_KEYPAD_DRIVER_H_
