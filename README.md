# MangaGetter

It's a command line tool writen in Python to download mangas from manga reading websites. Until this moment there is only one plugin for http://mangareader.net.


### Usage:
python manga.py **[-h|--help] [-m|--manga Title:Range]**

### Options
```
    -h, --help
        show this help message and exit
    
    -m, --manga Title:Range
        Download manga chapters in range
        Range formats: <from>-<to> | <chapter> | all
        <from>-<to>: chapters between <from> & <to>, '*' is wildcard
        <chapter>:   specific chapter number
        all:         equivalent to *-*, all available chapter
```

### Examples
1- Get Bleach chapter 544
```
    $ python manga.py -m Bleach:544
```

2- Get Kiseiju the full manga
```
    $ python manga.py -m Kiseiju:all

    Or

    $ python manga.py -m Kiseiju:*-*
```
3- Get One piece Marineford Arc
```
    $ python manga.py -m "One piece:550-580"
    1- One Piece
    2- One Piece (Databook)
    Which Manga you want? 1
```

4- Get Naruto from 634 to 637
```
    $ python manga.py -m Naruto:634-637
	1- Naruto
	2- Road To Naruto The Movie
	Which Manga you want? 1

```

You can stop downloading by stoping the script **^C**, and then continue downloading by the same command and the script will continue from the uncomplete chapter.

**Note:** MangaGetter is not yet packaged, so you need to install dependencies manually. The only dependency for the moment is lxml.