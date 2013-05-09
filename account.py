import sqlite3, sha, time, Cookie, os, datetime, hashlib
from bottle import get, post, route, debug, run, template, request
from bottle import static_file, url, response, redirect, install
from bottle_redis import RedisPlugin



########################################################################
#create_account - create a new account record in the database with the 
#                 posted data from the form
#   param - rdb - redis db ojbect passed by plugin
#   return - boolean - True if the account was successfully created
########################################################################
def create_account(rdb):
    firstname = request.POST.get('first_name','').strip()
    lastname = request.POST.get('last_name','').strip()
    useremail = request.POST.get('email_address','').strip()
    username = request.POST.get('username','').strip()
    password = request.POST.get('password','').strip()
    
    print firstname, lastname, username, password
    no = 0
    #check for username uniqueness
    if rdb.zscore('accounts:usernames', username):
        return template('loginfail.tpl', error='User name is already taken', logged_in=False)

    #check for email uniqueness
    if rdb.sismember('accounts:emails', useremail):
        return template('loginfail.tpl', error='Email is already in use', logged_in=False)

    logged_in = False
    try:
        #get the next available user id number
        no = str(next_id(rdb))

        #get salt
        uSalt = str(datetime.datetime.now())
        saltedpw = uSalt + password

        #encrypt salted password
        encpw = hashlib.sha512(saltedpw).hexdigest()

        #set username and user_id in accounts:usernames
        rdb.zadd('accounts:usernames', username, no)
        #set email
        rdb.sadd('accounts:emails', useremail)

        rdb.hmset('account:' + no,
                 {  'firstname' : firstname, 
                    'lastname' : lastname,
                    'useremail' : useremail, 
                    'username' : username,
                    'password' : encpw, 
                    'salt' : uSalt,
                    'numevents' : 0 })
        
        response.set_cookie('account', username, secret='pass', max_age=600)
        logged_in = True
    except:
        #rdb.zrem('accounts:usernames', username)
        #rdb.srem('accounts:emails', useremail)
        #rdb.delete('account:' + strno)
        #response.delete_cookie('account', secret='pass')
        return False
    return logged_in


########################################################################
#check_login - compares given username and password with stored info
#   param - rdb - redis db ojbect passed by plugin
#   param - username - users account name used
#   param - password - users password to compare
#   return - Boolean - True if account info matches
########################################################################

def check_login(rdb, username, password):
    #get user's account number
    no = rdb.zscore('accounts:usernames', username)
    print no
    if not no:
        return False

    no = str(int(no))
    #get user's salt
    uSalt = rdb.hget('account:' + no, 'salt')
    saltedpw = uSalt + password

    #encrypt salted password
    encpw = hashlib.sha512(saltedpw).hexdigest()

    #compare and return result
    if rdb.hget('account:' + no, 'password') == encpw:
        return True

    return False



########################################################################
#isLoggedIn - checks to see if the current user is logged into our
#             system
#return - Boolean - True if the user is logged in
########################################################################

def isLoggedIn():
    if request.get_cookie('account', secret='pass'):
        return True
    else:
        return False



########################################################################
#next_id - gets the next account number to be used
#   param - rdb - redis db ojbect passed by plugin
#   return - int - the next account number that is ready for use
########################################################################

def next_id(rdb):
    if rdb.hgetall('account:' + str(rdb.get('no'))) :
        rdb.incr('no')
    else:
        rdb.setnx('no', 1)

    return  rdb.get('no')



