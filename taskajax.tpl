<h3>Task </h3>
        <labelfor=event_name">Task Name: {{tinfo['tname']}}</label><br/>
        <label for="event_description">Task Description: {{tinfo['tinfo']}}</label><br/>
        <label for="event_status">Task Cost ($): {{tinfo['tcost']}}</label><br/>
        <label for="event_type">Task Type: {{tinfo['strtstatus']}}</label><br/>
    <form>
        %if perms:
        <button type="submit" formaction="/edittask/{{uid}}/{{eid}}/{{tid}}" formmethod="GET">edit</button><br/>
        %end
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
                %if perms:
                <button type="submit" formaction="/delitem/{{uid}}/{{eid}}/{{tid}}/{{item[0]}}" formmethod="POST">Delete</button>
                %end
            </form>
        </span>
    %end
