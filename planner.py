import sqlite3, sha, time, Cookie, os
from bottle import route, post, debug, run, template, request, static_file, url, response, redirect

#app = bottle.Bottle()
#plugin = sqlite.Plugin(dbfile='todo.db')
#app.install(plugin)

@route('/')
def default_route():
    username = request.get_cookie("account", secret='pass')
    if username:
        logged_in = True
    else:
        logged_in = False
    return template('default.tpl', get_url=url, logged_in=logged_in)

@route('/:path#.+#', name='static')
def static(path):
    return static_file(path, root='')

@route('/login')
def login_route():
    username = request.get_cookie("account", secret='pass')
    if username:
        redirect('/userhome')
    else:
        logged_in = False
        return template('login.tpl', get_url=url, logged_in=logged_in)

@route('/logout')
def logout_route():
    username = request.get_cookie("account", secret='pass')
    if username:
        response.delete_cookie("account", secret='pass')
    redirect('/')

@post('/login') # or @route('/login', method='POST')
def login_submit():
    username = request.forms.get('username')
    password = request.forms.get('password')
    
    if check_login(username, password):
        response.set_cookie("account", username, secret='pass')
        redirect('/userhome')      
    else:
        logged_in = False
        return template('loginfail.tpl', get_url=url, logged_in=logged_in)

@route('/userhome')
def userhome_route():
    username = request.get_cookie("account", secret='pass')
    if username:
        logged_in = True
        return template('userhome.tpl', get_url=url, logged_in=logged_in)
    else:
        redirect('/login')

@route('/signup')
def login_route():
    username = request.get_cookie("account", secret='pass')
    if username:
        redirect('/userhome')
    else:
        logged_in = False 
        return template('signup.tpl', get_url=url, logged_in=logged_in)

def check_login(username, password):
    conn = sqlite3.connect('planner.db')
    c = conn.cursor()
    c.execute("SELECT password FROM users WHERE username = ?", [username])
    result = c.fetchone()
    if result == None:
        return False
    else:
        if (password == result[0]):
            return True
        else:
            return False

debug(True)
run(reloader=True)
