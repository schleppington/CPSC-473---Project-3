%rebase layout.tpl url=get_url, logged_in=logged_in
<h3>Login</h3>
<p>Enter your username and password.</p>
<form action="/login" method="POST">
    <p>
        <label for="username">Username:</label><br/>
        <input type="text" name="username"><br/>
    </p>
    <p>
        <label for="password">Password:</label><br/>
        <input type="password" name="password">
    </p>
    <p>
        <input type="submit" value="Log In"><br/>
    </p>
</form>
