# import pandas, numpy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import itertools
from collections import Counter
from tigerml.eda import Analyser

# Create the required data frames by reading in the files
df=pd.read_excel('SaleData.xlsx')
df1=pd.read_csv("imdb.csv",escapechar='\\')
df2=pd.read_csv('diamonds.csv')
df3=pd.read_csv('movie_metadata.csv')


# Q1 Find least sales amount for each item
# has been solved as an example
def least_sales(df):
    # write code to return pandas dataframe
    ls = df.groupby(["Item"])["Sale_amt"].min().reset_index()
    return ls

# Q2 compute total sales at each year X region   
def sales_year_region(df):   
    # write code to return pandas dataframe
    df['yr'] = df.OrderDate.apply(lambda x: x.strftime('%Y'))
    syr = df.groupby(['yr','Region'])["Sale_amt"].sum().reset_index()
    return syr

# Q3 append column with no of days difference from present date to each order date
def days_diff(df):
    # write code to return pandas dataframe
    curr_time = pd.to_datetime("now")
    def day_left(x):
        t=str(x)
        return t[0:3]
    
    df['days_difference'] = curr_time - df['OrderDate']
    df['days_diff']=df['days_difference'].apply(day_left)
    df=df.drop(['days_difference'],axis=1)
    return df  

# Q4 get dataframe with manager as first column and  salesman under them as lists in rows in second column.
def mgr_slsmn(df):
    # write code to return pandas dataframe
    x=df.groupby(['Manager'])['SalesMan'].unique().reset_index()
    return x

# Q5 For all regions find number of salesman and number of units
def slsmn_units(df):
    # write code to return pandas dataframe
    s=df.groupby('Region')['Units'].sum().reset_index()
    r=df.groupby('Region')['SalesMan'].nunique().reset_index()
    new_df=pd.merge(r,s,how='inner',on='Region')
    new_df.rename(columns={'SalesMan':'salesmen_count','Units' : 'total_sales'}, inplace=True)
    return new_df


# Q6 Find total sales as percentage for each manager
def sales_pct(df):
    # write code to return pandas dataframe
    b=df.groupby('Manager')['Sale_amt'].sum().reset_index()
    total_1=b['Sale_amt'].sum()
    b['percent_sales ']=(b['Sale_amt']/total_1)*100
    b=b.drop(['Sale_amt'],axis=1)
    return b
    

# Q7 get imdb rating for fifth movie of dataframe
def fifth_movie(df):
	# write code here
    p=df.iloc[4]['imdbRating']
    return p

# Q8 return titles of movies with shortest and longest run time
def movies(df):
	# write code here
    l=[]
    mydict={}
    short = df[df['duration']==df['duration'].min()]['title'].reset_index().iloc[0][1]
    long = df[df['duration']==df['duration'].max()]['title'].reset_index().iloc[0][1]
    #l['shortest_run_time_movie_name']=short
    #l['longest_run_time_movie_name']=long
    l.append(short)
    l.append(long)
    movie=['shortest_run_time_movie_name','longest_run_time_movie_name']
    mydict['movie']=movie
    mydict['name']=l
    res=pd.DataFrame(mydict)
    
    return res

# Q9 sort by two columns - release_date (earliest) and Imdb rating(highest to lowest)
def sort_df(df):
	# write code here
    '''
    a=df.groupby(['year','imdbRating'])['title'].unique().reset_index()
    a['title']=a['title'].apply(lambda x: x[0])
    b=df.drop(['imdbRating','year'],axis=1)
    new_df=pd.merge(a,b,how='inner',on='title')
    return new_df
    '''
    ls=df.sort_values(['year','imdbRating'],ascending=[True,False])
    return ls
    
# Q10 subset revenue more than 2 million and spent less than 1 million & duration between 30 mintues to 180 minutes
def subset_df(df):
    
	# write code here
    result_1 = df[(df['gross'] > 20000000) & (df['budget'] < 10000000) & (df['duration'] >= 30) & (df['duration'] <= 180)]
    #result = df[(df['duration'] >= 30) & (df['duration'] <= 180)]
    return result_1

# Q11 count the duplicate rows of diamonds DataFrame.
def dupl_rows(df):
	# write code here
    result=len(df)-len(df.drop_duplicates())
    return result

# Q12 droping those rows where any value in a row is missing in carat and cut columns
def drop_row(df):
	# write code here
    df = df[pd.notnull(df['carat']) & pd.notnull(df['cut'])]
    return df
    
# Q13 subset only numeric columns
def sub_numeric(df):
	# write code here 
    t=df._get_numeric_data()
    return t

# Q14 compute volume as (x*y*z) when depth > 60 else 8
def volume(df):
	# write code here
    df['x'].fillna((df['x'].mean()), inplace=True)
    df['y'].fillna((df['y'].mean()), inplace=True)
    df["z"].fillna(method ='ffill', inplace = True)
    for i,j in enumerate(df['z']):
        if j=='None':
            df['z'][i]='1'
            
    df['z']=df['z'].apply(lambda x: float(x))
    
    for i,j in enumerate(df['depth']):    
        if (df['depth'][i]>60):
            df['volume']=df['x']*df['y']*df['z']
        else:
            df['volume']=8
    
    return df
    

# Q15 impute missing price values with mean
def impute(df):
	# write code here
    df['price'].fillna((df['price'].mean()), inplace=True)
    return df

#Bonus question
#1.
def report_1(df1):
    data1=df1.groupby(['type','year'])['nrOfGenre'].unique().reset_index()
    data2=df1.groupby(['type','year'])['imdbRating'].max().reset_index()
    data2.rename(columns={'imdbRating':'max_rating'}, inplace=True)
    data3=df1.groupby(['type','year'])['imdbRating'].min().reset_index()
    data3.rename(columns={'imdbRating':'min_rating'}, inplace=True)
    data4=df1.groupby(['type','year'])['imdbRating'].mean().reset_index()
    data4.rename(columns={'imdbRating':'mean_rating'}, inplace=True)
    data5=df1.groupby(['type','year'])['duration'].sum().reset_index()
    data5.rename(columns={'duration':'total_run_time'}, inplace=True)
    
    data1['min_imdbRating']=data3['min_rating']
    data1['max_imdbRating']=data2['max_rating']
    data1['mean_imdbRating']=data4['mean_rating']
    data1['total_run_time_minute']=data5['total_run_time']
    
    final_list=[]
    for i in range(len(df1)):
    
        temp_list_1=['Action', 'Adult', 'Adventure', 'Animation', 'Biography',
           'Comedy', 'Crime', 'Documentary', 'Drama', 'Family', 'Fantasy',
           'FilmNoir', 'GameShow', 'History', 'Horror', 'Music', 'Musical',
           'Mystery', 'News', 'RealityTV', 'Romance', 'SciFi', 'Short', 'Sport',
           'TalkShow', 'Thriller', 'War', 'Western']
        temp_list_2=[]
        temp_var_1=df1.iloc[i]
        temp_var_2=temp_var_1[16:44]
        #print(i)
        #print('\n')
        #print(temp_var_2)
        for k,j in enumerate(temp_var_2):
            #print(j)
            #print(type(j))
        
            if j==1:
                temp_list_2.append(temp_list_1[k])
        #print(temp_list_2)
        final_list.append(temp_list_2)
    
        #print('\n')
        #df1['genere_combination_row_wise']=temp_list_2
        
    df1['genere_combination_row_wise']=final_list
    temp_df_1=df1.groupby(['type','year'])['genere_combination_row_wise'].sum().reset_index()
    
    global_list=[]
    for i,j in enumerate(temp_df_1['genere_combination_row_wise']):
        x=list(set(j))
        #print(i,j,x)
        global_list.append(x)
    data1['genere_groups']=global_list
    
    data1.to_csv(r'report_1.csv')
    
#2.
#by ploting the graph we came to know that there is no specific relation but by apllying df1.corr() we came to know that these two columns #are correlated to some extent
#.........
df1['len_of_char']=df1['title'].apply(lambda x:len(x.split(' (')[0]))
def showgraph(df1):
    #df1['len_of_char']=df1['title'].apply(lambda x:len(x.split('(')[0]))
    x = df1['len_of_char']
    y = df1['imdbRating']
    plt.plot(x,y)
    plt.show()
    
def count_less_than_25(x):
    #a=df['len_of_char'] 
    c=0
    percentile_25=np.percentile(df1['len_of_char'], 25)
    '''
    percentile_50=np.percentile(df1['len_of_char'], 50)
    percentile_75=np.percentile(df1['len_of_char'], 75)
    percentile_100=np.percentile(df1['len_of_char'], 100)
    '''
    for j in x:
        #c=c+1
        if j<percentile_25:
            c=c+1
    return c

def count_between_25_50(x):
    #a=df['len_of_char'] 
    c=0
    percentile_25=np.percentile(df1['len_of_char'], 25)
    percentile_50=np.percentile(df1['len_of_char'], 50)
    '''
    percentile_75=np.percentile(df1['len_of_char'], 75)
    percentile_100=np.percentile(df1['len_of_char'], 100)
    '''
    for j in x:
        #c=c+1
        if j>=percentile_25 and j<percentile_50:
            c=c+1
    return c

def count_between_50_75(x):
    #a=df['len_of_char'] 
    c=0
    #percentile_25=np.percentile(df1['len_of_char'], 25)
    percentile_50=np.percentile(df1['len_of_char'], 50)
    percentile_75=np.percentile(df1['len_of_char'], 75)
    #percentile_100=np.percentile(df1['len_of_char'], 100)
    for j in x:
        #c=c+1
        if j>=percentile_50 and j<percentile_75:
            c=c+1
    return c

def count_greater_than_75(x):
    #a=df['len_of_char'] 
    c=0
    #percentile_25=np.percentile(df1['len_of_char'], 25)
    #percentile_50=np.percentile(df1['len_of_char'], 50)
    percentile_75=np.percentile(df1['len_of_char'], 75)
    #percentile_100=np.percentile(df1['len_of_char'], 100)
    for j in x:
        #c=c+1
        if j>=percentile_75:
            c=c+1
    return c
    

def report_2(df1):
    p=df1.groupby(['year'])['len_of_char'].min().reset_index()
    p.rename(columns={'len_of_char':'min_len_title'}, inplace=True)
    q=df1.groupby(['year'])['len_of_char'].max().reset_index()
    q.rename(columns={'len_of_char':'max_len_title'}, inplace=True)
    p['max_len_title']=q['max_len_title']
    t=df1.groupby(['year'])['len_of_char'].apply(np.hstack).reset_index()
    
    p['less_than_25']=t['len_of_char'].apply(count_less_than_25)
    p['between_25_50']=t['len_of_char'].apply(count_between_25_50)
    p['between_50_75']=t['len_of_char'].apply(count_between_50_75)
    p['greater_than_75']=t['len_of_char'].apply(count_greater_than_75)
    
    return p

#3.

def diamond_crosstab(df4):
    #volume function is written above 
    df4=volume(df4)
    df4['quantile_ex_1']=pd.qcut(df4['volume'],q=4)
    report_3=pd.crosstab(df4.quantile_ex_1,df4.cut,normalize='index')
    return report_3

#4

#this will work for movie_metadata.csv file
#quarter by quarter data is not given so i did it yearly
def report_4(df1):
    q=df1.sort_values(['title_year','gross'],ascending=[False,False])

    avg_ratings_top_10_percent=[]
    year=[2016,2015,2014,2013,2012,2011,2010,2009,2008,2007]
    for i in year:
        ten_percent=int(len(q[q['title_year']==i])*.1)
        avg_ratings_top_10_percent.append(q[q['title_year']==2016].sort_values(['gross'],ascending=False).iloc[0:ten_percent]['imdb_score'].mean())
    mydict={}
    mydict['year']=year
    mydict['avg_ratings_top_10_percent']=avg_ratings_top_10_percent
    res=pd.DataFrame(mydict)
    return res
    

#5
def report_5(df1):
    final_list=[]
    for i in range(0,14332):
    
        temp_list_1=['Action', 'Adult', 'Adventure', 'Animation', 'Biography',
           'Comedy', 'Crime', 'Documentary', 'Drama', 'Family', 'Fantasy',
           'FilmNoir', 'GameShow', 'History', 'Horror', 'Music', 'Musical',
           'Mystery', 'News', 'RealityTV', 'Romance', 'SciFi', 'Short', 'Sport',
           'TalkShow', 'Thriller', 'War', 'Western']
        temp_list_2=[]
        temp_var_1=df1.iloc[i]
        temp_var_2=temp_var_1[16:44]
        #print(i)
        #print('\n')
        #print(temp_var_2)
        for k,j in enumerate(temp_var_2):
            #print(j)
            #print(type(j))
        
            if j==1:
                temp_list_2.append(temp_list_1[k])
        #print(temp_list_2)
        final_list.append(temp_list_2)
    
        #print('\n')
        #df1['genere_combination_row_wise']=temp_list_2
        
    df1['genere_combination_row_wise']=final_list
    
    df1['duration_decile']=pd.qcut(df1['duration'],q=10)
    a=df1.groupby(['duration_decile'])['nrOfWins'].sum().reset_index()
    b=df1.groupby(['duration_decile'])['nrOfNominations'].sum().reset_index()
    c=df1.groupby(['duration_decile'])['ratingCount'].sum().reset_index()
    d=df1['duration_decile'].value_counts().reset_index()
    d.rename(columns={'index':'duration_decile', 'duration_decile':'count'}, inplace=True)
    
    a['nrOfNominations']=b['nrOfNominations']
    a['ratingCount']=c['ratingCount']
    a['count']=d['count']
    
    list_n=[]
    
    for i,j in enumerate(df1.groupby(['duration_decile'])['genere_combination_row_wise'].sum()):
        #print(i,list(set(j))[0:3])
        #list_n.append(list(set(j))[0:3])
        #Counter(df1.groupby(['duration_decile'])['genere_combination_row_wise'].sum()[0])
        p=Counter(j)
        p=sorted(p.items(), key=lambda x: x[1], reverse=True)
        q=p[0:3]
        list_n.append(q)
        #print(i,p[0:3])
        #print('\n')
        
    
    a['top_3_genere']=list_n
    return a

#6
'''
#pass both the data imdb and movie_metadata in this function and it will generate two separate insight report
def report_6(df1,df2):
    
    an = Analyser(df1)
    an.get_report()
    
    an_movie_metadata=Analyser(df2)
    an_movie_metadata.get_report()
    
'''    

    

