from dataclasses import dataclass

import serial
import minimalmodbus

serial_client = minimalmodbus.Instrument('/dev/ttyAMA0', mode=minimalmodbus.MODE_RTU, slaveaddress=1, debug=False)
serial_client.serial.baudrate = 19200
serial_client.serial.bytesize = 8
serial_client.serial.parity = serial.PARITY_EVEN
serial_client.serial.stopbits = serial.STOPBITS_ONE
serial_client.clear_buffers_before_each_transaction = True


@dataclass
class Register:
    description: str
    addr: int
    number_of_registers:int =2


REGISTERS = [
    Register("Phase 1 : phase voltage", 4096),
    Register("Phase 2 : phase voltage", 4098),
    Register("Phase 3 : phase voltage", 4100),

    Register("Phase 1 : current", 4102),
    Register("Phase 2 : current", 4104),
    Register("Phase 3 : current", 4106),

    Register("Chained voltage : L1-L2", 4110),
    Register("Chained voltage : L2-L3", 4112),
    Register("Chained voltage : L3-L1", 4114),

    Register("Phase 1 : active power", 4140),
    Register("Phase 2 : active power", 4142),
    Register("Phase 3 : active power", 4144),

    Register("Phase 1 : sign of active power", 4146, 1),
    Register("Phase 2 : sign of active power", 4147, 1),
    Register("Phase 3 : sign of active power", 4148, 1),

    Register("Phase 1 : apparent power", 4158),
    Register("Phase 2 : apparent power", 4160),
    Register("Phase 3 : apparent power", 4162),

    Register("Phase 1 : reactive power", 4149),
    Register("Phase 2 : reactive power", 4151),
    Register("Phase 3 : reactive power", 4153),

    Register("Phase 1 : power factor", 4164, 1),
    Register("Phase 2 : power factor", 4165, 1),
    Register("Phase 3 : power factor", 4166, 1),

    Register("Phase 1 : THD V1", 4170, 1),
    Register("Phase 2 : THD V2", 4171, 1),
    Register("Phase 3 : THD V3", 4172, 1),

    Register("Phase 1 : THD I1", 4173, 1),
    Register("Phase 2 : THD I2", 4174, 1),
    Register("Phase 3 : THD I3", 4175, 1),
]

for reg in REGISTERS:
    value = serial_client._generic_command(
        functioncode=3,
        registeraddress=reg.addr,
        number_of_registers=reg.number_of_registers,
        payloadformat=minimalmodbus._Payloadformat.LONG if reg.number_of_registers > 1 else minimalmodbus._Payloadformat.REGISTER,
    )
    print(f"{reg.description}: {value * 0.001}")
