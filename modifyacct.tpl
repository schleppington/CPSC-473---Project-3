%rebase layout.tpl url=get_url, logged_in = logged_in
<h3>Modify Account</h3>
Change your account information:<br/>
<form action="/modifyacct" method="POST">
    <p>
        <label for="first_name">Change First Name: (currently {{acct[0]}})</label> <br/>
        <input type="text" name="first_name"><br/>
    </p>
    <p>
        <label for="last_name">Change Last Name: (currently {{acct[1]}})</label><br/>
        <input type="text" name="last_name"><br/>
    </p>
    <p>
        <label for="email_address">Change Email Address: (currently {{acct[2]}})</label><br/>
        <input type="text" name="email_address"><br/>
    </p>
    <p>    
        <label for="password">Change Password:</label><br/>
        <input type="password" name="password"><br/>
    </p>
    <p>
        <input type="submit" value="Submit Changes"><br/>
    </p>
</form>