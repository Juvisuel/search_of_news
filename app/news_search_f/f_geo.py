# -*- coding: utf-8 -*-

import pandas as pd
df = pd.read_csv('F:/learn_neuro/search_of_news/app/work_dicts/city_corrected.csv')


def find_city(list_of_inputs):
    print(list_of_inputs)
    city_name, district, rank = list_of_inputs[0], list_of_inputs[1], list_of_inputs[2]
    """
    функция поиска населенных пунктов по запросу
    принимает - 1 - название населенного пункта (string) или 0(int) если ничего
                2 - регион поиска (['ФО','г', 'обл', 'АО', 'Респ', 'край', 'Аобл'] или "страна")(string)
                3 - ранг населенных пунктов (0 - свыше 1 000 000, 1 - свыше 100 000, 2 - свыше 10 000, 3 - все)(int)

                если 1 - Россия и 2 - страна и 3 - любое число
                выдает - список = [Россия, федеральный, всероссийский, государственный, российский ]

                если 1 - населенный пункт и 2 - населенный пункт (любой) и 3 - любое число
                выдает список = [название этого пункта]

                если 1 - ничего(city_name=0) и 2 - страна и 3 - любое число
                выдает список = [Россия, федеральный, всероссийский, государственный, российский ]

                если 1 - населенный пункт и 2 - регион, то смотри 3 - ранг границы крупности
                и выдает список = [названия всех пунктов в регионе этого населенного пункта равных
                и выше ранга указанной крупности]
    """
    # задаем границы количества населения
    ranks = [1000000, 100000, 10000, 0]

    # задаем условия
    res = []
    # первое условие
    if city_name.lower() == 'россия' and district.lower() == 'страна':

        res = ['Россия', 'федеральный', 'всероссийский', 'государственный', 'российский']
        return res

    # третье условие
    if city_name == 0 and district.lower() == 'страна':
        res = ['Россия', 'федеральный', 'всероссийский', 'государственный', 'российский']
        return res

    # четвертое условие
    if city_name in df.city.values and district in df.federal_district_type.values:
        temp_name_series = df.loc[df['city'] == city_name, 'federal_district']
        temp_name = temp_name_series.values[0]
        df_res = df.loc[((df.federal_district == temp_name) & (df.population >= ranks[rank]))]
        res = df_res.city.tolist()
        return res

    if city_name in df.city.values and district in df.region_type.values:
        temp_name_series = df.loc[df['city'] == city_name, 'region']
        temp_name = temp_name_series.values[0]
        df_res = df.loc[((df.region == temp_name) & (df.population >= ranks[rank]))]
        res = df_res.city.tolist()
        return res

    # второе условие
    if city_name:
        res.append(city_name)
        return res

# list_of_inputs = ["Казань", "Респ",3]
# print(find_city(list_of_inputs))