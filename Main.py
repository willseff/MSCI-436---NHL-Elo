from Scraper import scraper


y = scraper(2000, 2004)

df =y.returnDf()


y.toCsv()
