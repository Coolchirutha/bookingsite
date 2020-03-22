import pymysql.cursors

connection = pymysql.connect(   host = '127.0.0.1',
                                user = 'root',
                                password = 'pwd',
                                db = 'test',
                                charset = 'utf8mb4',
                                cursorclass = pymysql.cursors.DictCursor)

print("Connection Successful")

try:
    with connection.cursor() as cursor:
        sql = "SELECT Dept_No,Dept_Name FROM DEPARTMENT"

        cursor.execute(sql)

        print("cursor.description: ",cursor.description)

        print()

        for row in cursor:
            print(row)
finally:
    connection.close()
