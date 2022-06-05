import datetime
import json
import time
import urllib.request

import pandas as pd

token = "TOKEN"


def analyze_vk():
    g = 0
    posts = {}
    # задаем начальную и конечную дату получения публикаций
    start_date = datetime.datetime(2020, 9, 1, 0, 0)
    end_date = datetime.datetime(2021, 6, 30, 23, 59)
    # получаем данные всех публикаций со стены сообщества
    while g <= 8200:
        url = "https://api.vk.com/method/wall.get?v=5.131&access_token={token}&domain=itis_kpfu&count=100&offset={g}" \
            .format(token=token, g=str(g))
        response = urllib.request.urlopen(url)
        data = json.loads(response.read())
        for item in data['response']['items']:
            if start_date <= datetime.datetime.fromtimestamp(item['date']) <= end_date:
                posts[item['id']] = item['date']
        g += 100
    # создаем датасет
    likes = pd.DataFrame(columns=['post_id', 'post_date', 'first_name', 'last_name'])
    # получаем данные всех участников, постаавивших лайк публикациям
    # и созраняем информацию в датасет
    for post_id in posts.keys():
        url5 = "https://api.vk.com/method/likes.getList?v=5.131&access_token={token}&type=post&owner_id=-41696672&" \
               "extended=true&item_id={k}".format(token=token, k=str(
            post_id))
        response5 = urllib.request.urlopen(url5)
        data5 = json.loads(response5.read())
        try:
            for item in data5['response']['items']:
                fn = item['first_name']
                ln = item['last_name']
                likes = likes.append(
                    {'post_id': post_id, 'post_date': datetime.datetime.fromtimestamp(posts[post_id]), 'first_name': fn,
                     'last_name': ln}, ignore_index=True)
                time.sleep(2)
        except KeyError:
            print(data5)
    # сохраняем датасет в формате .csv
    likes.to_csv(r'likes.csv')


if __name__ == '__main__':
    analyze_vk()
