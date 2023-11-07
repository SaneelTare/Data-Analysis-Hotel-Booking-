#!/usr/bin/env python
# coding: utf-8

# # Importing Libraries

# In[6]:


pip install pandas


# In[9]:


pip install matplotlib


# In[11]:


pip install seaborn


# In[13]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')


# # Loading the dataset

# In[14]:


df = pd.read_csv('hotel_booking.csv')


# # Exploratory Data Analysis and Data Cleaning

# In[18]:


# To perform EDA we need to find what exactly is the data present
# if we do not pass any numbers in the head it will show 1st 5 rows
df.head()
# for last 5 rows use .tail()


# In[19]:


df.shape
# to find no. of rows and columns use .shape


# In[20]:


df.drop(['name','email','phone-number','credit_card'],axis=1)
# client wont share personal data of customer like name, email card details phone number rather some general data
# so we delete it
# use axis=1, inplace=True so in new cells the deleted columns does not appear


# In[21]:


df.columns


# In[22]:


df.info()


# In[23]:


# we see reservation status date is object format but we need it in date time format
df['reservation_status_date']=pd.to_datetime(df['reservation_status_date'])


# In[24]:


df.info()


# In[25]:


df.describe(include = 'object')
#used for numerical values only
# include is used for specific mentioned value


# In[26]:


for col in df.describe(include = 'object').columns:
    print(col)
    print(df[col].unique())
    print('-'*50)


# In[27]:


df.isnull().sum()


# In[28]:


df.drop(['agent','company'], axis=1, inplace=True)


# In[29]:


df.columns


# In[30]:


df.dropna(inplace=True)


# In[31]:


df.isnull().sum()


# In[35]:


df.describe()


# In[33]:


df['adr'].plot(kind='box')


# In[34]:


df=df[df['adr']<5000]


# # Data Analysis and Visualization

# In[46]:


cancelled_perc = df['is_canceled'].value_counts(normalize = True)
print(cancelled_perc)

plt.figure(figsize=(5,4))
plt.title('Reservation status count')
color=['lightgreen','red']
plt.bar(['Not cancelled','Cancelled'],df['is_canceled'].value_counts(), color=color, edgecolor='k',width=0.7)
# 37% cancellation


# In[51]:


plt.figure(figsize=(8,4))
ax1=sns.countplot(x='hotel',hue ='is_canceled', data=df, palette = 'Blues')
legend_labels,_ = ax1.get_legend_handles_labels()
# ax1.legend(bbox_to_anchor(1,1))
plt.title('Reservation status in different hotels', size=20)
plt.xlabel('hotel')
plt.ylabel('number of reservations')
plt.legend(['not cancelled', 'cancelled'])
plt.show()


# In[55]:


resort_hotel=df[df['hotel']=='Resort Hotel']
resort_hotel['is_canceled'].value_counts(normalize=True)
# 27% of reservations are getting cancelled


# In[56]:


city_hotel=df[df['hotel']=='City Hotel']
city_hotel['is_canceled'].value_counts(normalize=True)
# 41% reservations are getting cancelled


# In[57]:


resort_hotel = resort_hotel.groupby('reservation_status_date')[['adr']].mean()
city_hotel = city_hotel.groupby('reservation_status_date')[['adr']].mean()


# In[60]:


plt.figure(figsize=(20,8))
plt.title('Average Daily Rate in City and Resort Hotel', fontsize = 30)
plt.plot(resort_hotel.index,resort_hotel['adr'], label ='Resort Hotel')
plt.plot(city_hotel.index,city_hotel['adr'], label ='City Hotel')
plt.legend(fontsize=20)
plt.show()


# In[62]:


df['month']=df['reservation_status_date'].dt.month
plt.figure(figsize=(16,8))
ax1=sns.countplot(x='month',hue='is_canceled',data=df,palette='bright')
legend_labels,_ = ax1.get_legend_handles_labels()
ax1.legend(bbox_to_anchor=(1,1))
plt.title('Reservation status per month',size=20)
plt.xlabel('month')
plt.ylabel('number of reservations')
plt.legend(['not cancelled', 'cancelled'])
plt.show()


# In[68]:


plt.figure(figsize=(15,8))
plt.title('ADR per month',fontsize=30)
colors = sns.color_palette("husl", 12) # used to provide 12 multiple colors to different bar graphs
sns.barplot(x='month',y='adr',data = df[df['is_canceled']==1].groupby('month')[['adr']].sum().reset_index(),palette=colors)
plt.legend(fontsize = 20)
plt.show()


# In[71]:


cancelled_data = df[df['is_canceled']==1]
top_10_countries = cancelled_data['country'].value_counts()[:10]
plt.figure(figsize=(8,8))
plt.title('Top 10 countries with reservation cancelled')
plt.pie(top_10_countries, autopct='%.2f',labels=top_10_countries.index)
plt.show()


# In[72]:


df['market_segment'].value_counts()


# In[74]:


df['market_segment'].value_counts(normalize=True)


# In[75]:


cancelled_data['market_segment'].value_counts(normalize=True)


# In[90]:


cancelled_df_adr = cancelled_data.groupby('reservation_status_date')[['adr']].mean()
cancelled_df_adr.reset_index(inplace = True)
cancelled_df_adr.sort_values ('reservation_status_date', inplace = True)

not_cancelled_data=df[df['is_canceled']==0]
not_cancelled_df_adr = not_cancelled_data.groupby('reservation_status_date')[['adr']].mean()
not_cancelled_df_adr.reset_index(inplace = True)
not_cancelled_df_adr.sort_values('reservation_status_date', inplace = True)

plt.figure (figsize = (20,6))
plt.title('Average Daily Rate')
plt.plot(not_cancelled_df_adr['reservation_status_date'],not_cancelled_df_adr['adr'], label = 'not cancelled')
plt.plot(cancelled_df_adr['reservation_status_date'],cancelled_df_adr['adr'], label ='cancelled')
plt.legend()


# In[91]:


cancelled_df_adr = cancelled_df_adr[(cancelled_df_adr['reservation_status_date']>'2016')&(cancelled_df_adr['reservation_status_date']<'2017-09')]
not_cancelled_df_adr = not_cancelled_df_adr[(not_cancelled_df_adr['reservation_status_date']>'2016')&(not_cancelled_df_adr['reservation_status_date']<'2017-09')]


# In[93]:


# cancelled_df_adr = cancelled_data.groupby('reservation_status_date')[['adr']].mean()
# cancelled_df_adr.reset_index(inplace = True)
# cancelled_df_adr.sort_values ('reservation_status_date', inplace = True)

# not_cancelled_data=df[df['is_canceled']==0]
# not_cancelled_df_adr = not_cancelled_data.groupby('reservation_status_date')[['adr']].mean()
# not_cancelled_df_adr.reset_index(inplace = True)
# not_cancelled_df_adr.sort_values('reservation_status_date', inplace = True)

plt.figure (figsize = (20,6))
plt.title('Average Daily Rate',fontsize=30)
plt.plot(not_cancelled_df_adr['reservation_status_date'],not_cancelled_df_adr['adr'], label = 'not cancelled')
plt.plot(cancelled_df_adr['reservation_status_date'],cancelled_df_adr['adr'], label ='cancelled')
plt.legend()


# In[ ]:




