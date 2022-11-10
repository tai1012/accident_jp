# import文
import pandas as pd


# データ取得
honhyo_2021 = pd.read_csv('./00_data/01_honhyo/honhyo_2021.csv', encoding="shift-jis")
honhyo_2020 = pd.read_csv('./00_data/01_honhyo/honhyo_2020.csv', encoding="shift-jis")
honhyo_2019 = pd.read_csv('./00_data/01_honhyo/honhyo_2019.csv', encoding="shift-jis")
hojuhyo_2021 = pd.read_csv('./00_data/02_hojuhyo/hojuhyo_2021.csv', encoding="shift-jis")
hojuhyo_2020 = pd.read_csv('./00_data/02_hojuhyo//hojuhyo_2020.csv', encoding="shift-jis")
hojuhyo_2019 = pd.read_csv('./00_data/02_hojuhyo/hojuhyo_2019.csv', encoding="shift-jis")
kosokuhyo_2021 = pd.read_csv('./00_data/03_kosokuhyo/kosokuhyo_2021.csv', encoding="shift-jis")
kosokuhyo_2020 = pd.read_csv('./00_data/03_kosokuhyo/kosokuhyo_2020.csv', encoding="shift-jis")
kosokuhyo_2019 = pd.read_csv('./00_data/03_kosokuhyo/kosokuhyo_2019.csv', encoding="shift-jis")

'''
to do 
一旦それぞれ縦に全部UNION
＊　もしかしたら被っている事故が書いてある可能性(2021-2015年までデータ自体はある。。。)
'''

honhyo = pd.concat([honhyo_2021,honhyo_2020,honhyo_2019],axis=0)
print(2021, honhyo_2021["発生日時　　年"].value_counts())
print(2020, honhyo_2020["発生日時　　年"].value_counts())
print(2019, honhyo_2019["発生日時　　年"].value_counts())
print('union', honhyo["発生日時　　年"].value_counts())
print('***'*10)
print(2021, honhyo_2021.shape)
print(2020, honhyo_2020.shape)
print(2019, honhyo_2019.shape)
print('union', honhyo.shape)
hojuhyo = pd.concat([hojuhyo_2021,hojuhyo_2020,hojuhyo_2019],axis=0)
kosokuhyo = pd.concat([kosokuhyo_2021,kosokuhyo_2020,kosokuhyo_2019],axis=0)

print(honhyo.columns)


# print(honhyo['都道府県コード'].unique())
# print(hojuhyo['都道府県コード'].unique())
# print(kosokuhyo['都道府県コード'].unique())
# print(honhyo.columns)
# print(hojuhyo.columns)
# print(kosokuhyo.columns)
# print(honhyo.shape, hojuhyo.shape, kosokuhyo.shape)
# data = pd.merge(honhyo, hojuhyo, on=['都道府県コード','警察署等コード','本票番号'],how='outer')
# data = pd.merge(data, kosokuhyo, on=['都道府県コード','警察署等コード','本票番号'],how='outer')
# print(data.shape)
# print(data)
# print(data["発生日時　　年"].value_counts())
# print(honhyo["資料区分"].unique())
# print(hojuhyo)
# print(kosokuhyo)

"""
Merge→Concat
data_2021 = pd.merge(honhyo_2021,hojuhyo_2021, on=['都道府県コード','警察署等コード','本票番号'],how='outer')
data_2021 = pd.merge(data_2021,kosokuhyo_2021, on=['都道府県コード','警察署等コード','本票番号'],how='outer')
print(data_2021.shape)
print(data_2021.columns)
print(data_2021)
"""
"""
TO DO

使いそうな特徴量
['都道府県コード', '事故内容']

都道府県コード 10 - 97
事故内容 1:死亡 2:負傷
死者数？　何人死ぬか？
負傷者数？　何人怪我するか？


回帰(量)　何ができるか考える。。。　スピード、規則性がもしあるなら時間的な予測、
分類(質)　気温、季節とか路面状況で、こういう時事故起こるよな？　死者ありかなしか分類で特徴量判断、
教師なし　グループ分けするのもいいかもね
可視化　ダッシュボード？　地図上に描くのはやりたい
"""
