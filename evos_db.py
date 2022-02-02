import sqlite3

class Database:
    def __init__(self):
        self.db_name = "evos_project.db"
        self.conn = sqlite3.connect(self.db_name,check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("""
          CREATE TABLE IF NOT EXISTS "catalog_category"(
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                parent_id  INTEGER,
                FOREIGN KEY (parent_id)
                REFERENCES catalog_category(id)
                  ON UPDATE CASCADE 
                  ON DELETE CASCADE     
          )
        """)
        self.conn.execute("""
         CREATE TABLE IF NOT EXISTS "catalog_type"(
          id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
          name TEXT NOT NULL       
         )        
        """)
        self.conn.execute("""
         CREATE TABLE IF NOT EXISTS "catalog_product"(
         id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
         name TEXT NOT NULL,
         price INTEGER NOT NULL,
         description TEXT NOT NULL,
         photo TEXT NOT NULL,
         category_id INTEGER NOT NULL,
         type_id INTEGER NOT NULL,
         FOREIGN KEY (category_id)  REFERENCES catalog_category(id)
         ON UPDATE CASCADE  ON DELETE CASCADE ,
         FOREIGN KEY (type_id) REFERENCES catalog_type(id)
         ON UPDATE CASCADE ON DELETE CASCADE 
         )
        """)
        self.conn.commit()
    def get_menu(self):
        a = self.conn.execute("""
        SELECT id,name FROM "catalog_category"
        WHERE parent_id is null
        """).fetchall()
        return a
    def get_child_menu(self,id):
        a = self.conn.execute("""
         SELECT id,name FROM catalog_category
         where parent_id = ?
        """,[id]).fetchall()
        return a
    def get_type(self,ctg_id):
        a = self.conn.execute("""
        SELECT ct.id,ct.name FROM catalog_product as cp
        INNER JOIN  catalog_type as ct
        ON cp.type_id = ct.id
        where cp.category_id = ?
        """,[ctg_id]).fetchall()
        return a
    def get_product(self,ctg_id,type_id):
        a = self.conn.execute("""
        SELECT * FROM catalog_product
        WHERE category_id = ? and type_id = ?
        """,[ctg_id,type_id]).fetchone()
        return a
    def get_product_by_id(self,id):
        a = self.conn.execute("""
        SELECT * FROM catalog_product
        WHERE id = ?
        """,[id]).fetchone()
        return a
    def add_category(self):
        ctg = [
            (1,"🌯Lavash",None),
            (2,"🥙Shaurma",None),
            (3,"🍲Donar",None),
            (4,"Goshtli Lavash",1)
        ]
        self.conn.executemany("""
        INSERT INTO "catalog_category" (id,name,parent_id)
        VALUES (?,?,?)
        """,ctg)
        self.conn.commit()