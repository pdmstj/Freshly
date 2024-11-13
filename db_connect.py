import mysql.connector
from mysql.connector import Error


def connect_to_freshlydb():
    try:
        # MySQL 데이터베이스에 연결
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="111111",  # 사용자의 비밀번호 입력
            database="freshlydb",
        )

        if connection.is_connected():
            print("Successfully connected to freshlydb!")
            cursor = connection.cursor()
            cursor.execute("SHOW TABLES")

            tables = cursor.fetchall()
            print("Tables in freshlydb:")
            for table in tables:
                print(table[0])

    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


# 함수 실행
connect_to_freshlydb()
