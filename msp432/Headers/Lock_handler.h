/*
 * lock.h
 *
 *  Created on: Apr 8, 2019
 *      Author: 477grp2
 */

#ifndef DEVICES_LOCK_HANDLER_H_
#define DEVICES_LOCK_HANDLER_H_

typedef enum state {IDLE, LOCK, UNLOCK , WAIT, CLEAR, ENTER } State;

static char pwd[4] = "1243";
static char entered[4] = "0000";
int button_count;
int lock_count;

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

#endif /* DEVICES_LOCK_H_ */
