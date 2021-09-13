import csv

import main
from bean.Article import Article
from bean.DataLog import DataLog
from dao import DataLogDAO
import db.Connection as Con
dbControlConnection =  Con.getConnection('db_control')
dbWarehouseConnection = Con.getConnection('db_warehouse')
import pathlib
rootPath = pathlib.Path(__file__).parent

# insert Article to "Article" table in "db_warehouse" database. If article has missing data, Don't insert it.
def insertArticle(connection,article):
  url = article.url
  title = article.title
  publishDate = article.publishDate
  authors = article.authors
  mycursor = connection.cursor()

  # check if has missing data?
  if(publishDate.isspace() or authors.isspace() or
          publishDate.find("[]")>=0 or authors.find("[]")>=0):
      print("Inserting Article failed! ", article.url)
      # write into log
      dataLog = DataLog(description="Inserting Article to Article table in db_warehouse's FAILED! Article URL: "
                                    + str(article.url), name="Insert Article")
      DataLogDAO.insertDataLog(dbControlConnection, dataLog)
      return False

  # insert data
  sql = "INSERT INTO article (url, title, publish_date, authors) VALUES (%s, %s, %s, %s)"
  val = (url,title,publishDate,authors)
  try:
    mycursor.execute(sql, val)
    connection.commit()
  except Exception:
    print("Inserting Article failed! ",article.url)
    # write into log
    dataLog = DataLog(description="Inserting Article to Article table in db_warehouse's FAILED! Article URL: "
                                  + str(article.url), name="Insert Article")
    DataLogDAO.insertDataLog(dbControlConnection, dataLog)
    return False

  # write into log
  dataLog = DataLog(description="Inserting Article to Article table in db_warehouse's SUCCESSFUL! Article URL: "
                                + str(article.url), name="Insert Article")
  DataLogDAO.insertDataLog(dbControlConnection, dataLog)
  print("Insert Article successful! ", article.url)

  return True


def loadDataFromCSVFile2DB(dataFileConfig,connection):
    pathFile = str(main.rootPath)+"/"+dataFileConfig.pathFileDes + "." + dataFileConfig.formatFile
    csv_file = open(pathFile,mode='r', encoding='UTF8')
    csv_reader = csv.reader(csv_file, delimiter=dataFileConfig.separators)
    line_count = 0
    for row in csv_reader:
      if line_count == 0:
        line_count += 1
        continue
      else:
        article = Article(url=row[0],title=row[1],publishDate=row[2],authors=row[3])
        insertArticle(connection,article)
        line_count += 1
    csv_file.close()
    print('Loading data from CSV file to database has completed')
