import sqlite3, sha, time, Cookie, os, datetime, hashlib
from bottle import get, post, route, debug, run, template, request
from bottle import static_file, url, response, redirect, install
from bottle_redis import RedisPlugin

import constants, account

#
#      Key: task:ano:eno:tno
#      Fields:      'tname' : tname,                        str
#                   'tinfo' : tinfo,                        str
#                   'tcost' : tcost,                       double
#                   'tstatus' : tstatus,                    int - from constatns
#                   'numitems' : numitems                   int
#

def create_item(rdb):
    #Get the item data from the form:
    event_id = request.POST.get('event_id','').strip()
    task_id = request.POST.get('task_id','').strip()
    iname = request.POST.get('item_name','').strip()
    icost = request.POST.get('item_cost','').strip()
    inotes = request.POST.get('item_notes','').strip()

    #get current user info
    user = request.get_cookie('account', secret='pass')
    user_id = str(int(rdb.zscore('accounts:usernames', user)))

    #item_id = current number of task items +1
    #   Options:
    #       1:  item_id = str(rdb.hincrby('task:' + user_id + ':' + event_id + ':' + task_id, 'numitems',1))
    #           Can use hincrby to increment the number of event tasks before
    #           update takes place. If task insertion fails, will need to
    #           decrement number of event tasks.
    #       2:  item_id = int(rdb.hget('task:' + user_id + ':' + event_id + ':' + task_id, 'numitems')) + 1
    #           Can retrieve the number of event tasks, then increment the
    #           result by 1. If task insertion is successful, will need to
    #           increment the number of event tasks.
    
    item_key = 'item:%s:%s:%s' % (user_id, event_id, task_id, item_id)

    #Try to add the new item to the database.
    try:
        rdb.hmset(item_key,
                 { 'iname' : iname,
                   'icost' : icost,
                   'inotes' : inotes,
                   'istatus' : constants.getStatusIntFromStr(tstatus) })
    except:
        #TODO: error item insertion failed.
        #If hincrby was used, need to undo:
        #ino = int(item_id) - 1
        #rdb.hset('task:' + user_id + ':' + event_id + ':' + task_id, { 'numitems' : ino} )
        return None

return item_key
