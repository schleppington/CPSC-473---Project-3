%rebase layout.tpl url=get_url, logged_in = logged_in
<h3>New Event</h3>
Enter Your Event's Details:<br/>
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
        <label for="status">Event Status:</label><br/>
        <select name="status">
            <option value="'Needs Attention">Needs Attention</option>
            <option value="In Progress">In Progress</option>
            <option value="Completed">In Progress</option>
        </select>
    </p>
    <p>
        <input type="submit" value="Create Event"><br/>
    </p>
</form>
