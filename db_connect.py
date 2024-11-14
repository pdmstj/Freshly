import mysql.connector
from mysql.connector import Error


def connect_to_freshlydb():
    try:
        # MySQL 데이터베이스에 연결
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="111111",
            database="freshlydb",
        )

        if connection.is_connected():
            print("Successfully connected to freshlydb!")
            return connection

    except Error as e:
        print(f"Error: {e}")
        return None

connection = connect_to_freshlydb()
if connection:
    try:
        cursor = connection.cursor()
        cursor.execute("SHOW TABLES")

        # 테이블 목록 가져오기
        tables = cursor.fetchall()
        tables_list = [table[0] for table in tables]  # 테이블 이름을 리스트로 저장
        tables_list

    finally:
        cursor.close()
        connection.close()
