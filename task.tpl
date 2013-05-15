%rebase layout.tpl url=get_url, logged_in=logged_in

<div id="events">
	<h3>Task </h3>
        <labelfor=event_name">Task Name: {{tinfo['tname']}}</label><br/>
        <label for="event_description">Task Description: {{tinfo['tinfo']}}</label><br/>
        <label for="event_status">Task Cost ($): {{tinfo['tcost']}}</label><br/>
        <label for="event_type">Task Type: {{tinfo['strtstatus']}}</label><br/>
    <form>
        <button type="submit" formaction="/edittask/{{uid}}/{{eid}}/{{tid}}" formmethod="GET">edit</button><br/>
    </form>

<h3>Current Items </h3>
%#print row['tasks']
%#if tinfo['items']: 
    %for item in tinfo['items']:
        <span class="list_item>
            <label for="task_name">Item Name: {{item[1]}}</label><br/>
            <label for="task_description">Item Info: {{item[3]}}</label><br/>
            <label for="task_cost">Item Cost: {{item[2]}}</label><br/>
            <label for="task_status">Item Status: {{item[4]}}</label><br/>
            <form >
                <button type="submit" formaction="/edititem/{{uid}}/{{eid}}/{{tid}}/{{item[0]}}" formmethod="GET">Edit</button>
                <button type="submit" formaction="/delitem/{{uid}}/{{eid}}/{{tid}}/{{item[0]}}" formmethod="POST">Delete</button>
            </form>
        </span>
    %end
</div>
<br><br/>
%if perms:
<h2>Add an item to this task</h2><br/>
<form action="/newitem/{{uid}}/{{eid}}/{{tid}}" method="POST">
    <p>
        <label for="item_name">Item Name:</label><br/>
        <input type="text" name="item_name" size="30"/><br/>
    </p>
    <p>
        <label for="item_info">Description:</label><br/>
        <input type="text" name="item_info" size="30"/><br/>
    </p>
    <p>
        <label for="item_cost">Cost ($):</label><br/>
        <input type="text" name="item_cost" size="30"/><br/>
    </p>
	<input id="newitem" type="submit" value="Add Item"/>
</form>
%end
<script src="/ajax.js"></script>
