%rebase layout.tpl url=get_url, logged_in = logged_in
<h3>Sign Up</h3>
Enter your account information.<br/>
<form action="/signup" method="POST">
    <p>
        <label for="first_name">First Name:</label><br/>
        <input type="text" name="first_name"><br/>
    </p>
    <p>
        <label for="last_name">Last Name:</label><br/>
        <input type="text" name="last_name"><br/>
    </p>
    <p>
        <label for="email_address">Email Address:</label><br/>
        <input type="text" name="email_address"><br/>
    </p>
    <p>    
        <label for="username">Username:</label><br/>
        <input type="text" name="username"><br/>
    </p>
    <p>    
        <label for="password">Password:</label><br/>
        <input type="password" name="password"><br/>
    </p>
    <p>
        <input type="submit" value="Sign Up"><br/>
    </p>
</form>
