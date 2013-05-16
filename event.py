import sqlite3, sha, time, Cookie, os, datetime, hashlib
from bottle import get, post, route, debug, run, template, request
from bottle import static_file, url, response, redirect, install
from bottle_redis import RedisPlugin

import constants, account

#      Key: event:ano:eno
#       Fields:		'ename' : ename,                        str
#                   'eduedate' : eduedate,                  datetime
#                   'eventdesc' : eventdesc,                str
#                   'numinvited' : numinvited,              int
#                   'responded' : responded,                int
#                   'numattending' : numattending,          int
#                   'estatus' : 'estatus',                  int - from constants
#                   'etype' : etype,                        int - from constants
#                   'numtasks' : numtasks                   int

########################################################################
#create_event - create a new event entry in redis db
#   param   - rdb - redis db ojbect passed by plugin
#   return  - touple - (user's id, events id) if creation is successful
#                      None if creation failed
########################################################################
def create_event(rdb):
    try:
        #get incoming fields
        etype = request.POST.get('visibility','').strip()
        estatus = request.POST.get('status','').strip()
        eduedate = request.POST.get('datepicker','').strip()
        eventdesc = request.POST.get('event_description','').strip()
        ename = request.POST.get('event_name','').strip()
        #print ename, eventdesc, eduedate, etype

        #get current user info
        user = request.get_cookie('account', secret='pass')
        user_id = str(int(rdb.zscore('accounts:usernames', user)))
        #print user, user_id

        #Increment number of user's events, get new value:
        event_id = str(rdb.hincrby('account:' + user_id, 'numevents', 1))
        #print event_id

        #Add event info to db
        rdb.hmset('event:' + user_id + ':' + event_id,
                 {  'ename' : ename, 
                    'eduedate' : eduedate, 
                    'eventdesc' : eventdesc,
                    'numinvited' : 0, 
                    'responded' : 0,
                    'numattending' : 1,
                    'estatus' : constants.getStatusIntFromStr(estatus),
                    'etype' : constants.getEventTypeFromStr(etype), 
                    'numtasks' : 0 })
        
        #add event to its respective lists
        if constants.getEventTypeFromStr(etype) == constants.EVENT_TYPE_PUBLIC:
            #add event to public list
            rdb.sadd('events:public', 'event:' + user_id + ':' + event_id)
            #add event to user's public list
            rdb.sadd('account:' + user_id + ':public', 'event:' + user_id + ':' + event_id)
        else:
            #add even to user's private list
            rdb.sadd('account:' + user_id + ':private', 'event:' + user_id + ':' + event_id)
        
        #add owner to admin list for this event
        rdb.sadd('event:' + user_id + ':' + event_id + ':admins', user_id)
        
        return (user_id,  event_id)
    except:
        return None



def edit_event(rdb, user_id, event_id):
    try:
        #get incoming fields
        etype = request.POST.get('visibility','').strip()
        estatus = request.POST.get('status','').strip()
        eduedate = request.POST.get('datepicker','').strip()
        eventdesc = request.POST.get('event_description','').strip()
        ename = request.POST.get('event_name','').strip()

        task_key = 'task:%s:%s' % (user_id, event_id)

        rdb.hmset(task_key,
            {  'ename' : ename,                        
                   'eduedate' : eduedate,                  
                   'eventdesc' : eventdesc,                
                   'numinvited' : numinvited,              
                   'responded' : responded,                
                   'numattending' : numattending,          
                   'estatus' : 'estatus',                  
                   'etype' : etype,               
             })
        return (user_id, event_id, task_id)
    except:
        return None


########################################################################
#invUserToEvent - Gives another user rights to view the event.
#   param   - rdb - redis db ojbect passed by plugin
#   return  - useremail - The email address retrieved from the form and
#                         added to the list of people invited.
########################################################################
def invUserToEvent(rdb, owner_id, event_no):
    username = request.POST.get('username', '').strip()
    Add = request.POST.get('perm','').strip()
    print Add
    #Retrieve user account number from database
    admin_no = str(rdb.zscore('accounts:usernames', username))

    if Add=="Invite":   
        #If account was found, add account to admin list:
        if admin_no:
            event = 'event:' + str(owner_id) + ':' + str(event_no)
            rdb.sadd('account:' + admin_no + ':invite', event)
    
        rdb.sadd('event:' + str(owner_id) + ':' + str(event_no) + ':invited', username)

    else:
        if admin_no:
            event = 'event:' + str(owner_id) + ':' + str(event_no)
            rdb.sadd('account:' + admin_no + ':admin', event)
            rdb.sadd('event:' + str(owner_id) + ':' + str(event_no) + ':admins', username)
        else:
            return False
    
    return username


########################################################################
#addAdminToEvent - Gives another user rights to modify event.
#   param   - rdb - redis db ojbect passed by plugin
#   return  - username - The username of the account added.
########################################################################
def addAdminToEvent(rdb):
    username = request.POST.get('username','').strip()
    owner_id = request.POST.get('owner_id','').strip()
    event_no = request.POST.get('event_no','').strip()

    #Retrieve user account number from database
    admin_no = str(rdb.zscore('accounts:usernames', username))

    #If account was found, add account to admin list:
    if admin_no:
        event = 'event:' + owner_id + ':' + event_no
        rdb.sadd('account:' + admin_no + ':admin', event)
        rdb.sadd('event:' + owner_id + ':' + event_no + ':admins', username)
        return username
    else:
        return False


########################################################################
#remAdminFromEvent - Removes another user's rights to modify event.
#   param   - rdb - redis db ojbect passed by plugin
#   return  - username - The username of the account removed.
########################################################################
def remAdminFromEvent(rdb):
    username = request.POST.get('username','').strip()
    owner_id = request.POST.get('owner_id','').strip()
    event_no = request.POST.get('event_no','').strip()

    #Retrieve user account number from database
    admin_no = str(rdb.zscore('accounts:usernames', username))

    #If account was found, add account to admin list:
    if admin_no:
        event = 'event:' + owner_id + ':' + event_no
        rdb.srem('account:' + admin_no + ':admin', event)
        rdb.srem('event:' + owner_id + ':' + event_no + ':admins', username)
        return username
    else:
        return False


########################################################################
#getAllPublicEvents - Creates a list of all public events
#   param   - rdb - redis db ojbect passed by plugin
#   return  - lst - a list containing the public events.
########################################################################
def getAllPublicEvents(rdb):
    lst = []
    event_ids = rdb.smembers('events:public')

    #Use the ID's to retrieve the event information we're looking for
    if event_ids and event_ids != 'None':
        for i in event_ids:
            acct_id = i.split(":")[1]
            event_id = i.split(":")[2]
            username = rdb.zrange('accounts:usernames', int(acct_id) - 1, int(acct_id) -1)
            info = []
            info.insert(0, acct_id)
            info.insert(1, event_id)
            #inserting each field individually to make sure order is as expected.
            info.insert(2, rdb.hget(i, 'ename'))
            info.insert(3, rdb.hget(i, 'eventdesc'))
            info.insert(4, rdb.hget(i, 'eduedate'))
            info.insert(5, username[0])
            lst.insert(0,  (info))
    
    return lst
