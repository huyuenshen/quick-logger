import datetime
import os
import sys
import json
import inspect
import traceback
from functools import wraps  # 保留原函数元信息，关键！

# ===================== 路径与配置初始化 =====================
# 定义路径常量，跨平台兼容
LOG_ROOT = "Logs"
CONFIG_PATH = ".logconfig.json"

# 自动创建目录（简化写法，exist_ok=True 避免重复创建报错）
os.makedirs(LOG_ROOT, exist_ok=True)

# 默认配置（把file里的{time}改为{date}，语义更清晰）
DEFAULT_CONF = {
    "pattern": "[{time}][{func}/{type}]:{inform}",
    "log_dir": LOG_ROOT,
    "file_name": "{date}.log",
    "enable_color": True
}

# 初始化配置文件（不存在则创建）
if not os.path.exists(CONFIG_PATH):
    with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
        json.dump(DEFAULT_CONF, f, indent=4)  # 格式化配置，方便手动修改

# 读取配置
with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
    conf = json.load(f)
    if not os.path.exists(conf["log_dir"]):
        os.makedirs(conf["log_dir"])


# 日志级别控制（-O参数启用生产模式，只显示INFO及以上）
level = 1 if "-O" in sys.argv else 0

# ===================== ANSI颜色配置 =====================
COLORS = {
    "DEBUG": "\033[36m",        # 青色（比灰色醒目）
    "INFO": "\033[32m",         # 绿色
    "WARN": "\033[33m",         # 黄色
    "ERROR": "\033[31m",        # 红色
    "FATAL": "\033[5;41;1;37m"    # 红底白字加粗
}
RESET = "\033[0m"  # 重置颜色，避免终端全局变色

# ===================== 日志核心类 =====================
class Logger(object):
    def __init__(self, pattern=conf["pattern"], file=os.path.join(conf["log_dir"],conf["file_name"])):
        self.pattern = pattern
        # 按日期命名日志文件（每天一个文件，避免文件过多）
        date_str = datetime.datetime.now().strftime(r"%Y_%m_%d")
        time_str = datetime.datetime.now().strftime(r"%H_%M")
        self.file_path = file.format(date=date_str, time=time_str)  # 对应配置里的{date}
        # 追加模式打开，UTF-8编码兼容所有字符（如中文）
        self.file = open(self.file_path, "a", encoding="utf-8")

    def __del__(self):
        """On exit"""
        if hasattr(self, "file") and not self.file.closed:
            self.file.close()

    def _get_real_func_name(self):
        """Get Real Function Name"""
        frame = inspect.currentframe()
        # 向上追溯2层：跳过log方法 → 跳过ErrorCatch → 拿到真实函数
        for _ in range(2):
            frame = frame.f_back if frame else None
        func_name = frame.f_code.co_name if frame else "<unknown>"
        del frame  # 释放栈帧，避免内存泄漏
        return func_name

    def log(self, inf, typ=1):
        '''Logger Main Functon.
            inf: The information to log.
            typ: The type of log.
                0: DEBUG, 1: INFO, 2: WARN, 3: ERROR, 4: FATAL'''
        type_map = {0: "DEBUG", 1: "INFO", 2: "WARN", 3: "ERROR", 4: "FATAL"}
        log_type = type_map.get(typ, "DEBUG")
        if conf["enable_color"]:
            color=COLORS[log_type]
            rst=RESET
        else:
            color=""
            rst=""
        if typ >= level:
            log_content = self.pattern.format(
                time=datetime.datetime.now().strftime(r"%Y-%m-%d %H:%M:%S.%f"),
                func=self._get_real_func_name(),
                type=log_type,
                inform=inf
            )
            print(f"{color}{log_content}{rst}")
            print(log_content, file=self.file, flush=True)
    def debug(self,inf):
        '''Log the informations as DEBUG level.'''
        self.log(inf,typ=0)
    def info(self,inf):
        '''Log the informations as INFO level.'''
        self.log(inf,typ=1)
    def warning(self,inf):
        '''Log the informations as WARN level.'''
        self.log(inf,typ=2)
    def warn(self,inf):
        '''Log the informations as WARN level.'''
        self.log(inf,typ=2)
    def error(self,inf):
        '''Log the informations as ERROR level.'''
        self.log(inf,typ=3)
    def critical(self,inf):
        '''Log the informations as FATAL level.'''
        self.log(inf,typ=4)
    def fatal(self,inf):
        '''Log the informations as FATAL level.'''
        self.log(inf,typ=4)

# ===================== 装饰器（异常捕获器） =====================
def start_logger(fatals=[ImportError, SyntaxError, ModuleNotFoundError, OSError, FileNotFoundError, MemoryError, ConnectionRefusedError,PermissionError, AssertionError]):
    '''Logger Decorator.
        fatals: The fatal errors you want to catch.
            Default: [ImportError, SyntaxError, 
                      ModuleNotFoundError, OSError, 
                      FileNotFoundError, MemoryError, 
                      ConnectionRefusedError,PermissionError, 
                      AssertionError]'''
    def decorator(func):
        @wraps(func)
        def ErrorCatch(*args, **kwargs):
            logger = Logger()
            frame = inspect.currentframe().f_back
            frame.f_locals["logger"] = logger
            try:
                return func(*args, **kwargs)
            except Exception as e:
                is_fatal = any((isinstance(e, fatal_cls) for fatal_cls in fatals))
                error_info = f"Function [{func.__name__}] error: "
                error_info += f"\n{traceback.format_exc()}"
                logger.log(error_info, typ=4 if is_fatal else 3)
                raise e
            finally:
                del frame
        return ErrorCatch
    return decorator

