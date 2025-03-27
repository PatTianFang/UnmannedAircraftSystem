import cv2
import numpy as np

def detect_circles(img_path):
    # 读取图片
    image = cv2.imread(img_path)
    if image is None:
        raise ValueError("无法读取图片，请检查路径是否正确")

    # 转换为灰度图像
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 使用高斯模糊减少噪声
    blurred = cv2.GaussianBlur(gray, (9, 9), 2)

    # 使用霍夫圆变换检测圆
    circles = cv2.HoughCircles(
        blurred,
        cv2.HOUGH_GRADIENT,
        dp=1.2,          # 累加器分辨率与图像分辨率的反比
        minDist=40,      # 检测到的圆心之间的最小距离
        param1=40,       # Canny 边缘检测的高阈值
        param2=40,       # 累加器阈值，较小的值将检测到更多的圆
        minRadius=40,    # 圆的最小半径
        maxRadius=150    # 圆的最大半径
    )

    if circles is None:
        return [], image

    # 将检测到的圆转换为列表，并按半径从大到小排序
    circles = np.round(circles[0, :]).astype("int")
    circles = sorted(circles, key=lambda x: x[2], reverse=True)

    # 提取圆心和半径
    result = [{'center': (x, y), 'radius': r} for (x, y, r) in circles]

    # 在图像上绘制检测到的圆
    for circle in circles:
        center = (circle[0], circle[1])
        radius = circle[2]
        cv2.circle(image, center, radius, (0, 255, 0), 4)  # 用绿色绘制圆
        cv2.rectangle(image, (center[0] - 5, center[1] - 5), (center[0] + 5, center[1] + 5), (0, 128, 255), -1)  # 用橙色绘制圆心

    return result, image

# 示例调用
if __name__ == "__main__":
    result, image_with_circles = detect_circles("mission2/H.png")
    if result:
        for circle in result:
            print(f"圆心: {circle['center']}, 半径: {circle['radius']}")
        # 显示结果图像
        cv2.imshow('Detected Circles', image_with_circles)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("未检测到圆")
