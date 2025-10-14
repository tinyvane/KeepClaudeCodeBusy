# Keep Claude Code Busy

> **[中文](README_CN.md) | English | [Français](README_FR.md) | [日本語](README_JA.md) | [Español](README_ES.md)**

A Windows screen region monitoring tool designed to keep Claude Code working continuously while you sleep.

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.7+-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)

## ✨ Features

- ✅ **Visual Region Selection** - Draw a rectangle to select the monitoring area
- ✅ **Real-time Monitoring** - Detects screen changes using image comparison
- ✅ **Smart Detection** - Auto-triggers when no changes detected for 30-120 seconds
- ✅ **Automatic Messaging** - Sends commands to Claude Code automatically
- ✅ **Configuration Persistence** - Remembers your settings (optional)
- ✅ **Clean Exit** - Stop monitoring anytime when you wake up
- ✅ **One-Click Package** - Build standalone EXE file

## 🚀 Quick Start

### Installation

1. **Install dependencies**:
```bash
install.bat
```
or manually:
```bash
pip install -r requirements.txt
```

2. **Run the program**:
```bash
python monitor_tool.py
```
or double-click `run.bat`

### Build EXE (Recommended)

```bash
build_onedir.bat
```

The executable will be in `dist/monitor_tool/monitor_tool.exe`

## 📖 How to Use

### Step 1: Select Monitoring Region

1. Click "选择区域" (Select Region) button
2. Screen becomes semi-transparent
3. **Drag** to draw a rectangle around Claude Code's output area
4. **Press Enter** to confirm (or ESC to cancel)

### Step 2: Select Click Position

1. After confirming region, screen stays semi-transparent
2. **Click** on Claude Code's input field location
3. **Press Enter** again to confirm

### Step 3: Configure Parameters

- **Check Interval**: How often to check for changes (10-60s, default: 30s)
- **Trigger Time**: How long with no changes before triggering (30-120s, default: 45s)
- **Similarity Threshold**: Image comparison strictness (0.90-0.99, default: 0.98)
- **Remember Position**: Auto-restore region on next startup (checkbox)
- **Message**: Text to send when triggered (supports Chinese)

### Step 4: Start Monitoring

Click "开始监控" (Start Monitoring) button and go to sleep! 😴

### Step 5: Stop When You Wake Up

Click "停止监控" (Stop Monitoring) button or close the window.

## 🎯 How It Works

1. Takes screenshots of the monitored region every N seconds
2. Compares current screenshot with previous one
3. If changes detected → reset timer
4. If NO changes for M seconds → automatically:
   - Click the input field
   - Paste message using Ctrl+V (supports Chinese)
   - Press Enter to send
   - Continue monitoring

## ⚙️ Configuration

Settings are saved to `monitor_config.json`:
- Selected region coordinates
- Click position
- Check interval
- Trigger duration
- Similarity threshold
- Remember position setting
- Custom message

## 📁 Project Structure

```
KeepClaudeCodeBusy/
├── monitor_tool.py              # Main program (GUI)
├── screen_monitor.py            # Screen monitoring module
├── automation_controller.py     # Automation control
├── region_selector.py           # Region selection UI
├── border_overlay.py            # Border display
├── requirements.txt             # Python dependencies
├── install.bat                  # Install dependencies
├── run.bat                      # Quick start script
├── build_onedir.bat             # Build EXE
├── README.md                    # Documentation (English)
├── README_CN.md                 # Documentation (Chinese)
├── USAGE_GUIDE.md               # Detailed usage guide
└── UPDATE_LOG.md                # Version changelog
```

## 💡 Tips & Best Practices

### Region Selection
- Select Claude Code's main output area
- Avoid areas with blinking cursors or timestamps
- Region should be large enough (at least 100x100 pixels)

### Parameter Tuning
- **Too sensitive?** → Increase threshold to 0.99 or increase trigger time
- **Not triggering?** → Decrease threshold to 0.95 or reduce trigger time
- **For long tasks** → Set trigger time to 60-90 seconds
- **For quick responses** → Set trigger time to 30-45 seconds

### Before Sleeping Checklist
- ✅ Region and click position correctly selected
- ✅ Claude Code window is visible (not minimized)
- ✅ Computer power settings prevent auto-sleep
- ✅ Monitoring started successfully

## 🛠️ Tech Stack

- **Python 3.7+**
- **tkinter** - GUI framework
- **pyautogui** - Screenshot and automation
- **opencv-python** - Image comparison
- **Pillow** - Image processing
- **pyperclip** - Clipboard operations
- **pywin32** - Windows API
- **PyInstaller** - EXE packaging

## 🐛 Troubleshooting

### Issue: Program can't find Claude Code window
**Solution**: Ensure the window is open and visible, not minimized.

### Issue: Automation doesn't work
**Solution**:
- Don't move mouse to screen corners (PyAutoGUI safety feature)
- Run as administrator if needed
- Ensure no other windows cover Claude Code

### Issue: Always triggering (false positives)
**Solution**:
- Increase trigger time
- Increase similarity threshold (0.99)
- Re-select region without dynamic elements

### Issue: Never triggering (false negatives)
**Solution**:
- Decrease threshold (0.95)
- Check if region is correctly selected
- Verify monitoring is running (check status)

## 📝 Advanced Features

### Clear Configuration
Click "清除配置" (Clear Config) button to reset all settings to defaults.

### Remember Position
Toggle the checkbox to control whether the program remembers your region selection on next startup.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This tool is for personal use only to improve productivity. Use responsibly and in accordance with all applicable terms of service.

## 🌟 Star History

If you find this project useful, please consider giving it a star! ⭐

---

Made with ❤️ for the Claude Code community
