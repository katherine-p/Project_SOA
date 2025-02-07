from nameko.extensions import DependencyProvider
import mysql.connector
from mysql.connector import Error
from mysql.connector import pooling


class DatabaseWrapper:

    def __init__(self, connection):
        self.connection = connection

    def get_all_po(self):
        cursor = self.connection.cursor(dictionary=True)
        sql = "SELECT * FROM purchase_order"
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        return result

    def create_po(self, id_employee, id_supplier, detail_purchase_order):
        cursor = self.connection.cursor(dictionary=True)
        sql = "INSERT INTO purchase_order VALUES (NULL,{},{},CURDATE(),0)".format(
            id_employee, id_supplier)
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()
        #self.create_detail_po(detail_purchase_order)
        return "Add purchase order success"

    def create_detail_po(self, detail_purchase_order):
        cursor = self.connection.cursor(dictionary=True)
        for detail_po in detail_purchase_order:
            sql = "INSERT INTO detail_purchase_order VALUES (NULL,{},{},{},{},{})".format(
            detail_po['id_item'], detail_po['id_purchase'], detail_po['qty'], detail_po['unit'], detail_po['price_per_unit'])
            cursor.execute(sql)
            self.connection.commit()
            cursor.close()  
        return "Add detail purchase order success"
        
    def change_status_po(self, id, status):
        cursor = self.connection.cursor(dictionary=True)
        sql = "UPDATE purchase_order SET status = {} WHERE id = {}".format(status, id)
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()
        return "Update status purchase order success"

    def edit_po(self, id, id_employee, id_supplier, status):
        cursor = self.connection.cursor(dictionary=True)
        sql = "UPDATE purchase_order SET id_employee = {}, id_supplier = {}, status = {} where id = {}".format(
            id_employee, id_supplier, status, id)
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()
        return "Edit purchase order success"

    def delete_po(self, id):
        cursor = self.connection.cursor(dictionary=True)
        sql = "DELETE FROM purchase_order WHERE id = {}".format(id)
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()
        return "Delete purchase order success"

    def create_supplier(self, supplier_name, supplier_address, supplier_phone_number_2, supplier_phone_number_1, supplier_email, supplier_last_update_by):
        cursor = self.connection.cursor(dictionary=True)
        sql = "INSERT INTO `supplier` VALUES (DEFAULT,'{}','{}','{}','{}','{}',1,NOW(),{})".format(supplier_name, supplier_address, 
                supplier_phone_number_2, supplier_phone_number_1, supplier_email, supplier_last_update_by)
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()
        return "Add supplier success"


class Database(DependencyProvider):
    connection_pool = None

    def __init__(self):
        try:
            self.connection_pool = mysql.connector.pooling.MySQLConnectionPool(
                pool_name="database_pool",
                pool_size=5,
                pool_reset_session=True,
                host='localhost',
                database='proyek_soa_2',
                user='root',
                password=''
            )
        except Error as e:
            print("Error while connecting to MySQL using Connection pool ", e)

    def get_dependency(self, worker_ctx):
        return DatabaseWrapper(self.connection_pool.get_connection())
