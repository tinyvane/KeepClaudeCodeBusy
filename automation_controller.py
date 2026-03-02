"""
自动化控制模块
负责自动点击Claude Code输入框并发送指令
"""
import pyautogui
import time
import win32gui
import win32con


class AutomationController:
    def __init__(self):
        """初始化自动化控制器"""
        # 设置pyautogui的安全设置
        pyautogui.FAILSAFE = True  # 鼠标移到屏幕角落可以中断
        pyautogui.PAUSE = 0.5  # 每个操作之间暂停0.5秒

        # 要发送的默认消息
        self.default_message = "Go ahead with ur todo list. Remeber to update the PROJECT_PLAN.MD and essestials files, stick to the Claude.md file and git push for significant files changes."

    def find_window_by_title(self, title_keywords):
        """
        根据标题关键词查找窗口

        参数:
            title_keywords: 窗口标题关键词（如 "Claude Code", "Visual Studio Code"）
        返回:
            窗口句柄，如果未找到返回None
        """
        def callback(hwnd, windows):
            if win32gui.IsWindowVisible(hwnd):
                window_title = win32gui.GetWindowText(hwnd)
                if any(keyword.lower() in window_title.lower() for keyword in title_keywords):
                    windows.append(hwnd)
            return True

        windows = []
        win32gui.EnumWindows(callback, windows)
        return windows[0] if windows else None

    def activate_window(self, hwnd):
        """
        激活指定窗口（将其置于前台）

        参数:
            hwnd: 窗口句柄
        """
        try:
            # 如果窗口最小化，先恢复
            if win32gui.IsIconic(hwnd):
                win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)

            # 将窗口置于前台
            win32gui.SetForegroundWindow(hwnd)
            time.sleep(0.5)  # 等待窗口激活
            return True
        except Exception as e:
            print(f"激活窗口失败: {e}")
            return False

    def click_input_and_send_message(self, input_position=None, message=None):
        """
        点击输入框并发送消息

        参数:
            input_position: (x, y) 输入框的位置，如果为None则尝试自动查找
            message: 要发送的消息，如果为None则使用默认消息
        """
        if message is None:
            message = self.default_message

        try:
            # 尝试查找并激活Claude Code窗口
            claude_window = self.find_window_by_title(["Claude", "Visual Studio Code"])

            if claude_window:
                print(f"找到窗口: {win32gui.GetWindowText(claude_window)}")
                self.activate_window(claude_window)
            else:
                print("警告: 未找到Claude Code窗口，继续执行...")

            # 如果指定了输入框位置，点击它
            if input_position:
                x, y = input_position
                print(f"点击输入框位置: ({x}, {y})")
                pyautogui.click(x, y)
                time.sleep(0.5)
            else:
                # 如果没有指定位置，尝试使用热键聚焦输入框
                # 在VSCode/Claude Code中，通常可以用快捷键聚焦
                print("使用快捷键聚焦输入框")
                # Ctrl+L 或其他快捷键（根据实际情况调整）
                pyautogui.hotkey('ctrl', 'l')
                time.sleep(0.5)

            # 清空可能存在的内容
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(0.2)

            # 使用剪贴板粘贴（支持中文）
            print(f"准备粘贴消息: {message}")
            import pyperclip
            pyperclip.copy(message)  # 复制到剪贴板
            time.sleep(0.3)

            # 使用Ctrl+V粘贴
            print("使用Ctrl+V粘贴消息")
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.5)

            # 按下Enter发送
            print("按下Enter键发送")
            pyautogui.press('enter')
            time.sleep(0.3)

            print("消息发送成功！")
            return True

        except Exception as e:
            print(f"发送消息失败: {e}")
            return False

    def set_default_message(self, message):
        """设置默认消息"""
        self.default_message = message

    def test_click_position(self, x, y):
        """
        测试点击位置（用于调试）

        参数:
            x, y: 要点击的坐标
        """
        print(f"测试点击位置: ({x}, {y})")
        print("3秒后执行点击...")
        time.sleep(3)

        pyautogui.click(x, y)
        print("点击完成")


if __name__ == "__main__":
    # 测试代码
    controller = AutomationController()

    print("测试自动化控制器")
    print("5秒后将尝试发送消息...")
    time.sleep(5)

    # 测试发送消息（不指定输入框位置，使用快捷键）
    controller.click_input_and_send_message()
