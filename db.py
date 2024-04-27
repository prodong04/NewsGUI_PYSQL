import pymysql
 
class Database():
    def __init__(self):
        self.db= pymysql.connect(host='localhost', port= 3306,
                                  user='root',
                                  password='Dlehdfuf401!',
                                  db='mydb',
                                  charset='utf8')
        self.cursor= self.db.cursor(pymysql.cursors.DictCursor)


 
    def logcheck(self,id,password):
        sql = "select LastName from customer WHERE CustomerID=%s AND EncryptedPassword = %s"
        result = self.cursor.execute(sql,(id,password))
        name = self.cursor.fetchone()
        if result ==0:
            return False 
        else :
            return True,name

    def getmylist(self,CustomerID):
        sql ="""select work.Title 
                from work,trans
                where trans.CustomerID = %s and trans.WorkID = work.WorkID"""
        self.cursor.execute(sql,(CustomerID))
        data = self.cursor.fetchall()
        return data

    def getdata (self):
        sql= """select work.Title, artist.LastName, trans.AcquisitionPrice, trans.TransactionID 
                from work, artist, trans
                where trans.WorkID = work.WorkID and work.ArtistID = artist.ArtistID AND trans.CustomerID is null"""
        num=self.cursor.execute(sql)
        data = self.cursor.fetchall()
        return num, data

    def update(self, query, args=None):
            self.cursor.execute(query, args)
            self.db.commit()

    def execute(self, query, args={}):
        self.cursor.execute(query, args) 
 
    def executeOne(self, query, args={}):
        self.cursor.execute(query, args)
        row= self.cursor.fetchone()
        return row
 
    def executeAll(self, query, args={}):
        self.cursor.execute(query, args)
        row= self.cursor.fetchall()
        return row
 
    def commit():
        self.db.commit()
