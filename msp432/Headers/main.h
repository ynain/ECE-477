#ifndef MAIN_H_
#define MAIN_H_

#include <C:/ti/simplelink_msp432p4_sdk_2_40_00_10/source/ti/devices/msp432p4xx/driverlib/driverlib.h>
#include <Headers/CS_Driver.h>
#include <Headers/UART_Driver.h>
#include <Headers/timer.h>
#include <Headers/KEYPAD_driver.h>
#include <Headers/TIMER_handle.h>
#include <Headers/MSPIO.h>
#include <Headers/HC05_driver.h>

#include <Headers/LED_driver.h>
#include "LOCK_handler.h"
#include "msp.h"

#define BUFFER_SIZE    128
#define True             1
#define False            0


/*Data Buffer*/
char BufferRX[BUFFER_SIZE];
char BufferTX[BUFFER_SIZE];
char password[BUFFER_SIZE];

typedef struct _command{
    char id;
    char string[BUFFER_SIZE];
}Command;

extern int connected; // flag indicating we connected to pi


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
     78,
     2,
     0,
     EUSCI_A_UART_NO_PARITY,
     EUSCI_A_UART_LSB_FIRST,
     EUSCI_A_UART_ONE_STOP_BIT,
     EUSCI_A_UART_MODE,
     EUSCI_A_UART_OVERSAMPLING_BAUDRATE_GENERATION
};


uint32_t timer_count;

#endif /* MAIN_H_ */
