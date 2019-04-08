/*
 * lock.c
 *
 *  Created on: Apr 8, 2019
 *      Author: 477grp2
 */
#include <Headers/Lock_handler.h>
#include <stdio.h>

void lock_init(){

    state = IDLE;
    lock_count = 0;
    button_count = 0;
    printf("Lock init\n");
}

void lock_button_pressed(char c){

    State curr_state = getLockState();

    //Check current state to see if the lock should ignore the button press
    if(curr_state == WAIT || curr_state == LOCK || curr_state == UNLOCK){
         return;
    }

    // 'D' pressed -> start face recognition and go to wait state
    if(c == 'D'){

        setLockState(WAIT);
    }

    // 'E pressed' -> check to see if the passwords match
    else if(c == 'E'){
        if(button_count == 3 && passwords_match() == 1){
            setLockState(UNLOCK);
            setLockCount(0);
        }
        else{
            setLockState(LOCK);
            setLockCount(0);
        }

    }
    // Clear buffer and go to IDLE
    else if(c == 'C'){

        setLockState(IDLE);
        clearLock();
    }
    // Transition from IDLE state
    else if(curr_state == IDLE){
        // In idle state, go to enter state
        entered[button_count] = c;
        button_count++;
        setLockState(ENTER);
    }

    //Too many buttons pressed before enter key
    else if(curr_state == ENTER && button_count == 4){

        setLockState(LOCK);
        setLockCount(0);
    }

    // Already in Enter state, continue reading button presses
    else{
        entered[button_count] = c;
        button_count++;

    }

}

//return the current state
State getLockState(){
    return state;
}

//set the state
void setLockState(State s){
    state = s;
}

//print password - for debugging
void printPassword(){
    int i;
    for(i = 0; i < 4; i++){
        printf("pwd[i] = %c", pwd[i]);
    }
}

//clear the entered buffer
void clearLock(){
    int i;
    for(i = 0; i < 4; i++){
        entered[i] = '0';
    }
    button_count = 0;
    setLockCount(0);
}

//check to see if passwords match
int passwords_match(){
    int i;
    for(i = 0; i < 4; i++){
        if(pwd[i] != entered[i]){
            return 0;
        }
    }
    return 1;

}

// the lock should ignore new button presses if it is in these states
int lockIsBusy(){
    if(state == LOCK || state == UNLOCK || state == WAIT){
        return 1;
    }
    else{
        return 0;
    }
}

void setLockCount(int i){
    lock_count = i;
}

int getLockCount(void){
    return lock_count;
}






