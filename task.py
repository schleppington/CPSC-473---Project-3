import sqlite3, sha, time, Cookie, os, datetime, hashlib
from bottle import get, post, route, debug, run, template, request
from bottle import static_file, url, response, redirect, install
from bottle_redis import RedisPlugin

import constants, account

#
#      Key: task:ano:eno:tno
#      Fields:      'tname' : tname,                        str
#                   'tinfo' : tinfo,                        str
#                   'tcost' : tcost,                        not sure what this is? money? double?
#                   'tstatus' : tstatus,                    int - from constatns
#                   'numitems' : numitems                   int
#

def create_task(rdb, user_id, event_id):
    try:
        #get incoming fields
        tname = request.POST.get('task_name','').strip()
        tinfo = request.POST.get('task_info','').strip()
        tcost = request.POST.get('task_cost','').strip()
        tstatus = constants.STATUS_NEEDS_ATTENTION #request.POST.get('task_status','').strip()

        #Increment numtasks to get new task_id
        task_id = int(rdb.hget('event:' + user_id + ':' + event_id, 'numtasks')) + 1

        task_key = 'task:%s:%s:%s' % (user_id, event_id, str(task_id))
        
        #Add event info to db
        rdb.hmset(task_key,
                 {  'tname' : tname, 
                    'tinfo' : tinfo, 
                    'tcost' : tcost,
                    'tstatus' : tstatus, 
                    'numitems' : 0
                 })
                 
        #update event's task count
        rdb.hincrby('event:' + user_id + ':' + event_id, 'numtasks', 1)
        
        #add task id to list of tasks for this event
        rdb.sadd('taskids:%s:%s' % (user_id, event_id), task_id)
        
    except:
        return None
    
    return (user_id,  event_id)
