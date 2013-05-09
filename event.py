import sqlite3, sha, time, Cookie, os, datetime, hashlib
from bottle import get, post, route, debug, run, template, request
from bottle import static_file, url, response, redirect, install
from bottle_redis import RedisPlugin

import constants, account

def create_event(rdb):
    try:
        #get incoming fields
        etype = request.POST.get('visibility','').strip()
        eduedate = request.POST.get('datepicker','').strip()
        eventdesc = request.POST.get('event_description','').strip()
        ename = request.POST.get('event_name','').strip()
        print ename, eventdesc, eduedate, etype

        #get current user info
        user = request.get_cookie('account', secret='pass')
        user_id = str(int(rdb.zscore('accounts:usernames', user)))
        print user, user_id

        #Increment number of user's events, get new value:
        event_id = str(rdb.hincrby('account:' + user_id, 'numevents', 1))
        print event_id

        #Add event info to db
        rdb.hmset('event:' + user_id + ':' + event_id,
                 {  'ename' : ename, 
                    'eduedate' : eduedate, 
                    'eventdesc' : eventdesc,
                    'numinvited' : 0, 
                    'responded' : 0,
                    'numattending' : 1,
                    'estatus' : constants.STATUS_NEEDS_ATTENTION,
                    'etype' : constants.getEventTypeFromStr(etype), 
                    'numtasks' : 0 })
        print (user_id,  event_id)
        return (user_id,  event_id)
    except:
        return None




# This will be in create task or something

    
    #Loop to get all event tasks (if any)
    #Add them to the database:
    #tno = 1        #Initialize task number to be used in task key
    #rdb.hmset('task:' + ano + ':' + eno + ':' + tno,
             #{ 'event' : eno, 'tname' : tname, 'tinfo' : tinfo, 'tcost' : tcost,
               #'tstatus' : tstatus, 'numitems' : numitems })

        #Loop to get all task items (if any)
        #Add them to the database:
        #ino = 1    #initialize item number to be used in item key
        #rdb.hmset('item:' + ano + ':' + eno + ':' + tno + ':' + ino,
                #{ 'iname' : iname, 'icost' : icost, 'inotes' : inotes, 'istatus' : istatus })

    
