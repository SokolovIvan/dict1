import pandas as pd
import numpy as np
from scipy import stats as st
calls_df = pd.read_csv('/datasets/calls.csv')
internet_df = pd.read_csv('/datasets/internet.csv')
sms_df = pd.read_csv('/datasets/messages.csv')
tariffs_df = pd.read_csv('/datasets/tariffs.csv')
users_df = pd.read_csv('/datasets/users.csv')


# In[2]:


calls_df.info()
calls_df.head()


# In[3]:


calls_df['duration'].hist()

# In[4]:

import math

calls_df = calls_df.query('duration != 0')
calls_df['duration'] = calls_df['duration'].apply(math.ceil)
calls_df['duration'].astype('int')
calls_df['duration'].unique()

# Убираем из таблицы все значения с нулём минут. Округляем длительность разговора в большую сторону. Переводим тип данных в int. Проверяем уникальные значения.

# In[5]:


internet_df.info()
internet_df.head()


# In[6]:


internet_df['mb_used'].hist()
internet_df = internet_df.query('mb_used != 0')
internet_df['mb_used'] = internet_df['mb_used'].apply(math.ceil)
internet_df['mb_used'].unique()

# В таблице internet_df пропуски и нули не выявлены. Убираем возможные нули. Округляем траффик до мегабайтов в большую сторону. Строим гистограмму по количеству потреблённых мегабайт. Видим красивый, очень правдоподобный график. Никаких особенных значений не выявлено. Оставляем как есть.

# In[7]:


sms_df.info()
sms_df.head()


# Пропусков не выявлено. Здесь каждый id - это факт смс. Поэтому единственное что может быть - это пропуски. Пропусков не выявленго, оставляем всё как есть. Обработка не требуется.

# In[8]:


tariffs_df.info()
tariffs_df.head()


# In[9]:


users_df.info()
users_df.head()


# В таблице о тарифах никакой обработки и изменений не требуется.
# В таблице о пользователях, есть пропуски в столбце churn_date, то есть - дата прекращения использования тарифа. Поскольку мы работаем только с 2018 годом, то целесообразна замена на дату 31.12.2018. Заменяем на это число и проверяем.
# 
# Также в таблице users_df, вычисляем месяц регистрации (mnth_reg), и общий срок действия договора в месяцах, для каждого пользователя. Нам понадобятся эти значения для расчёта помесячных значений.

# In[10]:


users_df['churn_date'] = users_df['churn_date'].fillna('2018-12-31')
users_df['mnth_reg'] = pd.DatetimeIndex(users_df['reg_date']).month
users_df['mnth_chrn'] = pd.DatetimeIndex(users_df['churn_date']).month
users_df['mnth_ttl'] = users_df['mnth_chrn'] - users_df['mnth_reg'] + 1
users_df.info()


# In[11]:


sms_df['month'] = pd.DatetimeIndex(sms_df['message_date']).month
sms_df.head(10)


# In[12]:


calls_df['month'] = pd.DatetimeIndex(calls_df['call_date']).month


# In[13]:


internet_df['month'] = pd.DatetimeIndex(internet_df['session_date']).month


# Из столбца call_date выделяем месяц звонка, и для каждого звонка указываем, в каком месяце этот звонок был. Далее формируем итоговую таблицу, где в каждой строке указыавем отдельного абонента, и по каждому абоненту, формируем помесячную длительность разговоров, и общее количество разговоров. 
# 
# Аналогично делаем по количеству смс, и трафику.

# In[14]:


calls_df_by_user_month = calls_df.pivot_table(index='user_id', columns='month', values = 'duration', aggfunc='sum')
calls_count_df_by_user_month = calls_df.pivot_table(index='user_id', columns='month', values = 'duration', aggfunc='count')


# # Подсчёт количества сделанных звонков для каждого пользователя помесячно.
# 
# Теперь мы знаем количество сделанных звонков (соединений, длительностью одна минута и более), по каждому пользователю, за каждый месяц.
# Значение Nan не удаляем, и не заменяем, 

# In[15]:


calls_df_by_user_month.head()


# # Подсчёт количества сделанных звонков для каждого пользователя помесячно.

# Формируем таблицу, которая показывает количество отправленных сообщений, и траффик, по месяцам и по каждому абоненту. Проверяем, что получилось.

# In[16]:


calls_count_df_by_user_month.head()


# # Подсчёт количества отправленных сообщений каждым пользователем помесячно
# 
# Формируем таблицу, которая показывает количество смс, отправленных каждым пользователем помесячно. Смотрим что получилось.

# In[17]:


sms_df_by_user_month = sms_df.pivot_table(index='user_id', columns='month', values='id', aggfunc='count')
sms_df_by_user_month.head(5)


# # Подсчёт израсходованного интернет-траффика по каждому пользователю помесячно
# 
# Формируем таблицу, которая показывает количество израсходованного интернет траффика помесячно, в мегабайтах.

# In[18]:


internet_df_by_user_month = internet_df.pivot_table(index='user_id', columns='month', values = 'mb_used', aggfunc='sum')
internet_df_by_user_month.head(5)


# ### Готовим данные для формирования сводных таблиц по потреблённым услугам.
# 
# 
# Индексируем таблицу users_df, по полю user_id, чтобы потом объединять таблицу users_df с другими.

# In[19]:


users_df.set_index('user_id', inplace=True)


# ### Готовим данные для расчёта расходов на абонента
# 
# формируем таблицу, в которой будут рассчитываться доходы на абонента помесячно. Сначала выписываем, сколько минут тратил каждый пользователь в каждом месяце. Для удобства данные заносим в один столбец.

# In[20]:


calls_df_revenue = calls_df.pivot_table(index=['user_id', 'month'], aggfunc='sum')
calls_df_revenue.head(10)


# Присоединяем список пользоватлей, к помесячному списку звонков каждого пользователя.

# In[21]:


calls_df_revenue = calls_df_revenue.join(users_df)
calls_df_revenue.head()


# In[22]:


tariffs_df.set_index('tariff_name', inplace=True)
calls_df_revenue = calls_df_revenue.join(tariffs_df, on='tariff')
calls_df_revenue.head(10)


# ### Готовим данные для расчёта расходов на абонента
# 
# Считаем ежемесячный доход в рублях на каждого пользователя помесячно. Считается только стоимость звонков, которые не покрываются абонентской платой.

# In[23]:


def income_calls (duration, tariff, minutes_included, rub_per_minute):
    if tariff == 'ultra':
        if duration <= minutes_included:
            return 0
        else:
            return (duration - minutes_included) * rub_per_minute
    elif tariff == 'smart':
        if duration <= minutes_included:
            return 0
        else:
            return (duration - minutes_included) * rub_per_minute
    
    
    
calls_df_revenue['income_call'] = calls_df_revenue.apply(lambda x: income_calls(x['duration'], x['tariff'], x['minutes_included'], x['rub_per_minute']), axis = 1)


# Группируем расходы, не покрываемые абонентской платой помесячно

# In[24]:


calls_df_revenue_month = calls_df_revenue.pivot_table(index='user_id', columns = 'month', values = 'income_call')
calls_df_revenue_month = calls_df_revenue_month.fillna(0)
calls_df_revenue_month.head()


# ### <font color='red'>Комментарий от наставника 9
# Погоди, наши данные итак уже были агрегированы по месяцам (они же есть в индексе). Зачем тут снова вызывать pivot_table и как-бы вытаскивать месяц из индекса в колонки?
#     
# Ещё такой момент, никто не говорил, что мы должны считать для каждого пользователя сколько денег он потратил за всё время. Нас интересуют только его траты в месяц. И дальше мы можем считать средие траты сразу по всем людям с тарифом ultra и по всем людям с тарифом smart.
# 
# Ну и то же самое ниже.
# 
# Опять же, было бы сильно проще сразу всё собрать в одну таблицу (и звонки, и sms, и трафик). И работать с ними однотипно.
# 
# Но если не получится, то не переживай, я так и так это покажу на следующей консультации.
# 
# -----------


# Считаем итог за весь период по каждому пользователю. Для хранения итога создаём отдельную таблицу.

# In[25]:


calls_df_revenue_month['ttl_incm_clls'] = calls_df_revenue_month[[1,2,3,4,5,6,7,8,9,10,11,12]].sum(axis=1)
calls_df_revenue_total = calls_df_revenue_month['ttl_incm_clls']


# Формируем таблицу в которой считаем количество отправленных смс по каждому пользователю помесячно.

# In[26]:


sms_revenue = sms_df.pivot_table(index=['user_id', 'month'], values='id', aggfunc='count')
sms_revenue.head(10)


# Присоединяем таблицу к списку пользователей. Смотрим что получилось.

# In[27]:


sms_revenue = sms_revenue.join(users_df)
sms_revenue.head()


# Считаем доходы от отправленных смс. В доходы включаются только смс, которые не включены в тарифный план.

# In[28]:


sms_revenue = sms_revenue.join(tariffs_df, on='tariff')
sms_revenue.head(10)


# In[29]:


def income_sms (id_sms, tariff, messages_included, rub_per_message):
    if tariff == 'ultra':
        if id_sms <= messages_included:
            return 0
        else:
            return (id_sms - messages_included) * rub_per_message
    elif tariff == 'smart':
        if id_sms <= messages_included:
            return 0
        else:
            return (id_sms - messages_included) * rub_per_message
    
    
    
sms_revenue['income_sms'] = sms_revenue.apply(lambda x: income_sms(x['id'], x['tariff'], x['messages_included'], x['rub_per_message']), axis = 1)


# Группируем доходы от смс, не вошедшие в тарифные планы, помесячно.

# In[30]:


sms_revenue_month = sms_revenue.pivot_table(index='user_id', columns='month', values='income_sms')
sms_revenue_month = sms_revenue_month.fillna(0)
sms_revenue_month.head()


# Считаем итоговый доход от отправленных смс, не покрытых тарифным планом, по каждому пользователю.

# In[31]:


sms_revenue_month['ttl_incm_sms'] = sms_revenue_month[[1,2,3,4,5,6,7,8,9,10,11,12]].sum(axis=1)
sms_revenue_total = sms_revenue_month['ttl_incm_sms']


# Формируем таблицу, в которой считается израсходованный трафик по каждому пользователю помесячно

# In[32]:


internet_df_revenue = internet_df.pivot_table(index=['user_id', 'month'], values='mb_used', aggfunc='sum')
internet_df_revenue.head()


# Просоединяем таблицу, к общему списку пользователей.

# In[33]:


internet_df_revenue = internet_df_revenue.join(users_df)


# Считаем доходы от интернет-траффика, сверх предусмотренных тарифными планами, по каждому пользователю. Присоединеям к таблице условия тарифов. Смотрим что получилось.

# In[34]:


internet_df_revenue = internet_df_revenue.join(tariffs_df, on='tariff')
internet_df_revenue.head(10)


# In[35]:


def income_mb1 (mb_used, tariff, mg_per_month_included, rub_per_gb):
    if tariff == 'ultra':
        if mb_used <= mg_per_month_included:
            return 0
        else:
            gb = math.ceil((mb_used - mg_per_month_included) * 0.001)
            return gb * rub_per_gb
    elif tariff == 'smart':
        if mb_used <= mg_per_month_included:
            return 0
        else:
            gb = math.ceil((mb_used - mg_per_month_included) * 0.001)
            return gb * rub_per_gb
    
    
    
internet_df_revenue['income_mb'] = internet_df_revenue.apply(lambda x: income_mb1(x['mb_used'], x['tariff'], x['mg_per_month_included'], x['rub_per_gb']), axis = 1)


# ### <font color ='red'>Комментарий от наставника 10 <span style="color:green;font-size:200%">&#10003;</span>
# Давай внимательнее читать условия. У нас свех лимита интернет выдаётся пачками по 1Гб. Давай учтём это и будем округлять вверг до Гб перед умножением на цену.

# Группируем доходы от интернет-траффика, сверх предусмотренного тарифными планами по месяцам, по каждому пользователю. Смотрим что получилось.

# In[36]:


internet_df_revenue_month = internet_df_revenue.pivot_table(index='user_id', columns='month', values='income_mb')
internet_df_revenue_month = internet_df_revenue_month.fillna(0)
internet_df_revenue_month.head()


# Считаем общий доход за использование интернет-траффика, не включённый в тарифы. Итог включаем в отдельный столбец. Для хранения итога создаём отдельную таблицу.

# In[37]:


internet_df_revenue_month['ttl_incm_mb'] = internet_df_revenue_month[[1,2,3,4,5,6,7,8,9,10,11,12]].sum(axis=1)
internet_revenue_total = internet_df_revenue_month['ttl_incm_mb']


# Создаём таблицу, где считаются общие доходы по каждому пользователю.

# In[38]:


main_income = users_df.join(calls_df_revenue_total)


# In[39]:


main_income = main_income.join(sms_revenue_total)


# In[40]:


main_income = main_income.join(internet_revenue_total)


# In[41]:


main_income = main_income.fillna(0)
main_income.head()


# Считаем общий доход от каждого пользователя, и среднемесячную выручку каждого пользователя.

# In[42]:


tariffs_df_light = tariffs_df['rub_monthly_fee']
tariffs_df_light


# In[43]:


main_income = main_income.join(tariffs_df_light, on='tariff')


# In[44]:


def income_total (tariff, ttl_incm_clls, ttl_incm_sms, ttl_incm_mb, mnth_ttl, rub_monthly_fee):
    if tariff == 'smart':
        return mnth_ttl * rub_monthly_fee + ttl_incm_clls + ttl_incm_sms + ttl_incm_mb
    elif tariff == 'ultra':
        return mnth_ttl * rub_monthly_fee + ttl_incm_clls + ttl_incm_sms + ttl_incm_mb


main_income['incm_ttl'] = main_income.apply(lambda x: income_total(x['tariff'], x['ttl_incm_clls'], x['ttl_incm_sms'], x['ttl_incm_mb'], x['mnth_ttl'], x['rub_monthly_fee']), axis = 1)
main_income['incm_by_month'] = main_income['incm_ttl'] / main_income['mnth_ttl']
main_income.head()


# ### Поиск и удаление выбросов
# 
# Поскольку нас интересуют доходы от абонентов, то и выбросы мы смотрим по показателю - среднемесячный доход с абонента. Выбросов снизу быть не может, поскольку имеется минимальная оплата по тарифу. Ищем выбросы сверху. Из анализа графика видно, что выбросы сверху имеются. 5 абонентов имеют среднемесячную нагрузку в 3150 рублей и выше.
# 
# Из выборки в 500 абонентов, это 6 человек, или 1%. Оставляем их, поскольку 1% абонентов вполне может иметь расходы на связь вдвое выше абонентской платы.

# In[45]:


main_income['incm_by_month'].hist()
main_income_smart = main_income.query('tariff == "smart"')
main_income_smart['incm_by_month'].hist()


# In[46]:


main_income['incm_by_month'].hist(range=(3100, 4500))


# ### Общее поведение клиентов на тарифах smart и ultra
# 
# Поведение большей части клиентов, за весь наблюдаемый период достаточно рационально. На графике видно, что большинство клиентов пользуются тарифами smart и ultra, при этом укладываясь в указанные тарифы. При этом, часть клиентов не укладывается в лимиты, и превышает как лимиты по тарифы smart, так и лимиты по тарифу ultrа, а около 40 из 500 клиентов выбрали невыгодный для себя тариф smart, вместо тарифа ultra.
# 
# **Перевод клиентов на тариф ultra, позволит сдвинуть график доходности "вправо". При этом, за счёт клиентов, ведущие себя нерационально, этот перевод не резко усиливает доходность**
# 
# Распределение поведения клиентов по месяцам, будет исследованно ниже.

# ### Описание поведения клиентов
# 
# Пишем функцию, которая считает среднее значение, дисперсию и стандартное отклонение, а также распределение данных по квантилям (функция describe)

# In[47]:


def describe_func (df_month, tariff1, hd_name):
    df_month_tariff = df_month[(df_month['tariff'] == tariff1)]
    mean1 = df_month_tariff[hd_name].mean()
    std1 = np.std(df_month_tariff[hd_name])
    low_limit = mean1 - 3 * std1
    high_limit = mean1 + 3 * std1
    if low_limit <= df_month_tariff[hd_name].min():
        low_limit = df_month_tariff[hd_name].min()
    if high_limit >= df_month_tariff[hd_name].max():
        high_limit = df_month_tariff[hd_name].max()
    print("Среднее значение по тарифу", tariff1, mean1)
    print("Дисперсия по тарифу", tariff1, np.var(df_month_tariff[hd_name]))
    print("Станадртное отклонение по тарифу", tariff1, std1)
    print("Тариф", tariff1, "Максимум", df_month_tariff[hd_name].max(),"Минимум:", df_month_tariff[hd_name].min())
    print("Тариф", tariff1, "Границы нормы от", low_limit, "до:", high_limit)
    print(df_month_tariff[hd_name].hist())
    return tariff1, df_month_tariff[hd_name].describe()



# ### Описание поведения клиентов
# 
# Смотрим на распределения по количеству минут разговора у клиентов разных тарифов

# In[48]:


describe_func(calls_df_revenue, 'smart', 'duration')


# ### Вывод по минутам разговора, которые тратят пользователи тарифа smart
# 
# Пользователи тарифа smart, часто выходят за пределы, определённые тарифом, (25% значений превышает 546 минут) при этом, для большинства пользователей, количества минут в месяц хватает (медиана месячного разговора составляет 423 минуты).
# 
# Разница между средним и медианным значением минимальна, (419 и 423 минуты), при этом минимальные и максимальные значения крайне велики, и значение нормы, рассчитанное как +- три стандартных отклонения от среднего, также очень широки (от 2 до 986 минут).

# In[49]:


describe_func(calls_df_revenue, 'ultra', 'duration')


# ### Вывод по минутам разговора, которые тратят пользователи тарифа ultra
# 
# Пользователи тарифа ultra, говорят чуть больше чем пользователи тарифа smart. До определённого тарифом предела в 3000 минут, ни один абонент не подошёл даже близко.
# 
# Средние и медианные значения также досточно близки (548 и 529 минут), и вполне соответствуют тарифу smart. Границы нормы также очень широки от одной минуты до 1464 минут.

# In[50]:


describe_func(sms_revenue, 'smart', 'id')


# ### Вывод по количеству смс, которые тратят пользователи тарифа smart
# 
# Большая часть пользователей ежемесячно укладывается в лимит, определённый тарифом smart. При этом, часть пользователей или почти не использует смс, или пишет очень много смс, о чём говорят границы нормы (от 1 до 119 смс).
# 
# Среднее и медианное значение отличаются не сильно (39 и 34 смс).

# In[51]:


describe_func(sms_revenue, 'ultra', 'id')


# ### Вывод по количеству смс, которые тратят пользователи тарифа ultra
# 
# Пользователи тарифа ultra, также близко не используют необходимого лимита по услугам.
# Максимальное количество сообщений - 224. Границы нормы - 199.
# При этом, как и для минут разговора, среднее и медианное значение (61 и 51), больше соответствуют тарифу smart.

# In[52]:


describe_func(internet_df_revenue, 'smart', 'mb_used')


# ### Вывод по траффику, которые тратят пользователи тарифа smart
# 
# Пользователи, в осносном несколько превышают лимиты интернет-траффика, установленные тарифом. Как в потреблении минут и смс, имеются люди не пользующиеся интернетом, так и люди тратящие более 30 ГБ траффика.
# 
# Среднее и медианное значение одинаковы (16244 и 16533 мегабайт). При этом 50% пользователей используют от 12677 до 20068 мегабайт трафика в месяц. Границы нормы (среднее значение +- три отклонения) составляют от 202 до 33820 мегабайт.
# 
# Поведение большинства абонентов в принципе рационально. При этом, часть абонентов не переходя на более дорогой (и выгодный для них) тариф ultra, позволяет генерировать высокую прибыль.

# In[53]:


describe_func(internet_df_revenue, 'ultra', 'mb_used')


# ### Вывод по траффику, которые тратят пользователи тарифа ultra
# 
# Если, пользователи тарифа smart обычно превышают лимиты, то пользователи тарифа ultra лимиты, в основном не превышают. При этом, достаточно серьёзная часть пользователей тратит меньше 15 ГБ интернета в месяц, и для них тариф smart был бы более выгодным.
# 
# Разницы между средним и медианным значениями также нет (19707 и 19428 мегабайта). 50% пользователей используют от 12074 до 26936 мегабайт траффика. Границы нормы составляют от 366 до 49503 мегабайта траффика в месяц.

# # Общий вывод по поведению клиентов операторов
# 
# Тариф ultra, более выгоден оператору, поскольку абоненты платят почти в четыре раза больше, а потребляют услуг не принципиально больше чем абоненты тарифа smart. Больше услуг потребляется только в части мобильного интернета.
# Лимиты установленные тарифом ultra по мобильному интернету могут быть сдвинуты до 40 ГБ, этого хватит почти всем пользователям. Лимиты по звонкам и смс вполне достаточны.
# Лимиты, установленные тарифом smart, являются достаточными для большинства абонентов по минутам разговоров и смс. Для интернет-траффика лимиты являются недостаточными. Чтобы абоненты укладывались в лимит, нужно предоставить 23 ГБ интернет-траффика.
# 
# 
# Часть абонентов использует очень незначительное количество минут/смс/трафика.


# Генеральными совокупностями являются - все (а не только те, что представлены в исследуемых данных) пользователи тарифов smart и ultra, соответственно.
# Соответственно, нулевая гипотеза звучит так: 
# 
# Среднемесячная выручка всех абонентов тарифа smart, равна среднемесячной выручке всех абонентов тарифа ultra.
# А альтернативная гипотеза так:
# 
# Среднемесячная выручка всех абонентов тарифа smart, отличается от среднемесячной выручки абонентов тарифа ultra.
# 
# Для проверки используется метод - scipy.stats.ttest_ind(). Для проверки сравним выборки по тарифу smart и тарифу ultra. Поскольку выборки отбирались из схождих по параметрам совокупностей (случайный набор абонентов), то дисперсию выборки считаем равной.
# 
# Пороговое значение, устанавливаем в размере 0.05.

# In[54]:


main_income_ultra = main_income.query('tariff == "ultra"')
mean_ultra = main_income_ultra['incm_by_month']
main_income_smart = main_income.query('tariff == "smart"')
mean_smart = main_income_smart['incm_by_month']


# In[55]:


results = st.ttest_ind(
    mean_ultra,
    mean_smart
)
print(results.pvalue)


# Поскольку значение pvalue, для выборок по тарифам smart и ultra является крайне низкой, то **гипотеза о том, что выручка пользователей тарифа smart равна выручке пользователей тарифа ultra опровергнута.**

# Проверяем гипотезу по выручке пользователей в Москве и других регионах.
# Генеральными совокупностями являются - все (а не только те, что представлены в исследуемых данных) абоненты из города Москва и абоненты из других регионгов, соответственно. Соответственно, нулевая гипотеза звучит так:
# 
# Среднемесячная выручка абонентов из Москвы равна среднемесячной выручке пользоватлей из других регионов.
# 
# А альтернативная гипотеза так:
# 
# Среднемесячная выручка абонентов из Москвы отличается от среднемесячной выручки пользователей из других регионов.
# 
# Для проверки используется метод - scipy.stats.ttest_ind(). Для проверки сравним выборки по абонентам из Москвы и иных регионов. Поскольку выборки отбирались из схождих по параметрам совокупностей (случайный набор абонентов), то дисперсию выборки считаем равной.
# 
# Пороговое значение, устанавливаем в размере 0.05.

# ### Проверяем гипотезу по выручке пользователей Москвы и иных регионов <span style="color:green;font-size:200%">&#10003;</span>
#  
# Считаем среднюю выручку пользователей из Москвы. Затем берём список пользователей не из Москвы, и считаем вероятность того, что выручка пользователей из Москвы будет равна выручке пользователей из других регионов. Проверяем методом - st.ttest_1samp.

# In[56]:


main_income_moscow = main_income.query('city == "Москва"')
mean_moscow = main_income_moscow['incm_by_month']
main_income_regions = main_income.query('city != "Москва"')
mean_regions = main_income_regions['incm_by_month']


# In[57]:


results = st.ttest_ind(
    mean_moscow,
    mean_regions
)
print(results.pvalue)


# Поскольку значение pvalue, для выборок по абонентам, живущим в Москве и иных регионах является крайне достаточно высоким (0.37), то **гипотеза о том, что выручка пользователей из Москвы равна выручке пользователей из регионов не опровергнута.**


# # Общий вывод: <span style="color:green;font-size:200%">&#10003;</span>
# 
# После анализа установлено, что оператору более выгоден тариф ultra, но с оговорками:
# - часть пользователей (около 10%) действуют нерационально, применяя невыгодный для себя (и выгодный для оператора), тариф "смарт".
# - части пользователей тариф ultra заведомо не подходит.
# 
# Поведение большей части пользователей рационально, они не выходят за установленные тарифами лимиты. 
# 
# Пользователям хватает предоставленных минут разговора и смс, и не хватает предоставленного в рамках тарифных планов траффика. Соответственно, если нужно повышать лояльность, нужно повышать лимиты траффика.
# 
# Значительное количество пользователей даже близко не используют предоставленные объёмы траффика, минут и смс.
# 
# Выручка пользователей тарифа смарт, меньше чем у пользователей тарифа ультра. Выручка пользователей из Москвы, примерно совпадает с выручкой пользователей регионов.
