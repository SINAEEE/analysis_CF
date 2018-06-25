
import pandas as pd
import matplotlib.pyplot as plt

#-------------pelicana
pelicana_table = pd.DataFrame.from_csv('__result__/crawling/pelicana_table.csv',
                                       encoding='utf-8',
                                       index_col=0,
                                       header=0).fillna('') #비어있는 공간은 null로 채우기


pelicana_table = pelicana_table[pelicana_table.sido != ''] #row를 이용한 slicing(row 필터링)
pelicana_table = pelicana_table[pelicana_table.gungu != '']

#SIDO GUNGU 별 매장수
pelicana = pelicana_table.apply(lambda r: str(r['sido'])+' '+str(r['gungu']), axis=1).value_counts()
#print(pelicana)
#s2 = s1.value_counts() #value grouping
#print(s2)
#print(type(s1)) #series : index + column
#print(s1.value_counts())


#-------------nene
nene_table = pd.DataFrame.from_csv('__result__/crawling/nene_table.csv',
                                       encoding='utf-8',
                                       index_col=0,
                                       header=0).fillna('')
#print(nene_table)

nene_table = nene_table[nene_table.sido != ''] #row를 이용한 slicing(row 필터링)
nene_table = nene_table[nene_table.gungu != '']
nene = nene_table.apply(lambda r: str(r['sido'])+' '+str(r['gungu']), axis=1).value_counts()
#print(nene)



#-------------kyochon
kyochon_table = pd.DataFrame.from_csv('__result__/crawling/kyochon_table.csv',
                                       encoding='utf-8',
                                       index_col=0,
                                       header=0).fillna('')

kyochon_table = kyochon_table[kyochon_table.sido != '']
kyochon_table = kyochon_table[kyochon_table.gungu != '']
kyochon = kyochon_table.apply(lambda r: str(r['sido'])+' '+str(r['gungu']), axis=1).value_counts()
#print(kyochon)



#-------------goobne
goobne_table = pd.DataFrame.from_csv('__result__/crawling/goobne_table.csv',
                                       encoding='utf-8',
                                       index_col=0,
                                       header=0).fillna('')
#print(goobne_table)

goobne_table = goobne_table[goobne_table.sido != '']
goobne_table = goobne_table[goobne_table.gungu != '']
goobne = goobne_table.apply(lambda r: str(r['sido'])+' '+str(r['gungu']), axis=1).value_counts()
#-> float값으로 나오는 data를 방지하기 위해 str로 변경
#print(goobne)

chicken_table = pd.DataFrame({'pelicana' : pelicana,
                              'nene':nene,
                              'kyochon':kyochon,
                              'goobne':goobne}).fillna(0)

chicken_table = chicken_table.drop(chicken_table[chicken_table.index == '00 18'].index)
chicken_table = chicken_table.drop(chicken_table[chicken_table.index == '테스트 테스트구'].index)
chicken_sum_table = chicken_table.sum(axis=0)
#print(chicken_sum_table.iloc[:5])


plt.figure()
chicken_sum_table.plot(kind='bar')
plt.show()

#print(chicken_table[chicken_table.index == '00 18'])
#print(chicken_table[chicken_table.index == '00 18'].index)

