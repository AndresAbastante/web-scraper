import pandas as pd

df1=pd.read_csv('df1.csv')
df2=pd.read_csv('df2.csv')
df = pd.concat([df1, df2])
df = df.reset_index(drop=True)
df.to_csv('merged')

df3 = pd.merge(df1, df2, how='outer', indicator='Exist')
df3 = df3.loc[df3['Exist'] != 'both']
df3.to_csv('different')
# newdf = pd.DataFrame({'Product':products, 'Price':prices, 'Condition':condition, 'Set':sets, 'Stock':stocks})
# newdf.to_csv(csvfilename, index=True)

#olddf = pd.read_csv('mtgpirulo-new-results.csv')
#mergeddf.to_csv('merged' + dateandtime.strftime('%y-%m-%d %H:%M') + '.csv')

#subprocess.call(['open', 'merged.csv'])
#if df.empty==False:
#    subprocess.call(['notify', '-bulk', '-i', excelfilename])