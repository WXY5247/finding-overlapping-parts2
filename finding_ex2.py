import cv2
import numpy as np


def binarize_image(image_path):
    # 读取图像
    image = cv2.imread(image_path)

    # 转换为灰度图像
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 二值化处理
    _, binary_image = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY)

    return binary_image


def find_percent_black_region(binary_image, window_size):
    height, width = binary_image.shape

    # 定义滑动窗口的尺寸
    win_height, win_width = window_size

    # 遍历图像的每个区域
    for y in range(0, height - win_height + 10):
        for x in range(0, width - win_width + 10):
            # 提取窗口区域
            window = binary_image[y:y + win_height, x:x + win_width]

            # 计算黑色像素的数量
            black_pixel_count = np.sum(window == 0)

            # 计算窗口区域的总像素数量
            total_pixel_count = win_height * win_width

            # 计算黑色素的占比
            black_pixel_ratio = black_pixel_count / total_pixel_count

            # 判断黑色素是否占比50%以上
            if black_pixel_ratio > 0.01:
                return (x, y, win_width, win_height)

    return None


# 使用示例
image_path = r'E:\shrimpproject_duplication1\shrimpImages\2022_11_7\8_8mm_2cm\Image_20221107125151692.bmp'
window_size = (100, 100)  # 设定窗口的尺寸

# 二值化图像
binary_image = binarize_image(image_path)

# 查找黑色素占比50%的区域
region = find_percent_black_region(binary_image, window_size)

if region:
    print(f"找到黑色素占比的区域，左上角坐标: ({region[0]}, {region[1]})，窗口尺寸: ({region[2]}, {region[3]})")
    # 在图像中标记该区域
    result_image = cv2.cvtColor(binary_image, cv2.COLOR_GRAY2BGR)
    cv2.rectangle(result_image, (region[0], region[1]), (region[0] + region[2], region[1] + region[3]), (0, 255, 0), 2)
    cv2.imshow('Result Image', result_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("未找到满足条件的区域")
