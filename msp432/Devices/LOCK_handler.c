/*
 * lock.c
 *
 *  Created on: Apr 8, 2019
 *      Author: 477grp2
 */
#include <Headers/LOCK_handler.h>
#include <Headers/HC05_driver.h>
#include <stdio.h>

void lock_init(){

    state = IDLE;
    lock_count = 0;
    button_count = 0;
    //printf("Lock init\n");
    // PUSH button
    MAP_GPIO_setAsOutputPin(GPIO_PORT_P5, GPIO_PIN2);
    MAP_GPIO_setOutputLowOnPin(GPIO_PORT_P5, GPIO_PIN2);
}

void lock_button_pressed(char c){
    char c_in = 0x00;
    char response;
    int x = 0;
    State curr_state = getLockState();
    int pwd_change = isPwdChanging();

    //Check current state to see if the lock should ignore the button press
    if(curr_state == WAIT || curr_state == LOCK || curr_state == UNLOCK){
        red_off();
         return;
    }

    // 'D' pressed -> start face recognition and go to wait state
    if(c == 'D'){

            setLockState(WAIT);
            //response = start_recognition();
            setLockCount(0);
            if(getHC05State() == READY) {
                 green_on();
                 MSPrintf(EUSCI_A2_BASE, "start\n", BUFFER_SIZE);
                 x = 0;

                 while (x < 1 && getLockCount() < 20) {
                     x = getUARTRecieved();
                 }
                 if(getLockCount() >= 20){
                     setLockState(IDLE);
                 } else{
                     UART_Read(EUSCI_A2_BASE,(uint8_t*)&c, 1);

                     if(c == 'p')       {
                         setLockState(UNLOCK);
                         green_on();
                     }
                     else if(c == 'f')  {
                         setLockState(LOCK);
                     }
                     else if(c == 'l')  {
                         setLockState(IDLE);
                     }
                     setUARTRecieved(0);
                 }

            }


    }

    // 'E pressed' -> check to see if the passwords match
    else if(c == 'E'){
        red_off();
        printf("E pressed\n");
        if(button_count == 4 && passwords_match() == 1){
            //printPassword();
            printf("CORRECT!\n");
            setLockState(UNLOCK);

            setLockCount(0);
        } else if (button_count == 4 && isPwdChanging() == True){
            //printf("changed passcode\n");
            setNewPwd();
            setPwdChanging(False);
            setLockState(IDLE);
        }
        else{
            printPassword();
            //printf("INCORRECT!\n");
            setLockState(LOCK);
            setLockCount(0);
        }
        clearLock();
    }
    else if(c == 'F'){
        red_off();
        //printf("F pressed\n");
        if(button_count == 4 && passwords_match() == 1){
           //printPassword();
           //printf("CORRECT!\n");
           setLockState(ENTER);
           setLockCount(0);
           setPwdChanging(True);
       }
       else{
           printPassword();
          // printf("INCORRECT!\n");
           setLockState(IDLE);
           setLockCount(0);
       }
       clearLock();

    }
    // Clear buffer and go to IDLE
    else if(c == 'C'){
        red_off();
       // printf("C pressed\n");
        setLockState(IDLE);
        clearLock();
    }
    // Transition from IDLE state
    else if(curr_state == IDLE){
        red_off();
        // In idle state, go to enter state
        //printf("idle, c = %c\n", c);
        entered[button_count] = c;
        button_count++;
        setLockState(ENTER);
    }

    //Too many buttons pressed before enter key
    else if(curr_state == ENTER && button_count == 4){
        red_off();
        setLockState(LOCK);
        setLockCount(0);
    }

    // Already in Enter state, continue reading button presses
    else{
        red_off();
        //printf("c = %c\n", c);
        if(isSpecialChar(c) == 0){
            entered[button_count] = c;
            button_count++;
        }
        else{
           // printf("special char entered for pwd \n");
        }

    }
    return;

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
        printf("pwd[%d] = %c and entered[%d] = %c\n", i, pwd[i], i, entered[i]);
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

int isPwdChanging(){
    return pwd_changing;
}
void setPwdChanging(int b){
    pwd_changing = b;
}
void setNewPwd(){
        int i;
        for(i = 0; i < 4; i++){
            pwd[i] = entered[i];
        }
        //printf("New password: %c%c%c%c\n", pwd[0], pwd[1], pwd[2], pwd[3]);
}

int isSpecialChar(char c){
    int i;
    for(i = 0; i < 7; i++){
        if(c == SpecialChars[i]){
            return 1;
        }
    }
    return 0;

}







