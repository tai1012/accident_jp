# print(df)
# print(df.describe())
# G=nx.Graph()
# G = ox.graph_from_point(center_point=(35.688374, 139.640234), network_type='drive', dist=1000)
# ox.plot_graph(G,save=True,filepath='Test.jpg'

#プレーンな地図を用意する
map1 = folium.Map(
   #初期位置のセット
   location=[35.688374, 139.640234],
   
   #初期表示の拡大具合のセット
   zoom_start = 10,

   #地図のスタイルの選択 どれか一つ選んで#をはずしてください
   tiles = "OpenStreetMap"
   #tiles="cartodbpositron"
   #tiles = "Stamen Toner"
   #tiles = "Stamen Terrain"
)

# for i in range(len(df)):
#     folium.Circle(
#         radius=50,
#         location=[df.iloc[i]['latitude'], df.iloc[i]['longitude']],
#         # tooltip=str(df.iloc[i]['City'] +", " +df.iloc[i]['hostel.name']),
#        #ドットの外枠の色を指定します
#         color="green",
#        #ドットを色埋めするかを設定します
#         fill = True,        
#        #色埋めする際の色を設定します
#         fill_color = "lightgreen"
#    ).add_to(map1)
map1 = folium.Map(
    location=[35.688374, 139.640234],
    zoom_start = 10,
    tiles = "OpenStreetMap"
)
map1
#描画
print(map1)
jpn_df = gpd.read_file('../preprocessing/00_data/japan.topojson')
"""

"""
PATH = '../preprocessing/00_data/A002005212020DDSWC13/r2ka13.shp'
gdf = gpd.read_file(PATH, encoding='cp932')

print(gdf.columns)

# # for i, row in gdf.iterrows():
# #     print(f'ポリゴン位置{row["geometry"]}')  # ジオメトリ情報
# #     print(f'CITY:{row["CITY"]}')
# gdf.plot(
#     # column = '',  # 色分け対象の列
#             cmap = 'OrRd'  # 色分けのカラーマップ
#         )