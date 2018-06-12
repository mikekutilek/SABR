import pandas
import numpy
import math

pitch_value_batting_data = pandas.read_csv('c:/Users/makut/Documents/Data/Fangraphs/Batting/2018/Pitch Value Batting Data.csv')
pitch_type_pitching_data = pandas.read_csv('c:/Users/makut/Documents/Data/Fangraphs/Pitching/2018/Pitch Type Pitching Data.csv')
runners_in_scoring_batting_data = pandas.read_csv('c:/Users/makut/Documents/Data/Fangraphs/Batting/2018/Runners in Scoring Batting Data.csv')
runners_on_batting_data = pandas.read_csv('c:/Users/makut/Documents/Data/Fangraphs/Batting/2018/Runners On Batting Data.csv')
bases_empty_batting_data = pandas.read_csv('c:/Users/makut/Documents/Data/Fangraphs/Batting/2018/Bases Empty Batting Data.csv')

def clean_data(data):
	replace_percents(data)
	return data.fillna(0)

def replace_percents(data):
	strings = data.select_dtypes(['object'])
	data[strings.columns] = strings.apply(lambda x: x.str.replace('%', ''))

def convert_to_float(obj):
	return obj.astype('float64')

def calc_matchup(team, pitcher):
	batter_data = pitch_value_batting_data.loc[pitch_value_batting_data['Team'] == team]
	batter_data = batter_data.fillna(0)
	#batter_data = pitch_value_batting_data
	print("\n" + team + " vs. " + pitcher)
	for index, batter in batter_data.iterrows():
		#print(batter['Name'])
		calc_pitch_score(batter['Name'], pitcher)

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

def calc_situational_hitting_diff():
	batter_data = runners_on_batting_data.loc[runners_on_batting_data['PA'] > 25]
	wRC1 = batter_data['wRC+']
	batter_data = bases_empty_batting_data.loc[bases_empty_batting_data['PA'] > 25]
	wRC2 = batter_data['wRC+']
	
	wRC1_data = pandas.DataFrame()
	wRC1_data['Name'] = runners_on_batting_data['Name']
	wRC1_data['wRC+ (Runners On)'] = round(wRC1).astype("int")
	wRC2_data = pandas.DataFrame()
	wRC2_data['Name'] = bases_empty_batting_data['Name']
	wRC2_data['wRC+ (Bases Empty)'] = round(wRC2).astype("int")

	diff_data = wRC1_data.merge(wRC2_data, on='Name', how='left').fillna(0)
	diff_data['wRC+ (Bases Empty)'] = diff_data['wRC+ (Bases Empty)'].astype("int")
	diff_data['Difference'] = round(diff_data['wRC+ (Runners On)'] - diff_data['wRC+ (Bases Empty)']).astype("int")
	print(diff_data.sort_values(by='Difference', ascending=False))
	diff_data.to_csv('c:/Users/makut/Documents/Data/Fangraphs/Batting/2018/Situational Difference Batting Data.csv')

def player_calc_situational_hitting_diff(batter):
	batter_data = runners_on_batting_data.loc[runners_on_batting_data['Name'] == batter]
	wRC1 = batter_data['wRC+']
	batter_data = bases_empty_batting_data.loc[bases_empty_batting_data['Name'] == batter]
	wRC2 = batter_data['wRC+']
	print(round(float(wRC1) - float(wRC2), 2))

#replace_percents(pitch_type_pitching_data)
#calc_matchup('Pirates', 'Patrick Corbin')
#calc_matchup('Diamondbacks', 'Joe Musgrove')
#calc_matchup('Red Sox', 'Dylan Bundy')
#calc_matchup('Orioles', 'Steven Wright')
#calc_team_pitch_value("Pirates")
calc_situational_hitting_diff()