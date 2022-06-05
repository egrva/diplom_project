import warnings

from bs4 import BeautifulSoup
import pandas as pd
import os
import glob


def print_hi(name):
    os.chdir("marks")
    for file in glob.glob("*.html"):
        print(file)
        file_name = file.split('.')[0]
        with open(file, "r", encoding="Windows-1251") as f:
            contents = f.read()
            soup = BeautifulSoup(contents, "html.parser")
            marks = soup.find_all("table")
            rows = marks[0].find_all('tr')
            columns = []
            for column_name in rows[0].find_all('td'):
                name = column_name.get_text()
                columns.append(name)
            data = pd.DataFrame(columns=columns)
            for row in rows[1:]:
                cells = row.find_all('td')
                if (len(cells) > 0):
                    data = data.append({'Семестр': cells[0].get_text(),
                                        'Дисциплина': cells[1].get_text(),
                                        'Балл за работу в семестре': cells[2].get_text(),
                                        'Тип': cells[3].get_text(),
                                        'Полученный балл': cells[4].get_text(),
                                        'Дата сдачи': cells[5].get_text(),
                                        'Итоговый балл': cells[6].get_text(),
                                        'Итоговая оценка': cells[7].get_text()}, ignore_index=True)
            empty_marks = []
            for row in data.iterrows():
                if len(row[1][7]) == 1:
                    empty_marks.append(row[0])
            data = data.drop(data.index[empty_marks])
            data = data.reset_index(drop=True)
            data.to_csv(r'../../marks_result/{name}.csv'.format(name=file_name))


if __name__ == '__main__':
    warnings.filterwarnings("ignore")


