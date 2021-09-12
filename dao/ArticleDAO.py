import csv
from bean.Article import Article

def insertArticle(connection,article):
  url = article.url
  title = article.title
  publishDate = article.publishDate
  authors = article.authors
  mycursor = connection.cursor()
  if(publishDate.isspace() or authors.isspace() or publishDate.find("[]")>=0 or authors.find("[]")>=0):
      print("Inserting Article failed! ", article.url)
      return False
  sql = "INSERT INTO article (url, title, publish_date, authors) VALUES (%s, %s, %s, %s)"
  # val = ("đây là url của bài báo", "đây là title của bài báo",time.strftime('%Y-%m-%d %H:%M:%S'),"đây là các tác giả của bài báo")
  val = (url,title,publishDate,authors)
  try:
    mycursor.execute(sql, val)
    connection.commit()
  except Exception:
    print("Inserting Article failed! ",article.url)
    return False
  print(mycursor.rowcount, "was inserted.")
  return True


def loadDataFromCSVFile2DB(dataFileConfig,connection):
    pathFile = dataFileConfig.pathFileDes + "." + dataFileConfig.formatFile
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
