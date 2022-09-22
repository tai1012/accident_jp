# import文
import pandas as pd


# データ取得
honhyo = pd.read_csv('honhyo_2021.csv', encoding="shift-jis")
print(honhyo.head())
hojuhyo = pd.read_csv('hojuhyo_2021.csv', encoding="shift-jis")
kosokuhyo = pd.read_csv('kosokuhyo_2021.csv', encoding="shift-jis")