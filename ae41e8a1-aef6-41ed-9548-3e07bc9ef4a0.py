#!/usr/bin/env python
# coding: utf-8

# ### <font color='orange'>Комментарий от наставника 1 итерация 2
# Спасибо за исправления! Прочитала комментарии, спасибо, что выделяешь их цветом :) <br>
# Как обычно пометила тегом <span style="color:green;font-size:200%">&#10003;</span> те исправления, где всё отлично. Свои новые комментарии выделила оранжевым цветом, чтобы можно было их отличить от старых комментариев.

# ### <font color = 'red'> Комментарий для наставника
#     
#     Ирина доброе утро!
#     Спаибо за правки. Отправляю заново работу, постарался учесть всё что ты указала. В ряде мест будут комментарии. Комментарии я тоже напишу красным, потому что уже было два цвета, а будет ещё один.
#     
#     В следующих проектах также буду стараться учитывать насколько это возможно.

# ### <font color='green'>Комментарий от наставника 1
# Иван, привет! Спасибо, что учёл мои замечания из прошлого проекта :) <br>
# Как и прежде ищи мои комментарии в подобных ячейках. Пункты, где всё отлично, я отмечаю галкой <span style="color:green;font-size:200%">&#10003;</span> или <font color='green'><b>зелёным комментарием</b></font>. Там, где нужно что-то исправить для привлечения внимания я пишу другими цветами (зависят от итерации). Начну с <font color='red'><b>красного</b></font> :)

# # Общая информация
# 
# Целью исследования является установить зависимость рыночной стоимости объектов недвижимости, от различных факторов.
# 
# Для исследования представлена таблица, в которой приведены данные из объявлений о продаже объектов недвижимости, дополненные объективными данными об объектах из карт.

# In[1]:


import csv
import pandas as pd
data = pd.read_csv('/datasets/real_estate_data.csv', sep= '\t')
print(data.info())


# ceiling_height, floors_total, living_area, is_apartment, kitchen_area, balcony, locality_name, airports_nearest, cityCenters_nearest, parks_around3000, parks_nearest, ponds_around3000, ponds_nearest, days_exposition

# # Общая информация о таблице
# 
# Для анализа представлены данные о 23699 объектах, сгруппированные по 24 видам данных.
# Большинство столбцов имеет пропуски, причём пропущенно достаточно много значений.
# 
# Нет пропущенных значений в столбцах с данными по цене объектов, общей площади, дне выставления на продажу, количестве комнат, этаже и районе.

# ### Расчёт цены квадратного метра
# 
# Для работы с данными, в таблице не хватает важной информации, а именно - цены квадратного метра общей площади. Подсчитаем эту цену. Данные для расчёта есть. Нулевых объектов по столбцам: общая площадь, и цена объекта - нет.

# In[2]:


data['price_bym'] = data['last_price'] / data['total_area'] / 1000
data['price_bym'].astype('int')
data['price_bym'].describe()


# ### Заполнение пропусков столбца building_series_id 1.
# 
# В столбце building_series_id, представлена информация о типе объекта недвижимости (серии дома). Всего имеются данные о 6517 объектов из 23699. То есть информация имеется всего о 27% объектах.

# In[3]:


print(data['building_series_id'].unique())


# ### Заполнение пропусков столбца building_series_id 2.
# 
# Серий много. Вручную распределить невозможно. Необходимо подсчитать площадь объектов по сериям, и цену квадратного метра объектов по сериям.
# 
# Для работы с типами зданий необходимо выгрузить их в отдельную таблицу data_building_series. Выгружать будем значения, непосредственно относящиеся к типам зданий. Сами серии, общую площадь, цену, количество комнат, цену за квадратный метр.
# 
# Жилую площадь, площадь кухни, количество этажей, не выгружаю, поскольку считаю что разделение можно произвести по общей площади.
# 

# In[4]:


head_building_series = ['building_series_id', 'total_area', 'rooms']
data_building_series= pd.DataFrame(data = data, columns = (head_building_series))
print(data_building_series.head(5))


# ### Заполнение пропусков столбца building_series_id 3.
# 
# Создаём отдельную таблицу: data_building_series, где по каждому объекту отражена: цена, общая площадь, количество комнат, цена за метр. Столбцы записываем в отдельную переменную для удобства последующего редактирования

# In[5]:


data_building_series = data_building_series.dropna()
print(data_building_series.head())


# ### Заполнение пропусков столбца building_series_id 4.
# 
# Удаляем пропущенные строки. Теперь можно работать с типами объектов

# In[6]:


data_building_series['building_series_id'] = data_building_series['building_series_id'].str.lower()
data_building_series.sort_values(by='building_series_id', inplace=True)
print(data_building_series['building_series_id'].unique())


# ### Заполнение пропусков столбца building_series_id 5
# 
# Опускаем регистр, сортируем по полю building_series_id, выводим уникальные значения серий.
# Визуальный анализ серий зданий, показывает, что можно сократить количество серий, поскольку ряд серий является дубликатами.
# 
# Проводить лемматизацию серий нельзя, числовых значений слишком много.

# In[7]:


def bldng_srs_id_dplct (building_series_id):
        if building_series_id == "121 (гатчинская)" or building_series_id == "121 гатчинская" or building_series_id == "121(гатчинская)":
            return "121гатчинская"
        elif building_series_id == 'индивид.' or building_series_id == 'индивидуальный проект': 
            return 'индивидуальный'
        elif building_series_id == 'кирп.монолит':
            return 'кирпичный монолит'
        elif building_series_id == 'старый фонд + капремонт':
            return 'старый фонд с кр'
        else:
            return building_series_id
                           
data_building_series['building_series_id'] = data_building_series['building_series_id'].str.replace("серия", '')
data_building_series_tmp = pd.to_numeric(data_building_series['building_series_id'], errors='coerce') 
data_building_series_tmp = data_building_series_tmp.fillna(-1)
data_building_series_tmp = data_building_series_tmp.astype(int)
data_building_series_tmp.loc[data_building_series_tmp == -1] = data_building_series['building_series_id']
data_building_series['building_series_id'] = data_building_series_tmp
data_building_series['building_series_id'] = data_building_series.apply(lambda x: bldng_srs_id_dplct(x['building_series_id']), axis = 1)
data_building_series['building_series_id'].unique()


# ### <font color='red'>Комментарий от наставника 2 <span style="color:green;font-size:200%">&#10003;</span>
# Отлично, что ты заметил наличие дублей тут и понял, как их можно исправить.<br>
# Но твой способ замены всё-таки не самый изящный. Стоит избавиться от копипасты. Давай напишем функцию, которая принимает на вход building_id и возвращает его унифицированный вариант, а затем выполним apply. <br>
# При этом в функции предлагаю через try + except пытаться привести любой id к int (без их явного перечисления), а в случае ошибки, просто идти дальше. Тогда мы избавимся от необходимости копипастить значения хотя бы в половине случаев.

# ### Заполнение пропусков столбца building_series_id 6
# 
# Количество серий стало значительно меньше. Делаю сводную таблицу по сериям, и количеству комнат, чтобы оценить, можно ли сократить ещё серии.

# In[8]:


data_pivot_building_series_pt = data_building_series.pivot_table(index=['building_series_id', 'rooms'], values='total_area', aggfunc = ['median', 'count'])

print(data_pivot_building_series_pt.loc[['1 лг - 600.11']])
#print(data_pivot_building_series_pt.loc[['600.11']])
print(data_pivot_building_series_pt.loc[['1-лг-600-i']])


# ### Заполнение пропусков столбца building_series_id 7
# 
# 
# типы квартир - 1 лг - 600.11 и 1-лг-600-i, объединить нельзя.

# In[9]:


print(data_pivot_building_series_pt.loc[['1-528 кп - 2']])
print(data_pivot_building_series_pt.loc[['1-528-кп-97']])


# ### Заполнение пропусков столбца building_series_id 8
# 
# Типы квартир 1-528 кп - 2 и 1-528-кп-97, объединить нельзя, поскольку в выборке есть всего две квартиры каждой серии. Их придётся перевести в тип "Другие".

# In[10]:


print(data_pivot_building_series_pt.loc[[121]])
print(data_pivot_building_series_pt.loc[['121гатчинская']])


# ### Заполнение пропусков столбца building_series_id 9
# 
# Типы квартир 121 и 121гатчинская, объединить нельзя. Хотя однокомнатные квартиры совпадают по площади, но между двухкомнатными и трёхкомнатными квартирами существует значительная разница.

# In[11]:


print(data_pivot_building_series_pt.loc[['1лг-6066м']])
print(data_pivot_building_series_pt.loc[[606]])
data_building_series.replace('1лг-6066м.', 606, inplace = True)


# ### Заполнение пропусков столбца building_series_id 10
# 
# Типы квартир 1лг-6066м и 606, объединить можно, хотя в выборке есть только одна квартира - 1лг-6066м. Заменяем.

# In[12]:


print(data_pivot_building_series_pt.loc[[504]])
print(data_pivot_building_series_pt.loc[['504д']])    


# ### Заполнение пропусков столбца building_series_id 11
# 
# Типы квартир 504 и 504д, объединять нельзя, разница существенная.
# 
# Итак, после замены всех возможных дубликатов, смотрим какие типы квартир, встречаются в выборке часто. На показания этих типов и будем ориентироваться при замене пропущенных значений. Впоследствии те типы квартир, которые встречаются нечасто (менее 5 раз), будут заменены на тип "Другие".
# 

# In[13]:


data_pivot_building_series1 = (data_building_series
                              .query('rooms == 1')
                              .pivot_table(index='building_series_id', values='total_area', aggfunc = ['median', 'count'])                        
)
data_building_series1 = (data_building_series
                        .query('rooms == 1')
)
data_pivot_building_series1.columns = ['total_area', 'count']
dt_pvt_bldng1 = data_pivot_building_series1.query('count >= 5')
dt_pvt_bldng1_change = data_pivot_building_series1.query('count < 5')


# In[14]:


data_building_series1.head(10)


# ### Заполнение пропусков столбца building_series_id 12
# 
# Формируем выборку по сериям для однокомнатных квартир, которую будем использовать для замены.
# 
# data_pivot_building_series1 - таблица, со всеми сериями однокомнатных квартир, сгруппированная по медианной площади и количеству квартир. data_building_series1 - таблица, со всеми однокомнатными квартирами. dt_pvt_bldng1 - таблица, со всеми сериями однокомнатных квартир, сгруппированная по медианной площади и количеству квартир, с количеством квартир в выборке более 5

# In[15]:


rooms1_stat = []
rooms1_stat = dt_pvt_bldng1.index
print(rooms1_stat)


# ### Заполнение пропусков столбца building_series_id 13
# 
# Выводим список rooms1_stat, серий однокомнатных квартир по которым достаточно статистики.

# In[16]:


data_building_series1_select = data_building_series1.query('building_series_id in @rooms1_stat')
print(data_building_series1_select['building_series_id'].unique())


# In[17]:


data_building_series1_select_pvt = data_building_series1_select.pivot_table(index = 'building_series_id', values = 'total_area', aggfunc = ['median', 'describe'])
data_building_series1_select_pvt.set_axis(['median', '25%', '50%', '75%', 'count', 'max', 'mean', 'min', 'std'], axis = 'columns', inplace = True)
data_building_series1_select_pvt


# ### Заполнение пропусков столбца building_series_id 14
# 
# После анализа установлено, что все объекты по площади достаточно близки друг к другу, и их площади перекрываются.
# С другой стороны, объектов серии - 1564812, очень много, 1103 объекта из 1893, или 58%. Но по этому типу зданий, очень высокое минимальное значение, максимальное значение, и среднее отклонение.
# Определим предельные размеры выборки, а именно верхнюю и нижнюю границу.

# In[18]:


data_building_series1_select_pvt['low_b'] =  data_building_series1_select_pvt['25%'] - 1.5 * (data_building_series1_select_pvt['75%'] - data_building_series1_select_pvt['25%'])
data_building_series1_select_pvt['high_b'] =  data_building_series1_select_pvt['75%'] + 1.5 * (data_building_series1_select_pvt['75%'] - data_building_series1_select_pvt['25%'])
data_building_series1_select_pvt


# ### Выводы по заполнению пропусков столбца building_series_id (однокомнатные квартиры)
# 
# После анализа таблицы установлено, что:
# 
# подавляющее количество 1-комнатных квартир, серию которых можно определить, составляют квартиры проекта 1564812. (58% от всех квартир с указанным типом проекта).
# 
# Медианная площадь квартир составляет 38 квадратных метров, основной объём выборки находится в границах от 34 до	42.100 квадратных метров. Среднее отклонение составляет - 8.03. Границы нормы (где начинаются выбросы) от 21.85, до	54.25 квадратных метров.
# Других крупных серий нет. Вторая по количеству квартир серия - 1564792, представлена 156 квартирами, и имеет медианную площадь квартир - 38.95 квадратных метров. То есть, эти серии пересекаются.
# 
# Другие крупные серии объектов, группируются около медианной отметки 32 квадратных метра. Соответственно, выделить квартиры площадью около 32 квадратных метров в какую-то одну группу не представляется возможным. 
# 
# При этом, записывать все квартиры  в серию - 1564812, также считаю неверным, поскольку квартиры площадью менее 30 квадратов, и более 46 квадратов, скорее всего входят в другие серии.
# 
# Таким образом, считаю оптимальным, 1-комнатные квартиры с пропуском в типе данных building_series_id, площадью от 30 до 46 квадратов, признать квартирами серии - 1564812, а 1-комнатные квартиры иной площади, включить в группу "Другие".

# In[19]:


data_pivot_building_series2 = (data_building_series
                              .query('rooms == 2')
                              .pivot_table(index='building_series_id', values='total_area', aggfunc = ['median', 'count'])                        
)
data_building_series2 = (data_building_series
                        .query('rooms == 2')
)
data_pivot_building_series2.columns = ['total_area', 'count']
data_pivot_building_series2
dt_pvt_bldng2 = data_pivot_building_series2.query('count >= 5')
dt_pvt_bldng2


# ### Заполнение пропусков столбца building_series_id 15
# 
# Также выводим серии двухкомнатных квартир, с медианной площадью каждой серии. В выборку включаем только квартиры, где есть информация, о более чем пяти объектах.
# 
# 
# data_pivot_building_series2 - таблица, со всеми сериями двухкомнатных квартир, сгруппированная по медианной площади и количеству квартир.
# data_building_series2 - таблица, со всеми двухкомнатными квартирами.
# dt_pvt_bldng2 - таблица, со всеми сериями двухкомнатных квартир, сгруппированная по медианной площади и количеству квартир, с количеством квартир в выборке более 5.

# In[20]:


def create_building_id_table (data_building_series_r_select, rooms):
    data_building_series_r_select = data_building_series_r_select.query('building_series_id in @rooms')        
    data_building_series_r_select_pvt = data_building_series_r_select.pivot_table(index = 'building_series_id', values = 'total_area', aggfunc = ['median', 'describe'])
    data_building_series_r_select_pvt.set_axis(['median', '25%', '50%', '75%', 'count', 'max', 'mean', 'min', 'std'], axis = 'columns', inplace = True)
    data_building_series_r_select_pvt['low_b'] =  data_building_series_r_select_pvt['25%'] - 1.5 * (data_building_series_r_select_pvt['75%'] - data_building_series_r_select_pvt['25%'])
    data_building_series_r_select_pvt['high_b'] =  data_building_series_r_select_pvt['75%'] + 1.5 * (data_building_series_r_select_pvt['75%'] - data_building_series_r_select_pvt['25%'])
    return data_building_series_r_select_pvt
    
rooms2_stat = []
rooms2_stat = dt_pvt_bldng2.index
data_building_series2_select_pvt = create_building_id_table(data_building_series2, rooms2_stat)
data_building_series2_select_pvt


# ### <font color='red'>Комментарий от наставника 3
# Очень здорово, что ты при анализе данных и поиске выбросов ты строишь такую наглядную таблицу и смотришь на границы нормы! Давай только обратим внимание на то, что ты несколько раз при построении таких таблиц "копи-пастишь" код. Я предлагаю создать функцию, которая будет строить такую таблицу и переиспользовать её.

# ### <font color = 'red'> Комментарий для наставника
#     
#     Понимаю, что функция должна быть больше, но больше не получилось. Плодить функции также считаю неправильным, поэтому оставил так.

# ### <font color='orange'>Комментарий от наставника 2 итерация 2
# Плодить функции, конечно, не нужно :) Я имела в виду, что можно написать одну функцию и переиспользовать её несколько раз для различных параметров rooms выше.
#    
# Но это не критично, конечно. Я на консультации покажу "автоматизацию" похожего примера.

# ### Заполнение пропусков столбца building_series_id 16
# 
# 
# rooms2_stat - список серий двухкомнатных квартир, попавших в выборку
# 
# data_building_series2_select - список двухкомнатных квартир, из серий - попавших в выборку
# 
# data_building_series2_select_pvt - статистические данные о площадях двухкомнатных квартир, попавших в выборку. 

# ### Выводы по заполнению пропусков столбца building_series_id (двухкомнатные квартиры)
# 
# После анализа таблицы установлено, что:
# 
# подавляющее количество 2-комнатных квартир, серию которых можно определить, составляют квартиры проекта 1564812. (55% от всех квартир с указанным типом проекта).
# 
# Медианная площадь квартир составляет 58 квадратных метров, основной объём выборки находится в границах от 50.100 до	67 квадратных метров. Среднее отклонение составляет - 15.3. Границы нормы (где начинаются выбросы) от 24.75 до 92.35 квадратных метров.
# Других крупных серий нет. Вторая по количеству квартир серия - 1564792, представлена 174 квартирами, и имеет медианную площадь квартир - 52.3 квадратных метров. То есть, эти серии пересекаются.
# 
# Другие крупные серии объектов, группируются около медианной отметки 44 квадратных метра. Соответственно, выделить квартиры площадью около 44 квадратных метров в какую-то одну группу не представляется возможным. 
# 
# При этом, записывать все квартиры  в серию - 1564812, также считаю неверным, поскольку квартиры площадью менее 43 квадратов, и более 73 квадратов, с большой вероятностью входят в другие серии.
# 
# Таким образом, считаю оптимальным, 2-комнатные квартиры с пропуском в типе данных building_series_id, площадью от 43 до 73 квадратов, признать квартирами серии - 1564812, а 2-комнатные квартиры иной площади, включить в группу "Другие".

# In[21]:


data_pivot_building_series3 = (data_building_series
                              .query('rooms == 3')
                              .pivot_table(index='building_series_id', values='total_area', aggfunc = ['median', 'count'])                        
)
data_building_series3 = (data_building_series
                        .query('rooms == 3')
)
data_pivot_building_series3.columns = ['total_area', 'count']
data_pivot_building_series3
dt_pvt_bldng3 = data_pivot_building_series3.query('count >= 5')
dt_pvt_bldng3


# ### Заполнение пропусков столбца building_series_id 17
# data_pivot_building_series3 - таблица со всеми сериями трёхкомнатных квартир, сгруппированная по медианной площади, и с указанием количества.
# data_building_series3 - список всех трёхкомнатных квартир, с указанием общей площади.
# dt_pvt_bldng3 - таблица с медианной площадью трёхкомнатных квартир, с где есть более чем пять квартир.

# In[22]:


rooms3_stat = []
rooms3_stat = dt_pvt_bldng3.index
data_building_series3_select_pvt = create_building_id_table(data_building_series3, rooms3_stat)
data_building_series3_select_pvt


# ### Заполнение пропусков столбца building_series_id 18
# 
# rooms3_stat - перечень типов зданий, трёхкомнатных квартир по которым есть статистика.
# 
# data_building_series3_select - перечень всех трёхкомнатных квартир, по типам зданий которых есть статистика
# 
# data_building_series3_select_pvt - сводные данные по всех трёхкомнатных квартирах, по типам зданий которых есть статистика.

# ### Выводы по заполнению пропусков столбца building_series_id (трёхкомнатные квартиры)
# 
# После анализа таблицы установлено, что:
# 
# подавляющее количество 3-комнатных квартир, серию которых можно определить, составляют квартиры проекта 1564812. (57% от всех квартир с указанным типом проекта).
# 
# Медианная площадь квартир составляет 80.80 квадратных метров, основной объём выборки находится в границах от 69.5 до 96 квадратных метров. Среднее отклонение составляет - 22.8. Границы нормы (где начинаются выбросы) от 29.75 до	135.75 квадратных метров.
# Других крупных серий нет. И если вторая по количеству квартир серия - 1564792, представлена 160 квартирами, и имеет медианную площадь квартир - 71.45 квадратных метров. То есть, пересекаются с основной серией.
# То серия - 1564801, имеет медианую площадь - 58.30, среднее отклонение - 4.8, а допустимую границу диапазона - от 50.75 до 68.75 соответственно. То есть серия - 1564801, не пересекается с серией - 1564812, по медиане.
# 
# Две другие крупные серии объектов, группируются около медианной отметки 60 квадратных метра. Соответственно, выделить квартиры площадью около 60 квадратных метров в какую-то одну группу не представляется возможным. 
# 
# При этом, записывать все квартиры  в серию - 1564812, также считаю неверным, поскольку квартиры площадью менее 58 квадратов, и более 103 квадратов, скорее всего входят в другие серии.
# При этом, серия 1564801, имеет минимальное среднее отклонение - 4,8 и пересекается допустимыми границами диапазонов с серией - 1564812. Поскольку серия 1564801, имеет минимальное среднее отклонение, но гораздо меньшее количество квартир, то пересечение областей считаю правильным "разделить", между сериями.
# 
# Таким образом, квартиры площадью свыше 60 квадратных метров, целесообразно отнести к серии - 1564812. А квартиры площадью - менее 60 квадратных метров, к серии - 1564801.
# 
# 
# Таким образом, считаю оптимальным, трёхкомнатные квартиры с пропуском в типе данных building_series_id, площадью от 60 до 103 квадратов, признать квартирами серии - 1564812, трёхкомнатные квартиры площадью от 53,5 до 60 квадратных метров признать квартирами серии - 1564801, а трёхкомнатные квартиры иной площади, включить в группу "Другие".

# ### Заполнение пропусков столбца building_series_id 19
# 
# Повторим анализ для четырёх комнатных квартир, а потом для квартир, с количеством комнат более 4.

# In[23]:


data_pivot_building_series4 = (data_building_series
                              .query('rooms == 4')
                              .pivot_table(index='building_series_id', values='total_area', aggfunc = ['median', 'count'])                        
)
data_building_series4 = (data_building_series
                        .query('rooms == 4')
)
data_pivot_building_series4.columns = ['total_area', 'count']
data_pivot_building_series4
dt_pvt_bldng4 = data_pivot_building_series4.query('count >= 5')
dt_pvt_bldng4


# In[24]:


data_pivot_building_series4h = (data_building_series
                              .query('rooms > 4')
                              .pivot_table(index='building_series_id', values='total_area', aggfunc = ['median', 'count'])                        
)
data_building_series4h = (data_building_series
                        .query('rooms > 4')
)
data_pivot_building_series4h.columns = ['total_area', 'count']
data_pivot_building_series4h
dt_pvt_bldng4h = data_pivot_building_series4h.query('count >= 5')
dt_pvt_bldng4h


# ### Заполнение пропусков столбца building_series_id 20
# 
# Из анализа группировки данных о площадях, видно, что структура распределения 4-х комнатных, а также пятикомнатных и более квартир, соответствует структуре для одно-, двух-, и трёхкомнатных квартир.
# 
# А именно, значительную долю занимают квартиры проекта - 1564812.
# 
# Для пятикомнатных и более квартир, в статистику попала вообще только одна серия - 1564792, и всего пять квартир из всей серии.
# 
# В связи с этим, выводы по этим квартирам будут аналогичны, выводам сделаным ранее по одно-, двух-, и трёхкомнатным квартирам.
# Разница будет только в значениях.

# In[25]:


data_pivot_building_series4h


# ### Заполнение пропусков столбца building_series_id 21
# 
# data_pivot_building_series4 - данные о медианных значениях площадей четырёхкомнатных квартир, по типам.
# 
# data_building_series4 - список всех четырёхкомнатных квартир, с указанием типов квартир и площадей.
# 
# dt_pvt_bldng4 - сводная таблица по всем типам четырёхкомнатных квартир, вошедших в выборку
# 
# data_pivot_building_series4h - данные о медианных значениях площадей квартир, с количеством комнат более четырёх по типам.
# 
# data_building_series4h = список всех квартир, с количеством комнат более четырёх по типам.
# 
# dt_pvt_bldng4h - сводная таблица по всем типам квартир, с количеством комнат более четырёх, вошедших в выборку

# ### Заполнение пропусков столбца building_series_id 22
# 
# Готовим данные для 4+ комнатных квартир.

# In[26]:


data_pivot_building_series4 = (data_building_series
                              .query('rooms >= 4')
                              .pivot_table(index='building_series_id', values='total_area', aggfunc = ['median', 'count'])                        
)
data_building_series4 = (data_building_series
                        .query('rooms >= 4')
)
data_pivot_building_series4.columns = ['total_area', 'count']
data_pivot_building_series4
dt_pvt_bldng4 = data_pivot_building_series4.query('count >= 5')
dt_pvt_bldng4


# ### Заполнение пропусков столбца building_series_id 23
# 
# data_pivot_building_series4 - данные о медианных значениях площадей четырёх(и выше)комнатных квартир, по типам.
# 
# data_building_series4 - список всех четырёх(и выше)комнатных квартир, с указанием типов квартир и площадей.
# 
# dt_pvt_bldng4 - сводная таблица по всем типам четырёх(и выше)комнатных квартир, вошедших в выборку

# In[27]:


rooms4_stat = []
rooms4_stat = dt_pvt_bldng4.index
data_building_series4_select_pvt = create_building_id_table(data_building_series4, rooms4_stat)
data_building_series4_select_pvt


# ### Заполнение пропусков столбца building_series_id 24
# 
# rooms4_stat - перечень типов зданий, четырёх(и выше)комнатных квартир по которым есть статистика
# 
# data_building_series4_select - перечень всех четырёх(и выше)комнатных квартир, по типам зданий которых есть статистика
# 
# data_building_series4_select_pvt - сводные данные по всех четырёх(и выше)комнатных квартирах, по типам зданий которых есть статистика

# ### <font color='orange'>Комментарий от наставника 6 итерация 2
# Маленькое замечание по оформлению. Совсем не обязательно в каждом комментарии писать заголовок с индексом. Лучше, если заголовки отделяют более крупные шаги. Так же хорошо выделять заголовком выводы, как у тебя сделано ниже. Но дублировать название шага с указанием идентификатора лучше не стоит :)

# ### Выводы по заполнению пропусков столбца building_series_id (четырёх(иболее)комнатные квартиры)
# 
# После анализа таблицы установлено, что подавляющее количество 4(иболее)комнатных квартир, серию которых можно определить, составляют квартиры проекта 1564812. (70% от всех квартир с указанным типом проекта). Медианная площадь квартир составляет 109 квадратных метров, основной объём выборки находится в границах от 93.5 до 130 квадратных метров. Среднее отклонение составляет - 31 квадратный метр. Границы нормы (где начинаются выбросы) от 38.75 до 184.75 квадратных метров.
# 
# 
# Другая крупная серия - 1564801, представлена 55 квартирами, и имеет медианную площадь квартир - 74.3 квадратных метров, со средним отклонением 5,8 квадратных метров. То есть, эти серии не пересекаются по медианам, но пересекаются по значениям. Поскольку серия 1564812 имеет большее количество квартир, но гораздо большее среднее отклонение, то преимущество оставляю за серией 1564801.
# 
# 
# Две другие крупные серии объектов, группируются около медианной отметки 49 квадратных метров. При этом, серия 1568734, имеет 20 квартир, и среднее значение отклонения - 2,5. А серия - 1569041 имеет 12 квартир, и среднее значение отклонения - 4,7. В связи с эти, считаю правильным заменять пропуски на серию - 1568734.
# 
# 
# Таким образом, считаю оптимальным, квартиры, с количеством команат более и равно четырём, с пропуском в типе данных building_series_id, площадью от 46,5 до 51,5 квадратов, признать квартирами серии - 1568734; квартиры, с количеством команат четыре и более, площадью от 68,5 до 79,5 квадратов, признать квартирами серии 1564801; квартиры, с количеством команат четыре и более, площадью от 79,5 до 140 квадратов, признать квартирами серии 1564812; а квартиры, с количеством команат четыре и более иной площади, включить в группу "Другие".

# # Общий вывод по заполнению пропусков с столбце building_series_id
# 
# Основной тип квартир, представленный на рынке недвижимости Санкт-Петербурга, это квартиры проекта - 1564812. Выделить другие проекты сложно. Поэтому, был установлен общий принцип, что квартиры площадью медина плюс/минус, стандартное отклонение, записываем в проект - 1564812. (или другие, если получается) А те квартиры, которые не соответствуют стандартам - в категорию "Другие".
# 
# Таким образом, те квартиры, площадь которых не слишком отличается от основного проекта, 1564812, будут названы квартирами этого проекта, и это не слишком ухудшит результат. А уникальные, особые квартиры и будут учитываться как особые.

# In[28]:


dt_pvt_bldng1_index_set = set(dt_pvt_bldng1.index)
dt_pvt_bldng2_index_set = set(dt_pvt_bldng2.index)
dt_pvt_bldng3_index_set = set(dt_pvt_bldng3.index)
dt_pvt_bldng4_index_set = set(dt_pvt_bldng4.index)
dt_pvt_bldng_index_set = dt_pvt_bldng1_index_set.union(dt_pvt_bldng2_index_set, dt_pvt_bldng3_index_set, dt_pvt_bldng4_index_set)
print(dt_pvt_bldng_index_set)


# ### Заполнение пропусков столбца building_series_id 25
# 
# Определяем множество типов зданий, по которым есть статистика. С этими типами и будем работать.

# In[29]:


data_building_series['building_series_id'] = data_building_series['building_series_id'].where(data_building_series['building_series_id'].isin(dt_pvt_bldng_index_set), 'другие')
#data_building_series.groupby('building_series_id').count()
data_building_series.drop(['total_area', 'rooms'], axis='columns', inplace=True)


# In[30]:


data = data.merge(data_building_series, left_index=True, right_index=True, how='left')
data['building_series_id_y'] = data['building_series_id_y'].fillna('замена')
data.drop(['building_series_id_x'], axis='columns', inplace=True)
data.groupby('building_series_id_y').count()


# ### Заполнение пропусков столбца building_series_id 26
# 
# Заменяем типы зданий. Проверяем. Убираем столбец со старыми типами данных.

# In[31]:


data['rooms'].unique()


# ### Заполнение пропусков столбца building_series_id 27
# 
# Смотрим, какое количество комнат указано, по объектам. Количество комнат понадобится нам далее для функции замены типов зданий.

# In[32]:


def change_building_series_id (building_series_id_y, total_area, rooms):
    if building_series_id_y == 'замена':
        if rooms == 1:
            if 46 >= total_area >= 30:
                return '1564812'
            else:
                return 'другие'
        elif rooms == 2:
            if 73 >= total_area >= 43:
                return '1564812'
            else:
                return 'другие'
        elif rooms == 3:
            if 60 >= total_area >= 103:
                return '1564812'
            elif 53.5 >= total_area > 60:
                return '1564801'
            else:
                return 'другие'
        elif rooms >= 4:
            if 79.5 >= total_area >= 140:
                return '1564812'
            elif 68.5 >= total_area > 79.5:
                return '1564801'
            elif 46.5 >= total_area >= 51.5:
                return '1568734'        
            else:
                return 'другие'
        elif rooms == 0:
            return 'другие'
    else:
        return building_series_id_y
        

            
data['building_series_id_y'] = data.apply(lambda x: change_building_series_id(x['building_series_id_y'], x['total_area'], x['rooms']), axis = 1)
data.groupby('building_series_id_y').count()


# ### <font color='green'>Комментарий от наставника 4
# Ты проделал тут огромную детальную работу, это круто! Но всё же в последующих работах не забывай про баланс "трудозатратность / результат". Ведь у нас нет самоцели заполнить все пропуски, правда? :)

# # Заполнение пропусков по типам зданий:
# 
# Выводим итоговую таблицу. Проверяем типы зданий. Значительное количество объектов (7216) оказалось в категории "другие". Множество других объектов заменено на самую массовую серию - 1564812.
# 
# Теперь можно будет использовать типы зданий, для дальнейшей работы.

# In[33]:


data['ceiling_height'] = round(data['ceiling_height'], 1)


# In[34]:


print(data['ceiling_height'].unique())


# ### Заполнение пропусков столбца ceiling_height1.
# 
# Для большей наглядности округляем значение высоты потолков до одного знака после запятой. Более точные данные не нужны и только создают неудобства для работы.
# 
# Из визуального анализа видно, что помимо пропусков, присутствуют завышенные значения, значение "1", значение "100".
# Значение "1", значение "100" и пропуски необходимо убрать, заменить их ни на что невозможно.
# Завышенные значения, где смещена запятая - заменяем с заменой запятой.
# 
# Для анализа формируем таблицу data_ceiling_height, где сводим высоту потолков, и цену квадратного метра квартиры, для местности "Санкт-Петербург".

# ### Заполнение пропусков столбца ceiling_height2.
# 
# Таблицу сформировали, теперь убираем все строки, из столбца locality_name, кроме Санкт-Петербург, а также убираем строки с пропусками.

# In[35]:


head_ceiling_height = ['ceiling_height', 'locality_name', 'price_bym']
data_ceiling_height= pd.DataFrame(data = data, columns = (head_ceiling_height))
print(data_ceiling_height.head(5))


# In[36]:


data_ceiling_height.dropna(inplace=True)
data_ceiling_height = data_ceiling_height.loc[data_ceiling_height.loc[:, 'locality_name'] == 'Санкт-Петербург']
data_ceiling_height.sort_values(by='ceiling_height', inplace=True)
data_ceiling_height.head(10)


# ### Заполнение пропусков столбца ceiling_height3.
# 
# Теперь заменяем ошибочные значения ceiling_height, где есть смещение точки, и удаляем значения "1" и "100".

# In[37]:


data_ceiling_height['ceiling_height'] = pd.to_numeric(data_ceiling_height['ceiling_height'])


# In[38]:


data_ceiling_height = data_ceiling_height.query('ceiling_height not in [1, 14, 100, 1.8]')
def ceiling_height_chng (ceiling_height):
    if 100 == ceiling_height:
        return 0
    elif ceiling_height < 2:
        return 0
    elif 10 < ceiling_height <= 19:
        return 0
    elif 20 <= ceiling_height <= 32:
        return ceiling_height / 10
    else:
        return ceiling_height

    
data_ceiling_height['ceiling_height'] = data_ceiling_height.apply(lambda x: ceiling_height_chng(x['ceiling_height']), axis = 1)


# ### <font color='red'>Комментарий от наставника 5 <span style="color:green;font-size:200%">&#10003;</span>
# Вот тут тоже можно было немного уменьшить количество копипасты, если сделать это в цикле. И то же ниже.

# ### <font color='red'> Комментарий для наставника. В цикле не получилось, сделал функций. <span style="color:green;font-size:200%">&#10003;</span>

# ### <font color='green'>Комментарий от наставника 3 итерация 2
# Да, так отлично

# ### Заполнение пропусков столбца ceiling_height4
# 
# Теперь непонятных значений больше нет. И можно сопоставлять высоту потолков и стоимость квадратного метра квартир, расположенных в городе Санкт-Петербург.

# In[39]:


data_ceiling_height.plot(x='ceiling_height', y='price_bym', kind='scatter', alpha=0.09)


# ### Заполнение пропусков столбца ceiling_height5
# 
# Формируем пузырьковую диаграмму по очищенным данным.
# 
# Из диаграммы видно, что зависимость высоты потолков и цены квадратного метра объектов недвижимости отсутствует. При этом, имеется значительное количество выбросов, как по цене за метр, так и по высоте потолков.
# 
# Статистически выбросы это небольшие, для более наглядного представления данных считаю необходимым эти выбросы удалить. По критерию "цена квадратного метра", удаляю объекты стоимостью более 700000 рублей за квадратный метр, по критерию "высота потолков", удаляю объекты с высотой потолков более 5 метров.

# In[40]:


data_ceiling_height = data_ceiling_height.query('ceiling_height < 5')
data_ceiling_height = data_ceiling_height.query('price_bym < 700000')
ceiling_height_mean = data_ceiling_height['ceiling_height'].mean()
data_ceiling_height.plot(x='ceiling_height', y='price_bym', kind='scatter', alpha=0.09)
print(data_ceiling_height['ceiling_height'].corr(data_ceiling_height['price_bym']))


# # Выводы по столбцу ceiling_height
# 
# Между высотой потолков и ценой квадратного метра имеется корреляция, но не определяющая. При этом, важным фактом является то, что основной рынок находится около минимальных значений, и все выбросы идут вверх. 
# Коэффициент корреляции равен 0,31, и подтверждает сказанное выше.
# 
# Заменять значения будем медианой, определённой по очищенным данным.

# ### Процесс замены значений в столбце ceiling_height1
# 
# В процессе анализа данных столбца ceiling_height, были удалены значения с высотой потолка 1, 14 и 100.
# 
# При замене такое удаление нерационально. Необходимо заменить эти значения на 0, и впоследствии также заменить эти значения на медиану.

# In[41]:


data['ceiling_height'] = data_ceiling_height.apply(lambda x: ceiling_height_chng(x['ceiling_height']), axis = 1)
data['ceiling_height'] = data['ceiling_height'].fillna(0)
data['ceiling_height'].astype('int')
data['ceiling_height'] = round(data['ceiling_height'], 1)
print(data['ceiling_height'].unique())


# ### Процесс замены значений в столбце ceiling_height2
# 
# Смотрим значения с высотой потолков менее 2 метров, заменяем их на 0. Для расчёта средних, такие значения нам не нужны. Создаём временную таблицу для расчёта средней. Из временной таблицы убираем значения с высотой потолка равной нулю.

# In[42]:


data_tmp = data.query('ceiling_height != 0')


# In[43]:


ceiling_height_by_local_dict = data_tmp.groupby('building_series_id_y')['ceiling_height'].agg('mean').to_dict()
data['ceiling_height_mean'] = data['building_series_id_y'].map(ceiling_height_by_local_dict)
data.loc[data['ceiling_height'] == 0, 'ceiling_height'] = data.loc[data['ceiling_height'] == 0, 'ceiling_height_mean']
data[['ceiling_height', 'ceiling_height_mean', 'building_series_id_y']].head(10)


# ### <font color='green'>Комментарий от наставника 6
# Вижу, что ты используешь приём, который я показала на консультации, молодец!<br>

# ### Процесс замены значений в столбце ceiling_height2
# 
# Проверяем таблицу после замены.

# In[44]:


data.drop(['ceiling_height_mean'], axis='columns', inplace=True)
data.plot(x='ceiling_height', y='price_bym', kind='scatter', alpha=0.09)
print(data['ceiling_height'].corr(data['price_bym']))


# ### Процесс замены значений в столбце ceiling_height3
# 
# Строим пузырьковую диаграмму и считаем корреляцияю по всем значениям высоты потолков и цены квадратного метра. Диаграмма по всем объектам недвижимости в общем повторяет диаграмму по объекта м недвижимости города Санкт-Петербург. При этом появились объекты, где высота потолков увеличилась, а цена - нет.

# # Выводы по столбцам floors_total, living_area
# 
# Значения по столбцам floors_total, living_area, для нас не важны, поскольку в цене квадратного метра они не участвуют, и общее количество этажей на цену объектов массового рынка не влияет.
# 
# Цена на объекты, также считается исходя из общей площади объекта.
# 
# Заменяем пропуски в столбце "общая площадь", по медиане, исходя из типа объекта.

# In[45]:


data['living_area'] = data['living_area'].fillna(0)
data['living_area'].describe()
data['living_to_total_area'] = data['living_area'] / data['total_area']
data['living_to_total_area'].describe()


# ### Расчёт значений по столбцу living_to_total_area1
# 
# Для замены пропусков, ввожу допущение что в одной серии объектов недвижимости, отношение жилой площади к общей площади примерно равно.
# 
# Для этого вводим новый столбец living_to_total_area, где по каждому объекту рассчитывается отношение жилой площади, к общей. Из показателей видно, что среднее значение - 51,94% недалеко от медианы - 55,88%, и 50% объектов сосредоточенно в достаточно узком диапазоне значений.
# 
# Жилая площадь не может занимать всю площадь квартиры, и её не может не быть совсем. При этом, в столбце есть нулевые значения (в т.ч., из-за замены нулём пропусков), и есть значения больше единицы, которые являются заведомо неправильным и их нужно заменить.
# 
# Для выделения заведомо неправильных значений воспользуемся стандартным подходом, а именно - нижнюю границу установим на границе 25% минус 1,5 стандартных отклонения, аналогично для верхней границы - 75% плюс 1,5 стандартных отклонения.
# 
# То есть нижняя граница будет 47 - 18 = 29%, а верхняя - 63 + 18 = 81%.
# 
# Соответственно, коэффициент, где жилая площадь занимает менее 29% и более 81% будут пересчитаны по средним значениям, сгруппированным по типам объектов недвижимости.

# In[46]:


living_to_total_area_by_bldngid = data.groupby('building_series_id_y')['living_to_total_area'].agg('mean').to_dict()
data['living_to_total_area_mean'] = data['building_series_id_y'].map(living_to_total_area_by_bldngid)
data['living_to_total_area'] = data['living_to_total_area'].where(data['living_to_total_area'] > 0.29, data['living_to_total_area_mean'])
data['living_to_total_area'] = data['living_to_total_area'].where(data['living_to_total_area'] < 0.81, data['living_to_total_area_mean'])
data[['living_to_total_area', 'living_to_total_area_mean', 'building_series_id_y']].head(10)


# ### Расчёт значений по столбцу living_to_total_area2
# 
# Пропуски заменены, проверили, что при выходе значений за контрольные значения, всё стоит корректно.

# In[47]:


data.drop(['living_to_total_area_mean'], axis='columns', inplace=True)
data['rooms'].unique()


# In[48]:


print(data['is_apartment'].unique())
print(data['is_apartment'].value_counts())


# # Выводы по столбцу is_apartment
# 
# Столбец is_apartment, из 23699 значений, в 2725 случаях имеет значение False, а в 50 случаях имеет значение True.
# Делать выводы о данном столбце смысла не имеет. Какого-либо существенного значения он для анализа не имеет.

# # Анализ пропусков в столбце kitchen_area
# 
# Для анализа того, как площадь кухни влияет на показатель стоимости квадратного метра, рассмотрим разные категории площади кухонь, и выясним корреляцию площади кухни, и стоимости квадратного метра квартиры.  

# In[49]:


data['kitchen_area'].fillna(0, inplace = True)
data['kitchen_area'].astype('int')
data['kitchen_area'] = round(data['kitchen_area'], 0)
print(data['kitchen_area'].unique())


# ### Процесс замены значений в столбце kitchen_area1
# 
# Переводим значения "площадь кухни", в цифры. Заменяем nan, на нули. Округляем значения до целых цифр, и выводим уникальные значения.
# 
# Визуально видим следующие интересные значения: 0, от одного до четырёх, пять и выше, двадцать и выше. Распределим значения через гистограмму.

# In[50]:


print(data['kitchen_area'].hist())


# ### Процесс замены значений в столбце kitchen_area2
# 
# Основное количество объектов это 20 квадратных метров. Смотрим диаграмму ближе

# In[51]:


print(data['kitchen_area'].hist(range=(0, 20)))


# ### Процесс замены значений в столбце kitchen_area3
# 
# На графике явно видно, что существенными значениями являются значения от 5 до 20 квадратрых метров. Что представляется логичным.

# In[52]:


head_kitchen_area = ['kitchen_area', 'locality_name', 'price_bym']
data_kitchen_area = pd.DataFrame(data = data, columns = (head_kitchen_area))
print(data_kitchen_area.head(5))


# ### Процесс замены значений в столбце kitchen_area4
# 
# Чтобы отследить процесс зависимости цены квадратного метра, от площади кухни, точно также копируем данные по площади кухни, местонахождении (город Санкт-Петербург), и цене за метр.

# In[53]:


data_kitchen_area = (data_kitchen_area
                    .query('kitchen_area >= 5 and kitchen_area <= 20 and locality_name == "Санкт-Петербург"')
)
data_kitchen_area.groupby(by='kitchen_area').count()


# ### Процесс замены значений в столбце kitchen_area5
# 
# 
# Оставляем только квартиры с площадью от 5 до 20 квадратных метров, и городом Санкт-Петербургом.

# In[54]:


data_kitchen_area.plot(x='kitchen_area', y='price_bym', kind='scatter', alpha=0.09)
print(data_kitchen_area['kitchen_area'].corr(data['price_bym']))


# ### Процесс замены значений в столбце kitchen_area6
# 
# Поскольку выбросы по площадям кухонь убраны ранее, то остались только выбросы по цене за квадратных метр. Выше 250 тысяч рублей за метр значений очень мало. Убираем эти значения.

# In[55]:


data_kitchen_area = data_kitchen_area.query('price_bym <= 200000')
data_kitchen_area.plot(x='kitchen_area', y='price_bym', kind='scatter', alpha=0.09)
print(data['kitchen_area'].corr(data['price_bym']))


# ### Выводы по столбцу kitchen_area
# 
# Цена за квадратный метр объектов недвижимости зависит от площади кухни. Чем больше кухня, тем больше стоимость квадратного метра. При этом, в основном, рынок находится у средних значений, и цену квадратного метра повышает не массовый рынок, а выбросы.
# 
# Замену отсутствующих, и заведомо неверных площадей будем производить на медиану по типам объектов недвижимости.

# In[56]:


data_tmp = data.query('kitchen_area > 5')


# In[57]:


kitchen_area_by_local_dict = data_tmp.groupby('building_series_id_y')['kitchen_area'].agg('mean').to_dict()
data['kitchen_area_mean'] = data['building_series_id_y'].map(ceiling_height_by_local_dict)
data.loc[data['kitchen_area'] == 0, 'kitchen_area'] = data.loc[data['kitchen_area'] == 0, 'kitchen_area_mean']
data[['kitchen_area', 'kitchen_area_mean', 'building_series_id_y']].head(10)


# In[58]:


data.drop(['kitchen_area_mean'], axis='columns', inplace=True)
data['kitchen_to_total'] = data['kitchen_area'] / data['total_area']


# In[59]:


print(data['balcony'].unique())


# ### Процесс замены значений в столбце balcony1
# 
# В поле о количестве балконов приведены логичные цифры. Может ли nan, свидетельствовать что балконов нет?
# Посмотрим серии квартир там где в столбце balcony, указано - nan.

# In[60]:


#data.groupby('balcony').count()
data_tmp = data.query('balcony == "nan"')
data_tmp.groupby('building_series_id_y').agg({'price_bym':['count']})


# ### Процесс замены значений в столбце balcony2
# 
# Ничего необычного. Обычные серии квартир с балконами. Значит значение nan существует, когда информация о балконах не указана. При этом, замена nan возможна только на среднее по сериям, и количеству комнат.
# 
# Считаю, что такая замена не улучшит качество анализа, и её не произвожу.

# In[61]:


data['balcony'] = data['balcony'].fillna(-1)


# In[62]:


data.plot(x='balcony', y='price_bym', kind='scatter', alpha=0.09)
print(data['balcony'].corr(data['price_bym']))


# ### Вывод о корреляции количества балконов и стоимости квадратного метра
# 
# Количество балконов никак не влияет на цену квадратного метра квартиры.

# In[63]:


print(data['airports_nearest'].describe())


# ### Производим замену значений в столбце floors_total.<span style="color:green;font-size:200%">&#10003;</span>
# 
# Производим замену пропусков на заведомо невозможное число -1, проверяем.

# In[64]:


data['floors_total'] = data['floors_total'].fillna(-1)
data['floors_total'].unique()


# ### Установка типа этажа (первый, последний или другой)<span style="color:green;font-size:200%">&#10003;</span>
# 
# Выводим тип этажа (первый, последний, другой). Там где нет данных - указываем "другой", как наиболее вероятный.

# In[65]:


def floor_type_ins (floor, floors_total):
    if floor == 1:
        return 'first'
    elif floor == floors_total:
        return 'last'
    else:
        return 'другой'

    
data['floor_type'] = data.apply(lambda x: floor_type_ins(x['floor'], x['floors_total']), axis = 1)
data.groupby('floor_type').count()


# ### Приведение столбца time_publication, к формату to_datetime. Установка года, месяца, и дня недели публикации<span style="color:green;font-size:200%">&#10003;</span>
# 
# Приводим столбец time_publication, в формат даты и времени. Заводим отдельные колонки для месяца, дня недели, и года публикации. Проверяем чтобы день недели был поставлен правильно.

# In[66]:


data['time_publication'] = pd.to_datetime(data['first_day_exposition'], format='%Y-%m-%d')
data['month_expstn'] = pd.DatetimeIndex(data['first_day_exposition']).month
data['day_expstn'] = pd.DatetimeIndex(data['first_day_exposition']).weekday
data['year_expstn'] = pd.DatetimeIndex(data['first_day_exposition']).year
data['day_expstn'].unique()


# ### Определение дополнительных столбцов таблицы.
# Устанавливаем дополнительне столбцы, а именно: месяц публикации объявления, день недели публикации объявления, год публикации объявления.

# In[67]:


dataspb = data.query('locality_name == "Санкт-Петербург" and cityCenters_nearest > 0')
dataspb.plot(y='year_expstn', kind='hist', grid=True, legend=True)
dataspb2017 = dataspb.query('year_expstn == 2017')
dataspb2018 = dataspb.query('year_expstn == 2018')


# # Работа с ценой квадратного метра
# 
# После того, как для каждого объекта определены год, месяц и день публикации, можно посмотреть как менялось количество объявлений и цены по годам.
# 
# Из графика видно, что максимальное количество объявлений было дано в 2017 и 2018 году. Посмотрим, как менялись цены в эти годы, и распределение цен на объекты за квадратный метр. Создаём две таблицы для 2017, и 2018 года соответственно.

# In[68]:


dataspb2018.describe()


# In[69]:


dataspb2017.describe()


# ### Анализируем изменения цен в 2017 и 2018 годах.
# 
# Из анализа цен видно, что средние цены и их структура в 2017 и 2018 годах изменилась незначительно. А именно:
# - Средняя цена почти не изменилась - 114 / 111.
# - Медианная цена также почти не изменилась - 106 / 101
# - Среднее отклонение было 44, стало 53.
# 
# То есть имеются значительный объём объектов, отстоящих далеко от средних значений. Для анализа изменения цен берём 2017 и 2018 годы.

# ### Общая информация о столбце airports_nearest
# 
# В столбце airports_nearest представлены расстояния до аэропорта. Расстояния выражены в метрах, и различаются от нуля, до 84869 метров. При этом медиана незначительно меньше чем среднее значение.
# 
# Считаю правильным категоризировать значения по уровню расстоянию до аэропорта. Для категоризации строим гистограмму.

# In[70]:


data['airports_nearest'].hist()


# ### Замена значений в столбце airports_nearest1 <span style="color:green;font-size:200%">&#10003;</span>
# 
# Данные в таблице не позволят заменить пропуски по географическим привязкам, поскольку иные данные не имеют никакой связи с расстоянием от объекта до аэропорта. В связи с этим, замену данных не осуществляем. Для анализа зависимости влияния местоположения объекта на цену создадим отдельную таблицу, из которой удалим все пропуски. И выводы будем делать на основании этой таблицы. Данных для анализа после удаления более чем достаточно.

# In[71]:


data_airports_nearest = data.copy()
data_airports_nearest.dropna(subset = ['airports_nearest'], inplace=True)
data.info()


# In[72]:


data_airports_nearest.plot(x='airports_nearest', y='price_bym', kind='scatter', alpha=0.09)
print(data['airports_nearest'].corr(data['price_bym']))


# ### Вычисление влияния расстояния до аэропорта на цену на квартиру <span style="color:green;font-size:200%">&#10003;</span>
# 
# Строим пузырьковую диаграмму по расстоянию до аэропорта, и цене квадратного метра объекта. На диаграме видно отсутствие зависимости, что подтверждается коэффициентом корреляции.

# In[73]:


print(data['cityCenters_nearest'].describe())


# In[74]:


dataspb = data.query('locality_name == "Санкт-Петербург" and cityCenters_nearest > 0')
dataspb.groupby('cityCenters_nearest')['locality_name'].count()
dataspb.info()


# ### Анализ столбца cityCenters_nearest <span style="color:green;font-size:200%">&#10003;</span>
# 
# Для анализа представлены 18156 значений, из них 15636 - в городе Санкт-Петербург, где указано расстояние до центра города. При этом, сравнивать расстояние до центра города Санкт-Петербурга, и расстояние до центра других населённых пунктов считаю неверным.
# 
# В связи с этим анализ будет производиться только по объектам, находящимся в городе "Санкт-Петербург". Также в таблице нет данных, позволяющих заполнить пропуски по полю cityCenters_nearest.
# 
# Таким образом, необходимо создать таблицу, куда будут внесены только объекты находящиеся в городе "Санкт-Петербург", и только объекты с указанным расстоянием до центра города - dataspb. Выводы будем делать по этой таблице.

# In[75]:


dataspb = data.query('locality_name == "Санкт-Петербург" and cityCenters_nearest > 0')
dataspb.groupby('cityCenters_nearest')['locality_name'].count()
print(dataspb['cityCenters_nearest'].hist(bins=28, range=(0, 28000)))
print(dataspb['cityCenters_nearest'].hist(range=(3000, 8000)))
print(dataspb['cityCenters_nearest'].hist(range=(11000, 16000)))


# In[76]:


dataspb.plot(x='cityCenters_nearest', y='price_bym', kind='scatter', alpha=0.09)
print(dataspb['cityCenters_nearest'].corr(data['price_bym']))


# ###  Анализ столбца cityCenters_nearest1
# 
# На диаграмме отражён крайне интересный факт.
# **Несмотря на значительные выбросы в ценах, цены квадратного метра за основной объём не снижаются линейно**. Об этом же говорит и низкий коэффициент корелляции. Это очень странный вывод, цены на недвижимость должны линейно падать пропорционально расстоянию от центра.
# 
# Попробуем ввести дополнительные ограничения, а именно выделим только одну, наиболее массовую серию квартир - 1564812, и построить диаграмму по этой серии. Также ограничим цену квадратного мтера 500000 тысячами рублей за метр.
# 

# In[77]:


dataspb_1564812 = dataspb.query('building_series_id_y == "1564812" and price_bym <= 500000')    
dataspb_1564812.plot(x='cityCenters_nearest', y='price_bym', kind='scatter', alpha=0.09)
print(dataspb_1564812['cityCenters_nearest'].corr(data['price_bym']))


# ### Анализ столбца cityCenters_nearest2
# 
# Корреляция увеличилась, но незначительно. При этом, линейное снижение идёт по отдельным объектам с максимальной ценой
# **Несмотря на то, что в диапазоне до 7 километров, есть множество дорогих объектов, однозначная зависимость невысока**
# Вывод парадоксальный и абсолютно неочевидный.

# In[78]:


print(data['parks_around3000'].unique())
data['parks_around3000'].hist()


# In[79]:


dataspb.plot(x='parks_around3000', y='price_bym', kind='scatter', alpha=0.09)
print(dataspb['parks_around3000'].corr(data['price_bym']))


# ### Вывод по столбцу parks_around3000
# 
# Корреляции между ценой квадратного метра и количеством парков в радиусе трёх километров не установлено. Графики выглядят аналогично графикам, где исследовалась цена за квадратный метр. Отличается не массовый рынок, а количество выбросов в высокую цену.

# In[80]:


print(data['parks_nearest'].describe())
data['parks_nearest'].hist()


# ### Анализ столбца parks_nearest
# 
# Информация о расстоянии указана в 8059 объявлениях. При этом, данные указываются при расстоянии до 1200 метров. То есть, выборка должна повторять выборку по столбцу parks_around3000. Проверим корреляцию на данных о квартирах в Санкт-Петербурге.

# In[81]:


dataspb.plot(x='parks_nearest', y='price_bym', kind='scatter', alpha=0.09)
print(dataspb['parks_nearest'].corr(data['price_bym']))


# ### Вывод по столбцу parks_around3000
# 
# Корреляции между ценой квадратного метра и расстоянием до парка в радиусе трёх километров не установлено. И опять разница состоит не в массовом рынке, а в единичных предложениях.

# In[82]:


print(data['ponds_nearest'].describe())
data['ponds_nearest'].hist()


# ### Анализ столбца ponds_nearest
# Информация о расстоянии указана в 9102 объявлениях. При этом, данные указываются при расстоянии до 1300 метров. Проверим корреляцию на данных о квартирах в Санкт-Петербурге.

# In[83]:


dataspb.plot(x='ponds_nearest', y='price_bym', kind='scatter', alpha=0.09)
print(dataspb['ponds_nearest'].corr(data['price_bym']))


# ### Вывод по столбцу ponds_nearest
# И опять мы видим ровный рынок с выбросами в высокую цену при расстояни до 650 метров. Корреляции между ценой квадратного метра и расстоянием до пруда не установлено.

# In[84]:


data['last_price'] = data['last_price'].astype('int')
data['floors_total'] = data['floors_total'].astype('int')
data['floor'] = data['floor'].astype('int')
data['is_apartment'] = data['is_apartment'].astype('bool')
data['balcony'] = data['balcony'].astype('int')
data['price_bym'] = data['price_bym'].astype('int')


# ### Общий вывод по замене типов данных <span style="color:green;font-size:200%">&#10003;</span>
# 
# Были заменены следующие типы данных:
# - last_price (цены, установленные в рублях, дробных значений для таких цен не требуется);
# - floors_total (количество этажей, всегда является целым числом, при этом для пропусков использован вариант "-1")
# - floor (аналогично количеству этажей, всегда целое число)
# - is_apartment (принимает только два значения, поэтому считаю правильным использовать булеву переменную)
# - balcony (количество балконов, аналогично количеству этажей, всегда целое число)
# - price_bym (цена за метр, в тысячах рублей, для анализа большей точности не требуется
# 
# Остальные переменные, оставил без изменений, поскольку для них либо требуются дробные числа, либо имеются пропуска, которые невозможно заменить

# # Какие пропущенные значения обнаружены
# 
# Пропуски обнаружены в строках building_series_id, ceiling_height, floors_total, living_area, is_apartment, kitchen_area, balcony, locality_name, airports_nearest, cityCenters_nearest, parks_around3000, parks_nearest, ponds_around3000, ponds_nearest, days_exposition., то есть в большинстве столбцов таблицы.

# # В чём возможные причины возникновения пропусков <span style="color:green;font-size:200%">&#10003;</span>
# 
# 
# Самая очевидная причина возникновения пропусков - это неполная информация в скачанных объявлениях. Люди не указывают о продаваемых объектах полную информацию. Также пропуски могли возникнуть из-за ошибок в формировании объявлений. Это могло возникнуть если продавцы использовали нестарндартные или неадекватные сокращения или называния. Пропуски в географических характеристиках могли появиться из-за невозможности определить точный адрес продаваемого объекта.

# In[85]:


data['last_price'] = data['last_price'].astype('int')
data['floors_total'] = data['floors_total'].astype('int')
data['floor'] = data['floor'].astype('int')
data['is_apartment'] = data['is_apartment'].astype('bool')
data['balcony'] = data['balcony'].astype('int')
data['price_bym'] = data['price_bym'].astype('int')


# # В каких столбцах потребовалось изменить тип данных и почему <span style="color:green;font-size:200%">&#10003;</span>
# 
# 
# Были заменены следующие типы данных:
# 
# last_price (цены, установленные в рублях, дробных значений для таких цен не требуется);<br>
# floors_total (количество этажей, всегда является целым числом, при этом для пропусков использован вариант "-1")<br>
# floor (аналогично количеству этажей, всегда целое число)<br>
# is_apartment (принимает только два значения, поэтому считаю правильным использовать булеву переменную)<br>
# balcony (количество балконов, аналогично количеству этажей, всегда целое число)<br>
# price_bym (цена за метр, в тысячах рублей, для анализа большей точности не требуется<br>
# Остальные переменные, оставил без изменений, поскольку для них либо требуются дробные числа, либо имеются пропуска, которые невозможно заменить

# # По какому принципу заполнены пропуски <span style="color:green;font-size:200%">&#10003;</span>
# 
# - building_series_id - заменены совпадающие серии, серии с маленьким количеством объектов собраны в одну группу "Другие", серии с пропущенными значениями заменены на наиболее массовые серии по похожим площадям квартир.
# - ceiling_height (были заменены заведомо неадекватные значения, а также пропущенные значения, были заменены на медианы по типам квартир)
# - floors_total произведена замена пропусков на заведомо невозможное значение (-1). Замену по сериям считаю нецелесообразной, не влияющей на цену и поэтому не проводил. При определении типа этажа, там где не было указано этажа, указывал тип "другой".
# - living_area произведена замена пропусков на заведомо невозможное значение (0). Замену по сериям не производил. При определении показателя "отношение жилой площади к общей", по объектам для которых не была указана жилая площадь заменял на медины по типам здания. Также сделал для заведомо невозможных показателей.
# - is_apartment - замена пропусков не производилась, считаю эту замену ненужной. 
# - kitchen_area - пропуски были заменены медианой по сериям.
# - balcony, locality_name, airports_nearest, cityCenters_nearest, parks_around3000, parks_nearest, ponds_around3000, ponds_nearest, days_exposition - замены не производились. Считаю что для замены нет оснований, и замена не улучшит данные.

# # Каковы типичные параметры продаваемых квартир (например, площадь, цена)<span style="color:green;font-size:200%">&#10003;</span>
# 
# Выделить типичные квартиры нельзя, поскольку квартиры подразделяются по локациям и количеству комнат. При этом, можно выделить некие характеристики наиболее массовых квартир, а именно:
# - площадь - большая часть квартир площадью от 30 до 50 квадратных метров
# - цена за метр - медианная цена за метр составляет 95 тысяч рублей, средняя - 100 тысяч рублей, половина продаваемых квартир выставлена в диапазоне от 76,5 до 114,2 тысяч рублей.
# - серия - большая часть продаваемых квартир, относится к серии - 1564812.

# In[86]:


data['total_area'].plot(kind='hist', bins=30, grid=True, legend=True)


# In[87]:


data['total_area'].plot(kind='hist', bins=30, grid=True, legend=True, range=(10, 200))


# In[88]:


data['price_bym'].plot(kind='hist', bins=30, grid=True, legend=True)


# Распределение представленных объектов по цене за квадратный метр. Все объекты сконцентрированы в узком промежутке от 0 до 250 тысяч рублей за метр.

# In[89]:


data['price_bym'].hist(bins=30, range=(30, 280))


# Распределение объектов по цене в пределах от 30 до 280 тысяч рублей.
# 
# На этом графике распределение похоже на график нормального распределения.

# In[90]:


data_groupby_building_series_id = data.groupby('building_series_id_y').count()
data_groupby_building_series_id.plot(kind='pie', y='total_area', legend=False)


# In[91]:


data['days_exposition'].describe()


# # Сколько длится процесс продажи
# 
# В Процесс продажи длится от 45 до 232 дней. При этом, стандартное отклонение и разброс показателей очень значителен, от одного дня, до 1580 дней (почти пяти лет).

# # Убираем необычные параметры квартир
# 
# При анализе выявлены следующие необычные параметры:
# - площадь квартиры (менее 20 квадратных метров, более 200 квадратных метров)
# - цена за метр (менее 30 тысяч рублей за метр, и более 250 тысяч рублей за метр)
# - высота потолков (более 5 метров);
# - площадь кухни (более 20 квадратных метров);
# Учитывать географические параметры нецелесообразно, поскольку для значимого количества данных таких параметров нет.
# Уберём их из таблицы и сформируем новую таблицу для анализа data_standart

# In[92]:


data_standart = data.query('total_area > 20 and total_area < 200 and price_bym > 30 and price_bym < 250 and ceiling_height < 5 and kitchen_area < 20')
data_standart.info()


# In[93]:


data_standart['price_bym'].hist()


# Распределение обычных квартир по ценам. Нет особенностей - хороший, красивый график нормального распределения цен

# # Какие факторы больше всего влияют на стоимость квартиры? 
# 
# Для анализа влияния факторов на стоимость квадратного метра, сформируем среднюю выборку, по объектам, а именно:
# - стандартные квартиры, без отклонений, собранные в базе data_standart
# - тип квартиры 1564812
# - отбираем только квартиры из Санкт-Петербурга.
# Для этого сформируем базу data_standart1

# In[94]:


data_standart1 = data_standart.query('building_series_id_y == "1564812" and locality_name == "Санкт-Петербург"')


# data_standart1.plot(x='rooms', y='price_bym', kind='scatter', alpha=0.09)
# print(data_standart1['rooms'].corr(data['price_bym']))

# **Цена квадратного метра не зависит от количества комнат**

# In[95]:


data_standart1_first = data_standart1.loc[data_standart1.loc[:,'floor_type'] == 'first']
data_standart1_last = data_standart1.loc[data_standart1.loc[:,'floor_type'] == 'last']
data_standart1_other = data_standart1.loc[data_standart1.loc[:,'floor_type'] == 'другой']


# In[96]:


data_standart1_first['price_bym'].describe()


# In[97]:


data_standart1_last['price_bym'].describe()


# In[98]:


data_standart1_other['price_bym'].describe()


# **Цена квадратного метра, незначительно снижается если квартира расположена на первом этаже**

# data_standart1.plot(x='day_expstn', y='price_bym', kind='scatter', alpha=0.09)
# data_standart1_pivot_day = data_standart1.pivot_table(index='day_expstn', values='price_bym', aggfunc = 'describe')
# print(data_standart1['day_expstn'].corr(data['price_bym']))
# data_standart1_pivot_day

# In[99]:


head_table = ['rooms', 'ceiling_height', 'kitchen_area', 'cityCenters_nearest', 'living_to_total_area', 'kitchen_to_total', 'month_expstn', 'day_expstn', 'year_expstn']
i = 0
for i in range(len(head_table)):
    print(head_table[i], data_standart1[head_table[i]].corr(data['price_bym']))
    print(data_standart1.pivot_table(index = head_table[i], values='price_bym', aggfunc = 'describe'))
    i += 1


# ### <font color='orange'>Комментарий от наставника 5 итерация 2
# Старайся в циклах не использовать конструкции вида `range(len(array))`. В случае, когда тебе нужен и индекс и значение, пишут так:<br>
# `for column_index, column_name in enumerate(head_table): ...`
#     
# Но в твоём случае не нужно даже и индекса, ты же дальше его никак не используешь. Поэтому лучше написать так:<br>
# `for column_name in head_table: ...`
# 
# 

# In[127]:


i = 0
for i in range(len(head_table)):
    # НАСТАВНИК: тут был лишний print - убрала его
    data_standart1.plot(x=head_table[i], y='price_bym', kind='scatter', alpha=0.09)
    i += 1


# ### <font color='red'>Комментарий от наставника 7 <span style="color:green;font-size:200%">&#10003;</span>
# Я предлагаю тут немного "автоматизировать" построение однотипных графиков и таблиц с помощью цикла по выбранным столбцам. Ты можешь в одном цикле строить и графики, и таблицы, и выводить коэффициент корреляции. В такой клетке будет большой вывод, но это не страшно, его всегда можно спрятать. А дальше я предлагаю последовательно пробежаться глазами по этим графикам и в следующей клетке написать один хороший комментарий по тому, что ты там увидел.<br>
# И если будет нужно, то уже ниже можно построить "кастомные" графики.
#     
# P.S. В таком случае можно сразу построить графики для бОльшего числа параметров и на всякий случай сразу посмотреть и на них.

# ### <font color = 'red'> Комментарий для наставника <span style="color:green;font-size:200%">&#10003;</span>
# 
# Сделал циклом как ты сказала. Цикл очень красиво ложится на значения корреляции. Но вот для таблиц выглядит плохо. Таблицы гораздо лучше выглядят без принта, в отдельных ячейках. 
# 
# По параметрам поступил так - то, что не идёт в цикл - оставил. То что идёт - удалил.
# 
# ### <font color='green'>Комментарий от наставника 4 итерация 2
# Согласна, таблица без print выглядит лучше.

# ### Влияние факторов на цены стандартных квартир
# 
# - Цена не зависит от количества комнат
# - Цена снижается с удалением от центра, и снижается существенно
# - Цена не зависит от времени размещения объявления (день недели, месяц)
# - Цена зависит от года размещения объявлений, цены на недвижимость растут, и разброс цен тоже растёт.
# - Цена несколько зависит от кухни

# In[101]:


print("Влияние на цену удалённости от центра города", data_standart1['price_bym'].corr(data['cityCenters_nearest']))
print("Влияние на цену высоты потолков", data_standart1['price_bym'].corr(data['ceiling_height']))
print("Влияние на цену площади кухни", data_standart1['price_bym'].corr(data['kitchen_area']))


# # Вывод:
# 
# Максимальное влияние на цену квадратного метра оказывает удалённость от центра города (-33%).
# Высота потолков и площадь кухни влияет на цену квадратного метра на 20% каждый.

# # Цена квадратного метра в пригородах <span style="color:green;font-size:200%">&#10003;</span>

# In[102]:


data_locality = data.pivot_table(index = 'locality_name', values='price_bym', aggfunc = ['median', 'count'])
data_locality.columns = ['median', 'count']
data_locality.sort_values(by='count', ascending=False, inplace=True)
data_locality.drop(['Санкт-Петербург'], inplace=True)
data_locality.head(10)


# # Вывод по цене квадратного метра в пригородах
# 
# Цены в основных пригородах несколько ниже чем в Санкт-Петербурге. Причём в каждом пригороде квартир продаётся значительно меньше чем в самом Санкт-Петербурге.
# 
# Цены варьируются от 100 тысяч рублей за метр в Пушкине, до 58 тысяч за метр в Выборге.

# # Выделение типичных квартир в центре и вне центра

# In[103]:


#dataspb = dataspb.query('building_series_id_y == "1564812"')
print(dataspb['cityCenters_nearest'].hist(bins=28, range=(0, 28000)))
print(dataspb['cityCenters_nearest'].hist(range=(3000, 8000)))
print(dataspb['cityCenters_nearest'].hist(range=(11000, 16000)))


# ### Выделение типичных квартир в центре и вне центра, по удалённости от центра
# 
# Выделяем границы "в центре" и "вне центра", для группировки типичных квартир.
# 
# В "центр", попали квартиры с расстоянием от 3 до 8 километров. "вне центра" - попали квартиры на расстоянии от 11 до 16 километров.

# In[104]:


dataspb_citycenter3_8 = dataspb.query('cityCenters_nearest > 3000 and cityCenters_nearest < 8000')
dataspb_citycenter11_16 = dataspb.query('cityCenters_nearest > 11000 and cityCenters_nearest < 16000')
dataspb_citycenter3_8['total_area'].hist(bins=25, range=(0, 250))
dataspb_citycenter3_8['total_area'].hist(bins=25, range=(40, 100))


# In[105]:


dataspb_citycenter11_16['total_area'].hist(bins=15, range=(0, 150))
dataspb_citycenter11_16['total_area'].hist(bins=15, range=(30, 70))


# ### Выделение типичных квартир в центре и вне центра, по площадям
# 
# Определяем типичную площадь квартир "в центре" и "вне центра", для группировки типичных квартир.
# 
# Для квартир в центре, типичной площадью квартир является от 40 до 100 квадратных метров.
# Для квартир вне центра, типичной площадью является от 30 до 70 квадратных метров.

# In[106]:


dataspb_citycenter3_8_rooms = dataspb_citycenter3_8.pivot_table(index='rooms', values='price_bym', aggfunc = ['median', 'count'])
dataspb_citycenter11_16_rooms = dataspb_citycenter11_16.pivot_table(index='rooms', values='price_bym', aggfunc = ['median', 'count'])
dataspb_citycenter3_8_rooms


# In[107]:


dataspb_citycenter11_16_rooms


# ### Выделение групп квартир по удалённости, площади и количеству комнат.
# 
# Таким образом, сформированы четыре группы максимально типичных предложений, а именно:
# - В центре, это 2-3 комнатные квартиры с площадью от 40 до 100 квадратных метров.
# - Вне центра, это 1-комнатные, 2-комнатные, и трёх-комнатные квартиры, площадью от 30 до 70 квадратных метров.
# Всего четыре группы. По этим группам и будем смотреть корреляцию основных факторов (удалённость от центра, площадь кухни и высота потолков)

# In[108]:


dataspb_citycenter3_8_total_40_100 = dataspb_citycenter3_8.query('total_area > 40 and total_area < 100')
dataspb_citycenter11_16_rms1_ttl_30_70 = dataspb_citycenter11_16.query('rooms == 1 and total_area > 30 and total_area < 70')
dataspb_citycenter11_16_rms2_ttl_30_70 = dataspb_citycenter11_16.query('rooms == 2 and total_area > 30 and total_area < 70')
dataspb_citycenter11_16_rms3_ttl_30_70 = dataspb_citycenter11_16.query('rooms == 3 and total_area > 30 and total_area < 70')


# In[109]:


def del_columns (df_for_del):
    pricebym = df_for_del.drop(['total_area', 'rooms', 'total_images', 'last_price', 'ceiling_height', 'floors_total', 'living_area', 'floor', 'studio', 'area', 'parks_nearest', 'ponds_around3000',  'ponds_nearest', 'days_exposition', 'living_to_total_area', 'kitchen_to_total', 'month_expstn', 'day_expstn', 'year_expstn', 'open_plan', 'kitchen_area', 'balcony', 'airports_nearest', 'cityCenters_nearest', 'parks_around3000'], axis='columns')
    pricebym = pricebym.drop(['ceiling_height', 'parks_nearest', 'ponds_around3000',  'ponds_nearest', 'days_exposition', 'living_to_total_area', 'kitchen_to_total', 'month_expstn', 'day_expstn', 'year_expstn', 'open_plan', 'kitchen_area','cityCenters_nearest', 'parks_around3000'])
    return pricebym

data_price_by_m = dataspb_citycenter3_8_total_40_100.corr()
data_price_by_m_only = del_columns(data_price_by_m) 
data_price_by_m_only


# ### Вывод по группе квартир в центре
# 
# Если квартира уже находится в центре, то влияние расстояния до центра минимально, а именно - минус 3%. То есть чем ближе к центру тем дешевле. Данный факт абсолютно оправдан, поскольку ценность центра не в точке на карте, а в близости к району.
# 
# Высота потолков, также не влияет на цену квартиры. Уровень корреляции - 1%. Возможно, что высота потолков почти везде является достаточной, и поэтому дальнейшего роста влияния не происходит.
# 
# Влияние на цену площади кухни является более существенным 22%. Эта ситуация также является оправданной, поскольку люди живущие в центре ценят комфорт, и возможность пользоваться более большой кухней.

# In[110]:


data_price_by_m1 = dataspb_citycenter11_16_rms1_ttl_30_70.corr()
data_price_by_m1_only = del_columns(data_price_by_m1) 
data_price_by_m1_only


# ### Вывод по группе однокомнатных квартир вне центра
# 
# Для однокомнатных квартир, расположенных вне центра существует незначительная корреляция в расстоянии до центра, а именно - 11%. Логично, что корреляция есть, но нелогично что так мало.
# 
# На уровень цен для однокомнатных квартир, расположенных вне центра также незначительно влияет высота потолков. Это является оправданным, чем выше потолки тем комфортнее.
# 
# Влияние на цену площади кухни составляет всего 17%. Люди ценят комфорт, и хотят пользоваться большой кухней.

# In[111]:


data_price_by_m2 = dataspb_citycenter11_16_rms2_ttl_30_70.corr()
data_price_by_m2_only = del_columns(data_price_by_m2) 
data_price_by_m2_only


# ### Вывод по группе двухкомнатных квартир вне центра
# Для двухкомнатных квартир, расположенных вне центра, расстоянии до центра, не влияет на цену квартиры. Всего 7%. Возможно, что люди покупающие двухкомнатные квартиры больше ценят другие факторы.
# 
# При этом, высота потолков, для двухкомнатных квартир, расположенных вне центра влияет на 19%. То есть в отличии от однокомнатных квартир, покупатели двухкомнатных квартир больше ценят не удобство быть возле центра, а удобство нахождения в квартире.
# 
# Влияние на цену площади кухни составляет всего 33%. Существенно, и абсолютно оправданно. Двухкомнатные квартиры интересуют семьи, а не одиночек. А наличие большой кухни является существенным преимуществом.

# In[112]:


data_price_by_m3 = dataspb_citycenter11_16_rms3_ttl_30_70.corr()
data_price_by_m3_only = del_columns(data_price_by_m3) 
data_price_by_m3_only


# ### <font color='red'>Комментарий от наставника 8
# Старайся меньше использовать функцию print и чаще выводить информацию в виде таблиц :) <br>
# При этом можно переименовать столбцы/индекс строк в таблице, чтобы вывод был такой же понятный.
#     
# P.S. Это же касается и остальных мест

# ### Вывод по группе трёхкомнатных квартир вне центра
# Для трёхкомнатных квартир, расположенных вне центра, расстоянии до центра, оказывает незначительное влияние на цену квартиры, на уровне 13%.
# 
# При этом, высота потолков, для трёхкомнатных квартир, расположенных вне центра даёт отрицательный результат, что нелогично, и является аномалией.
# 
# Влияние на цену площади кухни составляет всего 10%. Странно, но владельцы трёхкомнатных квартир в представленных выборках ценят комфорт меньше всего.
# 
# Здесь значимым фактором являлся ещё и принцип отбора. Поскольку площадь отбиралась типичная для всех квартир, то логично, что в выборку попали большие однокомнатные квартиры, и маленькие трёхкомнатные. Соответственно, попали дорогие однокомнатные, где людям нужен комфорт, и трёхкомнатные, которые покупают более бедные люди.

# # Вывод по влиянию основных факторов на типичные квартиры <span style="color:green;font-size:200%">&#10003;</span>
# 
# При анализе были установлены три фактора, максимально влияющие на стоимость квартир, а именно: удалённость от центра города, высота потолков, и площадь кухни.
# 
# Произведено сравнение, как факторы влияли на выборку для квартир наиболее распространённой серии, в Санкт-Петербурге, очищенных от выбросов по площади квартир (менее 20 и более 200 квадратных метров), цене (более 250 тысяч рублей за метр), высоте потолков (более 5 метров), и площади кухни (более 20 метров).
# И квартир выбранных по удалённости от центра, площади и количеству комнат.
# 
# 
# Интересный факт состоит в том, что в более общей выборке факторы влияют более явно. А именно:
# 
# **Для максимально стандартной выборки по Санкт-Петербургу:**
# 
# Влияние на цену удалённости от центра города 0.33%
# 
# Влияние на цену высоты потолков 20%
# 
# Влияние на цену площади кухни 20%
# 
# **Для 2-3 комнатных квартир, расположенных в центре города, площадью от 40 до 100 квадратных метров**
# 
# Влияние на цену удалённости от центра города 11%
# 
# Влияние на цену высоты потолков 11%
# 
# Влияние на цену площади кухни 17%
# 
# **Для 1 комнатных квартир, расположенных вне центра города, площадью от 30 до 70 квадратных метров**
# 
# Влияние на цену удалённости от центра города 7%
# 
# Влияние на цену высоты потолков 19%
# 
# Влияние на цену площади кухни 33%
# 
# **Для 2 комнатных квартир, расположенных вне центра города, площадью от 30 до 70 квадратных метров**
# 
# Влияние на цену удалённости от центра города 13%
# 
# Влияние на цену высоты потолков 6%
# 
# Влияние на цену площади кухни 10%
# 
# **Для 3 комнатных кварти, расположенных вне центра города, площадью от 30 до 70 квадратных метров**
# 
# Влияние на цену удалённости от центра города 13%
# 
# Влияние на цену высоты потолков -0.06349660960965879
# Влияние на цену площади кухни 0.09862089880813915

# # Подбор типичных аппартаментов
# 
# Из общей таблицы выбираем аппартаменты по полю is_apartment. Смотрим распределение по расстоянию до центра, высоте потолков и площади кухни.

# In[113]:


data_appatment = data.query('is_apartment == True')
#data_appatment['cityCenters_nearest'].hist()
data_appatment['cityCenters_nearest'].hist(range=(10500, 16500))


# In[114]:


data_appatment['ceiling_height'].hist(range=(2.5, 2.8))


# In[115]:


data_appatment['kitchen_area'].hist(range=(7, 11))


# ### Описание типичных аппартаментов
# 
# Типичные аппартаменты представляют собой квартиры, отдалённые от центра от 10,5 до 16,5 километров, с высотой потолков от 2,5 до 2,8 метра, и площадью кухни от 7 до 11 квадратных метров.

# In[116]:


data_appatment = data_appatment.query('cityCenters_nearest >= 10500 and cityCenters_nearest <= 16500 and ceiling_height >= 2.5 and ceiling_height <= 2.8 and kitchen_area >= 7 and kitchen_area <= 11')
print("Влияние на цену удалённости от центра города", data_appatment['price_bym'].corr(data_appatment['cityCenters_nearest']))
print("Влияние на цену высоты потолков", data_appatment['price_bym'].corr(data_appatment['ceiling_height']))
print("Влияние на цену площади кухни", data_appatment['price_bym'].corr(data_appatment['kitchen_area']))


# # Вывод для аппартаментов
# 
# Для типичных аппартаментов значимыми факторами являются площадь кухни - 29%, и высота потолков - 24%. При этом, влияние на цену расстояния до центра города незначительное, только 7%.
# 
# По сравнению с выделенными типами квартир это гораздо выше, корреляция проявлена более чётко.

# # Подбор студий
# 
# Из общей таблицы выбираем аппартаменты по полю studio. Смотрим распределение по расстоянию до центра, и высоте потолков.

# In[117]:


data_studio = data.query('studio == True')
#data_appatment['cityCenters_nearest'].hist()
data_studio['cityCenters_nearest'].hist(range=(12000, 18000))


# In[118]:


data_studio['ceiling_height'].hist(range=(2.6, 2.8))


# ### Описание типичной студии
# 
# Типичная студия представляет собой студию, отдалённые от центра от 12 до 18 километров, с высотой потолков от 2,6 до 2,8 метра.

# In[119]:


data_studio = data_studio.query('cityCenters_nearest >= 12000 and cityCenters_nearest <= 18000 and ceiling_height >= 2.6 and ceiling_height <= 2.8')
print("Влияние на цену удалённости от центра города", data_studio['price_bym'].corr(data_studio['cityCenters_nearest']))
print("Влияние на цену высоты потолков", data_studio['price_bym'].corr(data_studio['ceiling_height']))


# # Вывод для студий
# 
# Для студий важным является показатель удалённости от центра - 45%, почти 50. Влияние на цену высоты потолков также присутствует, но ограничивается 16%.

# # Подбор квартир со свободной планировкой.
# 
# Из общей таблицы выбираем аппартаменты по полю open_plan. Смотрим распределение по расстоянию до центра, высоте потолков, и площади кухни.

# In[120]:


data_openplan = data.query('open_plan == True')
#data_openplan['cityCenters_nearest'].hist()
data_openplan['cityCenters_nearest'].hist(range=(11500, 14000))


# In[121]:


data_openplan['ceiling_height'].hist(range=(2.7, 2.8))


# In[122]:


data_openplan['kitchen_area'].hist(range=(2.8, 2.8))


# In[123]:


data_openplan = data_openplan.query('cityCenters_nearest >= 11500 and cityCenters_nearest <= 14000 and ceiling_height >= 2.7 and ceiling_height <= 2.8 and kitchen_area >= 2.7 and kitchen_area <= 2.9')
print("Влияние на цену удалённости от центра города", data_openplan['price_bym'].corr(data_openplan['cityCenters_nearest']))


# # Вывод для квартир с открытой планировкой
# 
# В типичных квартирах с открытой планировкой корреляция удалённости от центра и цены является линейной - 95%. Абсолютно логичный вывод, при этом странно, что такой вывод представлен толькодля таких квартир.
# Оценить влияение высоты потолков и площади кухни невозможно, поскольку показатели типичной квартиры с открытой планировкой очень близкие, а оценивать корреляцияю на близких показателях нельзя.

# # ОБЩИЙ ВЫВОД
# 
# **Типы зданий:**
# 
# Рынок недвижимости Санкт-Петербурга и его окрестностей отличается значительным разнообразием серий. При этом, подавляющую часть объектов занимает серия 1564812 - 13866 объектов и объекты других серий, определить которые или нельзя, или нецелесообразно (меньше пяти квартир в серии) - 7216 объектов.
# Остальные 2597 объектов распределены по разным сериям.
# 
# **Цены**
# 
# Массовый рынок находится около цены в 100 тысяч рублей за квадратный метр. При этом, установить какой-либо класс квартир с намного более высокой средней ценой не удалось.
# От массового рынка отделяется элитный рынок, который характеризуется близостью к центру, высокими потолками, большими площадями кухонь, близостью к паркам и прудам.
# 
# При этом, цены на элитные объекты нигде не группируются, определить уровень цен нельзя.
# 
# **Влияние на цены различных факторов**
# 
# Наиболее важным и стабильным фактором, влияющим на цены является удалённость объекта от центра. Дальше от центра - ниже цена. Для максимально стандартной выборки максимум влияния составляет 33%, что достаточно много, поскольку на цены влияет множество факторов. Также значимыми факторами являются высота потолком и площадь кухни (по 20%).

# ### <font color='red'>Комментарий от наставника по всей работе
# У тебя получилось очень детальное качественное исследование, молодец!
#     
# Единственное, давай поработаем над кодом: уберём копипасту и добавим "автоматизации" к нашему исследованию. Смотри комментарии 2, 3, 5, 7.<br>

# ### <font color='green'>Финальный комментарий от наставника
# Основные замечания были исправлены, молодец! Добавила немного новых комментарий. Они не критичные, поэтому работу я засчитываю. Просто постарайся их учесть в последующих проектах.
#     
# До встречи на консультации!
