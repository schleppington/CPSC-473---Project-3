%#template to generate a HTML table from a list of tuples (or list of lists, or tuple of tuples or ...)

%rebase layout.tpl url=get_url, logged_in=logged_in

<form method="GET">
	<input id="refresh" type="submit" value="Refresh"/>
</form>

<div id="events">
	<h3>Event </h3>
	%for key in sorted(row.iterkeys()):
	%#for event in row:   
	    <tr>
	       %# <td>{{key}}</td>
		<td>{{row[key]}}</td>
	%#        <td>{{ event }}</td>
	    </tr>
	%end
</div>
<script src="/ajax.js"></script>