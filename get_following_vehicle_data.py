def get_follow_vehicle_data(vehicle_data, vehicle_frames):

    # 遍历DataFrame中每一行
    for index, row in vehicle_data.iterrows():
        follow_id = row['Following']
        if (follow_id == 0):
            continue
        current_second = row['Second']

        # 检查前车ID是否存在于vehicle_frames字典中
        if follow_id in vehicle_frames:
            near_vehicle_data = vehicle_frames[follow_id]

            # 使用searchsorted找到对应时间戳的索引
            idx = near_vehicle_data['Second'].searchsorted(current_second)
            if idx < len(near_vehicle_data) and near_vehicle_data.iloc[idx]['Second'] == current_second:
                # 如果时间戳匹配，则获取前车的速度和空间位置
                vehicle_data.at[index,
                                'Following_Velocity'] = near_vehicle_data.iloc[idx]['Velocity']
                # vehicle_data.at[index,
                #                 'Following_Distance'] = near_vehicle_data.iloc[idx]['Space_headway']
            elif idx > 0:
                # 如果没有精确匹配，使用最接近的前一个数据点
                vehicle_data.at[index,
                                'Following_Velocity'] = near_vehicle_data.iloc[idx - 1]['Velocity']
                # vehicle_data.at[index,
                #                 'Following_Distance'] = near_vehicle_data.iloc[idx - 1]['Space_headway']

    return vehicle_data

def get_preceed_vehicle_data(vehicle_data, vehicle_frames):

    # 遍历DataFrame中每一行
    for index, row in vehicle_data.iterrows():
        preceed_id = row['Following']
        if (preceed_id == 0):
            continue
        current_second = row['Second']

        # 检查前车ID是否存在于vehicle_frames字典中
        if preceed_id in vehicle_frames:
            near_vehicle_data = vehicle_frames[preceed_id]

            # 使用searchsorted找到对应时间戳的索引
            idx = near_vehicle_data['Second'].searchsorted(current_second)
            if idx < len(near_vehicle_data) and near_vehicle_data.iloc[idx]['Second'] == current_second:
                # 如果时间戳匹配，则获取前车的速度和空间位置
                vehicle_data.at[index,
                                'Preceding_Velocity'] = near_vehicle_data.iloc[idx]['Velocity']
                vehicle_data.at[index,
                                'Preceding_Distance'] = near_vehicle_data.iloc[idx]['Space_headway']
            elif idx > 0:
                # 如果没有精确匹配，使用最接近的前一个数据点
                vehicle_data.at[index,
                                'Preceding_Velocity'] = near_vehicle_data.iloc[idx - 1]['Velocity']
                vehicle_data.at[index,
                                'Preceding_Distance'] = near_vehicle_data.iloc[idx - 1]['Space_headway']

    return vehicle_data