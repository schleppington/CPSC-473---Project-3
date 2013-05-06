import sqlite3, sha, time, Cookie, os
from bottle import route, post, debug, run, template, request, static_file, url, response, redirect, install
from bottle_redis import RedisPlugin
#from bottle.ext import sqlite


install(RedisPlugin())

#plugin = sqlite.Plugin(dbfile='todo.db')
#install(plugin)

#REDIS NOTES:
#ACCOUNT INFO (stored datatype TBD, but atm this is how it looks):
#accounts:username                          // where the username is the actual username... ex: accounts:TesterJester. 
#                                           // The value stored here is the key number.
#accounts:no:password                       // Password for the account @ the given "no"
#accounts:email                             // Set of all emails since emails need to be unique.

#EVENT INFO:
#planner:no:events
#event:num:tasks
#task:number:details                        // Details of task @ the given "number"
#publicevents                               // All public events



@route('/')
def default_route():
    logged_in = isLoggedIn()

    return template('default.tpl', get_url=url, logged_in=logged_in)



@route('/:path#.+#', name='static')
def static(path):
    return static_file(path, root='')



@route('/login')
def login_route():
    logged_in = isLoggedIn()

    return template('login.tpl', get_url=url, logged_in=logged_in)



@route('/logout')
def logout_route():
    if isLoggedIn():
        response.delete_cookie("account", secret='pass')
    redirect('/')



@post('/login') # or @route('/login', method='POST')
def login_submit(rdb):
    username = request.POST.get('username','').strip()
    password = request.POST.get('password','').strip()

    if check_login(rdb, username, password):
        response.set_cookie("account", username, secret='pass')
        redirect('/userhome')      
    else:
        logged_in = False
        return template('loginfail.tpl', get_url=url, logged_in=logged_in)



@route('/userhome')
def userhome_route():
    if isLoggedIn():
        logged_in = True
        return template('userhome.tpl', get_url=url, logged_in=logged_in)
    else:
        redirect('/login')



@route('/signup')
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

    if not rdb.sismember('account:emails', uEmail) and not rdb.get("accounts:" + uName):
        no = next_id(rdb)

        rdb.set('accounts:' + uName, no)
        rdb.sadd('account:emails', uEmail)
        rdb.set('accounts:' + no + ':password', uPass)
        rdb.set('accounts:' + no + ':username', uName)
        rdb.set('accounts:' + no + ':useremail', uEmail)
        rdb.set('accounts:' + no + ':firstname', uFirst)
        rdb.set('accounts:' + no + ':lastname', uLast)

        
        response.set_cookie("account", uName, secret='pass')
        redirect('/userhome')
    else:
        return template('loginfail.tpl', get_url=url, logged_in=False)



def next_id(rdb):

    #TODO: Randomize keys
    try:
        rdb.incr('no')
    except:
        rdb.setnx('no', 1)

    return  rdb.get('no')



def check_login(rdb, username, password):
    #TODO: implement salted password check
    no = rdb.get("accounts:" + username)
    if no and rdb.get("accounts:" + no + ":password") == password:
        return True

    return False



def isLoggedIn():
    if request.get_cookie("account", secret='pass'):
        return True
    else:
        return False



debug(True)
run(reloader=True)
