import pandas as pd

# 定義降雨強度公式
def intensity(t, a, b, c):
    return a / ((60 * t + b) ** c)

# 計算指定延時內的累積降雨量
def calculate_cumulative_rainfall(a, b, c, hours):
    hourly_intensity_corrected = []
    for t in range(1, hours + 1):
        current_intensity = intensity(t, a, b, c) * t
        if t > 1:
            current_intensity -= sum(hourly_intensity_corrected[:t-1])  # 減去前面所有的累積值
        hourly_intensity_corrected.append(current_intensity)
    
    return sum(hourly_intensity_corrected)

# 從CSV讀取資料並清除空白
df = pd.read_csv(r'C:\TC\rainfall_parameters.csv')
df.columns = df.columns.str.strip()  # 清除欄位名稱中的空白字符

# 檢查列名稱是否正確
print(df.columns)

# 要計算的不同延時
time_durations = [1, 3, 6, 12, 24, 48, 72]

# 為每個延時計算累積降雨量
for hours in time_durations:
    df[f'{hours}hr_cumulative_rainfall'] = df.apply(lambda row: calculate_cumulative_rainfall(row['a'], row['b'], row['c'], hours), axis=1)

# 保存結果到新的CSV檔案
df.to_csv(r'C:\TC\rainfall_cumulative_multiple_durations_1output.csv', index=False)

# 輸出1小時的結果進行檢查
print(df[['ST_name', 'ST_id', 'type', '1hr_cumulative_rainfall']])
