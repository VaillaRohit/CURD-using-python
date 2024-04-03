import mysql.connector 

con=mysql.connector.connect(host='localhost',
                            user='root',
                            password='12345',
                            database='python',
                            auth_plugin='mysql_native_password')

print('\nConnection established succesfully :)\n')