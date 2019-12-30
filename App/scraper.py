import pandas as pd
from datetime import datetime

df_lists = pd.DataFrame()
start_year= 2006
end_year = 2020

#scrapes data from hockeyreference.com
for year in range (start_year,end_year+1):
    k=1

    # 2005 was the lockout so there is no data to be scraped
    if year == 2005:
        print("2005 was the lockout")

    else:
        url = r'https://www.hockey-reference.com/leagues/NHL_' + str(year) + r'_games.html' 

        df_temp_reg = pd.DataFrame(pd.read_html(url)[0])
        df_temp_reg['season'] = year

    # use commented out code if playoff data is desired

        try:
            df_temp_post = pd.DataFrame(pd.read_html(url)[1])
            df_temp_post['season'] = year

        except IndexError as e:
            k = 0
            print('no playoffs available yet')
        
        print (str(year) + " scraped")

    df_lists = df_lists.append(df_temp_reg)

    if k == 1:
        df_lists.append(df_temp_post)

game_data = df_lists
