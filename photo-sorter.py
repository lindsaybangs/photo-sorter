import os
import platform
import sys
import csv

from os import listdir, rename, makedirs
from os.path import join, exists, isdir
from datetime import datetime

def get_month_name(month_number):
	monthname = {}
	monthname[1] = "January"
	monthname[2] = "February"
	monthname[3] = "March"
	monthname[4] = "April"
	monthname[5] = "May"
	monthname[6] = "June"
	monthname[7] = "July"
	monthname[8] = "August"
	monthname[9] = "September"
	monthname[10] = "October"
	monthname[11] = "November"
	monthname[12] = "December"

	return monthname[month_number]

def get_location_map(path_to_csv):
	result = {}
	with open(path_to_csv, "r") as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			month = row["month"]
			if not month in result:
				result[month] = {}
			result[month][row["day"]] = row["location"]
	return result

def creation_date(path_to_file):
	stat = os.stat(path_to_file)
	try:
		return stat.st_birthtime
	except AttributeError:
		return stat.st_mtime

def read_in_files(path_to_file, path_to_csv):

	locationmap = get_location_map(path_to_csv)

	result = {}
	for filename in listdir(path_to_file):
		path = join(path_to_file, filename)
		if isdir(path):
			continue

		date = datetime.fromtimestamp(creation_date(path))
		label = map_to_location(date, locationmap)
		if not label in result:
			result[label] = []
		result[label].append(filename)
	return result

def sort_into_folder(path_to_file, dictionary):
	for key in dictionary:
		dir_path = join(path_to_file, key)
		# Create a folder matching the date
		if not exists(dir_path):
			try:
				makedirs(dir_path)
			except OSError as e:
				if e.errno != errno.EEXIST:
					raise
		# Get a list of paths - these are files to move from the root
		for value in dictionary[key]:
			curr_path = join(path_to_file, value)
			new_path = join(dir_path, value)
			os.rename(curr_path, new_path)

def map_to_location(date, locationmap):
	m = str(date.month)
	d = str(date.day)
	if m in locationmap and d in locationmap[m]:
		return locationmap[m][d]

	# if we cannot map the location, put it into a folder by date
	month = get_month_name(date.month)
	return "{0}_{1}".format(month, date.day)

def main():
	path_to_file = sys.argv[1]
	path_to_csv = "date_location.csv" # The CSV is included at project level for now

	# TODO: check for a second argument and if exists, place the photos there

	print "Directory: ", path_to_file

	result = read_in_files(path_to_file, path_to_csv)
	sort_into_folder(path_to_file, result)

	# TODO: A third argument to specify a CSV for personalized date location


if __name__ == "__main__": main()