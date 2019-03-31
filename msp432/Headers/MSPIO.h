#ifndef MSPIO_H_
#define MSPIO_H_

#include <Headers/UART_Driver.h>
#include <stdio.h>

void MSPrintf(uint32_t UART, const char *fs, ...);
int MSPgets(uint32_t UART, char *b, int size);

#endif /* MSPIO_H_ */
