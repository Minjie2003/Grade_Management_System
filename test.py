import psycopg2

#连接数据库
def connect_db():
    try:
        conn = psycopg2.connect(database="postgres", user="postgres", password="123", host="localhost", port="5432")
    except Exception as e:
        print("connect db error:",e)
    else:
        return conn
    return None

#提交数据库语句并断开数据库连接
def close_db_connection(conn):
    conn.commit()
    conn.close()
    
    
    
    
    
if __name__ == "__main__":
    conn = connect_db() #连接数据库
    cur = conn.cursor() #创建会话


    # 增
    cur.execute("insert into apptest_user values(10001,'',0,'123456','root')")
    close_db_connection(conn) 

    print("successfully opreation database")
