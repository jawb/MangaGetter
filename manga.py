import os, sys, argparse, importlib
import utils
import re, errno

# Global variables
PATH = os.path.dirname(os.path.abspath(__file__))+"/"
config = utils.Deserialize(PATH+".config.json")
DOWNLOAD = config.download_dir

# Loading plugin
PLUGIN = importlib.import_module(config.plugins_dir+'.'+config.default_plugin)

# Reding user inputs
def readCli(argv):

	def SpecialString(v):
	    try:
	        return re.match("^.*\:((([0-9]+|\*)\-([0-9]+|\*))|[0-9]+|all)$", v).group(0)
	    except:
	        raise argparse.ArgumentTypeError("Invalid range: '%s' does not match required format" % (v))

	parser = argparse.ArgumentParser(description='MangaGetter, Download mangas easily', formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument("-m", "--manga", required=True, type=SpecialString, metavar=('Title:Range'),
		help="Download manga chapters in range\n"
		"Range formats: <from>-<to> | <chapter> | all\n"
		"<from>-<to>: chapters between <from> & <to>, '*' is wildcard\n"
		"<chapter>:   specific chapter number\n"
		"all:         equivalent to *-*, all available chapter\n")
	
	_input = parser.parse_args(argv)
	manga = _input.manga.split(':')
	title  = manga[0]
	action = manga[1]

	match = re.search(r'([0-9\*]*)\-([0-9\*]*)', action)
	if(action == "all"):
		min = 1
		max = 3000

	elif(action.isdigit()):
		min = int(action)
		max = int(action)
	
	elif(match):
		min = int(match.group(1)) if match.group(1).isdigit() else 1
		max = int(match.group(2)) if match.group(2).isdigit() else 3000

	else:
		usage()
		exit(0)

	return title, min, max

# Resolve conflict if many Mangas found
def resolve(results):
	if len(results) == 0:
		print "Manga not found."
		exit(2)
	elif len(results) > 1:
		i = 1
		for manga in results:
			print ("%d- "+manga.title) % i
			i += 1
		sys.stdout.write("Which Manga you want? ")
		n = int(raw_input())
		print ""
		return results[n-1].title,results[n-1].link

	elif len(results) == 1:
		return results[0].title, results[0].link


# Check downloaded items
def check(title, chapters):

	dir = DOWNLOAD+title+os.sep

	if os.path.isdir(dir):
		# Clean directory
		chaps = os.walk(dir).next()[1]
		available_chaps = [int(x) for x in chaps]
		clone_chaps = available_chaps[:]
		for chap in available_chaps:
			# Remove empty chapters
			if len(os.listdir(dir+str(chap))) == 0:
				os.rmdir(dir+str(chap))
				clone_chaps.remove(chap)

			
			# Redownload incompleted chapters
			elif not os.path.isfile(dir+str(chap)+os.sep+".completed"):
				clone_chaps.remove(chap)

		available_chaps = clone_chaps
		
		# Find which chapters to download
		wanted_chaps = [x.number for x in chapters]
		needed_chaps = [x for x in wanted_chaps if x not in available_chaps]
		
		return [x for x in chapters if x.number in needed_chaps]

	else:
		return chapters


# Download manga
def download(title, chapters):

	dir = DOWNLOAD+title+os.sep

	utils.mkdir_p(dir)

	print "Downloading "+title+" (", len(chapters) ,")..."
	for chap in chapters:

		utils.mkdir_p(dir+str(chap.number))

		images = PLUGIN.getImages(chap.link)
		for i,img in enumerate(images):
			utils.putUrlContent(img.link, dir+str(chap.number)+
				os.sep+img.title+utils.getExtension(img.link))
			utils.updateProgress(chap.title, int(i*1.0/(len(images)-1)*100))
		print ""

		file = open(dir+str(chap.number)+os.sep+'.completed', 'w+')


def main(argv):
	
	# Read params
	manga, min, max = readCli(argv)

	# Get the title and the url
	results = PLUGIN.search(manga)
	title, url = resolve(results)
	chapters = PLUGIN.getChapters(url)[min-1:max]

	# Check and download
	needed_chaps = check(title, chapters)
	download(title, needed_chaps)


if __name__ == "__main__":
    main(sys.argv[1:])