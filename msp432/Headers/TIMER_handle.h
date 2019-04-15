#ifndef HEADERS_TIMER_HANDLE_H_
#define HEADERS_TIMER_HANDLE_H_


#define PERIOD (2*24000000)

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <inttypes.h>
#include <ti/devices/msp432p4xx/driverlib/gpio.h>
#include <ti/devices/msp432p4xx/driverlib/interrupt.h>
#include <ti/devices/msp432p4xx/driverlib/driverlib.h>
#include <Headers/LED_driver.h>
#include <Headers/LOCK_handler.h>

void Timer_Init(void);
void set_overflow_count(int ovf_count);
void set_locking(int locking);
int get_locking(void);
void set_unlocking(int unlocking);
int get_unlocking(void);
void set_kp_count(int kp_cnt);
int get_kp_count(void);

#endif /* HEADERS_TIMER_HANDLE_H_ */
