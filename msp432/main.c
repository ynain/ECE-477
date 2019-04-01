#include <ti/devices/msp432p4xx/driverlib/driverlib.h>
#include <Headers/CS_Driver.h>
#include <Headers/UART_Driver.h>
#include <Headers/timer.h>
#include <Headers/KEYPAD_driver.h>
#include <Headers/MSPIO.h>
#include <Headers/HC05_driver.h>
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
    int connected = False; // flag indicating we connected to pi
    int DPressed = True; //TODO: change later


    MAP_WDT_A_holdTimer();

    //MSP432 running at 24 MHz
    CS_Init();

    //Initialize Hardware required for the HC-05

    UART_Init(EUSCI_A2_BASE, UART2Config);

    MAP_Interrupt_enableMaster();


    GPIO_Init();

    setup_bluetooth_state();

    while(True) {
        if(!connected) connect_bluetooth(&connected);
        else start_recognition(&connected, DPressed);
    }


}

