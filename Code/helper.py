from urlextract import URLExtract
import pandas as pd
from collections import Counter
from nltk.sentiment.vader import SentimentIntensityAnalyzer

extract = URLExtract()
def fetch_stats(selected_user,df):

    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    #total messages
    num_messages = df.shape[0]

    #total words
    words = []
    for message in df['message']:
        words.extend(message.split())

    #media shared
    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]

    #Links shared
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))
    return num_messages,len(words),num_media_messages,len(links)

def most_busy_users(df):
    # x = df['user'].value_counts().head()

    newdf = df.copy()
    newdf = newdf.drop(newdf[newdf.user == "group_notification"].index)
    x = newdf['user'].value_counts().head()

    df = round((df['user'].value_counts()/df.shape[0])*100,2)\
        .reset_index().rename(columns={'index':'name','user':'percent'})
    return x,df

def most_common_words(selected_user,df):
    f = open('stop_hinglish.txt','r')
    stop_words = f.read()

    if selected_user!='Overall':
        df=df[df['user'] == selected_user]
    temp = df[df['user']!= 'group_notification']
    temp =temp[temp['message']!='<Media omitted>\n']
    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

def monthly_timeline(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user'] == selected_user]
    timeline = df.groupby(['year','month_num','month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    timeline['time'] = time
    return timeline

def daily_timeline(selected_user,df):
    if selected_user!= 'Overall':
        df=df[df['user']==selected_user]
    daily_timeline = df.groupby('only_date').count()['message'].reset_index()
    return daily_timeline

def week_activity_map(selected_user,df):
    if selected_user!= 'Overall':
        df=df[df['user']==selected_user]
    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):
    if selected_user!= 'Overall':
        df=df[df['user']==selected_user]
    return df['month'].value_counts()

def activity_heatmap(selected_user,df):
    if selected_user!= 'Overall':
        df=df[df['user']==selected_user]
    user_heatmap = df.pivot_table(index='day_name',columns='period',
    values='message',aggfunc='count').fillna(0)
    return user_heatmap


def sentiment_score(selected_user,df):
    if selected_user!= 'Overall':
        df=df[df['user']==selected_user]
    data = df.copy()
    data = data[data.message != "<Media omitted>\n"]
    sentiments = SentimentIntensityAnalyzer()
    data["Positive"] = [sentiments.polarity_scores(i)["pos"] for i in data["message"]]
    data["Negative"] = [sentiments.polarity_scores(i)["neg"] for i in data["message"]]
    data["Neutral"] = [sentiments.polarity_scores(i)["neu"] for i in data["message"]]
    a = sum(data["Positive"])
    b = sum(data["Negative"])
    c = sum(data["Neutral"])
    if (a > b) and (a > c):
        sentiment = "Positive 😊 "
    elif (b > a) and (b > c):
        sentiment = "Negative 😠 "
    else:
        sentiment = "Neutral 🙂 "
    return sentiment

# import emoji
# def emoji_helper(selected_user,df):
#     if selected_user!='Overall':
#         df=df[df['user'] == selected_user]
#
#     emojis = []
#     for message in df['message']:
#         emojis.extend([c for c in message if c in emoji.EMOJI_DATA])
#     emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
#     return emoji_df