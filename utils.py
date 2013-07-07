import pycurl, cStringIO, json
import urlparse, os.path, errno, sys

class Deserialize(object):
	def __init__(self, file):
		self.__dict__ = json.load(open(file))

class Content:
	def __init__(self, title, link, number=0):
		self.number = number
		self.title = title
		self.link = link

	def __repr__(self):
		return ("{%d, "+self.title+", "+self.link+"}") % self.number

def mkdir_p(path):
	try:
		os.makedirs(path)
	except OSError as exc:
		if exc.errno == errno.EEXIST and os.path.isdir(path):
			pass
		else: raise


def getUrl(link, params=()):
	return (link % params)


def getUrlContent(url):
	buf = cStringIO.StringIO()
	c = pycurl.Curl()
	c.setopt(c.URL, url)
	c.setopt(c.WRITEFUNCTION, buf.write)
	c.perform()
	val = buf.getvalue()
	buf.close()
	return val


def putUrlContent(url, file):
	buf = cStringIO.StringIO()
	c = pycurl.Curl()
	c.setopt(c.URL, url)
	c.setopt(c.WRITEFUNCTION, buf.write)
	c.perform()
	f = open(file, 'wb')
	f.write(buf.getvalue())
	f.close()
	return True


def getExtension(url):
	return os.path.splitext(os.path.basename(urlparse.urlsplit(url).path))[1]

def updateProgress(prompt, progress):
	sys.stdout.write('\r{0} [{1}] {2}%'.format(prompt, ('#'*(progress/3)).ljust(33), progress))
	sys.stdout.flush()