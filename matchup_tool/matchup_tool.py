import pandas
import numpy

pitch_value_batting_data = pandas.read_csv('c:/Users/makut/Documents/Data/Fangraphs/Batting/2018/Pitch Value Batting Data.csv')
pitch_type_pitching_data = pandas.read_csv('c:/Users/makut/Documents/Data/Fangraphs/Pitching/2018/Pitch Type Pitching Data.csv')


def calc_matchup(team, pitcher):
	batter_data = pitch_value_batting_data.loc[pitch_value_batting_data['Team'] == team]
	batter_data = batter_data.fillna(0)

	for index, batter in batter_data.iterrows():
		#print(batter['Name'])
		calc_pitch_score(batter['Name'], pitcher)

	#calc_pitch_score('Starling Marte', 'Patrick Corbin')
	#calc_pitch_score('Gregory Polanco', 'Patrick Corbin')
	#calc_pitch_score('Francisco Cervelli', 'Patrick Corbin')
	#calc_pitch_score('Corey Dickerson', 'Patrick Corbin')
	#calc_pitch_score('Josh Bell', 'Patrick Corbin')


def clean_data(data):
	replace_percents(data)
	return data.fillna(0)

def replace_percents(data):
	strings = data.select_dtypes(['object'])
	data[strings.columns] = strings.apply(lambda x: x.str.replace('%', ''))

def convert_to_float(obj):
	return obj.astype('float64')

def calc_pitch_score(batter, pitcher):
	#total_pitch_score = 0
	#batter_data_sets = [pitch_value_batting_data_2016.loc[pitch_value_batting_data_2016['Name'] == batter], pitch_value_batting_data_2017.loc[pitch_value_batting_data_2017['Name'] == batter], pitch_value_batting_data.loc[pitch_value_batting_data['Name'] == batter]]
	#i = 0

	#while (i < len(batter_data_sets)):
	batter_data = pitch_value_batting_data.loc[pitch_value_batting_data['Name'] == batter]
	batter_index = batter_data.index[0]
	batter_data = batter_data.fillna(0)

	wFB = batter_data['wFB/C']
	wSL = batter_data['wSL/C']
	wCT = batter_data['wCT/C']
	wCB = batter_data['wCB/C']
	wCH = batter_data['wCH/C']
	wSF = batter_data['wSF/C']

	replace_percents(pitch_type_pitching_data)

	pitcher_data = pitch_type_pitching_data.loc[pitch_type_pitching_data['Name'] == pitcher]
	pitcher_index = pitcher_data.index[0]
	pitcher_data = pitcher_data.fillna(0)

	fb_percent = convert_to_float(pitcher_data['FB%'])
	sl_percent = convert_to_float(pitcher_data['SL%'])
	ct_percent = convert_to_float(pitcher_data['CT%'])
	cb_percent = convert_to_float(pitcher_data['CB%'])
	ch_percent = convert_to_float(pitcher_data['CH%'])
	sf_percent = convert_to_float(pitcher_data['SF%'])

	pitch_score = (wFB[batter_index] * fb_percent[pitcher_index]) + (wSL[batter_index] * sl_percent[pitcher_index]) + (wCT[batter_index] * ct_percent[pitcher_index]) + (wCB[batter_index] * cb_percent[pitcher_index]) + (wCH[batter_index] * ch_percent[pitcher_index]) + (wSF[batter_index] * sf_percent[pitcher_index])
	pitch_score = pitch_score / 100
	#total_pitch_score += pitch_score
	print('Pitch score for: ' + str(batter) + ' vs. ' + str(pitcher) + ': ' + str(round(pitch_score, 2)))

def calc_plate_discipline(batter, pitcher):
	batter_data = plate_discipline_batting_data.loc[pitch_value_batting_data['Name'] == batter]
	batter_index = batter_data.index[0]
	batter_data = batter_data.fillna(0)

	o_swing = batter_data['O-Swing%']
	z_swing = batter_data['Z-Swing%']
	swing = batter_data['Swing%']
	o_contact = batter_data['O-Contact%']
	z_contact = batter_data['Z-Contact%']
	contact = batter_data['Contact%']
	zone = batter_data['Zone%']
	f_strike = batter_data['F-Strike%']
	sw_str = batter_data['SwStr%']

def calc_team_pitch_value(team):
	batter_data = pitch_value_batting_data.loc[pitch_value_batting_data['Team'] == team]

	batter_data = batter_data.fillna(0)

	wFB = batter_data['wFB']
	wSL = batter_data['wSL']
	wCT = batter_data['wCT']
	wCB = batter_data['wCB']
	wCH = batter_data['wCH']
	wSF = batter_data['wSF']

	wFBc = batter_data['wFB/C']
	wSLc = batter_data['wSL/C']
	wCTc = batter_data['wCT/C']
	wCBc = batter_data['wCB/C']
	wCHc = batter_data['wCH/C']
	wSFc = batter_data['wSF/C']

	w_data = pandas.DataFrame()
	w_data['Name'] = batter_data['Name']

	w = wFB + wSL + wCT + wCB + wCH + wSF
	wc = wFBc + wSLc + wCTc + wCBc + wCHc + wSFc
	w_data['W'] = w
	w_data['W/C'] = wc
	print(w_data.sort_values(by='W', ascending=False))


#replace_percents(pitch_type_pitching_data)
calc_matchup('Pirates', 'Patrick Corbin')
#calc_team_pitch_value("Pirates")