from pydta116a621.bit_tool import pick_value, fill_field
from pydta116a621.const import CONST_MAX_BATCH_READ_SIZE, indoor_unit_id2index, CONST_MAX_INDOOR_UNIT_COUNT, REGISTER_TYPE_HOLDING


class ModbusDataProxy:
    def __init__(self, register_type, base_address, cells_count, modbus_client):
        self._base_address = base_address
        self._cells_count = cells_count
        self._cells = [0] * cells_count
        self._register_type = register_type
        self._modbus_client = modbus_client

    def _get_value_from_cell(self, cell, bit_start, bit_stop):
        return pick_value(cell, bit_start, (bit_stop - bit_start) + 1)

    def _make_cell_with_value(self, old_cell, bit_start, bit_stop, value):
        return fill_field(old_cell, bit_start, (bit_stop - bit_start) + 1, value)

    @property
    def register_type(self):
        return self._register_type
    @property
    def base_address(self):
        return self._base_address

    @property
    def cells(self):
        return self._cells

    @property
    def cells_count(self):
        return self._cells_count

    def update_cells(self, start_address, cells_count):
        if start_address + cells_count > self.base_address+ self.cells_count:
            raise("cells_count out of range ")

        batch_count = (cells_count + CONST_MAX_BATCH_READ_SIZE - 1) // CONST_MAX_BATCH_READ_SIZE
        for i in range(batch_count):
            address = start_address + i * CONST_MAX_BATCH_READ_SIZE
            this_turn_cells_count = CONST_MAX_BATCH_READ_SIZE if i < batch_count - 1 else cells_count - i * CONST_MAX_BATCH_READ_SIZE
            cells = self._modbus_client.read_cells(self.register_type, address, this_turn_cells_count)
            self._cells[address - self.base_address : address - self.base_address + this_turn_cells_count] = cells

    def update_all(self):
        self.update_cells(self._base_address, self._cells_count)

    def update_cell(self, address):
        self.update_cells(address, 1)

    def get_cell(self, address):
        return self._cells[address - self.base_address]

    def set_cell(self, address, cell):
        self.set_cells(address, [cell])

    def get_cells(self, start_address, count):
        start_index = start_address - self.base_address
        return self._cells[start_index : start_index + count]

    def set_cells(self, start_address, cells):
        start_index = start_address - self.base_address
        count = len(cells)
        self._cells[start_index: start_index + count] = cells

    def get_value(self, address, bit_start, bit_stop):
        cell = self.get_cell(address)
        value = self._get_value_from_cell(cell, bit_start, bit_stop)
        return value

    def set_value(self, address, bit_start, bit_stop, value):
        oldcell = self.get_cell(address)
        newcell = self._make_cell_with_value(oldcell, bit_start, bit_stop, value)
        self.set_cell(address, newcell)
        return value

    def write_cells(self, address, cells):
        if(self.register_type != REGISTER_TYPE_HOLDING):
            raise("Invalid register type, must be holding register")
        self._modbus_client.write_cells(address, cells)

    def write_cell(self, address, cell):
        if(self.register_type != REGISTER_TYPE_HOLDING):
            raise("Invalid register type, must be holding register")
        self._modbus_client.write_cell(address, cell)

    def write_value(self, address, bit_start, bit_stop, value):
        self.update_cell(address)
        oldcell = self.get_cell(address)
        newcell = self._make_cell_with_value(oldcell,bit_start, bit_stop, value)
        self.write_cell(address, newcell)


# 室内机信息
class IndoorUnitInfoProxy(ModbusDataProxy):
    def __init__(self, register_type, base_address, cells_count_per_indoor_unit, modbus_client):
        ModbusDataProxy.__init__(self, register_type, base_address, cells_count_per_indoor_unit * CONST_MAX_INDOOR_UNIT_COUNT, modbus_client)
        self.__cells_count_per_indoor_unit = cells_count_per_indoor_unit

    @property
    def cells_count_per_indoor_unit(self):
        return self.__cells_count_per_indoor_unit

    def get_device_start_address(self, device_id):
        return self.base_address + self.cells_count_per_indoor_unit * indoor_unit_id2index(device_id)

    def get_cells_by_indoor_unit(self, indoor_unit_id):
        address = self.get_device_start_address(indoor_unit_id)
        cells = self.get_cells(address, self.cells_count_per_indoor_unit)
        return cells

    def set_cells_by_indoor_unit(self, indoor_unit_id, cells):
        if(len(cells) != self.cells_count_per_indoor_unit):
            raise("cells count is not valid")
        address = self.get_device_start_address(indoor_unit_id)
        self.set_cells(address, cells)

    def get_cell_by_indoor_unit_offset(self, indoor_unit_id, offset):
        address = self.get_device_start_address(indoor_unit_id) + offset
        cell = self.get_cell(address)
        return cell

    def set_cell_by_indoor_unit_offset(self, indoor_unit_id, offset, cell):
        address = self.get_device_start_address(indoor_unit_id) + offset
        self.set_cell(address, cell)

    def get_value_by_indoor_unit_offset(self, indoor_unit_id, offset, bit_start, bit_stop):
        address = self.get_device_start_address(indoor_unit_id) + offset
        return self.get_value(address, bit_start, bit_stop)

    def set_value_by_indoor_unit_offset(self, indoor_unit_id, offset, bit_start, bit_stop, value):
        address = self.get_device_start_address(indoor_unit_id) + offset
        self.set_value(address,bit_start,bit_stop,value)

    def update_indoor_unit(self, indoor_unit_id):
        start_address = self.get_device_start_address(indoor_unit_id)
        self.update_cells(start_address, self.cells_count_per_indoor_unit)

    def write_cell_by_indoor_unit_offset(self, indoor_unit_id, offset, cell):
        address = self.get_device_start_address(indoor_unit_id) + offset
        self.write_cell(address, cell)

    def write_value_by_indoor_unit_offset(self, indoor_unit_id, offset, bit_start, bit_stop, value):
        address = self.get_device_start_address(indoor_unit_id) + offset
        self.write_value(address, bit_start, bit_stop, value)
