function convertToJson() {
    // Get the table rows
    var table = document.getElementById("myTable");
    var rows = table.rows;

    var data = [];

    // Loop through the rows and add the data to the array
    for (var i = 1; i < rows.length; i++) {
        var row = rows[i];
        var id = row.cells[0].innerHTML;
        var items = row.cells[1].innerHTML.replace("[", "").replace("]", "").split(", ");
        data.push({id: parseInt(id), items: items});
    }

    // Convert the data to JSON and display it in an alert dialog
    var json = JSON.stringify({"items": data});
    return json
}

function submit() {
    let json_items = convertToJson()
    const socket = new WebSocket(`ws://0.0.0.0:1111/`);

    socket.addEventListener('open', (event) => {
        // Create an example JSON object and integer value
        const intValue = 0;

        // Stringify the JSON data and integer value
        const jsonData = JSON.stringify(json_items);
        const intData = intValue.toString();

        // Send the data as a WebSocket message
        socket.send(jsonData);
        socket.send(intData);
    });


    socket.addEventListener('message', function (event) {
        console.log('Received message from server:', event.data);
    });

    socket.addEventListener('close', function (event) {
        console.log('WebSocket connection closed');
    });


    socket.onmessage = function (event) {
        if (event.data !== "Processing completed.") {
            console.log(event.data);
            document.getElementById("messages").innerHTML += event.data + '</br>';
        }
    }

}