def calculator(s):
    safe_words = "0123456789+-*/(). "
    # 修复：原来遍历的是 safe_words 本身，永远检查不出非法字符；
    # 改成遍历输入字符串 s，逐字符和白名单比对
    # 新增：输入不是字符串时直接返回提示，避免下面遍历时报 TypeError
    if not isinstance(s, str):
        return "输入必须是字符串"
    for c in s:
        if c not in safe_words:
            # 修复：返回错误信息而不是抛异常，让 ReAct 循环能继续观察和重试
            return f"非法字符: {c}"
    try:
        return eval(s)
    except ZeroDivisionError:
        return "除数不能为零"
    except (SyntaxError, TypeError):
        return "表达式无法解析"
