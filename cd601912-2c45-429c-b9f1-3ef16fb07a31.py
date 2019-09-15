#!/usr/bin/env python
# coding: utf-8

# # Этап 1. Получение данных

# Изучим данные, предоставленные сервисом для проекта.

# ## Импорт библиотек

# In[56]:


import pandas as pd


# Прочитаем файл *music_project.csv* и сохраним его в переменной *df*. 

# In[57]:


df = pd.read_csv('/datasets/music_project.csv')


# Получение первых 10 строк таблицы.

# In[58]:


df.head(10)


# Общая информация о данных таблицы *df*.
# 
# 
# 

# In[59]:


df.info()


# Рассмотрим полученную информацию подробнее.
# 
# Всего в таблице 7 столбцов, тип данных у каждого столбца - < напишите название типа данных >.
# 
# Подробно разберём, какие в *df* столбцы и какую информацию они содержат:
# 
# * userID — идентификатор пользователя;
# * Track — название трека;  
# * artist — имя исполнителя;
# * genre — название жанра;
# * City — город, в котором происходило прослушивание;
# * time — время, в которое пользователь слушал трек;
# * Day — день недели.
# 
# Количество значений в столбцах различается. Это говорит о том, что в данных есть <введите определение> значения.
# 
# 

# **Выводы**

# Каждая строка таблицы содержит информацию о композициях определённого жанра в определённом исполнении, которые пользователи слушали в одном из городов в определённое время и день недели. Две проблемы, которые нужно решать: пропуски и некачественные названия столбцов. Для проверки рабочих гипотез особенно ценны столбцы *time*, *day* и *City*. Данные из столбца *genre* позволят узнать самые популярные жанры.

# # Этап 2. Предобработка данных

# Получаем перечень названий столбцов. Какая наблюдается проблема — кроме тех, что уже были названы ранее?

# In[60]:


df.columns


# Переименуем столбцы для удобства дальнейшей работы. Проверим результат.
# 
# 

# В названиях столбцов есть пробелы, которые могут затруднять доступ к данным.

# In[61]:


df.set_axis(['user_id', 'track_name', 'artist_name', 'genre_name', 'city', 'time', 'weekday'], axis='columns', inplace=True)


# Исключим пропуски, переименуем столбцы, а также проверим данные на наличие дубликатов.

# In[62]:


df.columns


# Проверим данные на наличие пропусков вызовом набора методов для суммирования пропущенных значений.

# In[63]:


df.isnull().sum()


# # Пустые значения свидетельствуют, что для некоторых треков доступна не вся информация. Причины могут быть разные: скажем,  не назван конкретный исполнитель народной песни. Хуже, если проблемы с записью данных. Каждый отдельный случай необходимо разобрать и выявить причину.

# Заменяем пропущенные значения в столбцах с названием трека и исполнителя на строку 'unknown'. После этой операции нужно убедиться, что таблица больше не содержит пропусков.

# In[64]:


df.loc[:, 'track_name'] = df['track_name'].fillna('unknown')
# <замена пропущенных значений в столбце 'track_name' на строку 'unknown' специальным методом замены>


# In[65]:


df.loc[:, 'artist_name'] = df['artist_name'].fillna('unknown')
# <замена пропущенных значений в столбце 'artist_name' на строку 'unknown' специальным методом замены>


# In[66]:


df.isnull().sum()
# <проверка: вычисление суммарного количества пропусков, выявленных в таблице df>


# Удаляем в столбце с жанрами пустые значения; убеждаемся, что их больше не осталось.

# In[67]:


df.dropna(subset = ['genre_name'], inplace = True)
# <удаление пропущенных значений в столбце 'genre_name'>


# In[68]:


df.isnull().sum()
# <проверка>


# Необходимо установить наличие дубликатов.  Если найдутся, удаляем, и проверяем, все ли удалились.

# In[69]:


df.duplicated().sum()
# <получение суммарного количества дубликатов в таблице df>


# In[70]:


df = df.drop_duplicates().reset_index(drop=True)
# <удаление всех дубликатов из таблицы df специальным методом>


# In[71]:


df.duplicated().sum()
# <проверка на отсутствие>


# Дубликаты могли появиться вследствие сбоя в записи данных. Стоит обратить внимание и разобраться с причинами появления такого «информационного мусора».

# Сохраняем список уникальных значений столбца с жанрами в переменной *name_genres*. 
# 
# Объявим функцию *find_genre()* для поиска неявных дубликатов в столбце с жанрами. Например, когда название одного и того же жанра написано разными словами.
# 
# 
# 
# 

# In[72]:


name_genres = df['genre_name'].unique()
# <сохранение в переменной name_genres списка уникальных значений, выявленных специальным методом в столбце 'genre_name'>


# In[73]:


def find_genre (genre1):
    col_genre = 0
    j = -1
    for i in name_genres:
        j += 1
        if name_genres[j] == genre1:
            col_genre = col_genre + 1
    return(col_genre)

# <создание функции find_genre()>
# функция принимает как параметр строку с названием искомого жанра
# в теле объявляется переменная-счётчик, ей присваивается значение 0,
# затем цикл for проходит диапазон, равный длине списка уникальных значений
# если в цикле очередной элемент списка равен параметру функции, 
# то значение счётчика увеличивается на 1
# по окончании работы цикла функция возвращает значение счётчика


# Вызов функции *find_genre()* для поиска различных вариантов названия жанра хип-хоп в таблице.
# 
# Правильное название — *hiphop*. Поищем другие варианты:
# 
# * hip
# * hop
# * hip-hop
# 

# In[74]:


find_genre('hip')

# <вызовом функции find_genre() проверяется наличие варианта 'hip'>


# In[75]:


find_genre('hop')
# <проверяется наличие варианта 'hop'>


# In[76]:


find_genre('hip-hop')
# <проверяется наличие варианта 'hip-hop'>


# Объявим функцию *find_hip_hop()*, которая заменяет  неправильное название этого жанра в столбце *'genre_name'* на *'hiphop'* и проверяет успешность выполнения замены.
# 
# Так исправляем все варианты написания, которые выявила проверка.ult

# In[77]:


def find_hip_hop(df, wrong): 
    df['genre_name'] = df['genre_name'].replace(wrong,'hiphop') 
    final = df[df['genre_name'] == wrong]['genre_name'].count() 
    return final

# <создание функции find_hip_hop()>
# функция принимает как параметры таблицу df и неверное название
# к столбцу 'genre_name' применяется специальный метод, 
# который заменяет второй параметр на строку 'hiphop'
# результат работы равен подсчитанному методом count() числу значений столбца, 
# которые равны второму параметру
# функция возвращает результат


# In[78]:


find_hip_hop (df, 'hip')
# <замена одного неверного варианта на hiphop вызовом функции find_hip_hop()>


# In[79]:


find_hip_hop (df, 'hop')
# <замена второго неправильного варианта на hiphop>


# In[80]:


find_hip_hop (df, 'hip-hop')
# <замена третьего неправильного варианта на hiphop>


# Получаем общую информацию о данных. Убеждаемся, что чистка выполнена успешно.

# In[81]:


df.info()
# <получение общей информации о данных таблицы df>


# **Вывод**

# На этапе предобработки в данных обнаружились не только пропуски и проблемы с названиями столбцов, но и всяческие виды дубликатов. Их удаление позволит провести анализ точнее. Поскольку сведения о жанрах важно сохранить для анализа, не просто удаляем все пропущенные значения, но заполним пропущенные имена исполнителей и названия треков. Имена столбцов теперь корректны и удобны для дальнейшей работы.

# # Действительно ли музыку в разных городах слушают по-разному?

# Была выдвинута гипотеза, что в Москве и Санкт-Петербурге пользователи слушают музыку по-разному. Проверяем это предположение по данным о трёх днях недели — понедельнике, среде и пятнице.
# 
# Для каждого города устанавливаем количество прослушанных  в эти дни композиций с известным жанром, и сравниваем результаты.

# Группируем данные по городу и вызовом метода *count()* подсчитываем композиции, для которых известен жанр.

# In[82]:


df.groupby('city').count()
# <группировка данных таблицы df по столбцу 'city' и подсчёт количества значений столбца 'genre_name'>


# В Москве прослушиваний больше, чем в Питере, но это не значит, что Москва более активна. У Яндекс.Музыки в целом больше пользователей в Москве, поэтому величины сопоставимы.

# Сгруппируем данные по дню недели и подсчитаем прослушанные в понедельник, среду и пятницу композиции, для которых известен жанр.

# In[83]:


df.groupby('weekday')['genre_name'].count()
# <группировка данных по столбцу 'weekday' и подсчёт количества значений столбца 'genre_name'>


# Понедельник и пятница — время для музыки; по средам пользователи немного больше вовлечены в работу.

# Создаём функцию *number_tracks()*, которая принимает как параметры таблицу, день недели и название города, а возвращает количество прослушанных композиций, для которых известен жанр. Проверяем количество прослушанных композиций для каждого города и понедельника, затем среды и пятницы.

# In[84]:


def number_tracks (df, day, city): 
    track_list = df[(df['weekday'] == day) & (df['city'] == city)]
    track_list_count = track_list['genre_name'].count()
    return track_list_count


# <создание функции number_tracks()>
# объявляется функция с тремя параметрами: df, day, city
# в переменной track_list сохраняются те строки таблицы df, для которых 
# значение в столбце 'weekday' равно параметру day
# и одновременно значение в столбце 'city' равно параметру city
# в переменной track_list_count сохраняется число значений столбца 'genre_name',
# рассчитанное методом count() для таблицы track_list
# функция возвращает значение track_list_count


# In[85]:


number_tracks(df, 'Monday', 'Moscow')
    
    
# <список композиций для Москвы в понедельник>


# ## number_tracks(df, 'Monday', 'Saint-Petersburg')
# # <список композиций для Санкт-Петербурга в понедельник>

# In[86]:


number_tracks(df, 'Wednesday', 'Moscow')
# <список композиций для Москвы в среду>


# In[87]:


number_tracks(df, 'Wednesday', 'Saint-Petersburg')
# <список композиций для Санкт-Петербурга в среду>


# In[88]:


number_tracks(df, 'Friday', 'Moscow')
# <список композиций для Москвы в пятницу>


# In[89]:


number_tracks(df, 'Friday', 'Saint-Petersburg')
# <список композиций для Санкт-Петербурга в пятницу>


# Сведём полученную информацию в одну таблицу, где ['city', 'monday', 'wednesday', 'friday'] названия столбцов.
# 

# In[90]:


data1 = {
'city': ['Moscow', 'Saint-Petersburg'],
'monday':     [number_tracks(df, 'Monday', 'Moscow'), number_tracks(df, 'Monday', 'Saint-Petersburg')],
'wednesday':  [number_tracks(df, 'Wednesday', 'Moscow'), number_tracks(df, 'Wednesday', 'Saint-Petersburg')],
'friday': [number_tracks(df, 'Friday', 'Moscow'), number_tracks(df, 'Friday', 'Saint-Petersburg')]  
}
table = pd.DataFrame(data=data1)
table
# <таблица с полученными данными>


# **Вывод**

# Результаты показывают, что относительно среды музыку в Петербурге и Москве слушают «зеркально»: в Москве пики приходятся на понедельник и пятницу, а в среду время прослушивания снижается. Тогда как в Санкт-Петербурге среда — день самого большого интереса к музыке, а в понедельник и пятницу он меньше, причём почти одинаково меньше.

# # Утро понедельника и вечер пятницы — разная музыка или одна и та же?

# Ищем ответ на вопрос, какие жанры преобладают в разных городах в понедельник утром и в пятницу вечером. Есть предположение, что в понедельник утром пользователи слушают больше бодрящей музыки (например, жанра поп), а вечером пятницы — больше танцевальных (например, электронику).

# Получим таблицы данных по Москве *moscow_general* и по Санкт-Петербургу *spb_general*.

# In[91]:


moscow_general = df[df.city == 'Moscow']
# получение таблицы moscow_general из тех строк таблицы df, 
# для которых значение в столбце 'city' равно 'Moscow'


# In[92]:


spb_general = df[df.city == 'Saint-Petersburg']
# <получение таблицы spb_general>


# Создаём функцию *genre_weekday()*, которая возвращает список жанров по запрошенному дню недели и времени суток с такого-то часа по такой-то.

# In[93]:


def genre_weekday (df, day, time1, time2):
    genre_list = df[(df['weekday'] == day) & (df['time'] > time1) & (df['time'] < time2)]
    genre_list_sorted = genre_list.groupby('genre_name').count().sort_values('user_id', ascending=False).head(10)
    return genre_list_sorted

# объявление функции genre_weekday() с параметрами df, day, time1, time2
# в переменной genre_list сохраняются те строки df, для которых одновременно:
# 1) значение в столбце 'weekday' равно параметру day,
# 2) значение в столбце 'time' больше time1 и
# 3) меньше time2.
# в переменной genre_list_sorted сохраняются в порядке убывания  
# первые 10 значений Series, полученной подсчётом числа значений 'genre_name'
# сгруппированной по столбцу 'genre_name' таблицы genre_list
# функция возвращает значение genre_list_sorted


# Cравниваем полученные результаты по таблице для Москвы и Санкт-Петербурга в понедельник утром (с 7 до 11) и в пятницу вечером (с 17 до 23).

# In[94]:


genre_weekday (moscow_general, 'Monday', '07:00', '11:00')
# <вызов функции для утра понедельника в Москве (вместо df таблица moscow_general)>


# In[95]:


genre_weekday (spb_general, 'Monday', '07:00', '11:00')
# <вызов функции для утра понедельника в Петербурге (вместо df таблица spb_general)>


# In[96]:


genre_weekday (moscow_general, 'Friday', '17:00', '23:00')
# <вызов функции для вечера пятницы в Москве>


# In[97]:


genre_weekday (spb_general, 'Friday', '17:00', '23:00')
# <вызов функции для вечера пятницы в Питере>


# Популярные жанры в понедельник утром в Питере и Москве оказались похожи: везде, как и предполагалось, популярен поп. Несмотря на это, концовка топ-10 для двух городов различается: в Питере в топ-10 входит джаз и русский рэп, а в Москве жанр *world*.
# 
# В конце недели ситуация не меняется. Поп-музыка всё так же на первом месте. Опять разница заметна только в концовке топ-10, где в Питере пятничным вечером тоже присутствует жанр *world*.

# **Вывод**

# Жанр поп безусловный лидер, а топ-5 в целом не различается в обеих столицах. При этом видно, что концовка списка более «живая»: для каждого города выделяются более характерные жанры, которые действительно меняют свои позиции в зависимости от дня недели и времени.

# # Москва и Питер — две разные столицы, два разных направления в музыке. Правда?

# Гипотеза: Питер богат своей рэп-культурой, поэтому это направление там слушают чаще, а Москва — город контрастов, но основная масса пользователей слушает попсу.
# 
# 

# Сгруппируем таблицу *moscow_general* по жанру, сосчитаем численность композиций каждого жанра методом *count()*, отсортируем в порядке убывания и сохраним результат в таблице *moscow_genres*.
# 
# Просмотрим первые 10 строк этой новой таблицы.

# In[98]:


moscow_genres = moscow_general.groupby('genre_name')['genre_name'].count().sort_values(ascending=False)
#.moscow_general.groupby('genre_name')['genre_name'].count()
# одной строкой: группировка таблицы moscow_general по столбцу 'genre_name', 
# подсчёт числа значений 'genre_name' в этой группировке методом count(), 
# сортировка Series в порядке убывания и сохранение в moscow_genres


# In[99]:


moscow_genres.head(10)
# <просмотр первых 10 строк moscow_genres>


# Сгруппируем таблицу *spb_general* по жанру, сосчитаем численность композиций каждого жанра методом *count()*, отсортируем в порядке убывания и сохраним результат в таблице *spb_genres*.
# 
# Просматриваем первые 10 строк этой таблицы. Теперь можно сравнивать два города.

# In[100]:


spb_genres = spb_general.groupby('genre_name')['genre_name'].count().sort_values(ascending=False)
# <группировка таблицы spb_general, расчёт, сохранение в spb_genres>


# In[101]:


spb_genres.head(10)
# <просмотр первых 10 строк spb_genres>


# **Вывод**

# В Москве, кроме абсолютно популярного жанра поп, есть направление русской популярной музыки. Значит, что интерес к этому жанру шире. А рэп, вопреки предположению, занимает в обоих городах близкие позиции.

# # Этап 4. Результаты исследования
# 

# Рабочие гипотезы:
# 
# * музыку в двух городах — Москве и Санкт-Петербурге — слушают в разном режиме;
# 
# * списки десяти самых популярных жанров утром в понедельник и вечером в пятницу имеют характерные отличия;
# 
# * население двух городов предпочитает разные музыкальные жанры.
# 
# **Общие результаты**
# 
# Москва и Петербург сходятся во вкусах: везде преобладает популярная музыка. При этом зависимости предпочтений от дня недели в каждом отдельном городе нет — люди постоянно слушают то, что им нравится. Но между городами в разрезе дней неделей наблюдается зеркальность относительно среды: Москва больше слушает в понедельник и пятницу, а Петербург наоборот - больше в среду, но меньше в понедельник и пятницу.
# 
# В результате первая гипотеза <подтверждена>, вторая гипотеза <не подтверждена> и третья <не подтверждена>.
