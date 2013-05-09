%rebase layout.tpl url=get_url, logged_in = logged_in
<h3>Sign Up</h3>
Enter your account information.<br/>
<form action="/newevent" method="POST">
    <p>
        <label for="event_name">Event Name:</label><br/>
        <input type="text" name="event_name" size="30"/><br/>
    </p>
    <p>
        <label for="event_description">Event Description:</label><br/>
        <textarea name="event_description" cols="60" rows="10"></textarea><br/>
    </p>
    <p>
        <label for="datepicker">Select A Date:</label><br/>
        <input type="text" id="datepicker" name="datepicker"/>
    </p>
    <p>
        <label for="visibility">Event Visibility:</label><br/>
        <select name="visibility">
            <option value="private">Private</option>
            <option value="public">Public</option>
        </select>
    </p>
    <p>
        <input type="submit" value="Create Event"><br/>
    </p>
</form>
