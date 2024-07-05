import pandas as pd
import numpy as np
import os
from read_table import ReadTable
from drive_state_identify import IdentifyDrivingState
data = ReadTable()
vehicle_ids = data['Vehicle_ID'].unique()
for vehicle_id in vehicle_ids:
    print('for vehile id: ', vehicle_id)
    vehicle_data = data[data['Vehicle_ID'] == vehicle_id]
    vehicle_data = IdentifyDrivingState(vehicle_data)

