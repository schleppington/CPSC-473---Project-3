%rebase layout.tpl url=get_url, logged_in = logged_in
%#event_id is passed to this form.
<h3>Add A New Task</h3>
Enter The Task's Details<br/>
<form action="/newtask" method="POST">
    <p>
        <label for="task_name">Event Name:</label><br/>
        <input type="text" name="task_name" size="30"/><br/>
    </p>
    <p>
        <label for="task_description">Event Description:</label><br/>
        <textarea name="task_description" cols="60" rows="10"></textarea><br/>
    </p>
    <p>
        <label for="task_cost">Select A Date:</label><br/>
        <input type="text" name="task_cost"/>
    </p>
    <p>
        <label for="task_status">Event Status:</label><br/>
        <select name="task_status">
            <option value="'Needs Attention">Needs Attention</option>
            <option value="In Progress">In Progress</option>
            <option value="Completed">In Progress</option>
        </select>
    </p>
    <input type="hidden" name="event_id" value={{event_id}}/>
    <p>
        <input type="submit" value="Add Task"><br/>
    </p>
</form>
