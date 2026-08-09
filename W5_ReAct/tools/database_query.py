# 新增：import 统一放文件顶部（原来 sqlite3 写在函数内部，且缺少 typing 导入，
# 导致模块一加载就报 NameError: name 'Optional' is not defined）
import sqlite3
from typing import Optional, List, Tuple


def database_query(db_path: str, sql: str, params: tuple = (), one_row: bool = False) -> Optional[List[Tuple]]:
    """
    SQLite 查询封装，仅执行SELECT
    :param db_path:数据库路径
    :param sql:select语句，占位符用 ?（修复：原 docstring 写的 %s 是错的，sqlite3 用 ?）
    :param params:条件参数元组
    :param one_row:True获取单行，False获取全部
    """
    # 新增：先校验只允许 SELECT，避免误执行 INSERT/UPDATE/DELETE
    if not sql.strip().lower().startswith("select"):
        return "只允许执行 SELECT 语句"

    conn = None
    cur = None
    try:
        conn = sqlite3.connect(db_path)
        cur=conn.cursor()
        cur.execute(sql,params)
        if one_row:
            result = cur.fetchone()
        else:
            result = cur.fetchall()
        return result
    except sqlite3.Error as err:
        # 修复：返回错误字符串而非只打印，便于 ReAct 循环观察
        return f"数据库查询异常:{err}"
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
