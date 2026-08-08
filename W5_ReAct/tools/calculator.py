def calculator(s):
    safe_words="0123456789+-*/(). "
    for c in safe_words:
        if c not in safe_words:
            raise ValueError("非法字符")
    try:
        return eval(s)
    except ZeroDivisionError:
        return "除数不能为零"
    except TypeError:
        return "输入类型错误"
