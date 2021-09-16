import db.Connection as Con
from mysql.connector import Error
from dateutil.parser import parse
import db.Connection as Con
from dao import  DataFileDAO
import pathlib

rootPath = pathlib.Path(__file__).parent
dbStagingConnection = Con.getConnection('db_staging')
dbWarehouseConnection = Con.getConnection('db_control')

# @description load data form data staging to data warehouse
    # @return
    # @author Duyen Tran (duyen.tran@ecepvn.org)

def load(dataFile):
    # update status datafile by id
    dataFile.status = "loading"
    DataFileDAO.updateStatusDataFile(dataFile)
    try:
        #  select data
        mySql_Select_Query = """SELECT url, title, publish_date, authors
                                FROM article_transform"""
        cursor_wh = dbStagingConnection.cursor();
        result = cursor_wh.execute(mySql_Select_Query);
        records = cursor_wh.fetchall()
     
        sql = "INSERT INTO article (url, title, publish_date, authors) VALUES (%s, %s, %s, %s)"
        cursor_article_app = dbWarehouseConnection.cursor();

        for row in records:
            cursor_article_app.execute(sql, (row[0], row[1], row[2], row[3]));
        dbWarehouseConnection.commit()
        dbStagingConnection.commit()

    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if dbStagingConnection.is_connected():
            # cursor_wh.close()
            # connection_wh.close()
            print("MySQL connection is closed")
        
        if dbWarehouseConnection.is_connected():
            # cursor_article_app.close()
            # connection_article.close()
            print("MySQL connection is closed")
    # update status datafile by id
    dataFile.status = "loaded"
    DataFileDAO.updateStatusDataFile(dataFile)

