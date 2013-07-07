import utils
import lxml.html as lh


MAIN = "http://www.mangareader.net"
SEARCH = "http://www.mangareader.net/actions/search/?q=%s"


def search(query):
	results = []
	mangas = utils.getUrlContent(utils.getUrl(SEARCH, query.replace(" ", "+")))
	for manga in mangas.split('\n'):
		if manga:
			obj = manga.split('|')
			results.append(utils.Content(obj[0].strip(), MAIN+obj[4].strip()))
	return results


def getChapters(link):
	chapters = []
	html = utils.getUrlContent(link)
	doc = lh.fromstring(html)
	for i,a in enumerate(doc.cssselect('#listing tr a')):
		chapters.append(utils.Content(a.text_content(), MAIN+a.attrib['href'], i+1))
	return chapters

def getImages(chapter):
	images = []
	html = utils.getUrlContent(chapter)
	doc = lh.fromstring(html)
	for option in doc.cssselect('#pageMenu option'):
		html2 = utils.getUrlContent(MAIN+option.attrib['value'])
		doc2 = lh.fromstring(html2)
		img = doc2.cssselect('#img')[0]
		images.append(utils.Content(option.text_content(), img.attrib['src']))
	return images