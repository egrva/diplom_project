import sys

from django.db.models import CASCADE

try:
    from django.db import models
except Exception:
    print('Exception: Django Not Found, please install it with "pip install django".')
    sys.exit()


class Students(models.Model):
    student_id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=100)
    second_name = models.CharField(max_length=100)
    group = models.CharField(max_length=100)

    class Meta:
        managed = True
        db_table = 'students'


class Marks(models.Model):
    id = models.IntegerField(primary_key=True)
    student = models.ForeignKey(Students, db_column='student_id', on_delete=CASCADE)
    discipline = models.CharField(max_length=100)
    total_score = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'marks'


class Likes(models.Model):
    id = models.IntegerField(primary_key=True)
    student = models.ForeignKey(Students, db_column='student_id', on_delete=CASCADE)
    post_id = models.IntegerField()
    post_date = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'likes'


class Messages(models.Model):
    id = models.IntegerField(primary_key=True)
    author = models.ForeignKey(Students, db_column='student_id', on_delete=CASCADE, related_name='author')
    recipient = models.ForeignKey(Students, db_column='recipient_id', on_delete=CASCADE, related_name='recipient')
    text_message = models.CharField(max_length=10000)
    date_message = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'messages'


class StudentStatistic(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    student = models.ForeignKey(Students, db_column='student_id', on_delete=CASCADE)
    likes_count = models.IntegerField()
    avg_score = models.FloatField()
    student_messages_count = models.IntegerField()
    decanat_messages_count = models.IntegerField()
    avg_speech_student = models.FloatField()
    avg_neutral_student = models.FloatField()
    avg_negative_student = models.FloatField()
    avg_skip_student = models.FloatField()
    avg_positive_student = models.FloatField()
    avg_speech_decanat = models.FloatField()
    avg_neutral_decanat = models.FloatField()
    avg_negative_decanat = models.FloatField()
    avg_skip_decanat = models.FloatField()
    avg_positive_decanat = models.FloatField()
    most_popular_time = models.CharField(max_length=100)

    class Meta:
        managed = True
        db_table = 'student_statistic'

