%rebase layout.tpl url=get_url, logged_in=logged_in

<h2>Edit this task</h2><br/>
<form action="/edittask/{{uid}}/{{eid}}/{{tid}}" method="POST">
    <p>
        <label for="task_name">Task Name:</label><br/>
        <input type="text" name="task_name" size="30" value="{{tinfo['tname']}}"/><br/>
    </p>
    <p>
        <label for="task_info">Description:</label><br/>
        <input type="text" name="task_info" size="30" value="{{tinfo['tinfo']}}"/><br/>
    </p>
    <p>
        <label for="task_cost">Cost ($):</label><br/>
        <input type="text" name="task_cost" size="30" value="{{tinfo['tcost']}}"/><br/>
    </p>
    <p>
        <label for="status">Task Status:</label><br/>
%if tinfo['tstatus'] == "0":
        <select name="status">
            <option value="Needs Attention" selected="selected">Needs Attention</option>
            <option value="In Progress">In Progress</option>
            <option value="Completed">Completed</option>
        </select>
%elif tinfo['tstatus'] == "1":
        <select name="status">
            <option value="Needs Attention" >Needs Attention</option>
            <option value="In Progress" selected="selected">In Progress</option>
            <option value="Completed">Completed</option>
        </select>
%else:
        <select name="status">
            <option value="Needs Attention" >Needs Attention</option>
            <option value="In Progress">In Progress</option>
            <option value="Completed" selected="selected">Completed</option>
        </select>
%end
    </p><br/>
  <input id="edittask" type="submit" value="Submit Changes"/>
</form>
</div>
