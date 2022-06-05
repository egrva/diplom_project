import glob
import os
import warnings
import re

import pandas as pd


def create_students_info_dataframe():
    os.chdir("../marks_result")
    student_info = pd.DataFrame()
    marks = pd.DataFrame()
    i = int(1)
    for file in glob.glob("*.csv"):
        data = pd.read_csv(file, sep=',', header=0)
        # data.info()
        for idx, row in data.iterrows():
            student_name = row[0]
            if not pd.isna(student_name) and student_name:
                student_group = row[1]
                try:
                    student_second_name = str(student_name).split(' ')[0]
                    student_first_name = str(student_name).split(' ')[1]
                    student_info = student_info.append({'student_id': i,
                                                        'first_name': student_first_name,
                                                        'second_name': student_second_name,
                                                        'group': student_group}, ignore_index=True)
                    for j in range(2, len(data.columns) - 2):
                        marks = marks.append({'student_id': i,
                                              'discipline': row.index[j],
                                              'total_score': row[j]}, ignore_index=True)
                    data.loc[idx, 'student_id'] = i
                    i += 1
                except IndexError:
                    continue
    return student_info, marks


def get_likes(student_info):
    os.chdir("../likes_result")
    for file in glob.glob("*.csv"):
        data = pd.read_csv(file, sep=',', header=0)
        data.info()
        for idx, row in data.iterrows():
            first_name = row[3]
            second_name = row[4]
            s = student_info.loc[(student_info['first_name'].eq(first_name) &
                                  student_info['second_name'].eq(second_name))
                                  , 'student_id']
            if len(s) > 0:
                student_id = s.iat[0]
                data.loc[idx, 'student_id'] = student_id
    return data


def get_chats(student_info):
    os.chdir("../dialogues_results")
    messages = pd.DataFrame()
    for file in glob.glob("*.csv"):
        data = pd.read_csv(file, sep=',', header=0)
        data.info()
        student_id_glob = 0
        for idx, row in data.iterrows():
            first_name = re.split("\s{1,}", str(row[3]))[0]
            second_name = [i for i in re.split("\s{1,}", str(row[3])) if i][-1]
            s = student_info.loc[(student_info['first_name'].eq(first_name) &
                                  student_info['second_name'].eq(second_name)), 'student_id']
            if len(s) > 0:
                recipient_id = 0
                student_id = s.iat[0]
                if (student_id != 726):
                    student_id_glob = student_id
                    recipient_id = 726
                else:
                    recipient_id = student_id_glob
                messages = messages.append({'student_id': student_id,
                                            'Date': row['Date'],
                                            'Text': row['Text'],
                                            'recipient_id' : recipient_id,
                                            'Author': row['Author']}, ignore_index=True)
                data.loc[idx, 'student_id'] = student_id
    return messages




if __name__ == '__main__':
    warnings.filterwarnings("ignore")
    student_info, marks = create_students_info_dataframe()
    student_info.to_csv(r'students_total.csv', index=False)
    marks.to_csv(r'marks.csv', index=False)
    likes = get_likes(student_info)
    likes.to_csv(r'likes_new.csv', index=False)
    messages = get_chats(student_info)
    messages.to_csv(r'messages_total.csv')

