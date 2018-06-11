import pandas
import numpy
from bs4 import BeautifulSoup
import requests

pandas.options.mode.chained_assignment = None

std_batting_data = pandas.read_csv('c:/Users/makut/Documents/Data/Fangraphs/Batting/2018/Standard Batting Data.csv')
std_fielding_data = pandas.read_csv('c:/Users/makut/Documents/Data/Fangraphs/Fielding/2018/Standard Fielding Data.csv')
std_pitching_data = pandas.read_csv('c:/Users/makut/Documents/Data/Fangraphs/Pitching/2018/Standard Pitching Data.csv')

#batting and fielding data
batter_name = std_batting_data['Name']
batter_g = std_batting_data['G']
r = std_batting_data['R']
single = std_batting_data['1B']
double = std_batting_data['2B']
triple = std_batting_data['3B']
homer = std_batting_data['HR']
rbi = std_batting_data['RBI']
sb = std_batting_data['SB']
cs = std_batting_data['CS']
bb = std_batting_data['BB']
hbp = std_batting_data['HBP']
so = std_batting_data['SO']
fielder_name = std_fielding_data['Name']
e = std_fielding_data['E']
a = std_fielding_data['A']
pos = std_fielding_data['Pos']

pitcher_name = std_pitching_data['Name']
pitcher_g = std_pitching_data['G']
ip = std_pitching_data['IP']
w = std_pitching_data['W']
l = std_pitching_data['L']
cg = std_pitching_data['CG']
sv = std_pitching_data['SV']
h = std_pitching_data['H']
er = std_pitching_data['ER']
walks = std_pitching_data['BB']
ibb = std_pitching_data['IBB']
hb = std_pitching_data['HBP']
k = std_pitching_data['SO']
hld = std_pitching_data['HLD']
bsv = std_pitching_data['BS']

#handle batting/fielding data first
ofers = std_fielding_data.loc[std_fielding_data['Pos'].isin(['LF','CF','RF'])]
ifers = std_fielding_data.loc[std_fielding_data['Pos'].isin(['C','1B','2B','SS','3B'])]
e = std_fielding_data.loc[std_fielding_data['Pos'].isin(['C','1B','2B','SS','3B','LF','CF','RF'])]

ofers['Total'] = ofers.groupby(['Name'])['A'].transform('sum')
ifers['Total'] = ifers.groupby(['Name'])['A'].transform('sum')
e['Total'] = e.groupby(['Name'])['E'].transform('sum')

ofers_min = ofers.drop_duplicates(['Name'], keep='first')
ifers_min = ifers.drop_duplicates(['Name'], keep='first')
e_min = e.drop_duplicates(['Name'], keep='first')

df_with_ofa = std_batting_data.merge(ofers_min, on='Name', how='left').fillna(0)
df_with_ifa = std_batting_data.merge(ifers_min, on='Name', how='left').fillna(0)
df_with_e = std_batting_data.merge(e_min, on='Name', how='left').fillna(0)

ofa = df_with_ofa['Total']
ifa = df_with_ifa['Total']
e2 = df_with_e['Total']

#now we handle pitcher data
half_ip = []
inns = []
for i in ip:
	inn = int(i)
	half_i = str(i)[-1]
	inns.append(inn)
	half_ip.append(float(half_i))

innings = pandas.Series(inns)
rem = pandas.Series(half_ip)

page = requests.get("https://www.baseball-reference.com/leagues/MLB/2018-starter-pitching.shtml#players_starter_pitching::none").text
soup = BeautifulSoup(page, "html.parser")
#table = soup.select_one("table#players_starter_pitching")
tables = soup.findAll("table")
for table in tables:
	rows = table.find_all('tr')
	qs_list = []

	#for table in tables:
	#rows = table.find_all('tr')
	for row in rows:
		#print(row.text.strip())
		cells = row.findAll('td')
		for cell in cells:
			qs_list.append(cell.text.strip())
print(qs_list)
#print(soup.prettify().encode("utf-8"))

#names = qs_list[1::5]
#qstarts = qs_list[4::5]
#qstarts = [float(i) for i in qstarts]

#quality_starts = pandas.DataFrame()
#quality_starts['Name'] = names
#quality_starts['QS'] = qstarts
#df_with_qs = std_pitching_data.merge(quality_starts, on='Name', how='left').fillna(0)

#qs = df_with_qs['QS']
#print(std_pitching_data)

#print(table)
#qs = soup.findAll('td', {"class": "text-right"})
#for q in qs:
#	print(q.text)

#create fantasy point data frames
batter_data = pandas.DataFrame()
pitcher_data = pandas.DataFrame()
batter_data['Name'] = batter_name
pitcher_data['Name'] = pitcher_name

#add up points
batter_fp = r + single + (double * 2) + (triple * 3) + (homer * 4) + rbi + (sb * 1.75) - (cs * 0.5) + (bb * 0.75) + (hbp * 0.5) - (so * .1) - e2 + (ofa * 1.05) + (ifa * 0.05)
pitcher_fp = (innings * 1.0) + (rem * 0.33) + (w * 9) - (l * 6) + (cg * 7) + (sv * 8) - (h * 0.25) - er - (walks * 0.5) - (ibb * 0.5) + k + (hld * 7.5) - (bsv * 3)
batter_fpg = batter_fp / batter_g
pitcher_fpg = pitcher_fp / pitcher_g

#add points to the data set
batter_data['fp'] = batter_fp
pitcher_data['fp'] = pitcher_fp
batter_data['fp_per_game'] = batter_fpg
pitcher_data['fp_per_game'] = pitcher_fpg

#print(batter_data.loc[batter_data['Name'] == 'Colin Moran', 'fp_per_game'])
#print(batter_data.sort_values(by=['fp_per_game']))
#print(type(ip))
batter_data.to_csv('data/batter_fp.csv')
pitcher_data.to_csv('data/pitcher_fp.csv')