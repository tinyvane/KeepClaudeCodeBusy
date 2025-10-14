"""
屏幕边框叠加层
在监控区域周围显示一个持久的红色边框
"""
import tkinter as tk


class BorderOverlay:
    def __init__(self):
        self.root = None
        self.region = None

    def show_border(self, region):
        """
        显示边框
        region: (x, y, width, height) 元组
        """
        if self.root:
            self.hide_border()

        self.region = region
        x, y, width, height = region

        # 创建一个透明的顶层窗口
        self.root = tk.Toplevel()
        self.root.title("监控区域边框")

        # 设置窗口属性
        self.root.attributes('-topmost', True)  # 始终在最前面
        self.root.attributes('-alpha', 0.7)      # 半透明
        self.root.overrideredirect(True)         # 无边框

        # Windows特定：点击穿透（让鼠标点击穿过窗口）
        try:
            self.root.attributes('-transparentcolor', 'black')
        except:
            pass

        # 设置窗口位置和大小
        self.root.geometry(f"{width}x{height}+{x}+{y}")

        # 创建画布
        canvas = tk.Canvas(
            self.root,
            width=width,
            height=height,
            bg='black',
            highlightthickness=0
        )
        canvas.pack()

        # 绘制红色边框（内部透明）
        border_width = 4  # 边框宽度
        canvas.create_rectangle(
            0, 0,
            width, height,
            outline='red',
            width=border_width,
            fill='black'
        )

        # 在四个角显示小方块
        corner_size = 10
        corners = [
            (0, 0),  # 左上
            (width - corner_size, 0),  # 右上
            (0, height - corner_size),  # 左下
            (width - corner_size, height - corner_size)  # 右下
        ]

        for cx, cy in corners:
            canvas.create_rectangle(
                cx, cy,
                cx + corner_size, cy + corner_size,
                fill='red',
                outline='red'
            )

        print(f"[DEBUG] 边框已显示: x={x}, y={y}, width={width}, height={height}")

    def hide_border(self):
        """隐藏边框"""
        if self.root:
            try:
                self.root.destroy()
                print("[DEBUG] 边框已隐藏")
            except:
                pass
            self.root = None

    def is_visible(self):
        """检查边框是否可见"""
        return self.root is not None and self.root.winfo_exists()


# 全局单例
_global_border = None

def get_border_overlay():
    """获取全局边框叠加层实例"""
    global _global_border
    if _global_border is None:
        _global_border = BorderOverlay()
    return _global_border


if __name__ == "__main__":
    # 测试代码
    root = tk.Tk()
    root.geometry("300x200")

    border = BorderOverlay()

    def show():
        border.show_border((100, 100, 400, 300))

    def hide():
        border.hide_border()

    tk.Button(root, text="显示边框", command=show).pack(pady=10)
    tk.Button(root, text="隐藏边框", command=hide).pack(pady=10)

    root.mainloop()
