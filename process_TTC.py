import numpy as np
import pandas as pd
def process_following_state(vehicle_data):

    # # 筛选出 Following 不为 0 的帧
    # following_data = vehicle_data[vehicle_data['Following'] != 0].copy()

    # # 计算相对速度，避免原地修改警告
    # relative_velocity = np.abs(following_data['Velocity'] - following_data['Following_Velocity'])
    # following_data['Relative_Velocity'] = relative_velocity.replace(0, np.nan)  # 避免除以零

    # # 计算 TTC，即跟车时间
    # following_data['TTC'] = following_data['Space_headway'] / following_data['Relative_Velocity']
    # print('TTC', )
    # # 更新原数据集的 TTC 字段
    # vehicle_data.update(following_data[['TTC']])

    # return vehicle_data

    for index, row in vehicle_data.iterrows():
        preceed_id = row['Following']