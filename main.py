import pandas as pd
import numpy as np
import os
from read_table import ReadTable
# 加载数据
data = ReadTable()
data['Driving_State'] = pd.NA #加入驾驶状态
cluster_efficiency_map = {}
vehicle_ids = data['Vehicle_ID'].unique()
print(vehicle_ids.size)
for vehicle_id in vehicle_ids:
    vehicle_data = data[data['Vehicle_ID'] == vehicle_id]
    time_headway = vehicle_data['Time_headway']
    space_headway = vehicle_data['Space_headway']
    lane_id = vehicle_data['Lane_ID']
    velocity = np.hypot(vehicle_data['x_Velocity'], vehicle_data['y_Velocity'])
    for j in range(1, len(lane_id)):
        if lane_id.iloc[j] != lane_id.iloc[j-1] and 1 < time_headway.iloc[j] < 500:
            cluster = vehicle_data['Cluster'].iloc[j] + 1  # 获取该车辆的簇ID
            ego_vel = velocity.iloc[j]
            target_vel = ego_vel + space_headway.iloc[j] / time_headway.iloc[j]
            efficiency = (target_vel - ego_vel) / ego_vel

            if efficiency < 0.1 or np.isnan(efficiency):
                continue

            if cluster in cluster_efficiency_map:
                cluster_efficiency_map[cluster].append(efficiency)
            else:
                cluster_efficiency_map[cluster] = [efficiency]


# keys = list(cluster_efficiency_map.keys())
# values = [cluster_efficiency_map[key] for key in keys]
# num_cols = max(len(v) for v in values)
# map_matrix = np.zeros((len(keys), num_cols))


# output_file_name = 'lane_change_efficiency.csv'
# np.savetxt(output_file_name, map_matrix, delimiter=',')

print("Excel file has been created successfully!")
