import logging
import struct

from pydta116a621.bit_tool import bytes_to_list

from pydta116a621.const import (REGISTER_TYPE_INPUT, REGISTER_TYPE_HOLDING,
                                CONST_MAX_BATCH_READ_SIZE, CONST_MAX_INDOOR_UNIT_COUNT, CONST_CELL_BIT_SIZE,
                                INDOOR_UNIT_ID_INDEX, indoor_unit_id2index, indoor_unit_index2id,
                                CONST_REGISTER_AREA_ADAPTER_STATUS, CONST_REGISTER_AREA_INDOOR_UNIT_CONNECTION_STATE, CONST_REGISTER_AREA_INDOOR_UNIT_COMMUNICATION_STATE,
                                CONST_REGISTER_AREA_INDOOR_UNIT_ABILITY_1, CONST_REGISTER_AREA_INDOOR_UNIT_ABILITY_2,
                                CONST_REGISTER_AREA_INDOOR_UNIT_STATE_1,CONST_REGISTER_AREA_INDOOR_UNIT_STATE_2,CONST_REGISTER_AREA_INDOOR_UNIT_STATE_3,
                                CONST_REGISTER_AREA_INDOOR_UNIT_CONTROL_1,CONST_REGISTER_AREA_INDOOR_UNIT_CONTROL_2,CONST_REGISTER_AREA_INDOOR_UNIT_CONTROL_3,
                                CONST_HVAC_MODE_FAN_ONLY, CONST_HVAC_MODE_HEAT, CONST_HVAC_MODE_COOL, CONST_HVAC_MODE_AUTO, CONST_HVAC_MODE_DRY, CONST_HVAC_MODE_MAPPING,
                                CONST_FAN_MODE_AUTO, CONST_FAN_MODE_LOW,CONST_FAN_MODE_MID_LOW,CONST_FAN_MODE_MIDDLE,CONST_FAN_MODE_MID_HIGH,CONST_FAN_MODE_HIGH,CONST_FAN_MODE_MAPPING,CONST_FAN_MODE_SEG_DEF,
                                CONST_SWING_MODE_AUTO, CONST_SWING_MODE_P1,CONST_SWING_MODE_P2,CONST_SWING_MODE_P3,CONST_SWING_MODE_P4,CONST_SWING_MODE_P5,CONST_SWING_MODE_MAPPING,CONST_SWING_MODE_SEG_DEF,
                                CONST_HVAC_POWER_ON, CONST_HVAC_POWER_OFF, CONST_HVAC_POWER_MAPPING,
                                )
from pydta116a621.register_area import RegisterAreas

_LOGGER = logging.getLogger(__name__)

class Adapter:
    def __init__(self, areas : RegisterAreas):
        self._areas = areas

    def update_all(self):
        self._areas.get_area(CONST_REGISTER_AREA_ADAPTER_STATUS).update_all()
        self._areas.get_area(CONST_REGISTER_AREA_INDOOR_UNIT_CONNECTION_STATE).update_all()
        self._areas.get_area(CONST_REGISTER_AREA_INDOOR_UNIT_COMMUNICATION_STATE).update_all()

    @property
    def adapter_state(self):
        area = self._areas.get_area(CONST_REGISTER_AREA_ADAPTER_STATUS)
        return area.get_value(1, 0, 0)

    @property
    def diii_connection_state(self):
        area = self._areas.get_area(CONST_REGISTER_AREA_ADAPTER_STATUS)
        return area.get_value(1, 1, 1)

    def __cells_to_list(self, cells):
        bs = []
        for cell in cells:
            bs.extend(struct.pack("H", cell))
        return bytes_to_list(bs)

    def __get_indoor_unit_status_from_cells(self, cells, device_id):
        device_index = indoor_unit_id2index(device_id)
        return self.__cells_to_list(cells)[device_index]

    def __get_available_indoor_unit_from_cells(self, cells):
        states = self.__cells_to_list(cells)
        available_list = [indoor_unit_index2id(i) for i in range(len(states)) if states[i]]
        return available_list

    @property
    def connected_devices(self):
        area = self._areas.get_area(CONST_REGISTER_AREA_INDOOR_UNIT_CONNECTION_STATE)
        return self.__get_available_indoor_unit_from_cells(area.cells)

    @property
    def communicable_devices(self):
        area = self._areas.get_area(CONST_REGISTER_AREA_INDOOR_UNIT_COMMUNICATION_STATE)
        return self.__get_available_indoor_unit_from_cells(area.cells)
