"""
屏幕监控模块
监控指定区域的屏幕变化
"""
import time
import cv2
import numpy as np
from PIL import ImageGrab
import threading


class ScreenMonitor:
    def __init__(self, region, check_interval=30, similarity_threshold=0.98):
        """
        初始化屏幕监控器

        参数:
            region: (x, y, width, height) 要监控的区域
            check_interval: 检查间隔时间（秒），默认30秒
            similarity_threshold: 相似度阈值，默认0.98（98%相似视为无变化）
        """
        self.region = region  # (x, y, width, height)
        self.check_interval = check_interval
        self.similarity_threshold = similarity_threshold
        self.last_screenshot = None
        self.is_monitoring = False
        self.monitor_thread = None
        self.last_change_time = time.time()
        self.no_change_callback = None
        self.max_no_change_duration = 60  # 最大无变化时间（秒）

    def capture_region(self):
        """
        捕获指定区域的屏幕截图
        返回: numpy数组格式的图像
        """
        x, y, width, height = self.region
        # PIL截图: (left, top, right, bottom)
        screenshot = ImageGrab.grab(bbox=(x, y, x + width, y + height))
        # 转换为numpy数组
        img_np = np.array(screenshot)
        # 转换为BGR格式（OpenCV使用BGR）
        img_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
        return img_bgr

    def calculate_similarity(self, img1, img2):
        """
        计算两张图片的相似度

        参数:
            img1, img2: 两张要比较的图片（numpy数组）
        返回:
            相似度值（0-1之间，1表示完全相同）
        """
        # 确保图片尺寸相同
        if img1.shape != img2.shape:
            return 0.0

        # 方法1: 使用结构相似性指数（SSIM）
        # 转换为灰度图
        gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

        # 计算差异
        diff = cv2.absdiff(gray1, gray2)

        # 计算相似度（基于像素差异）
        similarity = 1 - (np.sum(diff) / (diff.size * 255))

        return similarity

    def has_changed(self, current_img, previous_img):
        """
        判断图像是否发生变化

        参数:
            current_img: 当前图像
            previous_img: 之前的图像
        返回:
            True表示有变化，False表示无变化
        """
        if previous_img is None:
            return True

        similarity = self.calculate_similarity(current_img, previous_img)
        print(f"图像相似度: {similarity:.4f} (阈值: {self.similarity_threshold})")

        return similarity < self.similarity_threshold

    def monitor_loop(self):
        """监控循环（在独立线程中运行）"""
        print(f"开始监控区域: {self.region}")
        print(f"检查间隔: {self.check_interval}秒")
        print(f"最大无变化时间: {self.max_no_change_duration}秒")

        self.last_screenshot = self.capture_region()
        self.last_change_time = time.time()

        while self.is_monitoring:
            time.sleep(self.check_interval)

            if not self.is_monitoring:
                break

            # 捕获当前屏幕
            current_screenshot = self.capture_region()

            # 检查是否有变化
            if self.has_changed(current_screenshot, self.last_screenshot):
                print("检测到变化！重置计时器。")
                self.last_change_time = time.time()
                self.last_screenshot = current_screenshot
            else:
                # 计算无变化的持续时间
                no_change_duration = time.time() - self.last_change_time
                print(f"无变化持续时间: {no_change_duration:.1f}秒")

                # 如果超过最大无变化时间，触发回调
                if no_change_duration >= self.max_no_change_duration:
                    print(f"无变化时间超过{self.max_no_change_duration}秒，触发回调！")
                    if self.no_change_callback:
                        self.no_change_callback()
                    # 重置计时器，避免重复触发
                    self.last_change_time = time.time()
                    self.last_screenshot = current_screenshot

    def start_monitoring(self, no_change_callback=None):
        """
        开始监控

        参数:
            no_change_callback: 当检测到长时间无变化时调用的回调函数
        """
        if self.is_monitoring:
            print("监控已在运行中")
            return

        self.no_change_callback = no_change_callback
        self.is_monitoring = True

        # 在独立线程中运行监控循环
        self.monitor_thread = threading.Thread(target=self.monitor_loop, daemon=True)
        self.monitor_thread.start()

    def stop_monitoring(self):
        """停止监控"""
        print("停止监控...")
        self.is_monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=2)

    def set_check_interval(self, interval):
        """设置检查间隔时间"""
        self.check_interval = max(1, min(60, interval))  # 限制在1-60秒之间

    def set_max_no_change_duration(self, duration):
        """设置最大无变化时间"""
        self.max_no_change_duration = max(30, min(300, duration))  # 限制在30-300秒之间


if __name__ == "__main__":
    # 测试代码
    def test_callback():
        print("触发了无变化回调！")

    # 测试区域 (x, y, width, height)
    test_region = (100, 100, 400, 300)

    monitor = ScreenMonitor(
        region=test_region,
        check_interval=5,  # 5秒检查一次
        similarity_threshold=0.98
    )
    monitor.set_max_no_change_duration(15)  # 15秒无变化触发

    monitor.start_monitoring(no_change_callback=test_callback)

    try:
        print("监控运行中，按Ctrl+C停止...")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        monitor.stop_monitoring()
        print("监控已停止")
