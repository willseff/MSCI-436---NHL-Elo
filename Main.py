from Scraper import scraper

y = scraper(2000, 1004)

k =y.returnDf()

print(k)

y.toCsv()
