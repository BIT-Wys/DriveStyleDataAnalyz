import os
import pandas as pd


def ReadTable():
    # 定义包含 CSV 文件的文件夹路径
    folder_path = './rl1'  # 替换为你的文件夹路径
    # 获取文件夹中所有 CSV 文件的信息
    file_list = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

    # 初始化一个空列表以存储数据框架
    data_frames = []
    loaded_data = 0
    # 循环读取每个文件，并将其数据框架追加到列表
    for file_name in file_list[:30]:  # 限制为前500个文件，如果文件夹中文件少于500，将读取所有文件
        current_file_path = os.path.join(folder_path, file_name)
        current_data_frame = pd.read_csv(current_file_path)

        # 检查 'Following_Lane_ID' 是否存在并为字符串列（等效于 MATLAB 中的 cell array）
        # if pd.api.types.is_string_dtype(current_data_frame['Following_Lane_ID']):
        data_frames.append(current_data_frame)
        loaded_data = loaded_data + 1
    # 合并所有数据框架为一个单一的数据框架
    combined_data = pd.concat(data_frames, ignore_index=True)
    print('data loaded finished, ', loaded_data, ' files are processd.')
    return combined_data

# # 调用函数并将结果赋值给变量
# data = read_table()
