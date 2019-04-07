/*
 * TIMER_handle.c
 *
 *  Created on: Apr 7, 2019
 *      Author: 477grp2
 */
#include <Headers/TIMER_handle.h>
#include <Headers/KEYPAD_driver.h>
static int overflow_count = 0; // count the number of SysTick overflows that occur between presses
static int kp_count = 0; // count the key presses
static int timer_locking = 0;
static int timer_unlocking = 0;

void Timer_Init(void){

    MAP_SysTick_enableModule();
    MAP_SysTick_setPeriod(PERIOD);
    //MAP_Interrupt_enableSleepOnIsrExit();
    MAP_SysTick_enableInterrupt();

    printf("Timer init\n");

}

void set_overflow_count(int ovf_count){
    overflow_count = ovf_count;
}

void set_locking(int locking){
    timer_locking = locking;
}

int get_locking(void){
    return timer_locking;
}

void set_unlocking(int unlocking){
    timer_unlocking = unlocking;
}

int get_unlocking(void){
    return timer_unlocking;
}

void set_kp_count(int kp_cnt){
    kp_count = kp_cnt;
}

int get_kp_count(void){
    return kp_count;
}

void SysTick_Handler(void){

    // For keypad
    if(overflow_count > 5 && timer_locking){
        timer_locking = 0;
        red_off();
    }
    if(overflow_count > 5 && timer_unlocking){
        timer_unlocking = 0;
        green_off();
    }
    if(kp_count % 5 == 0 && timer_locking == 1 || timer_unlocking == 1){
        yellow_off();
    }
    if(kp_count % 5 == 0 && timer_locking == 0 && timer_unlocking == 0){
        toggle_yellow();
    }
    if(kp_count % 5 != 0 && timer_locking == 0 && timer_unlocking == 0){
        yellow_on();
    }
    overflow_count++;
    //GPIO_toggleOutputOnPin(GPIO_PORT_P3, GPIO_PIN7);
}



