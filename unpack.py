import sys

from os.path import join, isdir
from os import listdir, rmdir, rename

def unpack(path_to_file):
	for directory in listdir(path_to_file):
		#print directory
		
		parent_path = join(path_to_file, directory)
		#print parent_path

		if not isdir(parent_path): 
			continue

		for file in listdir(parent_path):
#			print file
			curr_path = join(parent_path, file)
			new_path = join(path_to_file, file)
#			print "{0} --> {1}".format(curr_path, new_path)

			if isdir(curr_path): 
				continue
			rename(curr_path, new_path)
		rmdir(parent_path)
#		print ".."



def main():
	path_to_file = sys.argv[1]
#	print "Directory: ", path_to_file
	unpack(path_to_file)


if __name__ == "__main__": main()