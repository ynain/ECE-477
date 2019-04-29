#include <Headers/main.h>

void main(void) {


    //uint32_t mclk = CS_getMCLK();
    //uint32_t dco  = CS_getDCOFrequency();
    //uint32_t smclk = CS_getSMCLK();

    //int DPressed = True; //TODO: change later
    connected = False;
    int pswdVerified = False;

    strcpy(password, "twild477");

    MAP_WDT_A_holdTimer();

    //MSP432 running at 24 MHz
    CS_Init();
    Timer_Init();
    //Initialize Hardware required for the HC-05
    UART_Init(EUSCI_A2_BASE, UART2Config);
    //for(int i=0; i<3*24000000;i++);

    leds_init();
    lock_init();
    keypad_init();
    setup_bluetooth_state();

    char c;
    int l;

    while(1) {
        connect_bluetooth(password);
        //connect_bluetooth(password);
        //MSPrintf(EUSCI_A2_BASE, "pswd\n", BUFFER_SIZE);
        //connected = get_state_status();

        l = getLockCount();
        if(was_key_pressed()){
            c = get_last_key_pressed();
            set_key_was_pressed(0);
            lock_button_pressed(c);
        }


    }

}

