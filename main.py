import time
import newspaper
import schedule
from newspaper import Article
from newspaper import news_pool
import mysql.connector
from mysql.connector import Error
from dateutil.parser import parse
import db.Connection as Con
from dao import DataFileConfigDAO, ArticleDAO, DataFileDAO
from src import ScrapeData
import pathlib

rootPath = pathlib.Path(__file__).parent
dbControlConnection = Con.getConnection('db_control')
dbStagingConnection = Con.getConnection('db_staging')



def connectDatabase(database):
    connection = mysql.connector.connect(
        host="localhost",
        database=database,
        user="root",
        password="MaiThanh@%)$99"
    )
    # db_Info = connection.get_server_info()
    # print("Connected to MySQL Server version ", db_Info)
    # cursor = connection.cursor()
    # cursor.execute("select database();")
    # record = cursor.fetchone()
    # print("You're connected to database: ", record)
    return connection;
    # @description Get Process Name
    # @return
    # @author Duyen Tran (duyen.tran@ecepvn.org)
def spellDate(strDate):
    date = strDate.split(', ')[1];
    # print (date)
    # date = '12/9/2021'
    required_date = parse(date).strftime('%Y-%m-%d')
    # print(required_date);
    return required_date;

# @description Get Process Name
    # @return
    # @author Duyen Tran (duyen.tran@ecepvn.org)
def transfrom(dataFile):
    # update status datafile by id
    dataFile.status = "transforming"
    DataFileDAO.updateStatusDataFile(dataFile)
    try:
        connection = connectDatabase('db_staging');
        # print(connection);
        #  select data
        mySql_Select_Query = """SELECT url, title, publish_date, authors
                                FROM article"""
        cursor = connection.cursor();
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
        connection.commit()

    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
    # update status datafile by id
    dataFile.status = "transformed"
    DataFileDAO.updateStatusDataFile(dataFile)

# @description Get Process Name
    # @return
    # @author Duyen Tran (duyen.tran@ecepvn.org)

def load(dataFile):
    # update status datafile by id
    dataFile.status = "loading"
    DataFileDAO.updateStatusDataFile(dataFile)
    try:
        connection_wh = connectDatabase('db_staging');
        connection_article = connectDatabase('db_warehouse');

        # print(connection);
        #  select data
        mySql_Select_Query = """SELECT url, title, publish_date, authors
                                FROM article_transform"""
        cursor_wh = connection_wh.cursor();
        result = cursor_wh.execute(mySql_Select_Query);
        records = cursor_wh.fetchall()
     
        sql = "INSERT INTO article (url, title, publish_date, authors) VALUES (%s, %s, %s, %s)"
        # cursor.execute(sql, ("123123123", "123123", "2021-12-09", "A"));
        cursor_article_app = connection_article.cursor();

        for row in records:
            cursor_article_app.execute(sql, (row[0], row[1], row[2], row[3]));
        connection_article.commit()
        connection_wh.commit()

    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection_wh.is_connected():
            # cursor_wh.close()
            # connection_wh.close()
            print("MySQL connection is closed")
        
        if connection_article.is_connected():
            # cursor_article_app.close()
            # connection_article.close()
            print("MySQL connection is closed")
    # update status datafile by id
    dataFile.status = "loaded"
    DataFileDAO.updateStatusDataFile(dataFile)

#how many articles paper has?
def checkSize(websiteURL):
    paper = newspaper.build(websiteURL,memoize_articles=False)
    print(paper.size())


def main():
    # checkSize("http://www.ted.com")
    configID = 4

    # fetch data from website, convert to csv file
    dataFile = ScrapeData.fetchArticles(configID)

    # load data from csv to table "article" in "db_warehouse" dababase
    # ArticleDAO.loadDataFromCSVFile2DB()

    # transform data
    transfrom(dataFile);

    # load data
    load(dataFile);

if __name__ == '__main__':
    # checkSize("http://cnn.com")

    # schedule
    # # schedule.every().monday.at("18:00").do(main)
    # schedule.every(1).minutes.do(main)
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)

    # run immedietly
    main()


popular_urls = ['http://www.huffingtonpost.com', 'http://cnn.com', 'http://www.time.com', 'http://www.ted.com',
                'http://pandodaily.com', 'http://www.cnbc.com', 'http://www.mlb.com', 'http://www.pcmag.com',
                'http://www.foxnews.com', 'http://theatlantic.com', 'http://www.bbc.co.uk', 'http://www.vice.com',
                'http://www.elle.com', 'http://www.vh1.com', 'http://espnf1.com', 'http://espn.com',
                'http://www.npr.org', 'http://www.sfgate.com', 'http://www.glamour.com', 'http://www.whosdatedwho.com',
                'http://kotaku.com', 'http://thebostonchannel.com', 'http://www.suntimes.com',
                'http://www.businessinsider.com', 'http://www.rivals.com', 'http://thebusinessjournal.com',
                'http://www.newrepublic.com', 'http://allthingsd.com', 'http://www.topgear.com',
                'http://thecitizen.com', 'http://www.ign.com', 'http://www.sci-news.com',
                'http://www.morningstar.com', 'http://www.variety.com', 'http://thebottomline.as.ucsb.edu',
                'http://www.gamefaqs.com', 'http://blog.searchenginewatch.com', 'http://thedailyfairfield.com',
                'http://www.solarnovus.com', 'http://medicalxpress.com', 'http://www.news.com.au',
                'http://www.health.com', 'http://www.computerandvideogames.com', 'http://wsj.com',
                'http://www.allure.com', 'http://www.theinsider.com', 'http://cnet.com',
                'http://venturebeat.com', 'http://www.topspeed.com', 'http://thedailyworld.com',
                'http://games.com', 'http://www.religionnews.com', 'http://blogs.berkeley.edu',
                'http://www.sbnation.com', 'http://www.polygon.com', 'http://nytimes.com',
                'http://www.thefrisky.com', 'http://telegram.com', 'http://yahoo.com', 'http://www.nbcnews.com',
                'http://thedailypage.com', 'http://www.popsci.com', 'http://www.pbs.org', 'http://www.nasa.gov',
                'http://www.guardiannews.com', 'http://www.weather.com', 'http://www.gq.com', 'http://www.etonline.com',
                'http://telegraph.co.uk', 'http://www.fastcompany.com', 'http://www.infoworld.com',
                'http://www.wired.com', 'http://www.pcgamer.com', 'http://sportingnews.com',
                'http://theatlanticwire.com', 'http://thecarconnection.com', 'http://www.sun-sentinel.com',
                'http://autoblog.com', 'http://www.environmentalleader.com', 'http://thecrimson.com',
                'http://thecypresstimes.com', 'http://www.dailyfinance.com', 'http://www.politico.com',
                'http://newsroom.fb.com', 'http://news.ycombinator.com', 'http://lifehacker.com', 'http://www.bet.com',
                'http://independent.co.uk', 'http://www.mlssoccer.com', 'http://www.bodybuilding.com',
                'http://www.cosmopolitan.com', 'http://www.apple.com', 'http://www.autonews.com',
                'http://www.eonline.com', 'http://www.vanityfair.com', 'http://techdigest.tv',
                'http://www.maximumpc.com', 'http://www.techradar.com', 'http://thedailyjournal.com',
                'http://www.mlive.com', 'http://techworld.com.au', 'http://www.techmeme.com',
                'http://thedailynewsegypt.com', 'http://thedailygrind.com.au', 'http://techcrunch.com',
                'http://tehrantimes.com', 'http://www.hollywoodreporter.com', 'http://thedailysound.com',
                'http://www.stltoday.com', 'http://deadspin.com', 'http://www.digitaltrends.com',
                'http://seattletimes.com', 'http://seattlepi.com', 'http://www.cleveland.com', 'http://heritage.org',
                'http://www.today.com', 'http://www.politifact.com', 'http://zdnet.com',
                'http://www.nationalenquirer.com', 'http://egotastic.com', 'http://blogs.creativeloafing.com',
                'http://townhall.com', 'http://www.eweek.com', 'http://www.vogue.co.uk', 'http://www.teenvogue.com',
                'http://www.nypost.com', 'http://www.reuters.com', 'http://www.scientificamerican.com',
                'http://www.miamiherald.com', 'http://www.nydailynews.com', 'http://www.newscientist.com',
                'http://bigstory.ap.org', 'http://www.ebony.com', 'http://thedailystar.com',
                'http://www.technologyreview.com', 'http://www.theverge.com', 'http://www.nba.com',
                'http://www.cbssports.com', 'http://betabeat.com', 'http://www.tmz.com', 'http://tcnewsnet.com',
                'http://www.latimes.com', 'http://www.c-span.org', 'http://www.style.com',
                'http://www.peoplestylewatch.com', 'http://theboot.com', 'http://www.foxbusiness.com',
                'http://www.pcworld.com', 'http://washingtontimes.com', 'http://thedailyreview.com',
                'http://www.nfl.com', 'http://www.space.com', 'http://washingtontechnology.com',
                'http://www.buzzfeed.com', 'http://inquirer.net', 'http://www.maxim.com', 'http://abcnews.com',
                'http://www.extremetech.com', 'http://thedailytimes.com', 'http://mashable.com',
                'http://washingtonexaminer.com', 'http://www.bhg.com', 'http://tech.mit.edu', 'http://hotair.com',
                'http://www.1up.com', 'http://www.cbc.ca', 'http://gawker.com', 'http://celebuzz.com',
                'http://sciencemag.org', 'http://www.rollingstone.com', 'http://slashdot.org', 'http://www.slate.com',
                'http://bleacherreport.com', 'http://www.nascar.com', 'http://www.forbes.com',
                'http://washingtonpost.com', 'http://nymag.com', 'http://www.microsoft.com', 'http://hbr.org',
                'http://www.ft.com', 'http://www.dailymail.co.uk', 'http://www.theautochannel.com',
                'http://g4tv.com', 'http://www.aljazeera.com', 'http://politicker.com', 'http://nbcsports.nbc.com',
                'http://www.gamespot.com', 'http://news.sky.com', 'http://www.joystiq.com',
                'http://www.escapistmagazine.com', 'http://www.thestreet.com', 'http://www.ew.com',
                'http://www.nj.com', 'http://msn.com', 'http://thedailyreporter.com', 'http://www.economist.com',
                'http://phys.org', 'http://www.glam.com', 'http://perezhilton.com', 'http://www.usmagazine.com',
                'http://aol.com', 'http://www.cbsnews.com', 'http://www.tennis.com', 'http://washingtonian.com',
                'http://www.sciencedaily.com', 'http://foxsports.com', 'http://www.popularmechanics.com', 'http://www.macworld.com',
                'http://thinkprogress.org', 'http://www.mtv.com',
                'http://discovery.com', 'http://www.people.com', 'http://thedailybeast.com', 'http://www.hollywood.com',
                'http://medium.com', 'http://www.engadget.com', 'http://www.usnews.com', 'http://www.billboard.com', 'http://nationalgeographic.com',
                'http://www.purseblog.com', 'http://www.giantbomb.com', 'http://www.automobilemag.com', 'http://thechronicle.com.au',
                'http://tbnweekly.com', 'http://techreport.com', 'http://thedailyfix.com', 'http://www.animenewsnetwork.com',
                'http://www.realclearpolitics.com', 'http://usatoday.com', 'http://www.techspot.com', 'http://discovermagazine.com',
                'http://arstechnica.com', 'http://foreignpolicy.com', 'http://www.redstate.com', 'http://www.marketwatch.com',
                'http://www.eurogamer.net', 'http://cbn.com', 'http://www.parade.com', 'http://www.bbcamerica.com',
                'http://washingtonindependent.com', 'http://drudgereport.com', 'http://beta.na.leagueoflegends.com']
