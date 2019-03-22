#include <ti/devices/msp432p4xx/driverlib/driverlib.h>
#include <Hardware/CS_Driver.h>
#include <Hardware/UART_Driver.h>
#include <Devices/timer.h>
#include <Devices/KEYPAD_driver.h>
#include <Devices/MSPIO.h>
#include <Devices/HC05_pins.h>
#include "msp.h"

#define BUFFER_SIZE    128
#define True           1
#define False          0

/*Data Buffer*/
char BufferRX[BUFFER_SIZE];
char BufferTX[BUFFER_SIZE];

typedef struct _command{
    char id;
    char string[BUFFER_SIZE];
}Command;
/*
Command* commands = [{.id = '0', .string = " Send nudes ples"},
                     {.id = '1', .string = " Todd is Bae"},
                     {.id = '2', .string = " Oh, okay, Ian"},
                     {.id = '3', .string = " Viktoryia is bae <3"}]; */

//char* DEBSTR_0 = ""

/* UART Configuration Parameter. These are the configuration parameters to
 * make the eUSCI A UART module to operate with a 115200 baud rate. These
 * values were calculated using the online calculator that TI provides
 * at:
 * http://software-dl.ti.com/msp430/msp430_public_sw/mcu/msp430/MSP430BaudRateConverter/index.html
 */
eUSCI_UART_Config UART0Config =
{
     EUSCI_A_UART_CLOCKSOURCE_SMCLK,
     13,
     0,
     37,
     EUSCI_A_UART_NO_PARITY,
     EUSCI_A_UART_LSB_FIRST,
     EUSCI_A_UART_ONE_STOP_BIT,
     EUSCI_A_UART_MODE,
     EUSCI_A_UART_OVERSAMPLING_BAUDRATE_GENERATION
};

/* UART Configuration Parameter. These are the configuration parameters to
 * make the eUSCI A UART module to operate with a 9600 baud rate. These
 * values were calculated using the online calculator that TI provides
 * at:
 * http://software-dl.ti.com/msp430/msp430_public_sw/mcu/msp430/MSP430BaudRateConverter/index.html
 */
eUSCI_UART_Config UART2Config =
{
     EUSCI_A_UART_CLOCKSOURCE_SMCLK,
     156,
     4,
     0,
     EUSCI_A_UART_NO_PARITY,
     EUSCI_A_UART_LSB_FIRST,
     EUSCI_A_UART_ONE_STOP_BIT,
     EUSCI_A_UART_MODE,
     EUSCI_A_UART_OVERSAMPLING_BAUDRATE_GENERATION
};


uint32_t timer_count;

void main(void) {
    char c = 0x00;
    int connected = 0; // flag indicating we connected to pi
    int bootInit = 0; // flag to indicate pi connected on the boot

    MAP_WDT_A_holdTimer();

    /*MSP432 running at 24 MHz*/
    CS_Init();
    timer_init();

    /*Initialize Hardware required for the HC-05*/
    UART_Init(EUSCI_A2_BASE, UART2Config);

    MAP_Interrupt_enableMaster();

    GPIO_Init();

    setup_bluetooth_state();


    while(1) {


        GPIO_status();
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
// Commented out for keypad testing, just temporary.
/*
        while(!connected){
            // send boot signal to pi
            if (get_state_status()) {
                printf("Connection status good\n");
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

            } else {
                printf("Waiting for a connection...");
            }
        }

        if (!get_state_status()) {
            connected = False;
        }
        //1 for now. later: check if button D is pressed
        else if(1) {
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
        }
*/

       /* if(UART_Read(EUSCI_A2_BASE, (uint8_t*)&c, 1) != 0) {
            //printf("c is %c\n", c);
            switch(c){
                    case 'P': MSPrintf(EUSCI_A2_BASE, " Face Passed\n", BUFFER_SIZE);
                                break;
                    case 'F': MSPrintf(EUSCI_A2_BASE, " Face Failed\n", BUFFER_SIZE);
                                break;
                    case 'R': MSPrintf(EUSCI_A2_BASE, " Ready for Face Recognition\n", BUFFER_SIZE);
                                break;
                    case 'L': MSPrintf(EUSCI_A2_BASE, " Lost Base Connection\n", BUFFER_SIZE);
                                break;
                    default:  MSPrintf(EUSCI_A2_BASE, " Input Not Recognized\n", BUFFER_SIZE);
                                break;
            }
        } */

        c = 0x00;

    }


}

