import cv2

def decode_qr(img_path):
    # 读取图片
    image = cv2.imread(img_path)
    if image is None:
        raise ValueError("无法读取图片，请检查路径是否正确")

    # 创建 QRCodeDetector 对象
    qr_detector = cv2.QRCodeDetector()

    # 检测并解码二维码
    content, points, _ = qr_detector.detectAndDecode(image)

    if not content:
        return None  # 如果没有检测到二维码，返回 None

    # 将检测到的角点转换为列表
    points = points[0].tolist()

    # 返回结果
    return {
        'content': content,
        'points': points
    }

if __name__ == "__main__":
    result = decode_qr("mission1/4,5,6,right.png")
    if result:
        print("二维码内容:", result['content'])
        print("二维码角点:", result['points'])
    else:
        print("未检测到二维码")
