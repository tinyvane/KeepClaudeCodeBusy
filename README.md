# Keep Claude Code Busy (让 Claude Code 保持忙碌)

> **中文 | [English](README_EN.md) | [Français](README_FR.md) | [日本語](README_JA.md) | [Español](README_ES.md)**

一个 Windows 平台下的屏幕区域监控工具，专为让 Claude Code 在你睡觉时持续工作而设计。

![版本](https://img.shields.io/badge/版本-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.7+-green.svg)
![平台](https://img.shields.io/badge/平台-Windows-lightgrey.svg)
![许可证](https://img.shields.io/badge/许可证-MIT-orange.svg)

## ✨ 功能特点

- ✅ **可视化区域选择** - 画矩形框选择监控区域
- ✅ **实时监控** - 使用图像对比检测画面变化
- ✅ **智能检测** - 30-120秒内无变化时自动触发
- ✅ **自动发送消息** - 自动向 Claude Code 发送指令
- ✅ **配置持久化** - 记住你的设置（可选）
- ✅ **干净退出** - 醒来后随时停止监控
- ✅ **一键打包** - 生成独立的 EXE 文件

## 🚀 快速开始

### 第一步：克隆仓库

```bash
# 使用 HTTPS
git clone https://github.com/tinyvane/KeepClaudeCodeBusy.git

# 或使用 SSH
git clone git@github.com:tinyvane/KeepClaudeCodeBusy.git

# 进入项目目录
cd KeepClaudeCodeBusy
```

### 第二步：安装依赖

1. **安装 Python 依赖**:
```bash
install.bat
```
或手动安装:
```bash
pip install -r requirements.txt
```

### 第三步：运行程序

**方式 1: 直接运行 Python 脚本**
```bash
python monitor_tool.py
```
或双击 `run.bat`

**方式 2: 打包成 EXE（推荐日常使用）**

```bash
build_onedir.bat
```

可执行文件将在 `dist/monitor_tool/monitor_tool.exe`

## 📖 使用方法

### 步骤 1: 选择监控区域

1. 点击"选择区域"按钮
2. 屏幕变为半透明
3. **拖动**鼠标在 Claude Code 输出区域画矩形
4. **按 Enter** 确认（或 ESC 取消）

### 步骤 2: 选择点击位置

1. 确认区域后，屏幕保持半透明
2. **点击** Claude Code 输入框的位置
3. **再次按 Enter** 确认

### 步骤 3: 配置参数

- **检查间隔**: 多久检查一次变化（10-60秒，默认30秒）
- **触发时间**: 无变化多久后触发（30-120秒，默认45秒）
- **相似度阈值**: 图像对比严格度（0.90-0.99，默认0.98）
- **记忆位置**: 下次启动自动恢复区域（复选框）
- **发送消息**: 触发时发送的文字（支持中文）

### 步骤 4: 开始监控

点击"开始监控"按钮，然后去睡觉！😴

### 步骤 5: 醒来后停止

点击"停止监控"按钮或关闭窗口。

## 🎯 工作原理

1. 每隔 N 秒截取监控区域的图像
2. 将当前图像与上一次对比
3. 如果检测到变化 → 重置计时器
4. 如果 M 秒内无变化 → 自动:
   - 点击输入框
   - 使用 Ctrl+V 粘贴消息（支持中文）
   - 按 Enter 发送
   - 继续监控

## ⚙️ 配置

设置保存在 `monitor_config.json`:
- 选择的区域坐标
- 点击位置
- 检查间隔
- 触发时间
- 相似度阈值
- 记忆位置设置
- 自定义消息

## 📁 项目结构

```
KeepClaudeCodeBusy/
├── monitor_tool.py              # 主程序（GUI）
├── screen_monitor.py            # 屏幕监控模块
├── automation_controller.py     # 自动化控制
├── region_selector.py           # 区域选择界面
├── border_overlay.py            # 边框显示
├── requirements.txt             # Python 依赖
├── install.bat                  # 安装依赖
├── run.bat                      # 快速启动脚本
├── build_onedir.bat             # 打包 EXE
├── README.md                    # 文档（中文）
├── README_EN.md                 # 文档（英语）
├── USAGE_GUIDE.md               # 详细使用指南
└── UPDATE_LOG.md                # 版本更新日志
```

## 💡 提示与最佳实践

### 区域选择
- 选择 Claude Code 的主要输出区域
- 避免包含闪烁光标或时间戳的区域
- 区域应足够大（至少 100x100 像素）

### 参数调整
- **太敏感?** → 提高阈值到 0.99 或增加触发时间
- **不触发?** → 降低阈值到 0.95 或减少触发时间
- **长任务** → 设置触发时间为 60-90 秒
- **快速响应** → 设置触发时间为 30-45 秒

### 睡前检查清单
- ✅ 区域和点击位置正确选择
- ✅ Claude Code 窗口可见（未最小化）
- ✅ 电脑电源设置防止自动休眠
- ✅ 监控成功启动

## 🛠️ 技术栈

- **Python 3.7+**
- **tkinter** - GUI 框架
- **pyautogui** - 截图和自动化
- **opencv-python** - 图像对比
- **Pillow** - 图像处理
- **pyperclip** - 剪贴板操作
- **pywin32** - Windows API
- **PyInstaller** - EXE 打包

## 🐛 故障排除

### 问题: 程序找不到 Claude Code 窗口
**解决方案**: 确保窗口打开且可见，未最小化。

### 问题: 自动化不工作
**解决方案**:
- 不要移动鼠标到屏幕角落（PyAutoGUI 安全机制）
- 必要时以管理员身份运行
- 确保没有其他窗口覆盖 Claude Code

### 问题: 总是触发（误判）
**解决方案**:
- 增加触发时间
- 提高相似度阈值（0.99）
- 重新选择区域，避免动态元素

### 问题: 从不触发（漏判）
**解决方案**:
- 降低阈值（0.95）
- 检查区域是否正确选择
- 验证监控正在运行（检查状态）

## 📝 高级功能

### 清除配置
点击"清除配置"按钮重置所有设置为默认值。

### 记忆位置
切换复选框控制程序是否在下次启动时记住区域选择。

## 🤝 贡献

欢迎贡献！请随时提交 Pull Request。

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。

## ⚠️ 免责声明

本工具仅供个人使用以提高生产力。请负责任地使用，并遵守所有适用的服务条款。

## 🌟 Star 历史

如果你觉得这个项目有用，请考虑给它一个 star！⭐

---

用 ❤️ 为 Claude Code 社区制作
