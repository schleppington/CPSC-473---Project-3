%rebase layout.tpl url=get_url, logged_in=logged_in

<form method="GET">
  <input id="refresh" type="submit" value="Refresh"/>
</form>


<h2>Edit this Item</h2><br/>
<form action="/edititem/{{uid}}/{{eid}}/{{tid}}/{{iid}}" method="POST">
    <p>
        <label for="item_name">Item Name:</label><br/>
        <input type="text" name="item_name" size="30" value="{{iinfo['iname']}}"/><br/>
    </p>
    <p>
        <label for="item_info">Description:</label><br/>
        <input type="text" name="item_info" size="30" value="{{iinfo['inotes']}}"/><br/>
    </p>
    <p>
        <label for="item_cost">Cost ($):</label><br/>
        <input type="text" name="item_cost" size="30" value="{{iinfo['icost']}}"/><br/>
    </p>
    <p>
        <label for="status">Item Status:</label><br/>
%if iinfo['istatus'] == "0":
        <select name="status">
            <option value="Needs Attention" selected="selected">Needs Attention</option>
            <option value="In Progress">In Progress</option>
            <option value="Completed">Completed</option>
        </select>
%elif iinfo['istatus'] == "1":
        <select name="status">
            <option value="Needs Attention" >Needs Attention</option>
            <option value="In Progress" selected="selected">In Progress</option>
            <option value="Completed">Completed</option>
        </select>
%else:
        <select name="status">
            <option value="Needs Attention" >Needs Attention</option>
            <option value="In Progress">In Progress</option>
            <option value="Completed" selected="selected">Completed</option>
        </select>
%end
    </p><br/>
  <input id="edititem" type="submit" value="Submit Changes"/>
</form>
</div>
<script src="/ajax.js"></script>
