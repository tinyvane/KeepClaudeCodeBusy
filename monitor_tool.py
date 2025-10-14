"""
Claude Code 监控工具 - 主程序
用于在睡觉时让Claude Code持续工作
"""
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import json
import os
from datetime import datetime
from region_selector import RegionSelector
from screen_monitor import ScreenMonitor
from automation_controller import AutomationController
from border_overlay import get_border_overlay

# 版本号
VERSION = "1.0.0"


class MonitorToolGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Claude Code 监控工具")
        self.root.geometry("600x680")  # 增加高度以显示所有内容，包括新的复选框
        self.root.resizable(False, False)

        # 数据
        self.selected_region = None
        self.monitor = None
        self.controller = AutomationController()
        self.is_monitoring = False

        # 配置文件路径
        self.config_file = "monitor_config.json"

        # 边框和点击位置
        self.border = get_border_overlay()
        self.click_position = None

        # 创建界面
        self.create_widgets()

        # 加载配置
        self.load_config()

        # 设置窗口关闭事件
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_widgets(self):
        """创建界面组件"""
        # 标题
        title_frame = tk.Frame(self.root, bg="#2c3e50", height=80)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)

        title_label = tk.Label(
            title_frame,
            text="Claude Code 自动监控工具",
            font=("Arial", 18, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        title_label.pack(pady=20)

        subtitle_label = tk.Label(
            title_frame,
            text="让AI在你睡觉时持续工作",
            font=("Arial", 10),
            bg="#2c3e50",
            fg="#ecf0f1"
        )
        subtitle_label.pack()

        # 主内容区域
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 区域选择部分
        region_frame = tk.LabelFrame(main_frame, text="1. 选择监控区域", font=("Arial", 11, "bold"), padx=10, pady=10)
        region_frame.pack(fill=tk.X, pady=10)

        self.region_label = tk.Label(region_frame, text="未选择区域", fg="gray")
        self.region_label.pack(side=tk.LEFT, padx=10)

        button_container = tk.Frame(region_frame)
        button_container.pack(side=tk.RIGHT)

        select_btn = tk.Button(
            button_container,
            text="选择区域",
            command=self.select_region,
            bg="#3498db",
            fg="white",
            padx=20,
            pady=5
        )
        select_btn.pack(side=tk.LEFT, padx=5)

        clear_btn = tk.Button(
            button_container,
            text="清除配置",
            command=self.clear_config,
            bg="#95a5a6",
            fg="white",
            padx=15,
            pady=5
        )
        clear_btn.pack(side=tk.LEFT)

        # 参数设置部分
        settings_frame = tk.LabelFrame(main_frame, text="2. 监控参数设置", font=("Arial", 11, "bold"), padx=10, pady=10)
        settings_frame.pack(fill=tk.X, pady=10)

        # 检查间隔
        interval_frame = tk.Frame(settings_frame)
        interval_frame.pack(fill=tk.X, pady=5)

        tk.Label(interval_frame, text="检查间隔 (秒):").pack(side=tk.LEFT, padx=5)
        self.interval_var = tk.IntVar(value=30)
        interval_spinbox = tk.Spinbox(
            interval_frame,
            from_=10,
            to=60,
            textvariable=self.interval_var,
            width=10
        )
        interval_spinbox.pack(side=tk.LEFT, padx=5)
        tk.Label(interval_frame, text="(每隔多久检查一次画面变化)").pack(side=tk.LEFT, padx=5)

        # 无变化触发时间
        duration_frame = tk.Frame(settings_frame)
        duration_frame.pack(fill=tk.X, pady=5)

        tk.Label(duration_frame, text="触发时间 (秒):").pack(side=tk.LEFT, padx=5)
        self.duration_var = tk.IntVar(value=45)
        duration_spinbox = tk.Spinbox(
            duration_frame,
            from_=30,
            to=120,
            textvariable=self.duration_var,
            width=10
        )
        duration_spinbox.pack(side=tk.LEFT, padx=5)
        tk.Label(duration_frame, text="(画面无变化多久后触发指令)").pack(side=tk.LEFT, padx=5)

        # 相似度阈值
        threshold_frame = tk.Frame(settings_frame)
        threshold_frame.pack(fill=tk.X, pady=5)

        tk.Label(threshold_frame, text="相似度阈值:").pack(side=tk.LEFT, padx=5)
        self.threshold_var = tk.DoubleVar(value=0.98)
        threshold_spinbox = tk.Spinbox(
            threshold_frame,
            from_=0.90,
            to=0.99,
            increment=0.01,
            textvariable=self.threshold_var,
            width=10,
            format="%.2f"
        )
        threshold_spinbox.pack(side=tk.LEFT, padx=5)
        tk.Label(threshold_frame, text="(越高越严格，0.98推荐，0.95更敏感)").pack(side=tk.LEFT, padx=5)

        # 记忆位置选项
        remember_frame = tk.Frame(settings_frame)
        remember_frame.pack(fill=tk.X, pady=5)

        self.remember_position_var = tk.BooleanVar(value=True)
        remember_checkbox = tk.Checkbutton(
            remember_frame,
            text="下次启动时自动使用本次框选和点选位置",
            variable=self.remember_position_var,
            command=self.on_remember_position_changed
        )
        remember_checkbox.pack(side=tk.LEFT, padx=5)

        # 自定义消息
        message_frame = tk.Frame(settings_frame)
        message_frame.pack(fill=tk.X, pady=5)

        tk.Label(message_frame, text="发送消息:").pack(anchor=tk.W, pady=5)
        self.message_text = tk.Text(message_frame, height=3, width=50)
        self.message_text.pack(fill=tk.X, pady=5)
        self.message_text.insert("1.0", "请继续完成没有实现的TODO内容或者你认为的更新")

        # 控制按钮部分
        control_frame = tk.LabelFrame(main_frame, text="3. 启动监控", font=("Arial", 11, "bold"), padx=10, pady=10)
        control_frame.pack(fill=tk.X, pady=10)

        button_frame = tk.Frame(control_frame)
        button_frame.pack()

        self.start_btn = tk.Button(
            button_frame,
            text="开始监控",
            command=self.start_monitoring,
            bg="#27ae60",
            fg="white",
            font=("Arial", 12, "bold"),
            padx=30,
            pady=10,
            width=12
        )
        self.start_btn.pack(side=tk.LEFT, padx=10)

        self.stop_btn = tk.Button(
            button_frame,
            text="停止监控",
            command=self.stop_monitoring,
            bg="#e74c3c",
            fg="white",
            font=("Arial", 12, "bold"),
            padx=30,
            pady=10,
            width=12,
            state=tk.DISABLED
        )
        self.stop_btn.pack(side=tk.LEFT, padx=10)

        # 状态显示部分
        status_frame = tk.LabelFrame(main_frame, text="状态", font=("Arial", 11, "bold"), padx=10, pady=10)
        status_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        self.status_label = tk.Label(
            status_frame,
            text="就绪",
            font=("Arial", 10),
            fg="#27ae60",
            anchor=tk.W
        )
        self.status_label.pack(fill=tk.X, pady=5)

        # 底部提示
        tip_frame = tk.Frame(self.root, bg="#ecf0f1", height=40)
        tip_frame.pack(fill=tk.X, side=tk.BOTTOM)
        tip_frame.pack_propagate(False)

        tip_label = tk.Label(
            tip_frame,
            text="提示: 按ESC可以在选择区域时取消 | 鼠标移到屏幕角落可以紧急停止自动化操作",
            font=("Arial", 8),
            bg="#ecf0f1",
            fg="#7f8c8d"
        )
        tip_label.pack(pady=10)

    def on_remember_position_changed(self):
        """当记忆位置复选框状态改变时"""
        if self.remember_position_var.get():
            self.update_status("已启用：下次启动将自动恢复区域设置", "green")
        else:
            self.update_status("已禁用：下次启动需要重新选择区域", "orange")

    def clear_config(self):
        """清除保存的配置"""
        if messagebox.askyesno("确认清除", "确定要清除所有保存的配置吗？\n\n这将清除：\n• 选择的区域和点击位置\n• 红色边框\n• 配置文件\n\n参数设置将恢复默认值。"):
            # 清除区域和边框
            self.selected_region = None
            self.click_position = None
            self.border.hide_border()

            # 重置显示
            self.region_label.config(text="未选择区域", fg="gray")

            # 恢复默认参数
            self.interval_var.set(30)
            self.duration_var.set(45)
            self.threshold_var.set(0.98)
            self.remember_position_var.set(True)
            self.message_text.delete("1.0", tk.END)
            self.message_text.insert("1.0", "请继续完成没有实现的TODO内容或者你认为的更新")

            # 删除配置文件
            try:
                if os.path.exists(self.config_file):
                    os.remove(self.config_file)
                    print(f"[INFO] 配置文件已删除: {self.config_file}")
            except Exception as e:
                print(f"删除配置文件失败: {e}")

            self.update_status("配置已清除，所有设置已恢复默认值", "green")
            messagebox.showinfo("清除成功", "配置已清除！\n所有设置已恢复为默认值。")

    def select_region(self):
        """选择监控区域"""
        self.update_status("请在屏幕上拖动鼠标选择区域...", "blue")

        # 最小化主窗口
        self.root.withdraw()  # 使用withdraw代替iconify，完全隐藏窗口
        self.root.update()     # 强制更新窗口状态

        # 使用线程执行区域选择，避免阻塞
        import threading
        threading.Thread(target=self._do_select_region_thread, daemon=True).start()

    def _do_select_region_thread(self):
        """在线程中执行区域选择"""
        print("[DEBUG] 线程开始执行区域选择...")
        import time
        time.sleep(0.5)  # 等待主窗口完全隐藏

        selector = RegionSelector()
        region = selector.select_region()

        print(f"[DEBUG] 区域选择返回值: {region}")

        # 使用after在主线程中更新GUI
        self.root.after(0, lambda: self._update_region_result(region))

    def _update_region_result(self, result):
        """在主线程中更新区域选择结果"""
        print(f"[DEBUG] 开始更新GUI，result={result}")

        # 恢复主窗口
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()

        if result:
            region, click_pos = result
            self.selected_region = region
            self.click_position = click_pos

            x, y, w, h = region

            # 显示边框
            self.border.show_border(region)

            # 更新显示
            if click_pos:
                cx, cy = click_pos
                self.region_label.config(
                    text=f"区域: X={x}, Y={y}, 宽={w}, 高={h} | 点击: ({cx}, {cy})",
                    fg="green",
                    font=("Arial", 9, "bold")
                )
                print(f"[DEBUG] 点击位置: ({cx}, {cy})")
            else:
                self.region_label.config(
                    text=f"区域: X={x}, Y={y}, 宽={w}, 高={h}",
                    fg="green",
                    font=("Arial", 9, "bold")
                )

            self.update_status("区域选择成功！", "green")
            print(f"[DEBUG] 区域保存成功: {self.selected_region}")
            print(f"[DEBUG] region_label文本已更新")

            # 播放系统提示音
            try:
                import winsound
                winsound.MessageBeep(winsound.MB_OK)
            except:
                pass

            # 显示成功提示
            messagebox.showinfo(
                "选择成功",
                f"区域和点击位置已设置！\n\n"
                f"监控区域:\n• 位置: ({x}, {y})\n• 大小: {w} x {h} 像素\n\n"
                f"点击位置: ({cx}, {cy})\n\n"
                f"红色边框将持续显示在屏幕上。"
            )
        else:
            self.update_status("区域选择已取消", "orange")
            print("[DEBUG] 区域选择失败或被取消")

    
    def start_monitoring(self):
        """开始监控"""
        if not self.selected_region:
            messagebox.showwarning("警告", "请先选择监控区域！")
            return

        if self.is_monitoring:
            messagebox.showinfo("提示", "监控已在运行中")
            return

        # 获取参数
        check_interval = self.interval_var.get()
        max_duration = self.duration_var.get()
        threshold = self.threshold_var.get()
        message = self.message_text.get("1.0", tk.END).strip()

        # 保存配置
        self.save_config()

        # 设置控制器消息
        self.controller.set_default_message(message)

        # 创建监控器
        self.monitor = ScreenMonitor(
            region=self.selected_region,
            check_interval=check_interval,
            similarity_threshold=threshold
        )
        self.monitor.set_max_no_change_duration(max_duration)

        print(f"[DEBUG] 监控参数: 间隔={check_interval}秒, 触发={max_duration}秒, 阈值={threshold}")

        # 启动监控
        self.monitor.start_monitoring(no_change_callback=self.on_no_change_detected)

        self.is_monitoring = True
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.update_status(f"监控运行中... (检查间隔:{check_interval}秒, 触发时间:{max_duration}秒)", "green")

        messagebox.showinfo(
            "监控已启动",
            f"监控已开始运行！\n\n"
            f"• 检查间隔: {check_interval}秒\n"
            f"• 触发时间: {max_duration}秒\n"
            f"• 监控区域: {self.selected_region}\n\n"
            f"你现在可以去睡觉了！程序会自动工作。\n"
            f"醒来后点击'停止监控'按钮退出。"
        )

    def stop_monitoring(self):
        """停止监控"""
        if self.monitor:
            self.monitor.stop_monitoring()

        self.is_monitoring = False
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.update_status("监控已停止", "orange")

    def on_no_change_detected(self):
        """当检测到长时间无变化时的回调"""
        self.update_status("检测到无变化，正在发送指令...", "blue")

        # 在独立线程中执行自动化操作，避免阻塞UI
        def send_command():
            success = self.controller.click_input_and_send_message(input_position=self.click_position)
            if success:
                self.update_status("指令发送成功，继续监控...", "green")
            else:
                self.update_status("指令发送失败，继续监控...", "red")

        threading.Thread(target=send_command, daemon=True).start()

    def update_status(self, message, color="black"):
        """更新状态显示"""
        self.status_label.config(text=f"状态: {message}", fg=color)

    def save_config(self):
        """保存配置到文件"""
        config = {
            "version": VERSION,
            "last_saved": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "region": self.selected_region,
            "click_position": self.click_position,
            "check_interval": self.interval_var.get(),
            "max_duration": self.duration_var.get(),
            "threshold": self.threshold_var.get(),
            "remember_position": self.remember_position_var.get(),
            "message": self.message_text.get("1.0", tk.END).strip()
        }

        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            print(f"[INFO] 配置已保存 (版本: {VERSION})")
        except Exception as e:
            print(f"保存配置失败: {e}")

    def load_config(self):
        """从文件加载配置"""
        if not os.path.exists(self.config_file):
            return

        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)

            # 显示配置版本信息
            config_version = config.get("version", "未知")
            last_saved = config.get("last_saved", "未知")
            print(f"[INFO] 加载配置文件 (版本: {config_version}, 保存时间: {last_saved})")

            # 先加载记忆位置设置
            remember_position = config.get("remember_position", True)
            self.remember_position_var.set(remember_position)

            # 只有在用户选择记忆位置时才恢复区域和点击位置
            if remember_position and config.get("region"):
                self.selected_region = tuple(config["region"])
                self.click_position = tuple(config["click_position"]) if config.get("click_position") else None

                x, y, w, h = self.selected_region

                # 显示边框
                if self.selected_region:
                    self.border.show_border(self.selected_region)

                # 更新显示
                if self.click_position:
                    cx, cy = self.click_position
                    self.region_label.config(
                        text=f"区域: X={x}, Y={y}, 宽={w}, 高={h} | 点击: ({cx}, {cy})",
                        fg="green"
                    )
                else:
                    self.region_label.config(
                        text=f"区域: X={x}, Y={y}, 宽={w}, 高={h}",
                        fg="green"
                    )

            # 其他参数始终加载
            if config.get("check_interval"):
                self.interval_var.set(config["check_interval"])

            if config.get("max_duration"):
                self.duration_var.set(config["max_duration"])

            if config.get("threshold"):
                self.threshold_var.set(config["threshold"])

            if config.get("message"):
                self.message_text.delete("1.0", tk.END)
                self.message_text.insert("1.0", config["message"])

            self.update_status("配置已加载", "green")
        except Exception as e:
            print(f"加载配置失败: {e}")

    def on_closing(self):
        """窗口关闭事件"""
        if self.is_monitoring:
            if messagebox.askokcancel("确认退出", "监控正在运行中，确定要退出吗？"):
                self.stop_monitoring()
                self.root.destroy()
        else:
            self.root.destroy()


def main():
    """主函数"""
    root = tk.Tk()

    # 设置窗口图标（如果有的话）
    # root.iconbitmap("icon.ico")

    app = MonitorToolGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
