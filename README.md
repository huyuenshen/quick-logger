# 🚀 Quick-Datalog

[![PyPI Version](https://img.shields.io/pypi/v/quick-datalog.svg)](https://pypi.org/project/quick-datalog/)
[![Python Versions](https://img.shields.io/pypi/pyversions/quick-datalog.svg)](https://pypi.org/project/quick-datalog/)
[![License](https://img.shields.io/pypi/l/quick-datalog.svg)](https://github.com/huyuenshen/Quick-Datalog/blob/main/LICENSE)

> 一个轻量级 Python 日志工具，支持分级日志、彩色终端输出、自动异常捕获、配置文件自动生成。无需复杂配置即可即插即用！

---

## ✨ 核心功能

- **日志分级**  
  支持 `DEBUG(0)` / `INFO(1)` / `WARN(2)` / `ERROR(3)` 四级别日志

- **彩色输出**  
  不同级别日志不同颜色：  
  `DEBUG` <span style="color: cyan;">青色</span>、`INFO` <span style="color: green;">绿色</span>、`WARN` <span style="color: orange;">黄色</span>、`ERROR` <span style="background: red; color: white;">红底白字</span>

- **异常自动捕获**  
  通过装饰器一键为函数添加异常捕获，自动记录错误堆栈

- **配置自动生成**  
  首次运行自动创建配置文件和日志目录，无需手动初始化

- **按日期分文件**  
  每天生成独立日志文件，避免单文件过大

- **模式切换**  
  支持调试/生产模式快速切换（通过命令行参数 `-O`）

---

## 📦 安装方式

### 方式 1：直接安装 Wheel 包（推荐）

```bash
pip install quick_datalog-1.0.0-py3-none-any.whl
```
（在 Releases/ 目录下找到相应 `.whl` 文件）

---

### 方式 2：源码安装

```bash
git clone https://your.repo.url.git
cd 项目目录
pip install .
```


---

## 🚀 快速上手

### 基础用法（装饰器自动注入 logger）

```python
from quick_datalog import start_logger

@start_logger
def test_func():
    logger.log("这是 DEBUG 日志（调试模式可见）", typ=0)
    logger.log("这是 INFO 日志", typ=1)
    logger.log("这是 WARN 日志", typ=2)
    1 / 0  # 故意抛出异常，会被装饰器捕获并记录 ERROR 日志

if __name__ == "__main__":
    try:
        test_func()
    except Exception:
        pass  # 可选择捕获异常，避免程序终止
```

---

### 手动创建 logger 实例

```python
from quick_datalog import Datalog

logger = Datalog()
logger.log("手动创建的 INFO 日志", typ=1)
logger.log("手动创建的 ERROR 日志", typ=3)
```

---

## ⚙️ 配置说明

### 配置结构自动生成

首次运行后，自动创建如下结构于项目根目录：

```
Datalog/
├── .config/
│   └── Config.json        # 配置文件
└── log_2025_12_12.txt     # 当日日志文件
```

### 配置文件示例：`Config.json`
(事实上默认配置也是这样)

```json
{
    "pattern": "[{time}][{func}][{type}]:{inform}",
    "file": "./Datalog/log_{time}.txt"
}
```

#### 配置项释义

| 配置项   | 说明                 | 可用变量（花括号包裹）       |
|:---------|:---------------------|:-----------------------------|
| pattern  | 日志输出格式         | time（时间），func（函数），type（级别），inform（内容） |
| file     | 日志文件路径/命名规则 | {time} 自动替换为 年_月_日（如 2025_12_12） |

#### 示例：自定义日志格式

```json
{
    "pattern": "[{time}][{module}][{func}][{type}]: {inform}",
    "file": "./Datalog/my_log_{time}.txt"
}
```

---

## 🔧 高级用法

### 模式切换（调试/生产）

- **调试模式（默认）**：
  ```bash
  python your_script.py
  ```
  显示全部等级日志（DEBUG/INFO/WARN/ERROR）

- **生产模式**：
  ```bash
  python your_script.py -O
  ```
  只显示 INFO 及以上级别日志

---

### 捕获异常细节

- 装饰器 `@start_logger` 会自动注入 `logger` 变量
- 捕获函数内部全部未处理异常
- 自动记录函数名、错误、完整堆栈
- 异常捕获后会继续抛出（不阻断），可在外层捕获或忽略

---

### 自定义日志颜色

可直接修改源码中 `COLORS` 字典（ANSI 转义序列）：

```python
COLORS = {
    "DEBUG": "\033[36m",        # 青色
    "INFO": "\033[32m",         # 绿色
    "WARN": "\033[33m",         # 黄色
    "ERROR": "\033[41;1;37m"    # 红底白字加粗
}
```

#### 常用 ANSI 颜色码

| 名称  | 字符串        | 说明               |
|:------|:-------------|:-------------------|
| 黑色  | `\033[30m`   |                   |
| 红色  | `\033[31m`   |                   |
| 绿色  | `\033[32m`   |                   |
| 黄色  | `\033[33m`   |                   |
| 蓝色  | `\033[34m`   |                   |
| 紫色  | `\033[35m`   |                   |
| 青色  | `\033[36m`   |                   |
| 白色  | `\033[37m`   |                   |
| 加粗  | `;1`         | 例: `\033[31;1m`   |
| 背景  | `\033[4xm`   | 例: `\033[41m` 红底 |

---

## 📋 日志级别一览

| 级别   | 数值 | 说明           | 显示场景                        |
|:-------|:-----|:---------------|:---------------------------------|
| DEBUG  | 0    | 调试信息       | 仅调试模式（无 -O 参数）         |
| INFO   | 1    | 普通运行信息   | 所有模式                         |
| WARN   | 2    | 警告，不影响运行 | 所有模式                         |
| ERROR  | 3    | 错误，影响功能 | 所有模式                         |

---

## ❓ 常见问题

1. **中文乱码**
   - 日志文件编码为 UTF-8（已默认）
   - 配置文件自动处理为 ANSI（cp1252）
2. **日志文件不生成**
   - 检查是否有写入权限
   - 文件路径配置是否正确
3. **ERROR 日志的函数名显示为 ErrorCatch**
   - 为区分主动调用与装饰器捕获
   - 如需真实函数名可参考源码优化方案
4. **Windows 终端无颜色**
   - Win10+ 默认支持 ANSI，无需配置
   - 旧版可执行 `os.system("color")`

---

## 📄 License

本项目采用 **MIT 许可证**，可自由使用、修改和分发。

---

## 📞 反馈与贡献

如有任何问题或建议，欢迎 [提交 Issues](https://github.com/huyuennshen/issues) 或 Pull Request！

---