function addRow() {
    // Get the table and input values
    var table = document.getElementById("myTable");
    var id = document.getElementById("id").value;
    var items = document.getElementById("items").value.split(",");

    // Create a new row and cells
    var newRow = table.insertRow(-1);
    var idCell = newRow.insertCell(0);
    var itemsCell = newRow.insertCell(1);

    // Set the cell values
    idCell.innerHTML = id;
    itemsCell.innerHTML = "[" + items.join(", ") + "]";

    // Clear the input values
    document.getElementById("id").value = "";
    document.getElementById("items").value = "";
}