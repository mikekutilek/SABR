import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import requests
import sys
import fangraphs as fg
import argparse

def get_TTO_slash(data):
	s = "wOBA slash: "
	for i in range(len(data)):
		s += data['wOBA'][i]
		if i != len(data) - 1:
			s += "/"
	return s

def get_first_second_diff(data):
	wOBA = data['wOBA'].astype('float64')
	first = wOBA[0]
	second = wOBA[1]
	diff = round(first - second, 3)
	return diff

def determine_opener(diff)
	if diff >= 0.025 and diff < 0.05:
		s = "might"
	elif diff >= 0.05:
		s ="probably"
	else:
		s = "don't"
	return "You %s need an opener" % s

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("pid", help="playerid of the pitcher")
	args = parser.parse_args()

	page = fg.get_splits_page(args.pid)
	data = fg.get_split_data(page, "tto")
	print(get_TTO_slash(data))

if __name__ == '__main__':
	main()