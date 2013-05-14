%rebase layout.tpl url=get_url, logged_in=logged_in
%#event_id is passed to this form
<h3>Disallow A Person From Helping With This Event: </h3>
<form action="/remadmin" method="POST">
    <p>
        <label for="username">Enter the username of the person whose rights you would like to revoke:</label><br/>
        <input type="text" name="username" size="30"/><br/>
    </p>
    <input type="hidden" name="event_id" value={{event_id}}/>
    <p>
        <input type="submit" value="Add Task"><br/>
    </p>
</form>
