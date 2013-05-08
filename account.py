import sqlite3, sha, time, Cookie, os, datetime, hashlib
from bottle import get, post, route, debug, run, template, request
from bottle import static_file, url, response, redirect, install
from bottle_redis import RedisPlugin

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
