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
<<<<<<< HEAD
/*
        int i;
        for(i = 1; i < 5500; i++){
            printf("nope \n");
        } */

        /* Evan: we need software interrupts for the keypad access
         * or threading.
         * whatever is easier.
         *
         *
         * Note: please don't delete the following code.
         * It's a pretty solid prototype, but it s
         * */

        while(!connected){
            // send boot signal to pi
            printf("Connection status: %d\n", get_state_status());
            if(!bootInit) {
                MSPrintf(EUSCI_A2_BASE, "boot\n", BUFFER_SIZE);
                printf("sending boot signal...\n");
            }
            if(UART_Read(EUSCI_A2_BASE, (uint8_t*)&c, 1) != 0){
                if(c == 'c') {
                    printf("connected successfully\n");
                    connected = True;
                    bootInit = True;
                } else printf("pi is responding, still trying to connect...\n");
            } else printf("waiting for response from pi...\n");
        }

        if (!get_state_status()) {
            connected = False;
        }
        else if(1/*1 for now. later: check if button D is pressed*/) {
            MSPrintf(EUSCI_A2_BASE, " start\n", BUFFER_SIZE);
            UART_Read(EUSCI_A2_BASE, (uint8_t*)&c, 1);
            if(c == 'l') {
                printf("lost connection to server...\n");
                connected = False;
                bootInit = False;
                continue;
            }
            else if(c == 'p') {
                printf("face PASSED!\n");
                printf("unlocking the door...\n");
                //unlock the door
            }
            else if(c == 'f') {
                printf("face FAILED!\n");
                // try again
            } else if(c == 0x00){
                printf("default\n");
            }
            else printf("unrecognized input...\n");
=======
        connect_bluetooth(password);
        //connect_bluetooth(password);
        //MSPrintf(EUSCI_A2_BASE, "pswd\n", BUFFER_SIZE);
        //connected = get_state_status();

        l = getLockCount();
        if(was_key_pressed()){
            c = get_last_key_pressed();
            set_key_was_pressed(0);
            lock_button_pressed(c);
>>>>>>> micro-fix
        }


    }

}

