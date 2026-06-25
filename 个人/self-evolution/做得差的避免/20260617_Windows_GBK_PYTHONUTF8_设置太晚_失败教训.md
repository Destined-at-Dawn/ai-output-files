# Windows GBK + PYTHONUTF8 设置太晚 → 必须 -X utf8 重启解释器

## 原问题
在 Windows 环境下运行 Python 脚本时，即使设置了 `PYTHONUTF8=1` 环境变量，仍然出现编码错误（如 `UnicodeDecodeError: 'gbk' codec can't decode...`）。

## AI 回复
直接设置环境变量后继续运行脚本，未考虑 Python 解释器需要重启才能加载新的环境变量。

## 错误原因
1. **环境变量加载时机**：Python 解释器在启动时读取环境变量，运行中修改的环境变量不会被已启动的进程感知
2. **Windows GBK 默认编码**：Windows 中文环境默认使用 GBK 编码，PYTHONUTF8 设置后需要重启解释器才生效
3. **进程隔离**：子进程继承父进程的环境变量，但父进程修改环境变量后，已存在的子进程不会更新

## 正确做法

### 方案 1：重启 Python 解释器
```bash
# 设置环境变量后，重新启动 Python
set PYTHONUTF8=1
python your_script.py
```

### 方案 2：使用 -X utf8 参数
```bash
# 直接使用 -X utf8 参数启动 Python
python -X utf8 your_script.py
```

### 方案 3：在脚本开头强制编码
```python
import sys
import io

# 强制标准输出使用 UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
```

### 方案 4：使用 `PYTHONIOENCODING`
```bash
# 设置 PYTHONIOENCODING 环境变量
set PYTHONIOENCODING=utf-8
python your_script.py
```

## 关键教训
- **环境变量设置后需要重启进程**：这是操作系统的基本机制，不仅仅是 Python
- **Windows 中文环境的坑**：GBK 是默认编码，必须显式设置 UTF-8
- **-X utf8 是最可靠的方案**：不依赖环境变量，直接在启动参数中指定

## 适用场景
- Windows 中文环境下的 Python 脚本
- 处理中文文件路径、中文内容时出现编码错误
- 从 Linux/Mac 迁移到 Windows 时遇到的编码问题
