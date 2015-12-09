# -*- coding: iso-8859-15 -*-

import re
import urllib2
from urllib import quote
import time
import math
from urlparse import urlparse
import sqlite3

from prettytable import PrettyTable
from prettytable import PLAIN_COLUMNS

from datetime import datetime
from datetime import timedelta
    
import string
import json


#API_KEY = "Insert google API key here"
#WEATHER_API_KEY = "insert weather API key here"
headers = { 'User-Agent' : 'ircbot' }

vko = dict([('Monday', 'Maanantai'),
            ('Tuesday', 'Tiistai'), ('Wednesday', 'Keskiviikko'),
            ('Thursday', 'Torstai'), ('Friday', 'Perjantai'),
            ('Saturday', 'Lauantai'), ('Sunday', 'Sunnuntai')])

class liter:
    """A class that iterates dice results"""
    def __init__(self, l):
        self.l = l
        for i in range(len(self.l)):
            self.l[i] = int(self.l[i])
    def give(self, c):
        tmp = 0
        for i in range(c):
            tmp += self.l.pop(0)
        return tmp
    def giveBest3of4(self):
        tmp = []
        for i in range(4):
            tmp.append(self.l.pop(0))
        tmp.sort()
        tmp.pop(0)
        return sum(tmp)

class LocationError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
        
def w_day():
    """ Returns current weekday as a list including capitalized string"""
    return [vko[time.strftime("%A", time.localtime())]]

def titleparser(str1):
    """Not in use, but parses text between <title> tags"""
    fstrip = str1[str1.find("<title>"):]
    strip = fstrip[7:fstrip.find("</title>")]
    strip = strip.strip().replace("\n", "").replace("\t", "")
    
    return strip
    
def joutalo(day=""):
    f_handle = urllib2.urlopen("http://aalef.fi/ylioppilastalo")
    pattern = r'.*lunchdate %s4.+?lunchtitle">(?P<kokin>.*?)<.+?lunchtitle">(?P<kotoisia>.*?)<.+?lunchtitle">(?P<kasvis>.*?)<.+?lunchtitle">(?P<soppa>.*?)<.+?lunchtitle">(?P<puuro>.*?)<.+?lunchtitle">(?P<salaatti>.*?)<.+?lunchtitle">(?P<jalkiruoka>.*?)<.+?' % day.lower()
    page = f_handle.read()
    f_handle.close()
    result = re.match(pattern, page, re.DOTALL)
    
    if result == None:
        pattern = r'.*<h4>%s .*?</h4>.*?<div>(?P<kokin>.*?)</div>.*?<div>(?P<kotoisia>.*?)</div>.*?<div>(?P<kasvis>.*?)</div>.*?<div>(?P<soppa>.*?)</div>.*?<div>(?P<puuro>.*?)</div>.*?<div>(?P<salaatti>.*?)</div>.*?<div>(?P<jalkiruoka>.*?)<' % day.lower()
        
        result = re.match(pattern, page, re.DOTALL)
        
    return result
    
def kurnis(day=""):
    f_handle = urllib2.urlopen("http://aalef.fi/laseri")
    pattern = r'.*lunchdate %s4.+?lunchtitle">(?P<kokin>.*?)<.+?lunchtitle">(?P<kotoisia>.*?)<.+?lunchtitle">(?P<kasvis>.*?)<.+?lunchtitle">(?P<soppa>.*?)<.+?lunchtitle">(?P<salaatti>.*?)<.+?lunchtitle">(?P<kevyesti>.*?)<.+?lunchtitle">(?P<jalkiruoka>.*?)<.+?' % day.lower()
    page = f_handle.read()
    f_handle.close()
    result = re.match(pattern, page, re.DOTALL)
    
    if result == None:
        pattern = r'.*<h4>%s .*?</h4>.*?<div>(?P<kokin>.*?)</div>.*?<div>(?P<kotoisia>.*?)</div>.*?<div>(?P<kasvis>.*?)</div>.*?<div>(?P<soppa>.*?)</div>.*?<div>(?P<salaatti>.*?)</div>.*?<div>(?P<kevyesti>.*?)</div>.*?<div>(?P<jalkiruoka>.*?)<' % day.lower()
        
        result = re.match(pattern, page, re.DOTALL)
    
    return result

def safkat_table(day=""):
    """Not in use right now, looks horrible in smaller screens"""
    if day=="":
        day = w_day()[0]
    
    try:
        r1 = joutalo(day)
        r2 = kurnis(day)
    except:
        return ["Couldn't connect"]

    try:
        x = PrettyTable()
        x.field_names = ["", "YO-talo", "Kurnis"]
        x.add_row(['Kokin suositus', r1.group('kokin'), r2.group('kokin')])
        x.add_row(['Kotoisia makuja', r1.group('kotoisia'), r2.group('kotoisia')])
        x.add_row(['Soppa', r1.group('soppa'), r2.group('soppa')])
        x.add_row(['Salaatti', r1.group('salaatti'), r2.group('salaatti')])
        x.add_row(['Kasvis', r1.group('kasvis'), r2.group('kasvis')])
        x.set_style(PLAIN_COLUMNS)
        x.align[""] = "l"
        
        lines = x.get_string().split('\n')
        
    except:
        return["No data. Try the next day."]

    return lines

def safkat_rows(day=""):
    if day=="":
        day = w_day()[0]
        
    try:
        r1 = joutalo(day)
        r2 = kurnis(day)
    except:
        return ["Couldn't connect"]
        
    try:
        r3 = []
        for item in r2.groups():
            if item.strip() != "Kevyesti" and item != r2.group(r2.lastindex):
                r3.append(item.strip())
    
        kur = "Kurniekka: "
        for i in range(len(r3)-1):
            kur += r3[i] + " | "
        kur += r3[len(r3)-1]
        kur = kur.decode("utf-8")
        
        jou = "YO-talo: {} | {} | {} | {} | {}".format(r1.group('kokin'), r1.group('kotoisia'), r1.group('soppa'), r1.group('salaatti'), r1.group('kasvis')).decode("utf-8")
        #kur = "Kurniekka: {} | {} | {} | {} | {}".format(r2.group('kokin'), r2.group('kotoisia'), r2.group('soppa'), r2.group('salaatti'), r2.group('kasvis')).decode("utf-8")
    except: 
        return["No data. Try the next day."]
        
    return [kur, jou]
    #return [kur]
    
def sode(day=""):
    if day == "":
        day = w_day()[0]
    f_handle = urllib2.urlopen("http://www.sodexo.fi/ruokalistat/rss/weekly_rss/63/fi")
    pattern = r'<h2>(.*?)</h2>.+?<strong>(.*?)</strong>.+?<strong>(.*?)</strong>.+?<strong>(.*?)</strong>.+?<strong>(.*?)</strong>.+?<strong>(.*?)</strong>.+?<strong>(.*?)</strong>.+?<strong>(.*?)</strong>'
    f_list = re.findall(pattern, f_handle.read(), re.DOTALL)
    f_handle.close()
    ret = "Lol, Aalefille siitä"
    for d in f_list:
        if day.capitalize() in d:
            d = list(d)
            tmp = d.pop(0) + ": "
            ret = string.join(d, sep=', ')
    return ["Sodexo: " + ret]

def aalef(day=""):
    if day == "":
        day = w_day()[0]
    f_handle = urllib2.urlopen("http://www.aalef.fi/ruokalistat.php")
    pattern = r'">(Kurniekka|Ylioppilastalo).+?<tr class="huomio">.+?"2">%s.+?</b><br />(.*?)(?:</td>|<br />).+?</b><br />(.*?)(?:</td>|<br />).+?</b><br />(.*?)(?:</td>|<br />).+?</b><br />(.*?)(?:</td>|<br />).+?</b><br />(.*?)(?:</td>|<br />).+?(?:</b><br />(.*?)(?:</td>|<br />)|(?:huomio))' % day.capitalize()
    page = f_handle.read()
    f_handle.close()
    result = re.findall(pattern, page, re.DOTALL)
    l = []
    for i in range(len(result)):
        l.append(list(result[i]))
        for j in range(len(l[i])):
            l[i][j] = l[i][j].strip()
            #if len(l[i][j]) == 0:
                #del l[i][j]
        l[i] = l[i].pop(0) + ": " + string.join(l[i], ", ")
            
    if len(result) == 0:
        l = ["Kurniekka: Nothing found", "Ylioppilastalo: Nothing found"]
        return l
    else:
        return l

def imdb(title):
    """Fetches info about a movie according to title 
    from the imdb database.
    Returns a list containing a string."""
    page = urllib2.urlopen("http://www.imdbapi.com/?i=&t=" + title.replace(" ", "+")).read()
    table = json.loads(page)
    if table['Response'] == 'True':
        return ["%s (%s) http://www.imdb.com/title/%s" %(table['Title'], table['Year'], table['imdbID'])]
    else:
        return None


def ping():
    """Answers to servers PING request
    """
    return "PONG :Pong"

def yt(str1):
    q = str1.replace(" ", "+")
    prefix = "http://youtu.be/"
    pattern = r'"videoId": "(.+?)".+?"title": "(.+?)"'
    query = "https://www.googleapis.com/youtube/v3/search?part=snippet&order=relevance&q="+q+"&type=video&videoDefinition=high&key=" + API_KEY
    
    try:
        page = urllib2.urlopen(query).read()
        match = re.search(pattern, page, re.DOTALL)
        if match is not None:
            urli = prefix + match.group(1)
            return [urli + " Title: " + match.group(2)]
        else:
            return ["Could not find any matches"]
    
    except:
        print "Error in yt()"
        
def roller(die, num=1):
    urli = "http://www.random.org/integers/?format=plain&min=1&base=10&col=1"
    results = "&num=" + str(num)
    die_num = "&max=" + str(die)
    req = urllib2.Request(urli+results+die_num, None, headers)

    page = urllib2.urlopen(req)
    arr = page.read().split()
    c = 0
    for i in range(num):
        c += int(arr[i])
    
    return c
    
def roll_char():
    try:
        urli = "http://www.random.org/integers/?format=plain&min=1&base=10&col=1&num=22&max=6"
        req = urllib2.Request(urli, None, headers)
        page = urllib2.urlopen(req)
        arr = liter(page.read().split())
    except:
        return ["Timeout"]
        
    d = dict()
    d['str'] = arr.give(3)
    d['con'] = arr.give(3)
    d['dex'] = arr.give(3)
    d['siz'] = arr.give(2) + 6
    d['int'] = arr.give(2) + 6
    d['pow'] = arr.give(3)
    d['app'] = arr.give(3)
    d['edu'] = arr.give(3) + 3
    d['san'] = 5 * d['pow']
    d['luc'] = 5 * d['pow']
    d['ide'] = 5 * d['int']
    d['kno'] = 5 * d['edu']
    d['hp'] = int(math.ceil((d['con'] + d['siz']) / 2.0))
    d['mp'] = d['pow']
    d['db'] = bonus(d['str'] + d['siz'])
    
    d = """STR: %2d   DEX: %2d   INT: %2d   Idea: %2d
CON: %2d   APP: %2d   POW: %2d   Luck: %2d
SIZ: %2d   SAN: %2d   EDU: %2d   Know: %2d
HP:  %2d   MP:  %2d   DB: %3s""" % (d['str'], d['dex'], d['int'], d['ide'],
d['con'], d['app'], d['pow'], d['luc'],
d['siz'], d['san'], d['edu'], d['kno'],
d['hp'], d['mp'], d['db'])
    
    return d.split("\n")

def rollDnD():
    urli = "http://www.random.org/integers/?format=plain&min=1&base=10&col=1&num=24&max=6"
    req = urllib2.Request(urli, None, headers)
    page = urllib2.urlopen(req)
    arr = liter(page.read().split())
    s = "Roll: {0}  {1}  {2}  {3}  {4}  {5}".format(arr.giveBest3of4(), 
    arr.giveBest3of4(), arr.giveBest3of4(), arr.giveBest3of4(),
    arr.giveBest3of4(), arr.giveBest3of4())
    return [s]
    
def randomizer(str1):
    lst = []
    for i in str1.split(","):
        lst.append(i.strip())
    if len(lst) > 1:
        urli = "http://www.random.org/sequences/?min=1&max=%d&col=1&format=plain&rnd=new" % len(lst)
        req = urllib2.Request(urli)
        
        page = urllib2.urlopen(req)
        arr = page.read().split()
        
        return [lst[int(arr[0])-1]]
    else:
        return ["Give at least 2 arguments"]

        
def weather(msg):
"""API does not work anymore"""
    pattern = '\<city data\=\"(?P<kaupunki>.+?)\".+\<condition data\=\"(?P<tila>.+?)\".+\<temp_c data\=\"(?P<aste>.+?)\"'
    url = 'http://www.google.com/ig/api?weather=' + msg
    webpage = urllib2.urlopen(url)
    text = webpage.read()
    if text.find('problem') == -1:
        info = re.search(pattern, text)
        message1 = info.group('kaupunki') + ": " + info.group('aste') + "°C, " + info.group('tila') 
        return [message1]
    else:
        return ['No results']
        
def urlShortener(url):
    header = { "Content-Type" : "application/json"}
    data = json.dumps({'longUrl' : url })
    rurl = "https://www.googleapis.com/urlshortener/v1/url?key=" + API_KEY
    
    try:
        req = urllib2.Request(rurl, data, header)
        response = urllib2.urlopen(req)
        content = response.read()
        jsonParser = json.loads(content)
        return [jsonParser['id']]
    
    except:
        return ["Request error"]
        
def urlExpander(url):
    rurl = "https://www.googleapis.com/urlshortener/v1/url?shortUrl=http://" + url
    
    print rurl
    
    try:
        response = urllib2.urlopen(rurl)
        content = response.read()
        jsonParser = json.loads(content)
        return ["Redirects to: " + jsonParser['longUrl']]
    
    except:
        return ["Request error"]

def yttopic(str1):
    pattern = r'title": "(.+)"'
    if ("youtu.be/" in str1) or ("y2u.be/" in str1):
        matchobj = re.search(r"([a-zA-Z0-9_-]+$)", str1, re.I)
        suffix = matchobj.group(1)
    else:
        try:
            url = urlparse(str1)
            params = dict([part.split('=') for part in url[4].split('&')])
            suffix = params['v']
        except:
            print "Error: yttopic - urlparse"
            return []
           
    query = "https://www.googleapis.com/youtube/v3/videos?id="+suffix+"&key="+API_KEY+"&part=snippet&fields=items%28snippet%28title%29%29"
    try:
        page = urllib2.urlopen(query).read()
        match = re.search(pattern, page, re.DOTALL)
        if match is not None:
            return ["Youtube: "+ match.group(1).decode("utf-8")]
        else:
            print "Error: yttopic"
            return []
    except:
        print "Error: yttopic - exception.update"
        return []
### Utility methods ###       

def bonus(i):
    if i in range(2,13):
        return '-1D6'
    elif i in range(13,17):
        return '-1D4'
    elif i in range(17,25):
        return '+0'
    elif i in range(25,33):
        return '+1D4'
    elif i in range(33,41):
        return '+1D6'
              
def diceparser(str1):
    pattern = r'([0-9]+)?[dD]([0-9]+)'
    dice = re.sub(pattern, evaldice,str1)
    try:
        return [dice + " = " + str(eval(dice, {"__builtins__":None}, {}))]
    except NameError as e:
        return ["Error: "+e[0]]
       
def evaldice(matchobj):
    if matchobj.group(1) is None:
        frmt = "roller(" + matchobj.group(2) + ", 1)"
    else:
        frmt = "roller(" + matchobj.group(2) + ", " + matchobj.group(1) + ")"
    return str(eval(frmt, {"__builtins__":None}, {'roller': roller}))
	
def weather2(msg="lappeenranta"):
    now = datetime.now()
    delta = timedelta(minutes=15)
    db = sqlite3.connect("weather.db", detect_types=sqlite3.PARSE_DECLTYPES)
    c = db.cursor()
    
    c.execute("SELECT * FROM weather WHERE location='{0}'".format(msg.lower()))
    row = c.fetchone()
    if row is not None:
        if row[1] < now - delta:
            try:
                temp = parseWeather(fetchWeather(msg.lower()))
                c.execute(("UPDATE weather "+
                "SET timestamp='{0}', temp={1} "+
                "WHERE location='{2}'").format(now, temp, msg.lower()))
                db.commit()
            except LocationError as e:
                db.close()
                return [e.value]
            except Exception as e:
                db.close()
                print e
                return ["error"]
        else:
            temp = row[2]
    else:
        try:
            temp = parseWeather(fetchWeather(msg.lower()))
            c.execute(("INSERT INTO weather "+
            "VALUES('{0}', '{1}', {2})").format(msg.lower(), datetime.now(), temp))
            db.commit()
        except LocationError as e:
            db.close()
            return [e.value]
            
        
    db.close()
    return ["{0}: {1} C".format(msg.capitalize(), str(temp)).decode('cp1252')]

def fetchWeather(str):
    query = (("http://api.worldweatheronline.com/free/v1/"+
    "weather.ashx?q={0}&format=json&num_of_days="+
    "5&key="+WEATHER_API_KEY).format((str).replace("ä", "\xc3\xa4").replace("ö", "\xc3\xb6")))
    query = quote(query, safe="%/:=&?~#+!$,;'@()*[]\\")
    f_handle = urllib2.urlopen(query)
    return json.loads(f_handle.read())
    
def parseWeather(arr):
    if 'error' in arr['data'].keys():
        raise LocationError(arr['data']['error'][0]['msg'])
    return int(arr['data']['current_condition'][0]['temp_C'])
    


def main():
    import sys
    
    print eval(sys.argv[1])

if __name__ == "__main__":
    main()


    
