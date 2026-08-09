def file_reader(file_path: str, encoding: str = "utf-8") -> str:
    try:
        with open(file_path, "r", encoding=encoding) as f:
            return f.read()
    except OSError as e:
        return f"文件读取失败: {e}"
