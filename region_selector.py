"""
屏幕区域选择模块
允许用户在屏幕上拖动鼠标选择矩形区域
"""
import tkinter as tk
from PIL import ImageGrab


class RegionSelector:
    def __init__(self):
        self.start_x = None
        self.start_y = None
        self.end_x = None
        self.end_y = None
        self.rect = None
        self.root = None
        self.canvas = None
        self.selection_confirmed = False
        self.click_x = None
        self.click_y = None
        self.click_marker = None
        self.step = 1  # 1=选择区域, 2=选择点击位置

    def select_region(self):
        """
        创建全屏透明窗口，让用户选择区域和点击位置
        返回: ((x, y, width, height), (click_x, click_y)) 元组
        """
        self.root = tk.Tk()
        self.root.attributes('-fullscreen', True)
        self.root.attributes('-alpha', 0.3)
        self.root.attributes('-topmost', True)

        # 获取屏幕尺寸
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # 创建画布
        self.canvas = tk.Canvas(
            self.root,
            cursor="cross",
            bg='grey',
            highlightthickness=0
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # 添加提示文本
        self.help_text = self.canvas.create_text(
            screen_width // 2,
            50,
            text="拖动鼠标选择监控区域，释放鼠标后按 ENTER 确认，ESC 取消",
            font=("Arial", 20, "bold"),
            fill="white",
            tags="help"
        )

        # 绑定鼠标事件
        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

        # 绑定键盘事件
        self.root.bind("<Return>", self.on_confirm)  # Enter键确认
        self.root.bind("<Escape>", self.on_cancel)   # ESC键取消

        self.root.mainloop()

        # 返回选择的区域和点击位置
        if self.selection_confirmed and all([self.start_x, self.start_y, self.end_x, self.end_y]):
            x = min(self.start_x, self.end_x)
            y = min(self.start_y, self.end_y)
            width = abs(self.end_x - self.start_x)
            height = abs(self.end_y - self.start_y)

            region = (x, y, width, height)
            click_pos = (self.click_x, self.click_y) if self.click_x is not None else None

            print(f"[DEBUG] 最终返回区域: {region}")
            print(f"[DEBUG] 最终返回点击位置: {click_pos}")
            return (region, click_pos)

        print("[DEBUG] 返回None（未确认或取消）")
        return None

    def on_press(self, event):
        """鼠标按下事件"""
        if self.step == 1:
            # 步骤1：选择区域
            self.start_x = event.x
            self.start_y = event.y

            print(f"[DEBUG] 步骤1 - 鼠标按下: ({self.start_x}, {self.start_y})")

            # 删除之前的矩形
            if self.rect:
                self.canvas.delete(self.rect)
        elif self.step == 2:
            # 步骤2：选择点击位置
            self.click_x = event.x
            self.click_y = event.y

            print(f"[DEBUG] 步骤2 - 点击位置: ({self.click_x}, {self.click_y})")

            # 删除之前的标记
            if self.click_marker:
                self.canvas.delete(self.click_marker)

            # 绘制点击位置标记（红色十字）
            size = 20
            self.click_marker = self.canvas.create_line(
                self.click_x - size, self.click_y,
                self.click_x + size, self.click_y,
                fill='red', width=3, tags='click_marker'
            )
            self.canvas.create_line(
                self.click_x, self.click_y - size,
                self.click_x, self.click_y + size,
                fill='red', width=3, tags='click_marker'
            )

            # 绘制圆圈
            self.canvas.create_oval(
                self.click_x - 10, self.click_y - 10,
                self.click_x + 10, self.click_y + 10,
                outline='red', width=3, tags='click_marker'
            )

    def on_drag(self, event):
        """鼠标拖动事件"""
        if self.step != 1:
            return  # 只在步骤1时允许拖动

        if self.rect:
            self.canvas.delete(self.rect)

        # 绘制新的矩形
        self.rect = self.canvas.create_rectangle(
            self.start_x, self.start_y,
            event.x, event.y,
            outline='red',
            width=3,
            fill='blue',
            stipple='gray50'
        )

    def on_release(self, event):
        """鼠标释放事件"""
        self.end_x = event.x
        self.end_y = event.y

        print(f"[DEBUG] 鼠标释放: ({self.end_x}, {self.end_y})")

        # 删除旧矩形
        if self.rect:
            self.canvas.delete(self.rect)

        # 绘制最终选择的矩形（黄色表示待确认）
        self.rect = self.canvas.create_rectangle(
            self.start_x, self.start_y,
            self.end_x, self.end_y,
            outline='yellow',
            width=3,
            fill='yellow',
            stipple='gray50'
        )

        # 更新提示文本
        self.canvas.delete("help")
        screen_width = self.root.winfo_screenwidth()
        self.canvas.create_text(
            screen_width // 2,
            50,
            text="按 ENTER 确认选择，ESC 取消重选",
            font=("Arial", 20, "bold"),
            fill="yellow",
            tags="help"
        )

        # 显示区域信息
        center_x = (self.start_x + self.end_x) // 2
        center_y = (self.start_y + self.end_y) // 2

        x = min(self.start_x, self.end_x)
        y = min(self.start_y, self.end_y)
        width = abs(self.end_x - self.start_x)
        height = abs(self.end_y - self.start_y)

        self.canvas.create_text(
            center_x, center_y,
            text=f"区域: {width}×{height}\n按ENTER确认",
            font=("Arial", 14, "bold"),
            fill="white",
            justify=tk.CENTER
        )

        print(f"[DEBUG] 待确认区域: x={x}, y={y}, width={width}, height={height}")

    def on_confirm(self, event):
        """确认选择（Enter键）"""
        if self.step == 1:
            # 步骤1：确认区域选择，进入步骤2
            if self.start_x is not None and self.end_x is not None:
                print("[DEBUG] 步骤1完成，进入步骤2")
                self.step = 2

                # 将矩形变为绿色表示已确认
                if self.rect:
                    self.canvas.delete(self.rect)

                self.rect = self.canvas.create_rectangle(
                    self.start_x, self.start_y,
                    self.end_x, self.end_y,
                    outline='green',
                    width=5,
                    fill='',
                    stipple=''
                )

                # 更新提示文本
                self.canvas.delete("help")
                screen_width = self.root.winfo_screenwidth()
                self.canvas.create_text(
                    screen_width // 2,
                    50,
                    text="现在请点击输入框的位置（用于自动输入），然后按 ENTER 确认",
                    font=("Arial", 20, "bold"),
                    fill="cyan",
                    tags="help"
                )

                # 解除拖动绑定，只保留点击
                self.canvas.unbind("<B1-Motion>")
                self.canvas.unbind("<ButtonRelease-1>")
            else:
                print("[DEBUG] 没有选择区域，无法确认")

        elif self.step == 2:
            # 步骤2：确认点击位置，完成选择
            if self.click_x is not None:
                self.selection_confirmed = True
                print("[DEBUG] 步骤2完成，所有选择确认")

                # 短暂显示确认，然后关闭
                self.root.after(300, self.root.destroy)
            else:
                print("[DEBUG] 没有选择点击位置，请点击输入框位置")

    def on_cancel(self, event):
        """取消选择（ESC键）"""
        print("[DEBUG] 用户按下ESC，取消选择")
        self.selection_confirmed = False
        self.root.destroy()


if __name__ == "__main__":
    # 测试代码
    selector = RegionSelector()
    region = selector.select_region()
    if region:
        print(f"选择的区域: x={region[0]}, y={region[1]}, width={region[2]}, height={region[3]}")
    else:
        print("未选择区域")
