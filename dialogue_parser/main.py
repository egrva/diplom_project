import datetime
import glob
import os
import warnings

import pandas as pd
from bs4 import BeautifulSoup


def parse_messages():
    start_date = datetime.datetime(2020, 9, 1, 0, 0)
    end_date = datetime.datetime(2021, 6, 30, 23, 59)

    os.chdir("dialogues")
    for file in glob.glob("*.html"):
        print(file)
        file_name = file.split('.')[0]
        with open(file, "r") as f:
            contents = f.read()
            soup = BeautifulSoup(contents, "html.parser")
            messages = soup.find_all("div", {"class": "body"})
            data = pd.DataFrame(columns=['Date', 'Text', 'Author'])
            for message in messages:
                message_tag = message.find_all("div", {"class": "text"})
                if len(message_tag) > 0:
                    message_tag = message_tag[0].get_text().strip()
                message_author = message.find_all("div", {"class": "from_name"})
                if len(message_author) > 0:
                    message_author = message_author[0].get_text().replace('\n', '')
                    message_author = message_author.replace('\n', '')
                message_date = message.find_all("div", {"class": "pull_right date details"})
                if len(message_date) > 0:
                    message_date = message_date[0].get('title')
                    if start_date <= datetime.datetime.strptime(message_date, '%d.%m.%Y %H:%M:%S') <= end_date:
                        data = data.append({'Date': message_date, 'Author': message_author, 'Text': message_tag},
                                           ignore_index=True)
            indexes1 = []
            for row in data.iterrows():
                if len(row[1][0]) == 0 & len(row[1][1]) == 0 & len(row[1][2]) == 0:
                    indexes1.append(row[0])
            data = data.drop(data.index[indexes1])
            data = data.reset_index(drop=True)
            empty_messages = []
            for row in data.iterrows():
                if len(row[1][1]) == 0:
                    empty_messages.append(row[0])
            data = data.drop(data.index[empty_messages])
            data = data.reset_index(drop=True)
            indexes2 = []
            for row in data.iterrows():
                if len(row[1][2]) == 0:
                    indexes2.append(row[0])
            for index in indexes2:
                author = data.iloc[index - 1].Author
                data.loc[[index], 'Author'] = author
            data.to_csv(r'../../dialogues_results/{name}.csv'.format(name=file_name))


if __name__ == '__main__':
    warnings.filterwarnings("ignore")
    analyze_messages()
