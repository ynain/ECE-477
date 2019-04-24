#include <Headers/main.h>

void main(void) {
    int i,j;

    //uint32_t mclk = CS_getMCLK();
    //uint32_t dco  = CS_getDCOFrequency();
    //uint32_t smclk = CS_getSMCLK();

    //int DPressed = True; //TODO: change later
    connected = False;
    int pswdVerified = False;

    strcpy(password, "12345678");

    MAP_WDT_A_holdTimer();

    //MSP432 running at 24 MHz
    CS_Init();
    Timer_Init();
    //Initialize Hardware required for the HC-05
    UART_Init(EUSCI_A2_BASE, UART2Config);
    for(i=0; i<3*24000000;i++) j=i;

    leds_init();
    lock_init();
    keypad_init();
    setup_bluetooth_state();
    connect_bluetooth(password);


    while(True) {
        connect_bluetooth(password);
        //connected = get_state_status();
    }

}

