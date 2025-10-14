# 项目文件说明

## 核心程序文件

### Python 源代码
- **monitor_tool.py** - 主程序，GUI 界面和核心逻辑
- **screen_monitor.py** - 屏幕监控模块，图像对比和相似度计算
- **automation_controller.py** - 自动化控制模块，鼠标点击和键盘输入
- **region_selector.py** - 区域选择模块，交互式选择监控区域和点击位置
- **border_overlay.py** - 边框覆盖模块，显示红色边框标记监控区域

### 配置文件
- **requirements.txt** - Python 依赖包列表

## 批处理脚本

- **install.bat** - 安装依赖包（运行 pip install）
- **run.bat** - 直接运行 Python 程序
- **build_onedir.bat** - 打包程序为 EXE（目录模式）

## 文档

- **README.md** - 项目主文档，功能介绍和使用说明
- **USAGE_GUIDE.md** - 详细使用指南，分步骤操作说明
- **UPDATE_LOG.md** - 版本更新日志，新功能和改进记录

## Git 配置

- **.gitignore** - Git 忽略文件配置
  - 忽略：`__pycache__/`, `build/`, `dist/`, `*.pyc`
  - 忽略：`monitor_config.json` (用户配置)
  - 忽略：`others/` (开发文件)
  - 忽略：`organize_files.py` (整理脚本)

## 自动生成的文件/目录（不提交到 Git）

### 用户配置
- **monitor_config.json** - 用户保存的配置（区域、参数等）

### Python 运行时
- **__pycache__/** - Python 字节码缓存
- **hooks/** - PyInstaller 自定义钩子（构建时生成）

### 构建输出
- **build/** - PyInstaller 构建临时文件
- **dist/** - 打包后的可执行文件
- ***.spec** - PyInstaller 规格文件

### 开发文件
- **others/** - 旧版本文件和测试脚本（带时间戳）
- **organize_files.py** - 文件整理脚本（开发用）

## 文件依赖关系

```
monitor_tool.py (主程序)
├── region_selector.py (区域选择)
├── screen_monitor.py (屏幕监控)
├── automation_controller.py (自动化控制)
└── border_overlay.py (边框显示)
```

## 用户使用流程

1. 安装依赖：`install.bat`
2. 运行程序：`run.bat` 或 `python monitor_tool.py`
3. 或打包 EXE：`build_onedir.bat`

## 开发者说明

### 添加新功能
- 修改 `monitor_tool.py` - GUI 和主逻辑
- 修改其他模块文件 - 特定功能实现

### 测试程序
- 直接运行：`python monitor_tool.py`
- 查看控制台输出调试信息

### 打包发布
- 运行：`build_onedir.bat`
- 输出：`dist/monitor_tool/monitor_tool.exe`
- 分发整个 `dist/monitor_tool/` 目录

### 版本更新
1. 修改 `monitor_tool.py` 中的 `VERSION` 常量
2. 更新 `UPDATE_LOG.md` 记录改动
3. 测试所有功能
4. 提交到 Git

## 文件大小参考

- Python 源文件：~50 KB 总计
- 依赖包安装：~200 MB (numpy, opencv-python 等)
- 打包后 EXE：~100 MB (包含所有依赖)

## 许可证

（待添加 LICENSE 文件）
