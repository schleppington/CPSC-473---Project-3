import sqlite3, sha, time, Cookie, os, datetime, hashlib
from bottle import route, post, debug, run, template, request, static_file, url, response, redirect, install, HTTPResponse
from bottle_redis import RedisPlugin
#from bottle.ext import sqlite


install(RedisPlugin())

#plugin = sqlite.Plugin(dbfile='todo.db')
#install(plugin)

#REDIS NOTES:
#ACCOUNT INFO (stored datatype TBD, but atm this is how it looks):
#account:no                                 // Hash of user's info ( firstname, lastname, useremail, username, password )
#accounts:usernames                         // Set of all usernames--usernames need to be unique, this will make searching quicker.
#accounts:emails                             // Set of all emails--emails need to be unique, this will make searching quicker.

#Account Details
#        accounts:no:password
#        accounts:no:username
#        accounts:no:salt
#        accounts:no:useremail
#        accounts:no:firstname
#        accounts:no:lastname
#        accounts:no:private                // set of all private events ids belonging to the user
#        accounts:no:public                 // set of all public events ids belonging to the user
#        accounts:no:invited                // set of all events user is invited to see

#example usage for getting account info:
#
# account_id = rdb.get('accounts:username')
# pw = rdb.get('accounts:no:password')
# un = rdb.get('accounts:no:username')
# st = rdb.get('accounts:no:salt')
# ue = rdb.get('accounts:no:useremail')
# fn = rdb.get('accounts:no:firstname')
# ln = rdb.get('accounts:no:lastname')
# pri = rdb.smembers('accounts:no:private')
# pub = rdb.smembers('accounts:no:public')
# inv = rdb.smembers('accounts:no:invited')

#planner:no:events                          //not sure what this is used for... - Brian

#EVENT INFO:
#planner:no:events
#event:num:tasks
#task:number:details                        // Details of task @ the given "number"
#publicevents                               // All public events

#event:no:owner                             // creator of this event
#event:no:admins                            // Set of username's able to modify this event (including owner)
#event:no:tasks                             // List of task numbers?
#event:no:description                       // description of the event
#event:no:status                            // status of the event
#                                           //  - 0 - needs attention
#                                           //  - 1 - in progress
#                                           //  - 2 - completed
#event:no:type                              // Type of event
#                                           //  - 0 - Public
#                                           //  - 1 - Private
#event:no:date                              // Date of the event
#event:no:attending                         // Set of username's attending
#event:no:invited                           // Set of username's able to see/attend this event if private

#TASK INFO:
#task:no:description                        // description of the task
#task:no:duedate                            // Due date of the task
#task:no:status                             // status of the task
#                                           //  - 0 - needs attention
#                                           //  - 1 - in progress
#                                           //  - 2 - completed


#publicevents                               // Set of All public event numbers



########################################################################
#                           Constants                                  #
########################################################################

STATUS_NEEDS_ATTENTION = 0
STATUS_IN_PROGRESS = 1
STATUS_COMPLETED = 2

EVENT_TYPE_PUBLIC = 0
EVENT_TYPE_PRIVATE = 1

def getStatusStrFromInt(num):
    if num == 0:
        return "Needs Attention"
    elif num == 1:
        return "In Progress"
    elif num == 2:
        return "Completed"
    else:
        return "ERROR FETCHING STATUS STRING FOR: " + num

def getEventTypeStrFromInt(num):
    if num == 0:
        return "Public"
    elif num == 1:
        return "Private"
    else:
        return "ERROR FETCHING EVENT TYPE STRING FOR: " + num

########################################################################
#                         View Functions                               #
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
    if logged_in:
        redirect('/userhome')
    else:
        return template('login.tpl', get_url=url, logged_in=logged_in)



@post('/login')
def login_submit(rdb):
    username = request.POST.get('username','').strip()
    password = request.POST.get('password','').strip()

    if check_login(rdb, username, password):
        response.set_cookie("account", username, secret='pass')
        redirect('/userhome')      
    else:
        logged_in = False
        return template('loginfail.tpl', get_url=url, logged_in=logged_in)



@get('/logout')
def logout_route():
    if isLoggedIn():
        response.delete_cookie("account", secret='pass')
    redirect('/login')



@route('/userhome')
def userhome_route():
    if isLoggedIn():
        logged_in = True
        user = request.get_cookie("account", secret='pass')
        user_id = rdb.get("accounts:" + user)

        #get list of private events for current user
        private_event_ids = rdb.smembers('accounts:' + user_id + ':private')
        lstprivates = []
        for i in private_event_ids:
            desc = rdb.get('events:' + i + ':description')
            stat = rdb.get('events:' + i + ':status')
            etype = rdb.get('events:' + i + ':type')
            date = rdb.get('events:' + i + ':date')
            lstprivates.insert(0, (i, desc, stat, etype, date) )

        #get list of invited to events for current user
        invited_event_ids = rdb.smembers('accounts:' + user_id + ':invited')
        lstinvited = []
        for i in invited_event_ids:
            desc = rdb.get('events:' + i + ':description')
            stat = rdb.get('events:' + i + ':status')
            etype = rdb.get('events:' + i + ':type')
            date = rdb.get('events:' + i + ':date')
            lstinvited.insert(0, (i, desc, stat, etype, date) )

        #get list of public events for current user
        public_event_ids = rdb.smembers('publicevents')
        lstpublics = []
        for i in public_event_ids:
            desc = rdb.get('events:' + i + ':description')
            stat = rdb.get('events:' + i + ':status')
            etype = rdb.get('events:' + i + ':type')
            date = rdb.get('events:' + i + ':date')
            lstpublics.insert(0, (i, desc, stat, etype, date) )

        return template('userhome.tpl',public_events=lstpublics,private_events=lstprivates, invited_events=lstinvited, get_url=url, logged_in=logged_in)
    else:
        redirect('/login')



@get('/signup')
def signup_route():
    if isLoggedIn():
        redirect('/userhome')
    else:
        logged_in = False 
        return template('signup.tpl', get_url=url, logged_in=logged_in)



@post('/signup')
def signup_submit(rdb):
    uFirst = request.POST.get('first_name','').strip()
    uLast = request.POST.get('last_name','').strip()
    uEmail = request.POST.get('email_address','').strip()
    uName = request.POST.get('username','').strip()
    uPass = request.POST.get('password','').strip()

    

#check for username uniqueness
    usernameexists = rdb.sismember('accounts:usernames', uName)
    if usernameexists:
        return template('loginfail.tpl', error="User name is already taken", logged_in=False)

    #check for email uniqueness
    emailexists = rdb.sismember('accounts:email', uEmail)
    if emailexists:
        return template('loginfail.tpl', error="Email is already in use", logged_in=False)

    try:
        #get next available user id number
        #int no;
        no = next_id(rdb)

        #get salt
        uSalt = str(datetime.datetime.now())
        saltedpw = uSalt + uPass
        #encrypt salted password
        encpw = hashlib.sha512(saltedpw).hexdigest()

        rdb.sadd('accounts:usernames', uName)
        rdb.sadd('accounts:emails', uEmail)
        no = str(no)
        rdb.set('accounts:' + no + ':password', encpw)
        rdb.set('accounts:' + no + ':username', uName)
        rdb.set('accounts:' + no + ':salt', uSalt)
        rdb.set('accounts:' + no + ':useremail', uEmail)
        rdb.set('accounts:' + no + ':firstname', uFirst)
        rdb.set('accounts:' + no + ':lastname', uLast)
        rdb.set('accounts:' + no + ':lastname', uLast)
        response.set_cookie("account", uName, secret='pass')
        redirect('/')
    except:
        return template('loginfail.tpl', get_url=url, logged_in=False)


########################################################################
#                         Helper Functions                             #
########################################################################

########################################################################
#next_id - gets the next account number to be used
#   param - rdb - redis db ojbect passed by plugin
#   return - int - the next account number that is ready for use
########################################################################

def next_id(rdb):

    #TODO: Randomize keys
    #Why do we need to randomize keys? - brian
    if rdb.hgetall('account:' + rdb.get('no')) :
        rdb.incr('no')
    else:
        rdb.setnx('no', 1)

    return  rdb.get('no')

########################################################################
#check_login - compares given username and password with stored info
#   param - rdb - redis db ojbect passed by plugin
#   param - username - users account name used
#   param - password - users password to compare
#   return - Boolean - True if account info matches
########################################################################

def check_login(rdb, username, password):
#get user's account number
    no = rdb.get("accounts:" + username)

    #get user's salt
    uSalt = rdb.get("accounts:" + no + ":salt")
    saltedpw = uSalt + password

    #encrypt salted password
    encpw = hashlib.sha512(saltedpw).hexdigest()

    #compare and return result
    if no and rdb.get("accounts:" + no + ":password") == encpw:
        return True

    return False

########################################################################
#isLoggedIn - checks to see if the current user is logged into our
#             system
#return - Boolean - True if the user is logged in
########################################################################

def isLoggedIn():
    if request.get_cookie("account", secret='pass'):
        return True
    else:
        return False



debug(True)
run(reloader=True)
