import pymysql.cursors
class MySQLConnection:
    def __init__(self):
        connection = pymysql.connect(host = 'botanicaserver.mysql.database.azure.com',
                                    user = 'codingdojogrupal@botanicaserver',
                                    password = 'DKrH@!HcS78Y83a@',
                                    db = 'biitacora_botanica',
                                    charset = 'utf8mb4',
                                    cursorclass = pymysql.cursors.DictCursor,
                                    autocommit = True,
                                    ssl={'ca': '/home/site/wwwroot/BaltimoreCyberTrustRoot.crt.pem'})
        self.connection = connection
    def query_db(self, query, data=None):
        with self.connection.cursor() as cursor:
            try:
                query = cursor.mogrify(query, data)
                print("Ejecutando la siguiente consulta:", query)

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
                print("La base de datos ha devuelto el siguiente error:", e)
                return False
            finally:
                print("Todo ha salido correctamente, cerrando instancia de conexión...")
                self.connection.close() 

def connectToMySQL():
    return MySQLConnection()