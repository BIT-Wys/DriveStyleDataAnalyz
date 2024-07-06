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
        vehicle_data.loc[end, 'LC_Time'] = duration

    return vehicle_data

# 假设已经有vehicle_data
# vehicle_data = ... (你的vehicle_data DataFrame)

# 处理变道数据
vehicle_data = process_lane_changes(vehicle_data)

# 查看处理结果
print(vehicle_data[['Second', 'Driving_State', 'LC_Time']])