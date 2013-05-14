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

def create_item(rdb, user_id, event_id, task_id):
    #Get the item data from the form:
    iname = request.POST.get('item_name','').strip()
    icost = request.POST.get('item_cost','').strip()
    inotes = request.POST.get('item_notes','').strip()
    istatus = constants.STATUS_NEEDS_ATTENTION
    
    #Create new item_id
    item_id = int(rdb.hget('task:' + user_id + ':' + event_id + ':' + task_id, 'numitems')) + 1

    item_key = 'item:%s:%s:%s:%s' % (user_id, event_id, task_id, item_id)

    #Try to add the new item to the database.
    try:
        rdb.hmset(item_key,
                 { 'iname' : iname,
                   'icost' : icost,
                   'inotes' : inotes,
                   'istatus' : istatus })
        rdb.hset('task:' + user_id + ':' + event_id + ':' + task_id, 'numitems', item_id)
        
        
        #add item id to list of items for this event
        rdb.sadd('itemids:%s:%s:%s' % (user_id, event_id, task_id), item_id)
    except:
        return None

    return (user_id,  event_id, task_id)
