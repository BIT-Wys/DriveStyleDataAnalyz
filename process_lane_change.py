import pandas as pd
import numpy as np
def process_lane_changes(vehicle_data):
    # 找到所有变道的开始和结束
    change_indices = vehicle_data.index[vehicle_data['Driving_State'] == 'Lane Change'].tolist()
    starts = []
    ends = []

    # 标识连续的变道区间
    i = 0
    while i < len(change_indices):
        start = change_indices[i]
        while i < len(change_indices) - 1 and change_indices[i+1] == change_indices[i] + 1:
            i += 1
        end = change_indices[i]
        starts.append(start)
        ends.append(end)
        i += 1

    # 计算变道持续时间并赋值到最后一帧
    for start, end in zip(starts, ends):
        duration = vehicle_data.loc[end, 'Second'] - vehicle_data.loc[start, 'Second']
        if (duration > 3.0) :
            vehicle_data.loc[end, 'LC_Time'] = duration

    return vehicle_data

def calculate_lane_change_efficiency(vehicle_data):
    # 筛选适合的帧
    lane_change_data = vehicle_data[(vehicle_data['Driving_State'] == 'Lane Change') &
                                    ((vehicle_data['Following'] != 0) | (vehicle_data['Preceding'] != 0))]

    # 计算换道效率
    for idx, row in lane_change_data.iterrows():
        speeds = []

        # 获取前后车速度，如果为NaN则忽略
        if not pd.isna(row['Following_Velocity']):
            speeds.append(row['Following_Velocity'])
        if not pd.isna(row['Preceding_Velocity']):
            speeds.append(row['Preceding_Velocity'])

        # 计算平均速度
        average_speed = np.mean(speeds) if speeds else 0

        # 计算换道效率
        if row['Velocity'] > 0:  # 避免除以零
            vehicle_data.at[idx, 'LC_Efficiency'] = average_speed / row['Velocity']
        else:
            vehicle_data.at[idx, 'LC_Efficiency'] = np.nan  # 如果自车速度为零，换道效率无法计算

    return vehicle_data
