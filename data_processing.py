import pandas as pd
import numpy as np
import os
from drive_state_identify import IdentifyDrivingState
from get_following_vehicle_data import get_follow_vehicle_data
from get_following_vehicle_data import get_preced_vehicle_data
from process_lane_change import process_lane_changes
from process_lane_change import calculate_lane_change_efficiency
from process_TTC import process_following_state
from side_pass_vehicle import find_adjacent_vehicle_data_limited
def DrivingDataProcess(data):
    data['Driving_State'] = pd.NA  # 加入驾驶状态
    data['Velocity'] = pd.NA  # 速度

    data['Following_Velocity'] = pd.NA
    data['Following_Distance'] = pd.NA
    data['Preceding_Velocity'] = pd.NA
    data['Preceding_Distance'] = pd.NA

    data['Near_Vehicle_1_ID'] = pd.NA
    data['Near_Vehicle_1_Distance'] = pd.NA
    data['Near_Vehicle_1_Relative_Velocity'] = pd.NA
    data['Near_Vehicle_1_Position'] = pd.NA
    data['Near_Vehicle_1_Lane_ID'] = pd.NA

    data['Near_Vehicle_2_ID'] = pd.NA
    data['Near_Vehicle_2_Distance'] = pd.NA
    data['Near_Vehicle_2_Relative_Velocity'] = pd.NA
    data['Near_Vehicle_2_Position'] = pd.NA
    data['Near_Vehicle_2_Lane_ID'] = pd.NA

    data['Near_Vehicle_3_ID'] = pd.NA
    data['Near_Vehicle_3_Distance'] = pd.NA
    data['Near_Vehicle_3_Relative_Velocity'] = pd.NA
    data['Near_Vehicle_3_Position'] = pd.NA
    data['Near_Vehicle_3_Lane_ID'] = pd.NA

    # 跟车数据
    data['TTC'] = pd.NA  # 跟车时距

    # 变道数据
    data['LC_Time'] = pd.NA  # 换道时间
    data['LC_Efficiency'] = pd.NA  # 换道效率

    vehicle_frames = {}
    vehicle_ids = data['Vehicle_ID'].unique()
    for vehicle_id in vehicle_ids:
        vehicle_data = data[data['Vehicle_ID'] == vehicle_id]
        vehicle_data = IdentifyDrivingState(vehicle_data)
        vehicle_frames[vehicle_id] = vehicle_data
    data.update(pd.concat(vehicle_frames.values()))
    # print('Data Initialized')
    for vehicle_id in vehicle_ids:
        vehicle_data = data[data['Vehicle_ID'] == vehicle_id]
        vehicle_data = get_follow_vehicle_data(vehicle_data, vehicle_frames)
        vehicle_data = get_preced_vehicle_data(vehicle_data, vehicle_frames)
        vehicle_data = process_lane_changes(vehicle_data)
        vehicle_data = find_adjacent_vehicle_data_limited(vehicle_data, data)
        vehicle_data = calculate_lane_change_efficiency(vehicle_data)
        
        vehicle_frames[vehicle_id] = vehicle_data
    # 最终更新主数据集
    data.update(pd.concat(vehicle_frames.values()))
    # print('Data processing finished')
    return data