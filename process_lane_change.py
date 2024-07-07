import pandas as pd
import numpy as np


def process_lane_changes(vehicle_data):
    # 找到所有变道的开始和结束
    change_frame_ids = vehicle_data['Frame_ID'][vehicle_data['Driving_State'] == 'Lane_Change'].tolist()

    # 初始化变道开始和结束的列表
    starts = []
    ends = []

    # 标识连续的变道区间
    i = 0
    while i < len(change_frame_ids):
        start = change_frame_ids[i]
        while i < len(change_frame_ids) - 1 and change_frame_ids[i+1] == change_frame_ids[i] + 1:
            i += 1
        end = change_frame_ids[i]
        starts.append(start)
        ends.append(end)
        i += 1

    # 计算变道持续时间并赋值到最后一帧的LC_Time
    for start_frame_id, end_frame_id in zip(starts, ends):
        duration = vehicle_data.loc[vehicle_data['Frame_ID'] == end_frame_id, 'Second'].values[0] - \
                   vehicle_data.loc[vehicle_data['Frame_ID'] == start_frame_id, 'Second'].values[0]
        if 0.5 < duration < 10:  # 确保变道时间在合理的范围内
            vehicle_data.loc[vehicle_data['Frame_ID'] == end_frame_id, 'LC_Time'] = duration

    return vehicle_data


def calculate_lane_change_efficiency(vehicle_data):
    # 筛选适合的帧
    lane_change_data = vehicle_data[
        vehicle_data['Driving_State'] == 'Lane_Change']

    # 计算换道效率
    for idx, row in lane_change_data.iterrows():
        speeds = []

        # # 获取前后车速度，如果为NaN则忽略
        # if not pd.isna(row['Following_Velocity']):
        #     speeds.append(row['Following_Velocity'])
        # if not pd.isna(row['Preceding_Velocity']):
        #     speeds.append(row['Preceding_Velocity'])
        # 计算平均速度
        for i in range(1, 4):  # 假设最多有3辆临车
            relative_velocity_key = f'Near_Vehicle_{i}_Relative_Velocity'
            if relative_velocity_key in row and not pd.isna(row[relative_velocity_key]):
                speeds.append(abs(row[relative_velocity_key]))
        average_speed = np.mean(speeds) if speeds else 0

        # 计算换道效率
        if (row['Velocity'] > 1) & (average_speed > 0):  # 避免除以零
            vehicle_data.loc[idx, 'LC_Efficiency'] = abs(
                average_speed - row['Velocity']) / row['Velocity']
        else:
            vehicle_data.loc[idx, 'LC_Efficiency'] = np.nan  # 如果自车速度为零，换道效率无法计算

    return vehicle_data
