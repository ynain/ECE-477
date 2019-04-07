#include <Headers/main.h>

void main(void) {

    int DPressed = True; //TODO: change later
    int pswdVerified = False;

    strcpy(password, "12345678");

    MAP_WDT_A_holdTimer();

    //MSP432 running at 24 MHz
    CS_Init();
    Timer_Init();
    //Initialize Hardware required for the HC-05

    UART_Init(EUSCI_A2_BASE, UART2Config);

    Keypad_Init();
    //printf("after keypad\n");

    MAP_Interrupt_enableMaster();


    //setup_bluetooth_state();


    while(True) {

        if(!connected) connect_bluetooth(&connected, &pswdVerified, password);
        //else start_recognition(&connected, DPressed);
    }


}

