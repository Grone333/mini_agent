def file_reader(file_path: str, encoding: str = "utf-8") -> str:
    with open(file_path,"r",encoding=encoding)as f:
        return f.read()
