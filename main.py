from flask import *
import pandas as pd
import sys
sys.path.append('/matchup_tool')
from matchup_tool import matchup_tool as mt

#Define app
app = Flask(__name__)

@app.route('/')
def hello_world():
	return 'Hello, World!'

@app.route('/matchup_tool')
def show_tables():
	data = mt.calc_team_pitch_value('Pirates')
	data.set_index(['Name'], inplace=True)
	data.index.name=None
	return render_template('matchup_tool.html', table = data.to_html())
	#return mt.calc_team_pitch_value('Pirates')

if __name__ == '__main__':
	app.run()