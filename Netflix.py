import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import textwrap
import matplotlib.dates as mdates

month_order = ['January', 'February', 'March', 'April', 'May', 'June', 
               'July', 'August', 'September', 'October', 'November', 'December']


netflix_data = pd.read_csv("content.csv")

######  Knowing the Data

# print(netflix_data.info())
# print()
# print(netflix_data.describe())
# print()
# print(netflix_data.head())


#### Cleaning 

# netflix_data.dropna(inplace=True)
netflix_data.drop_duplicates(inplace=True)
# Conversion of Release Date to date and time format
netflix_data['Release Date'] = pd.to_datetime(netflix_data['Release Date'], format='%Y-%m-%d', errors='coerce')
netflix_data['Hours Viewed'] = netflix_data['Hours Viewed'].replace(',','',regex=True).astype(float)




### visualising Data(EDT Analysis)

# <--------------Hours vs Content Type--------------->
def billions(x,pos):
    return f'{int(x/ 1e9)}B'

views = netflix_data.groupby(['Content Type'])['Hours Viewed'].sum().reset_index()
views = views.sort_values(by='Hours Viewed',ascending=False)

plt.figure(figsize=(12,6))
plt.xlabel("Content Type")
x = plt.bar(views['Content Type'],views['Hours Viewed'])
x[0].set_color('salmon')
x[1].set_color('skyblue')
plt.ylabel("Hours Watched (in billions)")
plt.title('Total Viewership Hours By Content Type (2023)')
plt.gca().yaxis.set_major_formatter(FuncFormatter(billions))
plt.ylim(0, 120e9)  
plt.xticks(rotation=45, ha='right')  
plt.tight_layout()
plt.savefig('one.png',dpi = 300)
plt.show()


# <--------------Viewership Hours By langauge--------------->

plt.figure()

langViews = netflix_data.groupby(['Language Indicator'])['Hours Viewed'].sum().reset_index()
langViews = langViews.sort_values(by='Hours Viewed',ascending=False)
y = plt.bar(langViews['Language Indicator'],langViews['Hours Viewed'])
plt.title('Total Viewership Hours by Language (2023)')
plt.xlabel('Language')
plt.ylabel('Total Hours Viewed (in Billions)')
cooler_hex_codes = ['#1E3A8A', '#10B981', '#F43F5E', '#F59E0B', '#3B82F6', '#8B5CF6']

for i in y:
    i.set_color(cooler_hex_codes.pop())

plt.gca().yaxis.set_major_formatter(FuncFormatter(billions))
plt.savefig('two.png',dpi = 300)
plt.show()


# <--------------Viewership Hours By Release Month--------------->

netflix_data['Month'] = netflix_data['Release Date'].dt.month_name()
mviews = netflix_data.groupby(['Month'])['Hours Viewed'].sum().reset_index()
mviews['Month Number'] = pd.to_datetime(mviews['Month'], format='%B').dt.month
mviews = mviews.sort_values(by='Month Number')
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

#Bar
ax1.bar(mviews['Month'], mviews['Hours Viewed'], color='blue')
ax1.set_title('Total Viewership Hours By Release Month(2023)')
ax1.set_xlabel('Month')
ax1.set_ylabel('Total Hours Viewed (in billions)')
ax1.tick_params(axis='x', rotation=45)  

ax1.yaxis.set_major_formatter(FuncFormatter(billions))


#Line 
ax2.plot(mviews['Month'], mviews['Hours Viewed'], marker='o', color='red')
ax2.set_title('Total Viewership Hours By Release Month(2023)')
ax2.set_xlabel('Month')
ax2.set_ylabel('Total Hours Viewed (in billions)')
ax2.tick_params(axis='x', rotation=45) 
ax2.yaxis.set_major_formatter(FuncFormatter(billions))


plt.tight_layout()
plt.savefig('three.png',dpi = 300)
plt.show()




# <--------------The Top 5 Most Viewed Titles on Netflix--------------->
top_five = netflix_data.nlargest(5,'Hours Viewed')

def millions(x, pos):
    return f'{x / 1e6}M'

plt.figure(figsize=(10,6))

plt.bar(top_five['Title'],top_five['Hours Viewed'],color = 'skyblue')
plt.title("Top 5 Most Viewed Titles on Netflix")
plt.xlabel('Title',fontsize = 15)
plt.ylabel("Total Hours viewed (in Millions)",fontsize = 15)


wrapped_x = [textwrap.fill(title, width = 15) for title in top_five['Title'] ]


plt.gca().set_xticklabels(wrapped_x)
plt.gca().yaxis.set_major_formatter(FuncFormatter(millions))

plt.tight_layout()
plt.savefig('four.png',dpi = 300)
plt.show()


# <--------------Months vs Content Type--------------->

plt.figure(figsize=(10,6))


show_monthwise_group = netflix_data.loc[netflix_data['Content Type']=='Show']
show_monthwise_group = show_monthwise_group[['Month','Hours Viewed']].sort_values(by = 'Month')
show_monthwise_group['Month'] = pd.Categorical(show_monthwise_group['Month'], categories=month_order, ordered=True)
show_monthwise_group = show_monthwise_group.groupby(['Month'])['Hours Viewed'].sum().reset_index()

plt.plot(show_monthwise_group['Month'],show_monthwise_group['Hours Viewed'],color = 'red',label = 'Show',marker = '.')



mov_monthwise_group = netflix_data.loc[netflix_data['Content Type']=='Movie']
mov_monthwise_group = mov_monthwise_group[['Month','Hours Viewed']].sort_values(by = 'Month')
mov_monthwise_group['Month'] = pd.Categorical(mov_monthwise_group['Month'], categories=month_order, ordered=True)
mov_monthwise_group = mov_monthwise_group.groupby(['Month'])['Hours Viewed'].sum().reset_index()

plt.plot(mov_monthwise_group['Month'],mov_monthwise_group['Hours Viewed'],color = 'skyblue',label = 'Movie',marker = '.')

plt.legend()
plt.title("Viewership Trends by Content Type (2023)")
plt.xlabel('Month',fontsize = 10)
plt.gca().yaxis.set_major_formatter(FuncFormatter(billions))
plt.xticks(rotation = 45)
plt.grid(which='both', linestyle='--', linewidth=0.5) 
plt.minorticks_on() 


plt.ylabel('Total Hours Viewed in Billions',fontsize = 10)
plt.savefig('five.png',dpi = 300)
plt.show()


# <--------------Seasons vs Hours viewed--------------->


def billions(x,pos):
    return f'{int(x/ 1e9)}B'

conditions = [
    netflix_data['Month'].isin(['January', 'December', 'February']),
    netflix_data['Month'].isin(['March', 'April', 'May']),
    netflix_data['Month'].isin(['June', 'July', 'August']),
]

choices = ['Winter', 'Spring', 'Summer']


netflix_data['Season'] = np.select(conditions, choices, default='Fall')


plt.figure()

season_group = netflix_data.groupby(['Season'])['Hours Viewed'].sum().reset_index()
season_group = season_group.sort_values(by= 'Hours Viewed',ascending=False)

plt.bar(season_group['Season'],season_group['Hours Viewed'],color = 'orange')


plt.title('Total Viewership Hours by Release Season')
plt.xlabel('Seasons')
plt.ylabel('Total Hours Viewed (in billions)')
plt.gca().yaxis.set_major_formatter(FuncFormatter(billions))
plt.savefig('six.png',dpi = 300)
plt.show()


