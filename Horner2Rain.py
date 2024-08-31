# 定義Horner參數
a = 794.254
b = 20.868
c = 0.345

# 定義降雨強度公式
def intensity(t, a, b, c):
    return a / ((60 * t + b) ** c)

# 計算每小時的降雨強度，並減去之前各小時的累積降雨量
hourly_intensity_corrected = []
cumulative_intensity = 0
for t in range(1, 26):
    current_intensity = intensity(t, a, b, c) * t
    if t > 1:
        current_intensity -= sum(hourly_intensity_corrected[:t-1])  # 減去前面所有的累積值
    hourly_intensity_corrected.append(current_intensity)
    
hourly_intensity_corrected[-1] = 0  # 將最後一小時的修正降雨強度設為0

# 根據交替區塊法重新排序
sorted_intensities = sorted(hourly_intensity_corrected, reverse=True)
rearranged_intensities = [0] * 25
mid = len(rearranged_intensities) // 2

# 將最大值放置在中間
rearranged_intensities[mid] = sorted_intensities.pop(0)

# 放置其他值
left = mid - 1
right = mid + 1
toggle = True

while sorted_intensities:
    if toggle and right < len(rearranged_intensities):
        rearranged_intensities[right] = sorted_intensities.pop(0)
        right += 1
    elif not toggle and left >= 0:
        rearranged_intensities[left] = sorted_intensities.pop(0)
        left -= 1
    toggle = not toggle
    
# 計算各延時比例
total_intensity = sum(rearranged_intensities)
proportions = [intensity / total_intensity for intensity in rearranged_intensities]

# 計算總降雨量
total_rainfall = sum(hourly_intensity_corrected)

# 打印結果
print("小時 | 修正降雨強度 (mm/h) | 重新排序後降雨強度 (mm/h) | 比例")
print("-----|----------------------|-------------------------|-------")
for hour in range(25):
    proportion_percent = proportions[hour] * 100
    print(f"{hour + 1:4} | {hourly_intensity_corrected[hour]:20.2f} | {rearranged_intensities[hour]:23.2f} | {proportion_percent:5.2f}%")
    
print("\n總降雨量: {:.2f} mm".format(total_rainfall))
