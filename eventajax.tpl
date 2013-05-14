<h3>Event </h3>
	%for key in sorted(row.iterkeys()):
	%#for event in row:   
	    <tr>
	       %# <td>{{key}}</td>
		<td>{{row[key]}}</td>
	%#        <td>{{ event }}</td>
	    </tr>
	%end