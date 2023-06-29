from pymysql import connect


def connection():
    conn = connect(host="localhost", user="root", passwd="nepal", db="MajorProject")
    c = conn.cursor()
    return c, conn
