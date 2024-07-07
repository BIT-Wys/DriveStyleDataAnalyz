import numpy as np
import pandas as pd


def IdentifyDrivingState(vehicle_data):
    # vehicle_data = vehicle_data.sort_values('Second')  # 确保数据是按帧排序的
    vehicle_data['Driving_State'] = 'Cruising'  # 默认为巡航
    # 计算速度
    vehicle_data['Velocity'] = np.hypot(
        vehicle_data['x_Velocity'], vehicle_data['y_Velocity'])

    # 检测跟车状态 50米内有前车；两车间时距3s内差值在0.5s以内
    following_condition = (vehicle_data['Time_headway'] < 3) & (
        vehicle_data['Space_headway'] < 50) & (vehicle_data['Time_headway'] > 0)
    vehicle_data.loc[following_condition, 'Driving_State'] = 'Following'

    # 检测换道状态
    vehicle_data = detect_lane_change_by_yaw(vehicle_data)

    # 输出统计信息查看变道和巡航的帧数量

    # print(vehicle_data['Driving_State'].value_counts())
    return vehicle_data


def detect_lane_change_by_yaw(vehicle_data):
    vehicle_data['Lane_Change'] = False  # 新增列以标记换道状态
    yaw_diff = vehicle_data['Vehicle_yaw'].diff()  # 计算偏航角的变化

    # 计算连续三帧偏航角变化大于0.005的帧
    high_yaw_change = (yaw_diff.abs() > 0.003)
    high_yaw_change_indices = high_yaw_change.rolling(
        window=4, min_periods=4).sum() == 4

    # 计算连续三帧偏航角变化小于0.005的帧
    low_yaw_change = (yaw_diff.abs() < 0.005)
    low_yaw_change_indices = low_yaw_change.rolling(
        window=4, min_periods=4).sum() == 4

    # 检测换道开始和结束
    start_indices = high_yaw_change_indices[high_yaw_change_indices].index
    end_indices = low_yaw_change_indices[low_yaw_change_indices].index

    # 标记换道状态
    for start in start_indices:
        # 找到与开始索引最近的结束索引
        end = end_indices[end_indices > start]
        if not end.empty:
            end = end[0]
            vehicle_data.loc[start:end, 'Lane_Change'] = True  # 标记换道状态
            # duration = (end -start) * 0.1
            # if (duration > 0.5) & (duration < 10.0):
            #     vehicle_data.loc[end, 'LC_Time'] = duration  # 在结束帧记录换道持续时间
        else:
            # 如果没有找到结束索引，假定换道持续到数据末尾
            vehicle_data.loc[start:, 'Lane_Change'] = True
            # duration = (end -start) * 0.1
            # if (duration > 0.5) & (duration < 10.0):
            #     vehicle_data.loc[end, 'LC_Time'] = duration
    # 将所有标记为换道的帧的Driving_State设置为'Lane_Change'
    vehicle_data.loc[vehicle_data['Lane_Change'],
                     'Driving_State'] = 'Lane_Change'
    return vehicle_data
