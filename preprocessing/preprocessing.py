# import文
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# import seaborn as sns 
from decimal import Decimal, ROUND_HALF_UP


from pandas.io import gbq
import geopandas
from shapely.geometry import Point, LineString, Polygon
import geopatra
import folium


def dms2deg(dms):    
    # 度分秒から度への変換
    if len(str(dms)) == 10:        
        hour = int(str(dms)[0:3])
        minute = int(str(dms)[3:5])
        seconds = int(str(dms)[5:7])
    elif len(str(dms)) == 9:
        hour = int(str(dms)[0:2])
        minute = int(str(dms)[2:4])
        seconds = int(str(dms)[4:6])
    deg = Decimal(str(hour + (minute / 60) + (seconds / 3600))).quantize(Decimal('0.0001'), rounding=ROUND_HALF_UP)
    return str(deg)


# データ取得
honhyo_2021 = pd.read_csv('./00_data/01_honhyo/honhyo_2021.csv', encoding="shift-jis")
honhyo_2020 = pd.read_csv('./00_data/01_honhyo/honhyo_2020.csv', encoding="shift-jis")
honhyo_2019 = pd.read_csv('./00_data/01_honhyo/honhyo_2019.csv', encoding="shift-jis")

'''
to do 
一旦それぞれ縦に全部UNION
＊　もしかしたら被っている事故が書いてある可能性(2021-2015年までデータ自体はある。。。)
'''

honhyo = pd.concat([honhyo_2021,honhyo_2020,honhyo_2019],axis=0)
# print(2021, honhyo_2021["発生日時　　年"].value_counts())
# print(2020, honhyo_2020["発生日時　　年"].value_counts())
# print(2019, honhyo_2019["発生日時　　年"].value_counts())
# print('union', honhyo["発生日時　　年"].value_counts())
# print('***'*10)
# print(2021, honhyo_2021.shape)
# print(2020, honhyo_2020.shape)
# print(2019, honhyo_2019.shape)
# print('union', honhyo.shape)
honhyo = honhyo.drop(['資料区分'],axis=1)
# print(honhyo.columns)

data = honhyo[honhyo['発生日時　　年'] >= 2019]
# print(data["発生日時　　年"].value_counts())
# data = data.drop(['警察署等コード','本票番号','車両の損壊程度（当事者A）','車両の損壊程度（当事者B）','エアバッグの装備（当事者A）','エアバッグの装備（当事者B）','サイドエアバッグの装備（当事者A）','サイドエアバッグの装備（当事者B）','人身損傷程度（当事者A）','人身損傷程度（当事者B）'],axis=1)
# print(data.columns)
## 東京のみ
data = data.query('都道府県コード==30')


# 緯度経度を度分秒から度に変更
data = data[data['地点　緯度（北緯）'] > 100000]
data = data[data["地点　経度（東経）"] > 100000].reset_index(drop=True)

data["latitude"] = list(map(lambda id:dms2deg(data["地点\u3000緯度（北緯）"][id]),
                            range(data.index.size)))
data["longitude"] = list(map(lambda id:dms2deg(data["地点\u3000経度（東経）"][id]),
                            range(data.index.size)))
data["latitude"] = data["latitude"].astype(float)
data["longitude"] = data["longitude"].astype(float)
data = data.drop(['地点　緯度（北緯）','地点　経度（東経）'],axis=1)

# print(data.describe())

# 発生日時を１列に
data['datetime'] = pd.to_datetime({'year':data['発生日時　　年'],
                                'month':data['発生日時　　月'],
                                'day':data['発生日時　　日'],
                                'hour':data['発生日時　　時'],
                                'minute':data['発生日時　　分']
                                })
data = data.sort_values('datetime').reset_index()
data = data.drop(['index'],axis=1)
print(data)
# print(data.columns)
# print(data)
# print(data[data['発生日時　　年'] == 2020])



"""
TO DO
一旦BigQuery
やってみたい
①緯度経度の情報からその場所の地点を取得（東京の交通事故多い「23区別とかで」）
→その地点の写真を１０件とかとてってきて表示とか？BI？
時間軸の値を入れて予測してそこをアラート的に色付け？みたいなイメージ
二次元のマップじゃないと可視化はできなさそう
ストリートビューを持ってくるのはできる

東京の地図に予測した点をplotでいいかな。。。？

道路形状が特徴量として割と使われている


使いそうな特徴量
['都道府県コード', '事故内容',...etc]

都道府県コード 10 - 97
事故内容 1:死亡 2:負傷
死者数？　何人死ぬか？
負傷者数？　何人怪我するか？


回帰(量)　何ができるか考える。。。　スピード、規則性がもしあるなら時間的な予測、
分類(質)　気温、季節とか路面状況で、こういう時事故起こるよな？　死者ありかなしか分類で特徴量判断、
教師なし　グループ分けするのもいいかもね
可視化　ダッシュボード？　地図上に描くのはやりたい

②　Gisを使ってみたい

東京のみ
82943件のデータ
内2020年(25556)

不要な特徴量　：　'都道府県コード', '警察署等コード', '本票番号', 'エアバッグの装備（当事者A）',
       'エアバッグの装備（当事者B）', 'サイドエアバッグの装備（当事者A）', 'サイドエアバッグの装備（当事者B）',
       '発生日時　　日', '発生日時　　時', '発生日時　　分', '年齢（当事者A）', '年齢（当事者B）',

       車の性能は除く
       場所は経度緯度の情報で
       日時
       予測ではなく分類系

特注量は機械学習からやる

"""
## 目視で確認した車がぶつかりやすい場所とは関係なさそうな特徴の削除
data = data.drop(['都道府県コード', '地点コード', '市区町村コード', '警察署等コード', '本票番号', 'エアバッグの装備（当事者A）',
       'エアバッグの装備（当事者B）', 'サイドエアバッグの装備（当事者A）', 'サイドエアバッグの装備（当事者B）',
       '発生日時　　日', '発生日時　　時', '発生日時　　分', '年齢（当事者A）', '年齢（当事者B）',], axis=1)

## コードの説明変数を加える
print(data.columns)

# 事故内容
data['accident_type'] = np.where(data['事故内容']==1, '死亡',
                                np.where(data['事故内容']==2, '負傷', None))
data = data.drop('事故内容', axis=1)

# 路線コード
# print(data.value_counts('路線コード'))
data["road"] = list(map(lambda text:text[0:4], data["路線コード"].astype(str)))
data["road"] = data.road.astype(int)
data["road_1"] = list(map(lambda text:text[-1], data["路線コード"].astype(str)))
data["road_1"] = data.road_1.astype(int)

data['route'] = np.where(data.road<1000, '一般国道',data.road)
data['route'] = np.where((data.road>=1000) & (data.road<1500), '主要地方道－都道府県道', data.road)
data['route'] = np.where((data.road>=1500) & (data.road<2000), '主要地方道－市道', data.road)
data['route'] = np.where((data.road>=2000) & (data.road<3000), '一般都道府県道', data.road)
data['route'] = np.where((data.road>=3000) & (data.road<4000), '一般市町村道', data.road)
data['route'] = np.where((data.road>=4000) & (data.road<5000), '高速自動車道', data.road)
data['route'] = np.where((data.road>=5000) & (data.road<5500), '自動車専用道－指定"', data.road)
data['route'] = np.where((data.road>=5500) & (data.road<6000), '自動車専用道－その他', data.road)
data['route'] = np.where((data.road>=6000) & (data.road<7000), '道路運送法上の道路', data.road)
data['route'] = np.where((data.road>=7000) & (data.road<8000), '農（免）道', data.road)
data['route'] = np.where((data.road>=8000) & (data.road<8500), '林道', data.road)
data['route'] = np.where((data.road>=8500) & (data.road<9000), '港湾道', data.road)
data['route'] = np.where((data.road>=9000) & (data.road<9500), '私道', data.road)
data['route'] = np.where(data.road==9500, 'その他', data.road)
data['route'] = np.where(data.road==9900, '一般の交通の用に供するその他の道路', data.road)

data['bypass_route'] = np.where(data.road_1>=1, 'バイパス区間', 
                                np.where(data.road_1==0,'現道区間又は包括路線', None))
data = data.drop(['路線コード', 'road', 'road_1'] ,axis=1)


# 上下線
print(data['上下線'].value_counts())
data['road_updown'] = np.where(data['上下線']==1, '上',
                            np.where(data['上下線']==2, '下',
                            np.where(data['上下線']==0, '対象外', None)))                                                        
data = data.drop('上下線', axis=1)

# #　昼夜
data['day_night'] = np.where(data['昼夜']==11, '昼-明',
                        np.where(data['昼夜']==12, '昼ー昼',
                        np.where(data['昼夜']==13, '昼ー暮',
                        np.where(data['昼夜']==21, '夜ー暮',
                        np.where(data['昼夜']==22, '夜ー夜',
                        np.where(data['昼夜']==23, '昼ー明', None))))))
data = data.drop('昼夜', axis=1)

# # 名前の変更
data['num_death'] = data['死者数']
data['num_injure'] = data['負傷者数']
data['year'] = data['発生日時　　年']
data['month'] = data['発生日時　　月']

data = data.drop(['死者数', '負傷者数', '発生日時　　年', '発生日時　　月'], axis=1)

# # 天候

data['weather'] = np.where(data['天候']==1, '晴',
                        np.where(data['天候']==2, '曇',
                        np.where(data['天候']==3, '雨',
                        np.where(data['天候']==4, '霧',
                        np.where(data['天候']==5, '雪', None)))))

data = data.drop('天候', axis=1)

# # 地形
data['terrain'] = np.where(data['地形']==1, '市街地－人口集中',
                            np.where(data['地形']==2, '市街地－その他',
                            np.where(data['地形']==3, '非市街地', None)))

data = data.drop('地形', axis=1)                                                        

# # 路面状態
data['route_condition'] = np.where(data['路面状態']==1, '舗装－乾燥',
                                np.where(data['路面状態']==2, '舗装－湿潤',
                                np.where(data['路面状態']==3, '舗装ー凍結',
                                np.where(data['路面状態']==4, '舗装ー積雪',
                                np.where(data['路面状態']==5, '非舗装', None)))))

data = data.drop('路面状態', axis=1) 

# # 道路形状
data['route_shaoe'] = np.where(data['道路形状']==31, '交差点－環状交差点',
                                np.where(data['道路形状']==1,'交差点－その他',
                                np.where(data['道路形状']==37, '交差点付近－環状交差点付近',
                                np.where(data['道路形状']==7, '交差点付近－その他',
                                np.where(data['道路形状']==11,'単路－トンネル',
                                np.where(data['道路形状']==12,'単路－橋',
                                np.where(data['道路形状']==13,'単路－カーブ・屈折',
                                np.where(data['道路形状']==14,'単路－その他',
                                np.where(data['道路形状']==21,'踏切－第一種',
                                np.where(data['道路形状']==22,'踏切－第三種',
                                np.where(data['道路形状']==23,'踏切－第四種',
                                np.where(data['道路形状']==0,'一般交通の場所', None))))))))))))

data = data.drop('道路形状', axis=1)   

# # 環状交差点の直径
data['roundabout_diameter'] = np.where(data['環状交差点の直径']==1, '小（27ｍ未満）',
                                np.where(data['環状交差点の直径']==2, '中（27ｍ以上）',
                                np.where(data['環状交差点の直径']==3, '大（43ｍ以上）',
                                np.where(data['環状交差点の直径']==0, '環状交差点以外', None))))

# # 信号機
data['trafic_signals'] = np.where(data['信号機']==1, '点灯－３灯式',
                                np.where(data['信号機']==8, '点灯－歩車分式',
                                np.where(data['信号機']==2, '点灯－押ボタン式',
                                np.where(data['信号機']==3, '点滅－３灯式',
                                np.where(data['信号機']==4, '点滅－１灯式',
                                np.where(data['信号機']==5, '消灯',
                                np.where(data['信号機']==6, '故障',
                                np.where(data['信号機']==7, '施設なし', None))))))))

# # 一時停止規制　標識
data['pause_sign_type_a'] = np.where(data['一時停止規制　標識（当事者A）']==1, '標準－反射式',
                                np.where(data['一時停止規制　標識（当事者A）']==2,'標準－自発光式',
                                np.where(data['一時停止規制　標識（当事者A）']==3,'標準－内部照明式',
                                np.where(data['一時停止規制　標識（当事者A）']==4,'拡大－反射式',
                                np.where(data['一時停止規制　標識（当事者A）']==5,'拡大－自発光式',
                                np.where(data['一時停止規制　標識（当事者A）']==6,'拡大－内部照明式',
                                np.where(data['一時停止規制　標識（当事者A）']==7,'縮小',
                                np.where(data['一時停止規制　標識（当事者A）']==8,'その他',
                                np.where(data['一時停止規制　標識（当事者A）']==9,'規制なし',
                                np.where(data['一時停止規制　標識（当事者A）']==0,'対象外当事者',None))))))))))

data['pause_sign_type_b'] = np.where(data['一時停止規制　標識（当事者B）']==1, '標準－反射式',
                                np.where(data['一時停止規制　標識（当事者B）']==2,'標準－自発光式',
                                np.where(data['一時停止規制　標識（当事者B）']==3,'標準－内部照明式',
                                np.where(data['一時停止規制　標識（当事者B）']==4,'拡大－反射式',
                                np.where(data['一時停止規制　標識（当事者B）']==5,'拡大－自発光式',
                                np.where(data['一時停止規制　標識（当事者B）']==6,'拡大－内部照明式',
                                np.where(data['一時停止規制　標識（当事者B）']==7,'縮小',
                                np.where(data['一時停止規制　標識（当事者B）']==8,'その他',
                                np.where(data['一時停止規制　標識（当事者B）']==9,'規制なし',
                                np.where(data['一時停止規制　標識（当事者B）']==0,'対象外当事者',None))))))))))


# #  一時停止規制　表示
data['pause_display_type_a'] = np.where(data['一時停止規制　表示（当事者A）']==21,'表示あり',
                                    np.where(data['一時停止規制　表示（当事者A）']==22,'表示なし',
                                    np.where(data['一時停止規制　表示（当事者A）']==23,'その他',None)))

data['pause_display_type_b'] = np.where(data['一時停止規制　表示（当事者B）']==21,'表示あり',
                                    np.where(data['一時停止規制　表示（当事者B）']==22,'表示なし',
                                    np.where(data['一時停止規制　表示（当事者B）']==23,'その他',None)))                            


# # 車道幅員
data['road_width'] = np.where(data['車道幅員']==1,'単路－3.5m未満',
                                np.where(data['車道幅員']==2,'単路－3.5m以上',
                                np.where(data['車道幅員']==3,'単路－5.5m以上',
                                np.where(data['車道幅員']==4,'単路－9.0m以上',
                                np.where(data['車道幅員']==5,'単路－13.0m以上',
                                np.where(data['車道幅員']==6,'単路－19.5m以上',
                                np.where(data['車道幅員']==11,'交差点－小（5.5m未満）－小',
                                np.where(data['車道幅員']==14,'交差点－中（5.5m以上）－小',
                                np.where(data['車道幅員']==15,'交差点－中（5.5m以上）－中',
                                np.where(data['車道幅員']==17,'交差点－大（13.0ｍ以上）－小',
                                np.where(data['車道幅員']==18,'交差点－大（13.0ｍ以上）－中',
                                np.where(data['車道幅員']==19,'交差点－大（13.0ｍ以上）－大',                
                                np.where(data['車道幅員']==0,'一般交通の場所',None)))))))))))))

# # 道路線形
data['route_alignment'] = np.where(data['道路線形']==1,'カーブ・屈折－右－上り',
                                np.where(data['道路線形']==2,'カーブ・屈折－右－下り',
                                np.where(data['道路線形']==3,'カーブ・屈折－右－平坦',
                                np.where(data['道路線形']==4,'カーブ・屈折－左－上り',
                                np.where(data['道路線形']==5,'カーブ・屈折－左－下り',
                                np.where(data['道路線形']==6,'カーブ・屈折－左－平坦',
                                np.where(data['道路線形']==7,'直線－上り',
                                np.where(data['道路線形']==8,'直線－下り',
                                np.where(data['道路線形']==9,'直線－平坦',
                                np.where(data['道路線形']==0,'一般交通の場所',None))))))))))
# # 衝突地点
data['clush_pont'] = np.where(data['衝突地点']==1,'単路（交差点付近を含む）',
                      np.where(data['衝突地点']==30,'交差点内',
                      np.where(data['衝突地点']==20,'その他',None)))

# # ゾーン規制
data['zone_control'] = np.where(data['ゾーン規制']==1, 'ゾーン30',
                            np.where(data['ゾーン規制']==70, '規制なし',None))

# # 中央分離帯
data['divider'] = np.where(data['中央分離帯施設等']==1,'中央分離帯',
                                np.where(data['中央分離帯施設等']==2,'中央線－高輝度標示',
                                np.where(data['中央分離帯施設等']==3,'中央線－チャッターバー等',
                                np.where(data['中央分離帯施設等']==6,'中央線－ポストコーン', 
                                np.where(data['中央分離帯施設等']==4,'中央線－ペイント',
                                np.where(data['中央分離帯施設等']==5,'中央分離なし',
                                np.where(data['中央分離帯施設等']==0,'一般交通の場所',None)))))))

# # 歩車道区分
data['pedestrian_road_division_type'] = np.where(data['歩車道区分']==1,'区分あり－防護柵等',
                      np.where(data['歩車道区分']==2,'区分あり－縁石・ブロック等',
                      np.where(data['歩車道区分']==3,'区分あり－路側帯',
                      np.where(data['歩車道区分']==4,'区分なし',None))))

# # 事故類型
data['accident_vehicle_type'] = np.where(data['事故類型']==1,'人対車両',
                      np.where(data['事故類型']==21,'車両相互',
                      np.where(data['事故類型']==41,'車両単独',
                      np.where(data['事故類型']==61,'列車',None))))          

# # 当事者種別
data['parties_type_a'] = np.where(data['当事者種別（当事者A）']==1,'乗用車－大型車',
                                    np.where(data['当事者種別（当事者A）']==2,'乗用車－中型車',
                                    np.where(data['当事者種別（当事者A）']==7,'乗用車－準中型車',
                                    np.where(data['当事者種別（当事者A）']==3,'乗用車－普通車',
                                    np.where(data['当事者種別（当事者A）']==4,'乗用車－軽自動車',
                                    np.where(data['当事者種別（当事者A）']==5,'乗用車－ミニカー',
                                    np.where(data['当事者種別（当事者A）']==11,'貨物車－大型車',
                                    np.where(data['当事者種別（当事者A）']==12,'貨物車－中型車',
                                    np.where(data['当事者種別（当事者A）']==17,'貨物車－準中型車',
                                    np.where(data['当事者種別（当事者A）']==13,'貨物車－普通車',
                                    np.where(data['当事者種別（当事者A）']==14,'貨物車－軽自動車',
                                    np.where(data['当事者種別（当事者A）']==21,'特殊車－大型－農耕作業用',
                                    np.where(data['当事者種別（当事者A）']==22,'特殊車－大型－その他',
                                    np.where(data['当事者種別（当事者A）']==23,'特殊車－小型－農耕作業用',
                                    np.where(data['当事者種別（当事者A）']==24,'特殊車－小型－その他',
                                    np.where(data['当事者種別（当事者A）']==31,'二輪車－自動二輪－小型二輪－751ｃｃ以上', 
                                    np.where(data['当事者種別（当事者A）']==32,'二輪車－自動二輪－小型二輪－401～750ｃｃ',
                                    np.where(data['当事者種別（当事者A）']==33,'二輪車－自動二輪－小型二輪－251～400cc',
                                    np.where(data['当事者種別（当事者A）']==34,'二輪車－自動二輪－軽二輪－126～250cc',
                                    np.where(data['当事者種別（当事者A）']==35,'二輪車－自動二輪－原付二種－51～125cc', 
                                    np.where(data['当事者種別（当事者A）']==36,'二輪車－原付自転車',
                                    np.where(data['当事者種別（当事者A）']==41,'路面電車',
                                    np.where(data['当事者種別（当事者A）']==42,'列車',
                                    np.where(data['当事者種別（当事者A）']==51,'軽車両－自転車',
                                    np.where(data['当事者種別（当事者A）']==52,'軽車両－駆動補助機付自転車',
                                    np.where(data['当事者種別（当事者A）']==59,'軽車両－その他',
                                    np.where(data['当事者種別（当事者A）']==61,'歩行者',
                                    np.where(data['当事者種別（当事者A）']==71,'歩行者以外の道路上の人（補充票のみ）',
                                    np.where(data['当事者種別（当事者A）']==72,'道路外の人（補充票のみ）',
                                    np.where(data['当事者種別（当事者A）']==75,'物件等',
                                    np.where(data['当事者種別（当事者A）']==76,'相手なし',
                                    np.where(data['当事者種別（当事者A）']==0,'対象外当事者',None))))))))))))))))))))))))))))))))

data['parties_type_b'] = np.where(data['当事者種別（当事者B）']==1,'乗用車－大型車',
                                    np.where(data['当事者種別（当事者B）']==2,'乗用車－中型車',
                                    np.where(data['当事者種別（当事者B）']==7,'乗用車－準中型車',
                                    np.where(data['当事者種別（当事者B）']==3,'乗用車－普通車',
                                    np.where(data['当事者種別（当事者B）']==4,'乗用車－軽自動車',
                                    np.where(data['当事者種別（当事者B）']==5,'乗用車－ミニカー',
                                    np.where(data['当事者種別（当事者B）']==11,'貨物車－大型車',
                                    np.where(data['当事者種別（当事者B）']==12,'貨物車－中型車',
                                    np.where(data['当事者種別（当事者B）']==17,'貨物車－準中型車',
                                    np.where(data['当事者種別（当事者B）']==13,'貨物車－普通車',
                                    np.where(data['当事者種別（当事者B）']==14,'貨物車－軽自動車',
                                    np.where(data['当事者種別（当事者B）']==21,'特殊車－大型－農耕作業用',
                                    np.where(data['当事者種別（当事者B）']==22,'特殊車－大型－その他',
                                    np.where(data['当事者種別（当事者B）']==23,'特殊車－小型－農耕作業用',
                                    np.where(data['当事者種別（当事者B）']==24,'特殊車－小型－その他',
                                    np.where(data['当事者種別（当事者B）']==31,'二輪車－自動二輪－小型二輪－751ｃｃ以上', 
                                    np.where(data['当事者種別（当事者B）']==32,'二輪車－自動二輪－小型二輪－401～750ｃｃ',
                                    np.where(data['当事者種別（当事者B）']==33,'二輪車－自動二輪－小型二輪－251～400cc',
                                    np.where(data['当事者種別（当事者B）']==34,'二輪車－自動二輪－軽二輪－126～250cc',
                                    np.where(data['当事者種別（当事者B）']==35,'二輪車－自動二輪－原付二種－51～125cc', 
                                    np.where(data['当事者種別（当事者B）']==36,'二輪車－原付自転車',
                                    np.where(data['当事者種別（当事者B）']==41,'路面電車',
                                    np.where(data['当事者種別（当事者B）']==42,'列車',
                                    np.where(data['当事者種別（当事者B）']==51,'軽車両－自転車',
                                    np.where(data['当事者種別（当事者B）']==52,'軽車両－駆動補助機付自転車',
                                    np.where(data['当事者種別（当事者B）']==59,'軽車両－その他',
                                    np.where(data['当事者種別（当事者B）']==61,'歩行者',
                                    np.where(data['当事者種別（当事者B）']==71,'歩行者以外の道路上の人（補充票のみ）',
                                    np.where(data['当事者種別（当事者B）']==72,'道路外の人（補充票のみ）',
                                    np.where(data['当事者種別（当事者B）']==75,'物件等',
                                    np.where(data['当事者種別（当事者B）']==76,'相手なし',
                                    np.where(data['当事者種別（当事者B）']==0,'対象外当事者',None))))))))))))))))))))))))))))))))

# # 用途別
data['use_type_a'] =np.where(data['用途別（当事者A）']==1,'事業用',
                      np.where(data['用途別（当事者A）']==31,'自家用',
                      np.where(data['用途別（当事者A）']==0,'対象外当事者',None)))
                    #   np.where(data['用途別（当事者A）']==None, '-', None))))

data['use_type_b'] =np.where(data['用途別（当事者B）']==1,'事業用',
                      np.where(data['用途別（当事者B）']==31,'自家用',
                      np.where(data['用途別（当事者B）']==0,'対象外当事者',None)))
                    #   np.where(data['用途別（当事者B）']==None, 'ー', None))))

# #  車両形状
data['vehicle_shape_a'] = np.where(data['車両形状（当事者A）']==1,'乗用車',
                      np.where(data['車両形状（当事者A）']==11,'貨物車',
                      np.where(data['車両形状（当事者A）']==0,'対象外当事者',None)))
                    #   np.where(data['車両形状（当事者A）']==None,'ー', None ))))
data['vehicle_shape_b'] = np.where(data['車両形状（当事者B）']==1,'乗用車',
                      np.where(data['車両形状（当事者B）']==11,'貨物車',
                      np.where(data['車両形状（当事者B）']==0,'対象外当事者',None)))
                    #   np.where(data['車両形状（当事者B）']==None,'ー', None ))))

# # 速度規制
data['speed_regulation_a'] = np.where(data['速度規制（指定のみ）（当事者A）']==1,'20㎞／ｈ以下',
                      np.where(data['速度規制（指定のみ）（当事者A）']==2,'30㎞／ｈ以下',
                      np.where(data['速度規制（指定のみ）（当事者A）']==3,'40㎞／ｈ以下',
                      np.where(data['速度規制（指定のみ）（当事者A）']==4,'50㎞／ｈ以下',
                      np.where(data['速度規制（指定のみ）（当事者A）']==5,'60㎞／ｈ以下',
                      np.where(data['速度規制（指定のみ）（当事者A）']==6,'70㎞／ｈ以下',
                      np.where(data['速度規制（指定のみ）（当事者A）']==7,'80㎞／ｈ以下',
                      np.where(data['速度規制（指定のみ）（当事者A）']==8,'100㎞/h以下',
                      np.where(data['速度規制（指定のみ）（当事者A）']==9,'100㎞/h超過',
                      np.where(data['速度規制（指定のみ）（当事者A）']==10,'指定の速度規制なし等',
                      np.where(data['速度規制（指定のみ）（当事者A）']==0,'対象外当事者', None)))))))))))
                      
data['speed_regulation_b'] = np.where(data['速度規制（指定のみ）（当事者B）']==1,'20㎞／ｈ以下',
                      np.where(data['速度規制（指定のみ）（当事者B）']==2,'30㎞／ｈ以下',
                      np.where(data['速度規制（指定のみ）（当事者B）']==3,'40㎞／ｈ以下',
                      np.where(data['速度規制（指定のみ）（当事者B）']==4,'50㎞／ｈ以下',
                      np.where(data['速度規制（指定のみ）（当事者B）']==5,'60㎞／ｈ以下',
                      np.where(data['速度規制（指定のみ）（当事者B）']==6,'70㎞／ｈ以下',
                      np.where(data['速度規制（指定のみ）（当事者B）']==7,'80㎞／ｈ以下',
                      np.where(data['速度規制（指定のみ）（当事者B）']==8,'100㎞/h以下',
                      np.where(data['速度規制（指定のみ）（当事者B）']==9,'100㎞/h超過',
                      np.where(data['速度規制（指定のみ）（当事者B）']==10,'指定の速度規制なし等',
                      np.where(data['速度規制（指定のみ）（当事者B）']==0,'対象外当事者', None)))))))))))

# # 車両の衝突部位
data['collision_site_a'] = np.where((data['車両の衝突部位（当事者A）']>=10)&(data['車両の衝突部位（当事者A）']<20),'前_中央_',
                      np.where((data['車両の衝突部位（当事者A）']>=20)&(data['車両の衝突部位（当事者A）']<30),'右_中央_',
                      np.where((data['車両の衝突部位（当事者A）']>=30)&(data['車両の衝突部位（当事者A）']<40),'後_中央_',
                      np.where((data['車両の衝突部位（当事者A）']>=40)&(data['車両の衝突部位（当事者A）']<50),'左_中央_',
                      np.where((data['車両の衝突部位（当事者A）']>=50)&(data['車両の衝突部位（当事者A）']<60),'前_右_',
                      np.where((data['車両の衝突部位（当事者A）']>=60)&(data['車両の衝突部位（当事者A）']<70),'後_右_',
                      np.where((data['車両の衝突部位（当事者A）']>=70)&(data['車両の衝突部位（当事者A）']<80),'後_左_',
                      np.where((data['車両の衝突部位（当事者A）']>=80)&(data['車両の衝突部位（当事者A）']<90),'前_左_',
                      np.where((data['車両の衝突部位（当事者A）']>=0)&(data['車両の衝突部位（当事者A）']<10),'それ以外_', None)))))))))

data['collision_site_b'] = np.where((data['車両の衝突部位（当事者B）']>=10)&(data['車両の衝突部位（当事者B）']<20),'前_中央_',
                      np.where((data['車両の衝突部位（当事者B）']>=20)&(data['車両の衝突部位（当事者B）']<30),'右_中央_',
                      np.where((data['車両の衝突部位（当事者B）']>=30)&(data['車両の衝突部位（当事者B）']<40),'後_中央_',
                      np.where((data['車両の衝突部位（当事者B）']>=40)&(data['車両の衝突部位（当事者B）']<50),'左_中央_',
                      np.where((data['車両の衝突部位（当事者B）']>=50)&(data['車両の衝突部位（当事者B）']<60),'前_右_',
                      np.where((data['車両の衝突部位（当事者B）']>=60)&(data['車両の衝突部位（当事者B）']<70),'後_右_',
                      np.where((data['車両の衝突部位（当事者B）']>=70)&(data['車両の衝突部位（当事者B）']<80),'後_左_',
                      np.where((data['車両の衝突部位（当事者B）']>=80)&(data['車両の衝突部位（当事者B）']<90),'前_左_',
                      np.where((data['車両の衝突部位（当事者B）']>=0)&(data['車両の衝突部位（当事者B）']<10),'それ以外_', None)))))))))

# # 車両の損壊程度
data['vehicle_damege_a'] = np.where(data['車両の損壊程度（当事者A）']==1,'大破',
                      np.where(data['車両の損壊程度（当事者A）']==2,'中破',
                      np.where(data['車両の損壊程度（当事者A）']==3,'小破',
                      np.where(data['車両の損壊程度（当事者A）']==4,'損壊なし',
                      np.where(data['車両の損壊程度（当事者A）']==0,'対象外当事者',None)))))
                    #   np.where(data['車両の損壊程度（当事者A）']==None,'ー', None))))))

data['vehicle_damege_b'] = np.where(data['車両の損壊程度（当事者B）']==1,'大破',
                      np.where(data['車両の損壊程度（当事者B）']==2,'中破',
                      np.where(data['車両の損壊程度（当事者B）']==3,'小破',
                      np.where(data['車両の損壊程度（当事者B）']==4,'損壊なし',
                      np.where(data['車両の損壊程度（当事者B）']==0,'対象外当事者',None)))))
                    #   np.where(data['車両の損壊程度（当事者B）']==None,'ー', None))))))

# # 人身損傷程度
data['personl_injury_a'] = np.where(data['人身損傷程度（当事者A）']==1,'死亡',
                      np.where(data['人身損傷程度（当事者A）']==2,'負傷',
                      np.where(data['人身損傷程度（当事者A）']==4,'損傷なし',                
                      np.where(data['人身損傷程度（当事者A）']==0,'対象外当事者',None))))
data['personl_injury_b'] = np.where(data['人身損傷程度（当事者B）']==1,'死亡',
                      np.where(data['人身損傷程度（当事者B）']==2,'負傷',
                      np.where(data['人身損傷程度（当事者B）']==4,'損傷なし',                
                      np.where(data['人身損傷程度（当事者B）']==0,'対象外当事者',None))))

# # 曜日
data['weekday_type'] = np.where(data['曜日(発生年月日)']==1,'日',
                      np.where(data['曜日(発生年月日)']==2,'月',
                      np.where(data['曜日(発生年月日)']==3,'火',
                      np.where(data['曜日(発生年月日)']==4,'水', 
                      np.where(data['曜日(発生年月日)']==5,'木', 
                      np.where(data['曜日(発生年月日)']==6,'金',                 
                      np.where(data['曜日(発生年月日)']==7,'土', None)))))))

# #　祝日
data['holiday_type'] = np.where(data['祝日(発生年月日)']==1, '当日',
                                np.where(data['祝日(発生年月日)']==2, '祝前日',
                                np.where(data['祝日(発生年月日)']==3, '平日', None)))

data = data.drop(['衝突地点', 'ゾーン規制', '中央分離帯施設等', '歩車道区分', '事故類型', '当事者種別（当事者A）',
       '当事者種別（当事者B）', '用途別（当事者A）', '用途別（当事者B）', '車両形状（当事者A）', '車両形状（当事者B）',
       '速度規制（指定のみ）（当事者A）', '速度規制（指定のみ）（当事者B）', '車両の衝突部位（当事者A）',
       '車両の衝突部位（当事者B）', '車両の損壊程度（当事者A）', '車両の損壊程度（当事者B）', '人身損傷程度（当事者A）',
       '人身損傷程度（当事者B）', '曜日(発生年月日)', '祝日(発生年月日)','環状交差点の直径', '信号機', '一時停止規制　標識（当事者A）', 
       '一時停止規制　表示（当事者A）','一時停止規制　標識（当事者B）', '一時停止規制　表示（当事者B）', '車道幅員', '道路線形'], axis=1)

print(data)
# data.to_csv('data.csv')
print(data.columns)

gdf = geopandas.GeoDataFrame(data, geometry = geopandas.points_from_xy(data.longitude, data.latitude))


# print(data[data.isna().any(axis=1)].sum())
# null_data = data[data.isna().any(axis=1)]
# print(null_data.iloc[:,10:20])

# m = gdf.folium.plot(zoom = 10)
# m
# m.save("1.html")
# plt.show()
# print(m)

# def visualize_locations(df,  zoom=4):
#     """日本を拡大した地図に、pandasデータフレームのlatitudeおよびlongitudeカラムをプロットする。
#     """
        	
#     # 図の大きさを指定する。
    # f = folium.Figure(width=1000, height=500)

    # # 初期表示の中心の座標を指定して地図を作成する。
    # center_lat=34.686567
    # center_lon=135.52000
    # m = folium.Map([center_lat,center_lon], zoom_start=zoom).add_to(f)
        
    # # データフレームの全ての行のマーカーを作成する。
    # for i in range(0,len(df)):
    #     folium.Marker(location=[df["latitude"][i],df["longitude"][i]]).add_to(m)
        
    # return m
# print(visualize_locations(data))
