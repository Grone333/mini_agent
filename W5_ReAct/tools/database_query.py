def database_query(db_path: str,sql:str,params:tuple=(),one_row:bool=False)-> Optional[List[Tuple]|Tuple]:
    """
    SQLite 查询封装，仅执行SELECT
    :param db_path:数据库路径
    :param sql:select语句，占位符 %s
    :param params:条件参数元组
    :param one_row:True获取单行，False获取全部
    """
    import sqlite3

    conn=None
    cur=None
    try:
        conn=sqlite3.connnect(db_path)
        cur=conn.cursor()
        cur.execute(sql,params)
        if one_row:
            result = cur.fetchone()
        else:
            result = cur.fetchall()
        return result
    except sqlite3.Error as err:
        print(f"数据库查询异常:{err}")
        return None
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()