import numpy as np
import pandas as pd


def IdentifyDrivingState(vehicle_data):
    vehicle_data = vehicle_data.sort_values('Frame_ID')  # 确保数据是按帧排序的
    vehicle_data['Driving_State'] = 'Cruising'  # 默认为巡航
    # 计算速度
    velocity = np.hypot(vehicle_data['x_Velocity'], vehicle_data['y_Velocity'])

    # 检测跟车状态 50米内有前车；两车间时距3s内差值在0.5s以内
    following_condition = (vehicle_data['Time_headway'] < 3) & (
        vehicle_data['Space_headway'] < 50) & (vehicle_data['Time_headway'] > 0)
    vehicle_data.loc[following_condition, 'Driving_State'] = 'Following'

    # 检测换道状态
    lane_changes = vehicle_data['Lane_ID'].apply(check_lane_change)
    vehicle_data.loc[lane_changes, 'Driving_State'] = 'Lane Change'

    # 输出统计信息查看变道和巡航的帧数量

    print(vehicle_data['Driving_State'].value_counts())
    return vehicle_data


def check_lane_change(lane_id):
    parts = lane_id.split('_')
    if len(parts) >= 3:
        start_lane = parts[1]
        end_lane = parts[-1][1:]
        # 检查起始车道和结束车道是否相同
        return start_lane != end_lane
    return False


# # 输出统计信息查看变道和巡航的帧数量
# print(data['Driving_State'].value_counts())
