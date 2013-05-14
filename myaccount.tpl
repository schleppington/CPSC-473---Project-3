%rebase layout.tpl url=get_url, logged_in = logged_in
%#This template will:
%#    Display user account info
%#    Display an option to allow user edit their account info
%#    Display number of events owned
%#    Display number of other people's events modifiable by user

%#acct contains the following user account information:
        %#acct[0]  = Username
        %#acct[1]  = First Name
        %#acct[2]  = Last Name
        %#acct[3]  = User Email
        %#acct[4]  = Number of events user owns
        %#acct[5]  = Number of events user is invited to modify

<h3>{{acct[0]}}'s Information:</h3>

<div>
    First Name: {{acct[1]}} <br/>
    Last Name: {{acct[2]}} <br/>
    User Email: {{acct[3]}} <br/><br/>
    <form action="/modifyacct" method="GET">
        <label for="modify_acct">If you would like to modify your account information, please click:  </label>
        <input type="submit" value="Modify Account"><br/>
    </form>
</div>

<br/>

<div>
    Number of events I am planning: {{acct[4]}}<br/>
    Number of events I am assisting with: {{acct[5]}}<br/>
</div>
