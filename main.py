import os
from read_table import ReadTable
from data_processing import DrivingDataProcess

folder_path = './rl1'  # 替换为你的文件夹路径
file_list = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

output_dir = './output'
os.makedirs(output_dir, exist_ok=True)
read_progress = 0
interval = 1
files_processed = 20
# files_processed = len(file_list)
while read_progress < files_processed :
    data = ReadTable(read_progress, interval)
    data = DrivingDataProcess(data)

    # 保存到 CSV 文件
    data.to_csv(os.path.join(output_dir, f'processed_data_{read_progress}.csv'), index=False)
    print(f'data{read_progress} processed')
    read_progress = read_progress + 1