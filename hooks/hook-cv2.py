"""
自定义PyInstaller hook for opencv-python (cv2)
强制收集cv2模块的所有文件
"""
from PyInstaller.utils.hooks import collect_all, collect_submodules, collect_data_files, get_module_file_attribute
import os

# 收集所有cv2相关内容
datas, binaries, hiddenimports = collect_all('cv2')

# 额外收集子模块
hiddenimports += collect_submodules('cv2')

# 尝试收集numpy相关（cv2依赖numpy）
try:
    numpy_datas, numpy_binaries, numpy_hiddenimports = collect_all('numpy')
    datas += numpy_datas
    binaries += numpy_binaries
    hiddenimports += numpy_hiddenimports
except:
    pass

# 添加显式的隐藏导入
hiddenimports += [
    'numpy',
    'numpy.core',
    'numpy.core._multiarray_umath',
    'numpy.core._multiarray_tests',
]

print(f"[hook-cv2] 收集了 {len(datas)} 个数据文件")
print(f"[hook-cv2] 收集了 {len(binaries)} 个二进制文件")
print(f"[hook-cv2] 收集了 {len(hiddenimports)} 个隐藏导入")
