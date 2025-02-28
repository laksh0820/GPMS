// update table rows with new data
let table = document.getElementById('agricultural-data-table');
let table_rows = table.getElementsByTagName('tr');
for (let i = 1; i < Math.min(crop_type.length+1, table_rows.length); i++)
{
    table_rows[i].getElementsByTagName('td')[0].innerHTML = crop_type[i-1];
    table_rows[i].getElementsByTagName('td')[1].innerHTML = avg_area_acres[i-1];
    table_rows[i].getElementsByTagName('td')[2].innerHTML = total_area_acres[i-1];
}

// add additonal table row tr elements if needed, i.e. if crop_type.length > table_rows.length
for (let i = table_rows.length; i < crop_type.length+1; i++)
{
    let new_row = table.insertRow(-1);
    let cell1 = new_row.insertCell(0);
    let cell2 = new_row.insertCell(1);
    let cell3 = new_row.insertCell(2);
    cell1.innerHTML = crop_type[i-1];
    cell2.innerHTML = avg_area_acres[i-1];
    cell3.innerHTML = total_area_acres[i-1];
}