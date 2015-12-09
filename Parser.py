# -*- coding: iso-8859-15 -*-

import Helper
from re import search, compile
from imp import reload

googl = compile(r"(goo.gl/\w+)")
you2be = compile(r"(youtu.be/\S+|youtube.com/\S+|y2u.be/\S+)")

def privmsgformat(chan, msglist):
    f_list = []
    for msg in msglist:
        f_list.append("PRIVMSG %s :%s" %(chan, msg))
    return f_list

def servmsgformat(cmd, msg):
    f_list = []
    f_list.append("%s :%s" %(cmd, msg))
    return f_list
    

def parse(input_msg):
    argv = input_msg.split()
    argc = len(argv)
    global googl

    if argc == 0 or len(argv[0]) == 0:
        return [""]
    
    if argc > 0:
    
        if argv[0] == "PING":
            return ["PONG :Pong"]

        elif argv[0] == "ERROR":
            return [" ".join(argv)]
        
    if argc > 3:
        
        re_obj = search(r':(.+?)!', argv[0])
        if re_obj is not None:
            nick = re_obj.group(1)
        chan = argv[2]
        if chan == "mm_bot":
            try:
                chan = nick
            except:
                pass

        if argv[3] == ":.update":
            reload(Helper)
            return ["reload"]

        if argv[3] == ":.time":
            return privmsgformat(chan, Helper.w_day())
    
        if argv[3] == ":.safkat_wanha":
            if argc == 5:
                li = Helper.sode(argv[4]) + Helper.aalef(argv[4])
                return privmsgformat(chan, li)
            else:
                li = Helper.sode() + Helper.aalef()
                return privmsgformat(chan, li)
                
        if argv[3] == ":.safkat":
            if argc == 5:
                return privmsgformat(chan, Helper.safkat_rows(argv[4]))
            else:
                return privmsgformat(chan, Helper.safkat_rows())
                
        if argv[3] == ":.quit" and nick == 'MindM_':
            return servmsgformat("QUIT", "quit")

        if argv[3] == ":.coc-roll":
            return privmsgformat(chan, Helper.roll_char())
            
        if argv[3] == ":.dnd-roll":
            return privmsgformat(chan, Helper.rollDnD())
            
        goo_obj = googl.search(" ".join(argv[3:]))
        if goo_obj is not None:
            return privmsgformat(chan, Helper.urlExpander(goo_obj.group(1)))
            
        you_obj = you2be.search(" ".join(argv[3:]))
        if you_obj is not None:
            ret = Helper.yttopic(you_obj.group(1))
            if ret:
                return privmsgformat(chan, ret)
            else:
                return None
            
        


    if argc > 4:
            
        if argv[3] == ":.imdb":
            return privmsgformat(chan, Helper.imdb(argv[4]))
        
        if argv[3] == ":.join" and nick == 'MindM_':
            return servmsgformat("JOIN", argv[4])
    
        if argv[3] == ":.part" and nick == "MindM_":
            return servmsgformat("PART", argv[4])

        if argv[3] == ":.yt":
            return privmsgformat(chan, Helper.yt(" ".join(argv[4:])))

        if argv[3] == ":.roll":
            return privmsgformat(chan, Helper.diceparser(" ".join(argv[4:])))

        if argv[3] == ":.choose":
            return privmsgformat(chan, Helper.randomizer(" ".join(argv[4:])))
            
        if argv[3] == ":.saa" or argv[3] == ":.wtr":
            return privmsgformat(chan, Helper.weather2(" ".join(argv[4:])))
            pass

        if argv[3] == ":.shorten":
            return privmsgformat(chan, Helper.urlShortener(argv[4]))


    return None

if __name__ == "__main__":
    import sys
    print parse(" ".join(sys.argv[1:]))
