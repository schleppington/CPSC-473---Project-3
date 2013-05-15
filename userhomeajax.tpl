<div>
	<h3>My Public Events: </h3>
	%for public in public_events:
		<span class="list_item">
	    <label for="event_name">Event Name: {{public[1]}}</label><br/>
	    <label for="event_description">Event Description: {{public[2]}}</label><br/>
	    <label for="event_duedate">Date Of Event: {{public[5]}}</label><br/><br/>
        <a href="/event/{{uid}}/{{public[0]}}">
		<button type="button">Details</button>
	</a>
	<a href="/editevent/{{uid}}/{{public[0]}}">
		<button type="button">Edit</button>
	</a>
        <form >
            <button type="submit" formaction="/delevent/{{uid}}/{{public[0]}}" formmethod="POST">Delete</button>
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
	 <a href="/event/{{uid}}/{{private[0]}}">
		<button type="button">Details</button>
	</a>
	<a href="/editevent/{{uid}}/{{private[0]}}">
		<button type="button">Edit</button>
	</a>
        <form >
             <button type="submit" formaction="/delevent/{{uid}}/{{private[0]}}" formmethod="POST">Delete</button>
        </form>
        </br></br>
	    </span>
	%end
	</div>
<br style="clear:left" />
    <div>
	<h3>Events I Can Assist With:</h3>
	%for admin in admin_events:
		<span class="list_item">
	    <label for="event_name">Event Name: {{admin[1]}}</label><br/>
	    <label for="event_description">Event Description: {{admin[2]}}</label><br/>
	    <label for="event_duedate">Date Of Event: {{admin[5]}}</label><br/><br/>
	<a href="/event/{{uid}}/{{admin[0]}}">
		<button type="button">Details</button>
	</a>
	<a href="/editevent/{{uid}}/{{admin[0]}}">
		<button type="button">Edit</button>
	</a>
        <form >
            <button type="submit" formaction="/delevent/{{uid}}/{{admin[0]}}" formmethod="POST">Delete</button>
        </form>
        </br></br>
	   </span>
	%end
    </div>
    <div>
	<h3>Events I've Been Invited To:</h3>
	%for invited in invited_events:
		<span class="list_item">
	    <label for="event_name">Event Name: {{invited[1]}}</label><br/>
	    <label for="event_description">Event Description: {{invited[2]}}</label><br/>
	    <label for="event_duedate">Date Of Event: {{invited[5]}}</label><br/><br/>
	<a href="/event/{{uid}}/{{invited[0]}}">
		<button type="button">Details</button>
	</a>
        </br></br>
	   </span>
	%end
    </div>
