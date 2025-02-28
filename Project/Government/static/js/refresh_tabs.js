const agri_tab = document.getElementById('agricultural-data-tab');
const vac_tab = document.getElementById('vaccination-data-tab');
const census_tab = document.getElementById('census-data-tab');
const environment_tab = document.getElementById('environment-data-tab');

agri_tab.addEventListener('click', () => {
    $.ajax({
        url: '/government/refresh_agricultural_data',
        type: 'GET',
        success: function (response) 
        {
            let crop_type = response['crop_type'];
            let avg_area_acres = response['avg_area_acres'];
            let total_area_acres = response['total_area_acres'];

            // update table rows with new data
            let table = document.getElementById('agricultural-data-table');
            let table_rows = table.getElementsByTagName('tr');
            for (let i = 1; i < Math.min(crop_type.length+1, table_rows.length); i++)
            {
                table_rows[i].getElementsByTagName('td')[0].innerHTML = crop_type[i-1];
                table_rows[i].getElementsByTagName('td')[1].innerHTML = avg_area_acres[i-1];
                table_rows[i].getElementsByTagName('td')[2].innerHTML = total_area_acres[i-1];
            }

            // remove extra table rows if needed
            if (table_rows.length > crop_type.length)
            {
                for (let i = crop_type.length + 1; i < table_rows.length; i++)
                {
                    table.deleteRow(i);
                }
            }
            else {
                // add additonal table row tr elements if needed, i.e. if crop_type.length > table_rows.length
                for (let i = table_rows.length; i <= crop_type.length; i++)
                {
                    let new_row = table.insertRow(-1);
                    let cell1 = new_row.insertCell(0);
                    let cell2 = new_row.insertCell(1);
                    let cell3 = new_row.insertCell(2);
                    cell1.innerHTML = crop_type[i-1];
                    cell2.innerHTML = avg_area_acres[i-1];
                    cell3.innerHTML = total_area_acres[i-1];
                }
            }


            console.log('Agricultural data refreshed');
        }
    });
});