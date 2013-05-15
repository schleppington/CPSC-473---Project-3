<div>
	<h3>All Public Events: </h3>

	%for event in events:
		<span class="list_item">
        <label for="event_owner">Event Created By: {{event[5]}}</label></br>
	      <label for="event_name">Event Name: {{event[2]}}</label><br/>
	      <label for="event_description">Event Description: {{event[3]}}</label><br/>
	      <label for="event_duedate">Date Of Event: {{event[4]}}</label><br/><br/>
         <a href="/event/{{event[0]}}/{{event[1]}}">
            <button type="button">Details</button>
          </a>
        </br></br>
	   </span>
	%end

</div>
