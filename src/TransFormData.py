
import db.Connection as Con
from mysql.connector import Error
from dateutil.parser import parse
import db.Connection as Con
from dao import  DataFileDAO
import pathlib


rootPath = pathlib.Path(__file__).parent
dbStagingConnection = Con.getConnection('db_staging')


# @description split date form text date weekday,dd//mm//yy, hh:mm:ss
# @return
# @author Duyen Tran (duyen.tran@ecepvn.org)
def spellDate(strDate):
    date = strDate.split(', ')[1];
    # print (date)
    # date = '12/9/2021'
    required_date = parse(date).strftime('%Y-%m-%d')
    # print(required_date);
    return required_date;

# @description transform data form data extract to data staging
    # @return
    # @author Duyen Tran (duyen.tran@ecepvn.org)

def transfrom(dataFile):
    # update status datafile by id
    dataFile.status = "transforming"
    DataFileDAO.updateStatusDataFile(dataFile)
    try:
        #  select data
        mySql_Select_Query = """SELECT url, title, publish_date, authors
                                FROM article"""
        cursor = dbStagingConnection.cursor();
        result = cursor.execute(mySql_Select_Query);
        records = cursor.fetchall()
        # print("Total number of rows in table: ", cursor.rowcount)
        # print("\nPrinting each row")
        # transform & insert data
        sql = "INSERT INTO article_transform (url, title, publish_date, authors) VALUES (%s, %s, %s, %s)"
        # cursor.execute(sql, ("123123123", "123123", "2021-12-09", "A"));

        for row in records:
            date = spellDate(row[2]);
            cursor.execute(sql, (row[0], row[1], date, row[3]));
        dbStagingConnection.commit()

    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if dbStagingConnection.is_connected():
            # cursor.close()
            # dbStagingConnection.close()
            print("MySQL connection is closed")
    # update status datafile by id
    dataFile.status = "transformed"
    DataFileDAO.updateStatusDataFile(dataFile)
