#include "driverlib.h"

const eUSCI_UART_Config uartConfig =
{
    EUSCI_A_UART_CLOCKSOURCE_SMCLK,                // SMCLK Clock Source
    78,                                            // BRDIV = 78
    2,                                             // UCxBRF = 2
    0,                                             // UCxBRS = 0
    EUSCI_A_UART_NO_PARITY,                        // No Parity
    EUSCI_A_UART_LSB_FIRST,                        // MSB First
    EUSCI_A_UART_ONE_STOP_BIT,                     // One stop bit
    EUSCI_A_UART_MODE,                             // UART mode
    EUSCI_A_UART_OVERSAMPLING_BAUDRATE_GENERATION  // Oversampling
};


int main(void)
{
    /* Halting Watch Dog Timer  */
    WDT_A_holdTimer();

    // Select the port, then the pins, then module function
    GPIO_setAsPeripheralModuleFunctionInputPin(GPIO_PORT_P3,
                GPIO_PIN2 | GPIO_PIN3, GPIO_PRIMARY_MODULE_FUNCTION);

    /* Setting DCO (clock) to 12MHz */
    //DCO - Digitally Controller Oscillator
    CS_setDCOCenteredFrequency(CS_DCO_FREQUENCY_12);

    /* Configuring UART Module */
    // Pass in the configuration constant
    UART_initModule(EUSCI_A2_MODULE, &uartConfig);

    /* Enable UART module */
    UART_enableModule(EUSCI_A2_MODULE);

    // main loop running forever
    while(1)
    {
        /* Send the 'g' character over UART */
        UART_transmitData(EUSCI_A2_MODULE, 'g');
    }
}