import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from read_table import ReadTable
# 加载数据
df = ReadTable(2,1)

# 添加一个新列以提取纯数字的车道编号
df['Lane_Number'] = df['Lane_ID'].apply(lambda x: int(x.split('_-')[-1]))

# 计算每辆车最常见的车道编号
common_lanes = df.groupby('Vehicle_ID')['Lane_Number'].agg(lambda x: x.mode()[0])

# 创建一个空字典来存储每辆车的相邻车道
adjacent_lanes = {}

# 计算相邻车道
for vehicle, lane in common_lanes.items():
    # 相邻车道
    left_lane = lane - 1
    right_lane = lane + 1
    
    # 检查是否有车辆在相邻车道
    left_vehicles = df[(df['Lane_Number'] == left_lane) & (df['Vehicle_ID'] != vehicle)]
    right_vehicles = df[(df['Lane_Number'] == right_lane) & (df['Vehicle_ID'] != vehicle)]
    
    left_vehicles = left_vehicles['Vehicle_ID'].unique() if not left_vehicles.empty else 'None'
    right_vehicles = right_vehicles['Vehicle_ID'].unique() if not right_vehicles.empty else 'None'
    
    # 保存信息
    adjacent_lanes[vehicle] = {'Left Lane': left_lane, 'Left Vehicles': left_vehicles, 
                               'Right Lane': right_lane, 'Right Vehicles': right_vehicles}

# 输出结果
for vehicle, lanes_info in adjacent_lanes.items():
    print(f"Vehicle {vehicle}:")
    print(f"  Left Lane {lanes_info['Left Lane']}: Vehicles {lanes_info['Left Vehicles']}")
    print(f"  Right Lane {lanes_info['Right Lane']}: Vehicles {lanes_info['Right Vehicles']}")
    print()



# 初始化绘图
plt.figure(figsize=(10, 6))

# 获取所有车辆的ID列表
vehicles = df['Vehicle_ID'].unique()

# 为每辆车分配一个颜色
colors = plt.cm.jet(np.linspace(0, 1, len(vehicles)))

# 绘制每辆车的轨迹
for vehicle, color in zip(vehicles, colors):
    # 获取这辆车的数据
    vehicle_data = df[df['Vehicle_ID'] == vehicle]
    # 绘制轨迹
    common_lane_id = vehicle_data['Lane_ID'].mode()[0]
    
    plt.plot(vehicle_data['Local_X'], vehicle_data['Local_Y'], label=f'Vehicle {vehicle} on Lane {common_lane_id}', color=color)
    # plt.plot(vehicle_data['Global_X'], vehicle_data['Global_Y'], label=f'Vehicle {vehicle} on Lane {common_lane_id}', color=color)

# 添加图例
plt.legend()

# 添加标题和坐标轴标签
plt.title('Vehicle Trajectories')
plt.xlabel('Local X')
plt.ylabel('Local Y')

# 显示图表
plt.show()
