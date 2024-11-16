import os
import mysql.connector
from mysql.connector import Error

# 계정 정보를 담고 있는 딕셔너리
db_accounts = [
    {
       "user": "root",
        "password": os.getenv("DB_PASSWORD"),
    }
]

# MySQL 데이터베이스에 연결하는 함수
def connect_to_freshlydb(user, password):
    try:
    # MySQL 데이터베이스에 연결
        connection = mysql.connector.connect(
            host="localhost",
            port="3307",  # 워크벤치에 설정된 포트를 사용합니다
            user=user,  # 하드코딩된 값을 삭제하고 매개변수 사용
            password=password,  # 하드코딩된 값을 삭제하고 매개변수 사용
            database="freshly",
        )

        if connection.is_connected():
            print(f"Successfully connected to freshly database with user '{user}'!")
            return connection

    except Error as e:
        print(f"Error with user '{user}': {e}")
        return None

# 계정으로 연결 시도
for account in db_accounts:
    connection = connect_to_freshlydb(account['user'], account['password'])
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SHOW TABLES")

            # 테이블 목록 가져오기
            tables = cursor.fetchall()
            tables_list = [table[0] for table in tables]  # 테이블 이름을 리스트로 저장
            if tables_list:
                print(f"Tables in freshly database with user '{account['user']}':", tables_list)
            else:
                print(f"No tables found in freshly database with user '{account['user']}'.")

        except Error as e:
            print(f"Error executing query with user '{account['user']}': {e}")
        
        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()
            if 'connection' in locals() and connection.is_connected():
                connection.close()
    else:
        print(f"Failed to connect to freshly database with user '{account['user']}'.")
