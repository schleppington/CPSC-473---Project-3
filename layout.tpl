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
            <a href="/">Home</a>&nbsp;&nbsp;&nbsp;&nbsp;
            %if not logged_in:
            <a href="/login">Login</a>&nbsp;&nbsp;&nbsp;&nbsp;
            <a href="/signup">Sign Up</a>&nbsp;&nbsp;&nbsp;&nbsp;
            %else:
            <a href="/userhome">My Account</a>&nbsp;&nbsp;&nbsp;&nbsp;
            <a href="/logout">Logout</a>&nbsp;&nbsp;&nbsp;&nbsp;
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
