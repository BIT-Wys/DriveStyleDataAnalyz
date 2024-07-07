def find_adjacent_vehicle_data_limited(vehicle_data, all_data):
    # 解析 Lane_ID 的前缀和车道编号
    vehicle_data = vehicle_data.copy()  # 如果vehicle_data本身是通过筛选得到的，先创建一个副本
    vehicle_data['Lane_Prefix'] = vehicle_data['Lane_ID'].apply(lambda x: "_".join(x.split('_')[:-1]))
    vehicle_data['Lane_Number'] = vehicle_data['Lane_ID'].apply(lambda x: int(x.split('_')[-1]))

    # 遍历每个车辆的数据行
    for index, row in vehicle_data.iterrows():
        frame_id = row['Frame_ID']
        lane_prefix = row['Lane_Prefix']
        lane_number = row['Lane_Number']
        x_position = row['Local_X']
        self_velocity = row['Velocity']

        # 获取相邻车道的编号
        left_lane_id = f"{lane_prefix}_{lane_number - 1}"
        right_lane_id = f"{lane_prefix}_{lane_number + 1}"

        # 查找相同帧中在左右车道的车辆
        adjacent_vehicles = all_data[(all_data['Frame_ID'] == frame_id) &
                                     ((all_data['Lane_ID'] == left_lane_id) |
                                      (all_data['Lane_ID'] == right_lane_id))]

        # 计算相对位置和相对速度
        # adjacent_vehicles['Relative_Position'] = adjacent_vehicles['Local_X'] - x_position
        # adjacent_vehicles['Relative_Velocity'] = self_velocity - adjacent_vehicles['Velocity']

        adjacent_vehicles.loc[:, 'Relative_Position'] = adjacent_vehicles['Local_X'] - x_position
        adjacent_vehicles.loc[:, 'Relative_Velocity'] = self_velocity - adjacent_vehicles['Velocity']

        # 筛选距离小于30m的车辆
        close_vehicles = adjacent_vehicles[adjacent_vehicles['Relative_Position'].abs() < 30]

        # 排序并取最近的3辆车
        close_vehicles = close_vehicles.iloc[:3]

        # 记录数据
        for i, vehicle in enumerate(close_vehicles.itertuples(), 1):
            vehicle_data.loc[index, f'Near_Vehicle_{i}_ID'] = vehicle.Vehicle_ID
            vehicle_data.loc[index, f'Near_Vehicle_{i}_Distance'] = vehicle.Relative_Position
            vehicle_data.loc[index, f'Near_Vehicle_{i}_Relative_Velocity'] = vehicle.Relative_Velocity
            position = 'preceding' if vehicle.Relative_Position > 0 else 'following'
            vehicle_data.loc[index, f'Near_Vehicle_{i}_Position'] = position
            vehicle_data.loc[index, f'Near_Vehicle_{i}_Lane_ID'] = vehicle.Lane_ID

    return vehicle_data


