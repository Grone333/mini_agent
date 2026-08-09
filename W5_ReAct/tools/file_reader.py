def file_reader(file_path: str, encoding: str = "utf-8") -> str:
    # 新增：包一层 try/except，文件不存在、权限不足等错误
    # 以可读字符串返回，而不是抛异常中断整个 ReAct 循环
    try:
        with open(file_path, "r", encoding=encoding) as f:
            return f.read()
    except OSError as e:
        return f"文件读取失败: {e}"
