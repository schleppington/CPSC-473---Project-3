%rebase layout.tpl url=get_url, logged_in = logged_in
%#task_id and event_id are passed to this form.
<h3>Add A New Item</h3>
Enter The Item's Details<br/>
<form action="/newitem" method="POST">
    <p>
        <label for="item_name">Event Name:</label><br/>
        <input type="text" name="item_name" size="30"/><br/>
    </p>
    <p>
        <label for="item_notes">Event Description:</label><br/>
        <textarea name="item_notes" cols="60" rows="10"></textarea><br/>
    </p>
    <p>
        <label for="item_cost">Select A Date:</label><br/>
        <input type="text" name="item_cost"/>
    </p>
    <p>
        <label for="status">Event Status:</label><br/>
        <select name="status">
            <option value="'Needs Attention">Needs Attention</option>
            <option value="In Progress">In Progress</option>
            <option value="Completed">In Progress</option>
        </select>
    </p>
    <input type="hidden" name="event_id" value={{event_id}}/>
    <input type="hidden" name="task_id" value={{task_id}}/>
    <p>
        <input type="submit" value="Add Item"><br/>
    </p>
</form>
