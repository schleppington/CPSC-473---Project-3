%rebase layout.tpl url=get_url, logged_in=logged_in

%#The list of public events contains the following information:
        %#event[0]  = Account Key
        %#event[1]  = Event Key
        %#event[2]  = Event Name
        %#event[3]  = Event Description
        %#event[4]  = Event Due Date
        %#event[5]  = Username


<form method="GET"> 
  <input id="refresh" type="submit" value="Refresh"/>
</form>

<div id="events">
	<div>
	<h3>All Public Events: </h3>

	%for event in events:
		<span class="list_item">
        <label for="event_owner">Event Created By: {{event[5]}}</label></br>
	      <label for="event_name">Event Name: {{event[2]}}</label><br/>
	      <label for="event_description">Event Description: {{event[3]}}</label><br/>
	      <label for="event_duedate">Date Of Event: {{event[4]}}</label><br/><br/>
        <a href="/event/{{event[0]}}/{{event[1]}}">details</a>
        </br></br>
	   </span>
	%end

	</div>
</div>
