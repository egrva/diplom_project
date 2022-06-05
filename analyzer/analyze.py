import datetime
import sys
import warnings

sys.dont_write_bytecode = True

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
import django

django.setup()

from db.models import *
# import psycopg2

from dostoevsky.models import FastTextSocialNetworkModel
from dostoevsky.tokenization import RegexTokenizer


def get_likes_count(student_id):
    likes = Likes.objects.filter(student_id=student_id)
    return len(likes)

def get_avg_score(student):
    marks = Marks.objects.filter(student=student)
    if (len(marks) > 0):
        marks_sum = 0
        for mark in marks:
            marks_sum+=mark.total_score
        return (marks_sum/len(marks))
    else:
        print(student)


def get_student_emotions(student):
    messages = Messages.objects.filter(author=student)
    return get_emotions(messages)

def get_decanat_emotions(student):
    messages = Messages.objects.filter(recipient=student)
    return get_emotions(messages)

def get_emotions(messages):
    messages_count = len(messages)
    speech_result = None
    neutral_result = None
    negative_result = None
    skip_result = None
    positive_result = None
    if messages_count > 0:
        speech = 0.0
        speech_count = 0
        neutral = 0.0
        neutral_count = 0
        negative = 0.0
        negative_count = 0
        skip = 0.0
        skip_count = 0
        positive = 0.0
        positive_count = 0
        FastTextSocialNetworkModel.MODEL_PATH = 'fasttext_data/fasttext-social-network-model.bin'
        tokenizer = RegexTokenizer()
        model = FastTextSocialNetworkModel(tokenizer=tokenizer)
        for message in messages:
            text = message.text_message
            results = model.predict(text, k=5)
            for a in results:
                if ('positive' in a):
                    positive += a['positive']
                    positive_count += 1
                if ('speech' in a):
                    speech += a['speech']
                    speech_count += 1
                if ('neutral' in a):
                    neutral += a['neutral']
                    neutral_count += 1
                if ('negative' in a):
                    negative += a['negative']
                    negative_count += 1
                if ('skip' in a):
                    skip += a['skip']
                    skip_count += 1
        if (speech_count > 0):
            speech_result = speech / speech_count
        if (neutral_count > 0):
            neutral_result = neutral / neutral_count
        if (negative_count > 0):
            negative_result = negative / negative_count
        if (skip_count > 0):
            skip_result = skip / skip_count
        if (positive_count > 0):
            positive_result = positive / positive_count
    return messages_count, speech_result, neutral_result, negative_result, skip_result, positive_result

def get_most_popular_time(student):
    messages = Messages.objects.filter(author=student)
    if (len(messages) > 0):
        #Утро - 06:00 - 12:00
        #День - 12:00 - 18:00
        #Вечер - 18:00 - 24:00
        #Ночь - 00:00 - 06:00
        day_start_time = datetime.time(hour=12)
        evening_start_time = datetime.time(hour=18)
        night_start_time = datetime.time(hour=0)
        morning_start_time = datetime.time(hour=6)
        times = {"Утро": 0, "День": 0, "Вечер": 0, "Ночь": 0}
        for message in messages:
            message_time = message.date_message.time()
            if (day_start_time <= message_time < evening_start_time):
                times['День']+=1
            if (evening_start_time <= message_time < night_start_time):
                times['Вечер']+=1
            if (night_start_time <= message_time < morning_start_time):
                times['Ночь']+=1
            if (morning_start_time <= message_time < day_start_time):
                times['Утро']+=1
        return max(times, key=times.get)



if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    students = Students.objects.all()
    i = 1
    for student in students:
        student_messages_count, avg_speech_student, avg_neutral_student,avg_negative_student, avg_skip_student, avg_positive_student = get_student_emotions(student)
        decanat_messages_count, avg_speech_decanat, avg_neutral_decanat,avg_negative_decanat, avg_skip_decanat, avg_positive_decanat = get_decanat_emotions(student)
        student_statistic = StudentStatistic(
            id = i,
            student= student,
            likes_count = get_likes_count(student.student_id),
            avg_score = get_avg_score(student),
            student_messages_count = student_messages_count,
            avg_speech_student = avg_speech_student,
            avg_neutral_student = avg_neutral_student,
            avg_negative_student = avg_negative_student,
            avg_skip_student = avg_skip_student,
            avg_positive_student = avg_positive_student,
            decanat_messages_count = decanat_messages_count,
            avg_speech_decanat = avg_speech_decanat,
            avg_neutral_decanat = avg_neutral_decanat,
            avg_negative_decanat = avg_negative_decanat,
            avg_skip_decanat = avg_skip_decanat,
            avg_positive_decanat = avg_positive_decanat,
            most_popular_time = get_most_popular_time(student)
        )
        student_statistic.save()
        i+=1


