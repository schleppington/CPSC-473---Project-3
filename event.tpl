%rebase layout.tpl url=get_url, logged_in=logged_in

<div id="events">
	<h3>Event </h3>
        <labelfor=event_name">Event Name: {{row['ename']}}</label><br/>
        <label for="event_description">Event Description: {{row['eventdesc']}}</label><br/>
        <label for="event_status">Event Status: {{row['stretype']}}</label><br/>
        <label for="event_type">Event Type: {{row['strestatus']}}</label><br/>
        <label for="event_duedate">Date Of Event: {{row['eduedate']}}</label><br/>
        <label for="event_numinvited">Number of Invitations: {{row['numinvited']}}</label><br/>
        <label for="event_responded">Number of Responses: {{row['responded']}}</label><br><br/>
        	

%#NEED TO UNPACK THE TASKS FROM EVENTS
%#Tasks will contain the following:
        %#taskinfo[0]    = Event Key
        %#taskinfo[1]    = Task Name
        %#taskinfo[2]    = Task Info ??
        %#taskinfo[3]    = Task Cost
        %#taskinfo[4]    = Task Status      
        %#taskinfo[5]    = Task items--'numitems'

<h3>Current Tasks </h3>
%#print row['tasks']
%#if row['tasks']: 
    %for task in row['tasks']:
        <span class="list_item>
            <label for="task_name">Task Name: {{task[1]}}</label><br/>
            <label for="task_description">Task Info: {{task[2]}}</label><br/>
            <label for="task_cost">Task Cost: {{task[3]}}</label><br/>
            <label for="task_status">Task Status: {{task[4]}}</label><br/>
	    <a href="/task/{{uid}}/{{eid}}/{{task[0]}}">
		<button type="button">Details</button>
	    </a>
            <form >
                <button type="submit" formaction="/deltask/{{uid}}/{{eid}}/{{task[0]}}" formmethod="POST">Delete</button>
            </form>
	    
        </span>
    %end
%#NEED TO UNPACK THE ITEMS FROM TASKS 
        %#print tasks[7]
        %#for item in tasks[xx]:
     %#   <label for="item_name">Item Name: {{numitem[1]}}</label><br/>
       %# <label for="item_cost">Item Cost: {{numitem[2]}}</label><br/>
       %# <label for="item_notes">Item Notes: {{numitem[3]}}</label><br/>
       %# <label for="item_status">Item Status: {{numitem[4]}}</label><br/>
        %#end
    %#end
</div>
<br><br/>
<h2>Add a task to this event</h2><br/>
<form action="/newtask/{{uid}}/{{eid}}" method="POST">
    <p>
        <label for="task_name">Task Name:</label><br/>
        <input type="text" name="task_name" size="30"/><br/>
    </p>
    <p>
        <label for="task_info">Description:</label><br/>
        <input type="text" name="task_info" size="30"/><br/>
    </p>
    <p>
        <label for="task_cost">Cost ($):</label><br/>
        <input type="text" name="task_cost" size="30"/><br/>
    </p>
	<input id="newtask" type="submit" value="Add Task"/>
</form>
<script src="/ajax.js"></script>
