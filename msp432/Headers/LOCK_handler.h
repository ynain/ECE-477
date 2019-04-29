/*
 * lock.h
 *
 *  Created on: Apr 8, 2019
 *      Author: 477grp2
 */

#ifndef DEVICES_LOCK_HANDLER_H_
#define DEVICES_LOCK_HANDLER_H_

#include <C:/ti/simplelink_msp432p4_sdk_2_40_00_10/source/ti/devices/msp432p4xx/driverlib/driverlib.h>
#include <Headers/LED_driver.h>

typedef enum state {IDLE, LOCK, UNLOCK , WAIT, CLEAR, ENTER} State;

static char SpecialChars[7] = {'A', 'B', 'C', 'D', 'E', 'F', 'O'};

#define True  1
#define False 0

static char pwd[4] = "1234";
static char entered[4] = "0000";
static int pwd_changing = False;


int button_count;
static int lock_count;

State state;

void lock_init(); //initialize lock
void lock_button_pressed(char c);
State getLockState(); // get the current state
void setLockState(State s); // set the state
void printPassword(); //print the password
void clearLock(); // clear the entered array
int passwords_match();
int lockIsBusy();
void setLockCount(int i);
int getLockCount(void);

int isPwdChanging();
void setPwdChanging();
void setNewPwd();
int isSpecialChar(char c);

#endif /* DEVICES_LOCK_H_ */
