/*
 * TIMER_handle.c
 *
 *  Created on: Apr 7, 2019
 *      Author: 477grp2
 */
#include <Headers/TIMER_handle.h>
#include <Headers/KEYPAD_driver.h>
#include <Headers/MSPIO.h>
static int overflow_count = 0; // count the number of SysTick overflows that occur between presses
static int kp_count = 0; // count the key presses
static int timer_locking = 0;
static int timer_unlocking = 0;

static char buff[5];

void Timer_Init(void){

    MAP_SysTick_enableModule();
    MAP_SysTick_setPeriod(PERIOD);
    MAP_SysTick_enableInterrupt();

    //printf("Timer init\n");

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
    int var = getLockCount();
    enum state lock_state = getLockState();
    char c;
    // For keypad
/*
    if(getLockCount() > 10){
        toggle_red();
        toggle_yellow();
        toggle_green();
    } */

    if(getLockCount() > 10){
        green_off();
        setLockState(IDLE);
    }

    if(getLockCount() > 5 && (lock_state == LOCK || lock_state == UNLOCK)){
        green_off();
        MAP_GPIO_setOutputLowOnPin(GPIO_PORT_P5, GPIO_PIN2);
        setLockCount(0); //reset the lock count
        setLockState(IDLE); //go to idle
        clearLock();
        if(lock_state == LOCK){
            //red_off();
        }
        else{
            //green_off();
        }
    }

    if(lock_state == LOCK){
        //yellow_off();
        //red_on();
        MAP_GPIO_setOutputLowOnPin(GPIO_PORT_P5, GPIO_PIN2);
    }
    else if(lock_state == WAIT){
        c = 0x00;
        //green_off();
        green_on();
        MSPrintf(EUSCI_A2_BASE, "wait\n", BUFFER_SIZE);
        if(UART_Read(EUSCI_A2_BASE, (uint8_t*)&c, 1) !=0){
            setLockState(UNLOCK);
        }
        //setLockCount(0);

        /*
        if(c == 'p')                                 setLockState(UNLOCK);
        else if(c == 'f' || getLockCount() > 10)    setLockState(LOCK);
        else if(c == 'l')                            setLockState(IDLE);
        else setLockState(WAIT);*/

    }
    else if(lock_state == UNLOCK){
        MAP_GPIO_setOutputHighOnPin(GPIO_PORT_P5, GPIO_PIN2);
    }
    else if(lock_state == ENTER || lock_state == WAIT){
        green_off();
        MAP_GPIO_setOutputLowOnPin(GPIO_PORT_P5, GPIO_PIN2);
    }
    else if(lock_state == IDLE){
        green_off();
        MAP_GPIO_setOutputLowOnPin(GPIO_PORT_P5, GPIO_PIN2);
    }


    setLockCount(getLockCount() + 1); //This seems stupid but idk...
    set_hc05_count(get_hc05_count() + 1);

}



