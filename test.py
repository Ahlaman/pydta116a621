import time
from datetime import datetime, timedelta
import math

from pydta116a621 import DaikinAPI, IndoorUnit, DaikinModbusClient, RegisterAreas



if __name__ == '__main__':
    modbus_client = DaikinModbusClient('192.168.11.101', 502, 1)
    areas = RegisterAreas(modbus_client)
    indoor_unit = IndoorUnit(areas, '1-01')
    indoor_unit.update_all()
    print(indoor_unit.outdoor_mode)
    print(indoor_unit.supported_hvac_modes)
    print(indoor_unit.hvac_mode_change_permission)
