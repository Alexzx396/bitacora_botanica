import pymysql.cursors
# import os

class MySQLConnection:
    def __init__(self, db):
        connection = pymysql.connect(host = 'localhost',
                                    user = 'root', 
                                    # password = 'juega101', 
                                    password = 'programacion2022', 
                                    db = db,
                                    charset = 'utf8mb4',
                                    cursorclass = pymysql.cursors.DictCursor,
                                    autocommit = True)
        self.connection = connection

# Descomentar en producción

# class MySQLConnection:
#     def __init__(self, db):
#         connection = pymysql.connect(host = os.getenv('HOST_DB'),
#                                     user = os.getenv('USUARIO_DB'), 
#                                     password = os.getenv('CLAVE_DB'), 
#                                     db = db,
#                                     charset = 'utf8mb4',
#                                     cursorclass = pymysql.cursors.DictCursor,
#                                     autocommit = True,
#                                     ssl={'ca': '/flask_app/config/ssl/BaltimoreCyberTrustRoot.crt.pem'})
#         self.connection = connection

# Descomentar al usarlo en desarrollo


    def query_db(self, query, data=None):
        with self.connection.cursor() as cursor:
            try:
                query = cursor.mogrify(query, data)
                print("Running Query:", query)

                executable = cursor.execute(query, data)
                if query.lower().find("insert") >= 0:
                    self.connection.commit()
                    return cursor.lastrowid
                elif query.lower().find("select") >= 0:
                    result = cursor.fetchall()
                    return result
                else:
                    self.connection.commit()
            except Exception as e:
                print("Something went wrong", e)
                return False
            finally:
                self.connection.close() 

def connectToMySQL(db):
    return MySQLConnection(db)