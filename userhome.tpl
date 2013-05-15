%rebase layout.tpl url=get_url, logged_in=logged_in

%#Each list of events (public / private / inviated) will contain the following information:
        %#eventinfo[0]  = Event Key
        %#eventinfo[1]  = Event Name
        %#eventinfo[2]  = Event Description 
        %#eventinfo[3]  = Event Status
        %#eventinfo[4]  = Event Type
        %#eventinfo[5]  = Event Due Date

<div id="events">
	<div>
	<h3>My Public Events: </h3>
	%for public in public_events:
		<span class="list_item">
	    <label for="event_name">Event Name: {{public[1]}}</label><br/>
	    <label for="event_description">Event Description: {{public[2]}}</label><br/>
	    <label for="event_duedate">Date Of Event: {{public[5]}}</label><br/><br/>
        <a href="/event/{{uid}}/{{public[0]}}">details</a>
        <form action="/delevent/{{uid}}/{{public[0]}}" method="POST">
            <button type="submit">Delete</button>
        </form>
        </br></br>
	   </span>
	%end
	</div>
	<div>
	<h3>My Private Events:</h3>
	%for private in private_events:
		<span class="list_item">
	    <label for="event_name">Event Name: {{private[1]}}</label><br/>
	    <label for="event_description">Event Description: {{private[2]}}</label><br/>
	    <label for="event_duedate">Date Of Event: {{private[5]}}</label><br/><br/>
        <a href="/event/{{uid}}/{{private[0]}}">details</a>
        <form action="/delevent/{{uid}}/{{private[0]}}" method="POST">
            <button type="submit">Delete</button>
        </form>
        </br></br>
	    </span>
	%end
	</div>
<br style="clear:left" />
	<h3>Events I Can Assist With:</h3>
	%for invited in invited_events:
		<span class="list_item">
	    <label for="event_name">Event Name: {{invited[1]}}</label><br/>
	    <label for="event_description">Event Description: {{invited[2]}}</label><br/>
	    <label for="event_duedate">Date Of Event: {{invited[5]}}</label><br/><br/>
        <a href="/event/{{uid}}/{{invited[0]}}">details</a>
        <form action="/delevent/{{uid}}/{{invited[0]}}" method="POST">
            <button type="submit">Delete</button>
        </form>
        </br></br>
	   </span>
	%end

	
</div>
<script src="/ajax.js"></script>
