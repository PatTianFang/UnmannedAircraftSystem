import cv2
from PIL import Image, ImageDraw, ImageFont
import numpy as np

# 定义 draw_text 函数
def draw_text(img, text, pos, font, color):
    img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img_pil)
    draw.text(pos, text, font=font, fill=color)
    return cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)

# 初始化摄像头
cap = cv2.VideoCapture(0)

# 创建二维码检测器
qr_code_detector = cv2.QRCodeDetector()

# 加载中文字体
font_path = "simhei.ttf"  # 请确保路径正确，simhei.ttf 是黑体字体文件
font = ImageFont.truetype(font_path, 24)

while True:
    # 读取摄像头帧
    ret, frame = cap.read()
    if not ret:
        break

    # 检测二维码
    retval, decoded_info, points, straight_qrcode = qr_code_detector.detectAndDecodeMulti(frame)

    if retval:
        # 打印二维码内容
        for info in decoded_info:
            print("QR Code Content:", info)

        # 绘制二维码的四角位置
        if points is not None:
            points = points.astype(int)
            for i in range(len(points)):
                for j in range(4):
                    cv2.line(frame, tuple(points[i][j]), tuple(points[i][(j + 1) % 4]), (0, 255, 0), 3)
                # 在屏幕左上角显示四角的位置坐标
                text = f"{points[i]}"
                frame = draw_text(frame, text, (10, 30 + i * 30), font, (0, 255, 0))
    else:
        # 在屏幕左上角显示“未检测到二维码”
        frame = draw_text(frame, "未检测到二维码", (10, 30), font, (255, 0, 0))

    # 显示帧
    cv2.imshow("QR Code Detection", frame)

    # 按下 'q' 键退出
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放摄像头并关闭窗口
cap.release()
cv2.destroyAllWindows()
