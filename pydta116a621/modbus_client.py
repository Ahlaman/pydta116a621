import logging

from pymodbus.client.sync import ModbusTcpClient
from pydta116a621.const import REGISTER_TYPE_INPUT, REGISTER_TYPE_HOLDING

_LOGGER = logging.getLogger(__name__)

class DaikinModbusClient:
    def __init__(self, host, port, slave_id):
        self._host = host
        self._port = port
        self._slave_id = slave_id
        self.__init_modbus_client()

    def __init_modbus_client(self):
        self.__modbus_client = ModbusTcpClient(self._host, port=self._port)
        self.__modbus_client.connect()

    def _read_input_cells(self, address, count):
        result = self.__modbus_client.read_input_registers(address- 1, count, unit=self._slave_id)
        return result.registers

    def _read_holding_cells(self, address, count):
        result = self.__modbus_client.read_holding_registers(address- 1, count, unit=self._slave_id)
        return result.registers

    def read_cells(self, register_type, address, count):
        cells = None
        if(register_type==REGISTER_TYPE_INPUT):
            cells = self._read_input_cells(address, count)
        elif(register_type==REGISTER_TYPE_HOLDING):
            cells = self._read_holding_cells(address, count)
        else:
            raise("Invalid register_type")
        logging.debug(register_type, address, count,cells)
        return cells

    def write_cell(self, address, cell):
        logging.debug('write_cell: ', address, cell)
        result = self.__modbus_client.write_register(address - 1, cell, unit=self._slave_id)
        return result

    def write_cells(self, address, cells):
        logging.debug('write_cells: ', address, cells)
        result = self.__modbus_client.write_registers(address - 1, cells, unit=self._slave_id)
        return result
