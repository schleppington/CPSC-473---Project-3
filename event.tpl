%rebase layout.tpl url=get_url, logged_in=logged_in

<form method="POST">
	<input id="refresh" type="submit" value="Refresh"/>
</form>

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
    %#for task in row['task_info']:
      %#  <label for="task_name">Task Name: {{tasks[1]}}</label><br/>
      %#  <label for="task_description">Task Info: {{tasks[2]}}</label><br/>
      %#  <label for="task_cost">Task Cost: {{tasks[3]}}</label><br/>
      %#  <label for="task_status">Task Status: {{tasks[4]}}</label><br/>

%#NEED TO UNPACK THE ITEMS FROM TASKS 
        %#print tasks[7]
        %#for item in tasks[xx]:
     %#   <label for="item_name">Item Name: {{numitem[1]}}</label><br/>
       %# <label for="item_cost">Item Cost: {{numitem[2]}}</label><br/>
       %# <label for="item_notes">Item Notes: {{numitem[3]}}</label><br/>
       %# <label for="item_status">Item Status: {{numitem[4]}}</label><br/>
        %#end
    %#end

<br><br/>

<form method="POST">
	<input id="newtask" type="submit" value="New Task"/>
</form>
</div>
<script src="/ajax.js"></script>
