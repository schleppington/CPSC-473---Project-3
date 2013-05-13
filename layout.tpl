<!DOCTYPE html>
<html>
<head>
<link rel="stylesheet" type="text/css" href="{{ url('static', path='styles.css') }}">
</head>
<body>
<div class="container">
    <div class="header">
        <h1>Welcome To Event Planner</h1>
        <p>
            <a href="/">Home</a>
            %if not logged_in:
            <a href="/login">Login</a>
            <a href="/signup">Sign Up</a>
            %else:
            <a href="/modifyacct">Modify Account</a>
            <a href="/inviteuser">Invite User</a>
            <a href="/newevent">New Event</a>
            <a href="/newtask">New Task</a>
            <a href="/newitem">New Item</a>
            <a href="/userhome">My Account</a>
            <a href="/logout">Logout</a>
            %end
        </p>
    </div>
    <div class="content">
        %include
    </div>
    <div class="footer">
        <p><span class="special">Created By:</span> Brian Boland, Chris Anderson, Christina Knotts, Kurtis Schlepp, Richard Fields, Angela Woelm</p>
        <p>&copy; 2013</p>
    </div>
</div>
</body>
</html>
