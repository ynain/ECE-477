################################################################################
# Automatically-generated file. Do not edit!
################################################################################

SHELL = cmd.exe

CG_TOOL_ROOT := C:/ti/ccsv8/tools/compiler/ti-cgt-arm_18.1.5.LTS

GEN_OPTS__FLAG := 
GEN_CMDS__FLAG := 

ORDERED_OBJS += \
"./main.obj" \
"./startup_msp432p401r_ccs.obj" \
"./system_msp432p401r.obj" \
"./Devices/HC05_driver.obj" \
"./Devices/KEYPAD_driver.obj" \
"./Devices/LOCK_handler.obj" \
"./Devices/MSPIO.obj" \
"./Hardware/CS_Driver.obj" \
"./Hardware/LED_driver.obj" \
"./Hardware/TIMER_handle.obj" \
"./Hardware/UART_Driver.obj" \
"../msp432p401r.cmd" \
$(GEN_CMDS__FLAG) \
-l"C:/ti/simplelink_msp432p4_sdk_2_40_00_10/source/ti/devices/msp432p4xx/driverlib/ccs/msp432p4xx_driverlib.lib" \

-include ../makefile.init

RM := DEL /F
RMDIR := RMDIR /S/Q

# All of the sources participating in the build are defined here
-include sources.mk
-include subdir_vars.mk
-include Devices/subdir_vars.mk
-include Hardware/subdir_vars.mk
-include subdir_rules.mk
-include Devices/subdir_rules.mk
-include Hardware/subdir_rules.mk
-include objects.mk

ifneq ($(MAKECMDGOALS),clean)
ifneq ($(strip $(C55_DEPS)),)
-include $(C55_DEPS)
endif
ifneq ($(strip $(C_UPPER_DEPS)),)
-include $(C_UPPER_DEPS)
endif
ifneq ($(strip $(S67_DEPS)),)
-include $(S67_DEPS)
endif
ifneq ($(strip $(S62_DEPS)),)
-include $(S62_DEPS)
endif
ifneq ($(strip $(S_DEPS)),)
-include $(S_DEPS)
endif
ifneq ($(strip $(OPT_DEPS)),)
-include $(OPT_DEPS)
endif
ifneq ($(strip $(C??_DEPS)),)
-include $(C??_DEPS)
endif
ifneq ($(strip $(ASM_UPPER_DEPS)),)
-include $(ASM_UPPER_DEPS)
endif
ifneq ($(strip $(S??_DEPS)),)
-include $(S??_DEPS)
endif
ifneq ($(strip $(C64_DEPS)),)
-include $(C64_DEPS)
endif
ifneq ($(strip $(CXX_DEPS)),)
-include $(CXX_DEPS)
endif
ifneq ($(strip $(S64_DEPS)),)
-include $(S64_DEPS)
endif
ifneq ($(strip $(INO_DEPS)),)
-include $(INO_DEPS)
endif
ifneq ($(strip $(CLA_DEPS)),)
-include $(CLA_DEPS)
endif
ifneq ($(strip $(S55_DEPS)),)
-include $(S55_DEPS)
endif
ifneq ($(strip $(SV7A_DEPS)),)
-include $(SV7A_DEPS)
endif
ifneq ($(strip $(C62_DEPS)),)
-include $(C62_DEPS)
endif
ifneq ($(strip $(C67_DEPS)),)
-include $(C67_DEPS)
endif
ifneq ($(strip $(PDE_DEPS)),)
-include $(PDE_DEPS)
endif
ifneq ($(strip $(K_DEPS)),)
-include $(K_DEPS)
endif
ifneq ($(strip $(C_DEPS)),)
-include $(C_DEPS)
endif
ifneq ($(strip $(CC_DEPS)),)
-include $(CC_DEPS)
endif
ifneq ($(strip $(C++_DEPS)),)
-include $(C++_DEPS)
endif
ifneq ($(strip $(C43_DEPS)),)
-include $(C43_DEPS)
endif
ifneq ($(strip $(S43_DEPS)),)
-include $(S43_DEPS)
endif
ifneq ($(strip $(ASM_DEPS)),)
-include $(ASM_DEPS)
endif
ifneq ($(strip $(S_UPPER_DEPS)),)
-include $(S_UPPER_DEPS)
endif
ifneq ($(strip $(CPP_DEPS)),)
-include $(CPP_DEPS)
endif
ifneq ($(strip $(SA_DEPS)),)
-include $(SA_DEPS)
endif
endif

-include ../makefile.defs

# Add inputs and outputs from these tool invocations to the build variables 
EXE_OUTPUTS += \
micro.out \

EXE_OUTPUTS__QUOTED += \
"micro.out" \

BIN_OUTPUTS += \
micro.hex \

BIN_OUTPUTS__QUOTED += \
"micro.hex" \


# All Target
all: $(OBJS) $(CMD_SRCS) $(GEN_CMDS)
	@$(MAKE) --no-print-directory -Onone "micro.out"

# Tool invocations
micro.out: $(OBJS) $(CMD_SRCS) $(GEN_CMDS)
	@echo 'Building target: "$@"'
	@echo 'Invoking: ARM Linker'
	"C:/ti/ccsv8/tools/compiler/ti-cgt-arm_18.1.5.LTS/bin/armcl" -mv7M4 --code_state=16 --float_support=FPv4SPD16 -me --advice:power=all --define=__MSP432P401R__ --define=ccs -g --gcc --diag_warning=225 --diag_wrap=off --display_error_number --abi=eabi -z -m"micro.map" --heap_size=1024 --stack_size=512 -i"C:/ti/ccsv8/ccs_base/arm/include" -i"C:/ti/simplelink_msp432p4_sdk_2_40_00_10/source/ti/devices/msp432p4xx/driverlib/ccs" -i"C:/ti/simplelink_msp432p4_sdk_2_40_00_10/source/ti/devices/msp432p4xx/driverlib/ccs" -i"C:/ti/ccsv8/tools/compiler/ti-cgt-arm_18.1.5.LTS/lib" -i"C:/ti/ccsv8/tools/compiler/ti-cgt-arm_18.1.5.LTS/include" --priority --reread_libs --diag_wrap=off --display_error_number --warn_sections --xml_link_info="micro_linkInfo.xml" --rom_model -o "micro.out" $(ORDERED_OBJS)
	@echo 'Finished building target: "$@"'
	@echo ' '

micro.hex: $(EXE_OUTPUTS)
	@echo 'Building files: $(strip $(EXE_OUTPUTS__QUOTED))'
	@echo 'Invoking: ARM Hex Utility'
	"C:/ti/ccsv8/tools/compiler/ti-cgt-arm_18.1.5.LTS/bin/armhex" --memwidth=8 --romwidth=8 -o "micro.hex" $(EXE_OUTPUTS__QUOTED)
	@echo 'Finished building: $(strip $(EXE_OUTPUTS__QUOTED))'
	@echo ' '

# Other Targets
clean:
	-$(RM) $(BIN_OUTPUTS__QUOTED)$(EXE_OUTPUTS__QUOTED)
	-$(RM) "main.obj" "startup_msp432p401r_ccs.obj" "system_msp432p401r.obj" "Devices\HC05_driver.obj" "Devices\KEYPAD_driver.obj" "Devices\LOCK_handler.obj" "Devices\MSPIO.obj" "Hardware\CS_Driver.obj" "Hardware\LED_driver.obj" "Hardware\TIMER_handle.obj" "Hardware\UART_Driver.obj" 
	-$(RM) "main.d" "startup_msp432p401r_ccs.d" "system_msp432p401r.d" "Devices\HC05_driver.d" "Devices\KEYPAD_driver.d" "Devices\LOCK_handler.d" "Devices\MSPIO.d" "Hardware\CS_Driver.d" "Hardware\LED_driver.d" "Hardware\TIMER_handle.d" "Hardware\UART_Driver.d" 
	-@echo 'Finished clean'
	-@echo ' '

.PHONY: all clean dependents
.SECONDARY:

-include ../makefile.targets

