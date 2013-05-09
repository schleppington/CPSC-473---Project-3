import sqlite3, sha, time, Cookie, os, datetime, hashlib
from bottle import get, post, route, debug, run, template, request
from bottle import static_file, url, response, redirect, install
from bottle_redis import RedisPlugin

import constants, account

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
                    'estatus' : constants.STATUS_NEEDS_ATTENTION,
                    'etype' : constants.getEventTypeFromStr(etype), 
                    'numtasks' : 0 })
        
        #add event to its respective lists
        if etype == constants.EVENT_TYPE_PUBLIC:
            #add event to public list
            rdb.sadd('events:public', 'event:' + user_id + ':' + event_id)
            #add event to user's public list
            rdb.sadd('account:' + user_id + ':public', 'event:' + user_id + ':' + event_id)
        else:
            #add even to user's private list
            rdb.sadd('account:' + user_id + ':private', 'event:' + user_id + ':' + event_id)
        
        #add owner to admin list for this event
        rdb.sadd('eventadmins' + user_id + ':' + event_id, user_id)
        
        return (user_id,  event_id)
    except:
        return None



########################################################################
#create_task - create a new task entry in redis db
#   param   - rdb - redis db ojbect passed by plugin
#           - user_id - a string value containing the id number of the
#                       user
#           - event_id - a string value containing the id number of the
#                        event the new task will be referenced to.
#   return  - task_key - a string containing the task key if creation is
#                        successful;
#             None if creation failed
########################################################################
def create_task(rdb, user_id, event_id):
    #Get the task data from the form:
    #tname = request.POST.get('TODO','').strip()
    #tinfo = request.POST.get('TODO','').strip()
    #tcost = request.POST.get('TODO','').strip()

    #Increment the current number of tasks in the current event.
    task_id = str(rdb.hincrby('event:' + user_id + ':' + event_id, 'numtasks', 1))

    #Try to add the new task to the database.
    try:
        task_key = 'task:' + user_id + ':' + event_id + ':' + task_id
        rdb.hmset(task_key,
                 { 'event' : event_id, 
                    #'tname' : tname, 
                    #'tinfo' : tinfo, 
                    #'tcost' : tcost,
                    'tstatus' : constants.STATUS_NEEDS_ATTENTION,
                    'numitems' : 0 })
        return task_key
    except:
        #TODO: error task insertion failed.
        tno = int(task_id) - 1
        rdb.hset('event:' + user_id + ':' + event_id, { 'numtasks' : tno } )
        return None



########################################################################
#create_item - create a new item entry in redis db
#   param   - rdb - redis db ojbect passed by plugin
#           - user_id - a string value containing the id number of the
#                       user
#           - event_id - a string value containing the id number of the
#                        event the new task item will be referenced to.
#           - task_id - a string value containing the id number of the
#                       task the new item will be referenced to.
#   return  - item_key - a string containing the item key if creation is
#                        successful;
#             None if creation failed
########################################################################
def create_item(rdb, user_id, event_id, task_id):
    #Get the item data from the form:
    #iname = request.POST.get('TODO','').strip()
    #icost = request.POST.get('TODO','').strip()
    #inotes = request.POST.get('TODO','').strip()

    #Increment current number of items in the current task.
    item_id = str(rdb.hincrby('task:' + user_id + ':' + event_id + ':' + task_id, 'numitems',1))
    
    #Try to add the new item to the database.
    try:
        item_key = 'item:' + user_id + ':' + event_id + ':' + task_id + ':' + item_id
        rdb.hmset(item_key,
                 { #'iname' : iname,
                    #'icost' : icost,
                    #'inotes' : inotes,
                    'istatus' : constants.STATUS_NEEDS_ATTENTION })
        return item_key
    except:
        #TODO: error item insertion failed.
        ino = int(item_id) - 1
        rdb.hset('task:' + user_id + ':' + event_id + ':' + task_id, { 'numitems' : ino} )
        return None
