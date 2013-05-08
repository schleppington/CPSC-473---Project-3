import sqlite3, sha, time, Cookie, os, datetime, hashlib
from bottle import get, post, route, debug, run, template, request
from bottle import static_file, url, response, redirect, install
from bottle_redis import RedisPlugin

import account

install(RedisPlugin())


########################################################################
#                         Redis Notes                         #
########################################################################
#   Hash tables:
#
#      Key: account:no
#       Fields:     'firstname' : firstname,
#                   'lastname' : lastname,
#                   'useremail' : useremail, 
#                   'username' : username,
#                   'password' : password, 
#                   'salt' : salt
#
#      Key: event:ano:eno
#       Fields:		'ename' : ename, 
#                   'eduedate' : eduedate, 
#                   'eventdesc' : eventdesc,
#                   'numinvited' : numinvited, 
#                   'responded' : responded,
#                   'numattending' : numattending, 
#                   'public' : True/False,
#                   'estatus' : 'estatus', 
#                   'etype' : etype, 
#                   'numtasks' : numtasks
#
#      Key: task:ano:eno:tno
#      Fields:      'tname' : tname, 
#                   'tinfo' : tinfo, 
#                   'tcost' : tcost, 
#                   'tstatus' : tstatus,
#                   'numitems' : numitems  
#
#      Key: item:ano:eno:tno:ino
#      Fields:		'iname' : iname, '
#                   'icost' : icost, 
#                   'inotes' : inotes, 
#                   'istatus' : istatus
#
#   Sets:
#       accounts:usernames                          // Sorted Set of all usernames
#       accounts:emails                             // Set of all user emails
#       account:no:public                           // Set of all public events this account owns
#       account:no:private                          // Set of all private events this account owns
#       account:no:invited                          // Set of all events this account has been invited to help plan
#       events:public                               // Set of all public events
#       eventadmins:owneracctno:eventno             // Set of all accounts allowed to modify this event
#
#   CONSIDERATIONS:
#       Invitations, there are 2 meanings here:
#           1: Event numinvited -   This is the number of invitations the user has sent out.
#           2: Account invited -    This is a set of events the user has been invited to help plan.
########################################################################


########################################################################
#                         Constants                         #
########################################################################

#QUESTION: Would it be easier to store the string value inside the field?
STATUS_NEEDS_ATTENTION = 0
STATUS_IN_PROGRESS = 1
STATUS_COMPLETED = 2

EVENT_TYPE_PUBLIC = 0
EVENT_TYPE_PRIVATE = 1

def getStatusStrFromInt(num):
    if num == 0:
        return 'Needs Attention'
    elif num == 1:
        return 'In Progress'
    elif num == 2:
        return 'Completed'
    else:
        return 'ERROR FETCHING STATUS STRING FOR: ' + num

def getEventTypeStrFromInt(num):
    if num == 0:
        return 'Public'
    elif num == 1:
        return 'Private'
    else:
        return 'ERROR FETCHING EVENT TYPE STRING FOR: ' + num

########################################################################
#                         View Functions                         #
########################################################################

@get('/')
def default_route():
    logged_in = isLoggedIn()

    return template('default.tpl', get_url=url, logged_in=logged_in)



@get('/:path#.+#', name='static')
def static(path):
    return static_file(path, root='')



@get('/login')
def login_route():
    logged_in = account.isLoggedIn()
    if logged_in:
        redirect('/userhome')
    else:
        return template('login.tpl', get_url=url, logged_in=logged_in)



@post('/login')
def login_submit(rdb):
    username = request.POST.get('username','').strip()
    password = request.POST.get('password','').strip()

    if account.check_login(rdb, username, password):
        response.set_cookie('account', username, secret='pass', max_age=600)
        redirect('/userhome')
    else:
        return template('loginfail.tpl', get_url=url, logged_in=False)



@get('/logout')
def logout_route():
    if account.isLoggedIn():
        response.delete_cookie('account', secret='pass')
    redirect('/login')



@route('/userhome')
def userhome_route(rdb):
   if account.isLoggedIn():
       user = request.get_cookie('account', secret='pass')
       user_id = str(int(rdb.zscore('accounts:usernames', user)))

       #get list of private events for current user
       lstprivates = getUserEventsList(rdb, user_id, 'private')

       #get list of invited to events for current user
       lstinvited = getUserEventsList(rdb, user_id, 'invited')

       #get list of public events for current user
       lstpublics = getUserEventsList(rdb, user_id, 'public')

       return template('userhome.tpl',public_events=lstpublics,private_events=lstprivates,
                        invited_events=lstinvited, get_url=url, logged_in=True)
   else:
       redirect('/login')



@get('/signup')
def signup_route():
    if account.isLoggedIn():
        redirect('/userhome')
    else:
        logged_in = False 
        return template('signup.tpl', get_url=url, logged_in=logged_in)



@post('/signup')
def signup_submit(rdb):    
    result = account.create_account(rdb)
    print result
    if result:
        return template('userhome.tpl', get_url=url, logged_in=result)
    else:
        return template('loginfail.tpl', get_url=url, logged_in=result)
 
 

#@route('/newEvent')
#def newEvent_route():
    #if isLoggedIn():
        #TODO: Create template for new event, point to that template here insted of 'userhome.tpl'
        #return template('userhome.tpl', get_url=url, logged_in=logged_in)
    #else:
        #redirect('/login')



#@post('/newEvent')
#def newEvent_submit(rdb):
    #TODO: Create template for new event, grab info from fields
    #numtasks = number of tasks created for the event
    #public = boolean value from form--user decides whether they want the event seen by everyone or not.

    #Increment number of user's events, get new value:
    #eno = str(rdb.hincrby('account:' + ano, 'numevents', 1))
    
    #Add event info to db
    #rdb.hmset('event:' + ano + ':' + eno,
             #{ 'ename' : ename, 'eduedate' : eduedate, 'eventdesc' : eventdesc,
               #'numinvited' : None, 'responded' : None,
               #'numattending' : None, 'public' : public, 'estatus' : 0,
               #'etype' : etype, 'numtasks' : numtasks })

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



########################################################################
#                         Helper Functions                         #
########################################################################

########################################################################
#getUserEventsList - gets the event description, event status, event type, and event due date
#   param   - rdb - redis db ojbect passed by plugin
#           - no - account number
#           - pkey - partial key used to access a set (will either be 'private', 'public', or 'invited')
#   return  - lst - the list of information gathered
########################################################################

def getUserEventsList(rdb, no, pkey):
    lst = []
    event_ids = rdb.smembers('account:' + no + ':' + pkey)
    
    #Use the ID's to retrieve the event information we're looking for
    if event_ids and event_ids != 'None':
        for i in event_ids:
            info = rdb.hget('event:' + no + ':' + str(i), { 'eventdesc', 'estatus', 'etype', 'eduedate' })
            info.insert(i)
            lst.insert(0,  (info))
    
    return lst








debug(True)
run(reloader=True)
