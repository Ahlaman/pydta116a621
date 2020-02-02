#!/usr/bin/env python
#coding=utf-8
import logging

from pydta116a621.modbus_client import DaikinModbusClient
from pydta116a621.register_area import RegisterAreas
from pydta116a621.adapter import Adapter
from pydta116a621.indoor_unit import IndoorUnit

from pydta116a621.const import (CONST_HVAC_MODE_FAN_ONLY, CONST_HVAC_MODE_HEAT, CONST_HVAC_MODE_COOL, CONST_HVAC_MODE_AUTO, CONST_HVAC_MODE_DRY,
                   CONST_FAN_MODE_AUTO, CONST_FAN_MODE_LOW,CONST_FAN_MODE_MID_LOW,CONST_FAN_MODE_MIDDLE,CONST_FAN_MODE_MID_HIGH,CONST_FAN_MODE_HIGH,
                   CONST_SWING_MODE_AUTO, CONST_SWING_MODE_P1,CONST_SWING_MODE_P2,CONST_SWING_MODE_P3,CONST_SWING_MODE_P4,CONST_SWING_MODE_P5,
                   CONST_HVAC_POWER_ON, CONST_HVAC_POWER_OFF,
                   )

class DaikinAPI:
    def __init__(self, host, port, slave_id):
        self._modbus_client = DaikinModbusClient(host, port, slave_id)
        self._areas = RegisterAreas(self._modbus_client)
        self._areas.update_all()
        self._adapter = Adapter(self._areas)
        self._indoor_units = {}
        self.__init_all_connected_indoor_unit()

    def __init_all_connected_indoor_unit(self):
        connected_unit_list = self._adapter.connected_devices
        for connected_unit_name in connected_unit_list:
            self._indoor_units[connected_unit_name] = IndoorUnit(self._areas, connected_unit_name)

    @property
    def adapter(self):
        return self._adapter

    @property
    def indoor_units(self):
        return self._indoor_units

    def get_indoor_unit(self, indoor_unit_id):
        return self._indoor_units.get(indoor_unit_id)


