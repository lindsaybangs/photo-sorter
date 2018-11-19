import sys

from os.path import join, isdir
from os import listdir, rmdir, rename

def unpack(path_to_file):
	for directory in listdir(path_to_file):		
		parent_path = join(path_to_file, directory)

		if not isdir(parent_path): 
			continue

		for file in listdir(parent_path):
			curr_path = join(parent_path, file)
			new_path = join(path_to_file, file)

			if isdir(curr_path): 
				continue
			rename(curr_path, new_path)
		rmdir(parent_path)

def main():
	path_to_file = sys.argv[1]
	unpack(path_to_file)

if __name__ == "__main__": main()
