import urllib, urllib2
import xbmcaddon, xbmcgui, xbmcplugin
import requests
from bs4 import BeautifulSoup

addon_handle = int(sys.argv[1])

podcasts = []
podcasts.append('The Herd with Colin Cowherd;http://is4.mzstatic.com/image/thumb/Music118/v4/fc/8f/08/fc8f0866-86d9'
                '-446e-34d4-e0180c6dabd1/source/600x600bb.jpg;http://podbay.fm/show/1042368254;The Herd with Colin '
                'Cowherd is a thought-provoking, opinionated, and topic-driven journey through the top sports stori'
                'es of the day.')
podcasts.append('Skip and Shannon: Undisputed;http://is4.mzstatic.com/image/thumb/Music71/v4/ad/fb/24/adfb243d-6369'
                '-8b0d-9c23-6c201c15f6ad/source/600x600bb.jpg;http://podbay.fm/show/1150088852;The Skip and Shannon'
                ': Undisputed podcast with Skip Bayless, Shannon Sharpe & Joy Taylor. Catch the show Mon-Fri, 9:30a'
                'm ET on FS1 starting September 6th')
podcasts.append('Speak For Yourself with Cowherd & Whitlock;http://is5.mzstatic.com/image/thumb/Music71/v4/33/64/d8'
                '/3364d82a-9716-b2e7-353b-fdb077a7b2aa/source/600x600bb.jpg;http://podbay.fm/show/1123133293;Colin'
                ' Cowherd and Jason Whitlock team up for the Speak For Yourself podcast, featuring the best discuss'
                'ions from their television show (weekdays at 6pm ET on FS1) with original commentary and opinion '
                'from Jason McIntyre.')
podcasts.append('First Things First;http://is1.mzstatic.com/image/thumb/Music128/v4/3f/6f/33/3f6f330a-6ec5-1568-640'
                '3-ca2a94d25583/source/600x600bb.jpg;http://podbay.fm/show/1277873664;First Things First with Cris'
                ' Carter and Nick Wright launches Tuesday, September 5th at 6AM ET on FS1.')


def getDOM(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0')
    responce = urllib2.urlopen(req)
    returnDOM = responce.read()
    responce.close()
    return returnDOM

def removeListTags(item):
    return str(item).replace("'", '').replace('[', '').replace(']', '')

def listShows():
    list=[]
    for podcast in podcasts:
        podcast = podcast.split(';')
        query = urllib.urlencode({'mode': 'GE', 'url': podcast[2], 'image': podcast[1]})

        infoLabels = {'Title': podcast[0], 'FileName': podcast[0], 'Plot': podcast[3]}
        u = 'plugin://plugin.audio.barstoolpodcasts/?' + query

        li = xbmcgui.ListItem(podcast[0], iconImage=podcast[1])
        li.setInfo('video', infoLabels)
        li.setProperty('fanart_image', podcast[1])

        list.append((u, li, True))

    xbmcplugin.addDirectoryItems(addon_handle,list, len(list))
    xbmcplugin.endOfDirectory(addon_handle)

def getEpisodes(source, image):
    DOM = getDOM(source)
    soup = BeautifulSoup(DOM, 'html.parser')
    matches = soup.find_all('a', {'rel': 'tooltip'})

    list = []
    for match in matches:
        soup = BeautifulSoup(str(match), 'html.parser')
        link = soup.a['href']
        title = soup.a.string

        desc = soup.a['title'].replace('<p>', '').replace('</p>', '')
        desc = ''.join([i if ord(i) < 128 else ' ' for i in desc]).strip()
        infoLabels = {'Title': title, 'FileName': title, 'Plot' : desc}

        query = urllib.urlencode({'mode': 'PE', 'url': link})
        u = 'plugin://plugin.audio.barstoolpodcasts/?' + query

        li = xbmcgui.ListItem(title, iconImage=image)
        li.setInfo('video', infoLabels)
        li.setProperty('IsPlayable', 'true')
        li.setProperty('fanart_image', image)

        list.append((u, li, False))

    xbmcplugin.addDirectoryItems(addon_handle, list, len(list))
    xbmcplugin.endOfDirectory(addon_handle)

def playEpisode(url):
    individualPage = getDOM(url=url)
    soup = BeautifulSoup(str(individualPage), 'html.parser')
    match = soup.find('a', {'class': 'btn btn-mini btn-primary'})
    xbmcplugin.setResolvedUrl(addon_handle, True, xbmcgui.ListItem(path=match['href']))

# MAIN EVENT PROCESSING STARTS HERE
# Query Handler
parms = {}
try:
    parms = dict(arg.split('=') for arg in ((sys.argv[2][1:]).split('&')))
    for key in parms:
      try:    parms[key] = urllib.unquote_plus(parms[key]).decode(UTF8)
      except: pass
except:
    parms = {}

p = parms.get
mode = p('mode',None)

if mode==  None:    listShows()
elif mode=='GE':    getEpisodes(urllib.unquote(p('url')), urllib.unquote(p('image')))
elif mode=='PE':    playEpisode(urllib.unquote(p('url')))
else:               xbmcgui.Dialog().ok('ERROR', 'Error: MODE not found!!!')

