import pandas as pd
import numpy as np
import os
from read_table import ReadTable
from drive_state_identify import IdentifyDrivingState
from get_following_vehicle_data import get_follow_vehicle_data
from get_following_vehicle_data import get_preceed_vehicle_data
# 加载数据
data = ReadTable()
data['Driving_State'] = pd.NA  # 加入驾驶状态
data['Velocity'] = pd.NA  # 速度

data['Following_Velocity'] = pd.NA
data['Following_Distance'] = pd.NA
data['Preceeding_Velocity'] = pd.NA
data['Preceeding_Distance'] = pd.NA



# 跟车数据
data['TTC'] = pd.NA  # 跟车时距

# 变道数据
data['LC_Time'] = pd.NA  # 换道时间
data['LC_Efficiency'] = pd.NA  # 换道效率

# 创建一个字典来存储每个车辆的数据
vehicle_frames = {}
vehicle_ids = data['Vehicle_ID'].unique()
for vehicle_id in vehicle_ids:
    vehicle_data = data[data['Vehicle_ID'] == vehicle_id]
    vehicle_data = IdentifyDrivingState(vehicle_data)
    # 存储每辆车的数据到字典
    vehicle_frames[vehicle_id] = vehicle_data
    vehicle_data = get_follow_vehicle_data(vehicle_data, vehicle_frames)
    vehicle_data = get_preceed_vehicle_data(vehicle_data, vehicle_frames)
# 更新主数据集
data.update(pd.concat(vehicle_frames.values()))

for vehicle_id in vehicle_ids:
    vehicle_data = vehicle_frames[vehicle_id]
    # 跟车状态数据处理
    following_data = vehicle_data[vehicle_data['Following'] != 0]

    following_data['Following_Velocity'] = following_data.apply(
        lambda x: vehicle_frames[x['Following']]['Velocity'].iloc[
            vehicle_frames[x['Following']]['Second'].searchsorted(
                x['Second']) - 1
            if vehicle_frames[x['Following']]['Second'].searchsorted(x['Second']) < len(vehicle_frames[x['Following']])
            else -1
        ] if x['Following'] in vehicle_frames and not pd.isna(x['Following']) else np.nan, axis=1)
    # 计算相对速度
    following_data['Relative_Velocity'] = np.abs(
        following_data['Velocity'] - following_data['Following_Velocity'])
    following_data['Relative_Velocity'] = following_data['Relative_Velocity'].replace(
        0, np.nan)  # 避免除以零
    # 为跟车状态赋值
    following_data['TTC'] = following_data['Space_headway'] / \
        following_data['Relative_Velocity']
    
    data.update(following_data[['TTC',
                'Following_Velocity', 'Relative_Velocity']])

    # 换道状态数据处理


output_dir = './output'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 保存到 CSV 文件
data.to_csv(os.path.join(output_dir, 'processed_data.csv'), index=False)
print("Excel file has been created successfully!")
