import csv
import main
from bean.Article import Article
from bean.DataFile import DataFile
from bean.DataLog import DataLog
from dao import DataLogDAO, DataFileDAO
import db.Connection as Con
from dao.DataFileConfigDAO import getConfigRow
from dao.DataFileDAO import getDataFileByStatus

dbControlConnection =  Con.getConnection('db_control')
dbStagingConnection = Con.getConnection('db_staging')

def isArticleExist(article):
    url = article.url
    mycursor = dbStagingConnection.cursor()
    sql = "SELECT * from article WHERE url = %s"
    val = (url,)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    if(len(myresult)>0):
        return True
    return False

# insert Article to "Article" table in "db_staging" database.
def insertArticle(article):
    # if article existed, don't insert
  if(isArticleExist(article)):
      print("Inserting Article failed! Article existed ", article.url)
      # write into log
      dataLog = DataLog(description="FAILED insert Article to Article table in db_staging! Article EXISTED. Article URL: "
                                    + str(article.url), name="Insert Article")
      DataLogDAO.insertDataLog(dataLog)
      return False

  url = article.url
  title = article.title
  publishDate = article.publishDate
  authors = article.authors
  mycursor = dbStagingConnection.cursor()

  # insert data
  sql = "INSERT INTO article (url, title, publish_date, authors) VALUES (%s, %s, %s, %s)"
  val = (url,title,publishDate,authors)
  try:
    mycursor.execute(sql, val)
    dbStagingConnection.commit()
  except Exception:
    print("Inserting Article failed! ",article.url)
    # write into log
    dataLog = DataLog(description="FAILED insert Article to Article table in db_warehouse! Article URL: "
                                  + str(article.url), name="Insert Article")
    DataLogDAO.insertDataLog(dataLog)
    return False

  # write into log
  dataLog = DataLog(description="SUCCESSFUL insert Article to Article table in db_warehouse! Article URL: "
                                + str(article.url), name="Insert Article")
  DataLogDAO.insertDataLog(dataLog)
  print("Insert Article successful! ", article.url)
  return True


def loadDataFromCSVFile2DB():
    dataFiles = getDataFileByStatus("ER")
    for data in dataFiles:
        dataFile = DataFile(id=data[0], name = data[1],status=data[2],note=data[3],description=data[4],
               createdAt=data[5],updatedAt=data[6],rowCount=data[7],data_config_id=data[8])
        # get data file config
        dataConfigID = dataFile.data_config_id
        dataFileConfig = getConfigRow(dataConfigID)
        # extract data from csv file to staging database
        load(dataFileConfig,dataFile)
        # update status datafile by id
        dataFile.status = "TR"
        DataFileDAO.updateStatusDataFile(dataFile)
        print('Loading data from CSV file to database has completed')


def load(dataFileConfig,dataFile):
    destination = dataFileConfig.destination
    if destination == "article":
        loadCSV2ArticleTable(dataFileConfig,dataFile)



def loadCSV2ArticleTable(dataFileConfig,dataFile):
    pathFile = str(main.rootPath) + "/data/" + dataFile.name
    csv_file = open(pathFile, mode='r', encoding='UTF8')
    csv_reader = csv.reader(csv_file, delimiter=dataFileConfig.separators)

    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
            continue
        else:
            article = Article(url=row[0], title=row[1], publishDate=row[2], authors=row[3])
            insertArticle(article)
            line_count += 1
    csv_file.close()
