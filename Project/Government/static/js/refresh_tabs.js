const agri_tab = document.getElementById('agricultural-data-tab');
const vac_tab = document.getElementById('vaccination-tab');
const census_tab = document.getElementById('census-data-tab');
const environment_tab = document.getElementById('environmental-data-tab');

function toFixed(value, precision) {
    var power = Math.pow(10, precision || 0);
    return String(Math.round(value * power) / power);
}

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
                table_rows[i].getElementsByTagName('td')[1].innerHTML = toFixed(avg_area_acres[i-1],2);
                table_rows[i].getElementsByTagName('td')[2].innerHTML = toFixed(total_area_acres[i-1],2);
            }

            // remove extra table rows if needed
            if (table_rows.length > crop_type.length)
            {
                for (let i = table_rows.length - 1; i > crop_type.length; i++)
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
                    cell2.innerHTML = toFixed(avg_area_acres[i-1],2);
                    cell3.innerHTML = toFixed(total_area_acres[i-1],2);
                }
            }
            
            let avg_area_acres_per_citizen = response['avg_area_acres_per_citizen'];
            let avg_income_per_farmer = response['avg_income_per_farmer'];

            let p1 = document.getElementById('avg-area-citizen-para');
            let p2 = document.getElementById('avg-income-farmer-para');

            p1.innerHTML = 'Average Area (in acres) held by a citizen in the village is close to ' + toFixed(avg_area_acres_per_citizen,2); 
            p2.innerHTML = 'Average Income of a farmer in the village is close to ' + toFixed(avg_income_per_farmer,2);

            console.log('Agricultural data refreshed');
        }
    });
});

vac_tab.addEventListener('click', () => {
    $.ajax({
        url: '/government/refresh_vaccination',
        type: 'GET',
        success: function (response) 
        {
            let vaccine_type = response['vaccine_type'];
            let num_citizens = response['num_citizens'];
            let num_citizens_vaccinated = response['num_citizens_vaccinated'];
            let num_citizens_vaccinated_all = response['num_citizens_vaccinated_all'];
            let num_citizens_not_vaccinated = response['num_citizens_not_vaccinated'];
            let top_5_centers = response['top_5_centers']; 

            // update table rows with new data
            let table_vac = document.getElementById('vaccination-table');
            let table_rows = table_vac.getElementsByTagName('tr');
            for (let i = 1; i < Math.min(vaccine_type.length+1, table_rows.length); i++)
            {
                table_rows[i].getElementsByTagName('td')[0].innerHTML = vaccine_type[i-1];
                table_rows[i].getElementsByTagName('td')[1].innerHTML = num_citizens[i-1];
            }

            // remove extra table rows if needed
            if (table_rows.length > vaccine_type.length)
            {
                for (let i = table_rows.length - 1; i > vaccine_type.length; i++)
                {
                    table.deleteRow(i);
                }
            }
            else {
                // add additonal table row tr elements if needed, i.e. if vaccine_name.length > table_rows.length
                for (let i = table_rows.length; i <= vaccine_name.length; i++)
                {
                    let new_row = table_vac.insertRow(-1);
                    let cell1 = new_row.insertCell(0);
                    let cell2 = new_row.insertCell(1);
                    cell1.innerHTML = vaccine_type[i-1];
                    cell2.innerHTML = num_citizens[i-1];
                }
            }

            // update top 5 vaccination centers
            let table_top5 = document.getElementById('top5-centers-table');
            let table_rows_top5 = table_top5.getElementsByTagName('tr');
            for (let i = 1; i < Math.min(top_5_centers.length+1, table_rows_top5.length); i++)
            {
                table_rows_top5[i].getElementsByTagName('td')[0].innerHTML = top_5_centers[i-1];
            }

            // remove extra table rows if needed
            if (table_rows_top5.length > top_5_centers.length)
            {
                for (let i = table_rows_top5.length - 1; i > top_5_centers.length; i++)
                {
                    table_top5.deleteRow(i);
                }
            }
            else {
                // add additonal table row tr elements if needed, i.e. if top_5_centers.length > table_rows_top5.length
                for (let i = table_rows_top5.length; i <= top_5_centers.length; i++)
                {
                    let new_row = table_top5.insertRow(-1);
                    let cell1 = new_row.insertCell(0);
                    cell1.innerHTML = top_5_centers[i-1];
                }
            }

            let p1 = document.getElementById('atleast-one-para');
            let p2 = document.getElementById('all-vaccines-para');
            let p3 = document.getElementById('not-vaccinated-para');

            p1.innerHTML = 'Total Number of Citizens who have been administered atleast one vaccine is close to ' + num_citizens_vaccinated;
            p2.innerHTML = 'Total Number of Citizens who have been administered all the available vaccine types is close to ' + num_citizens_vaccinated_all;
            p3.innerHTML = 'Total Number of Citizens who have not been administered any vaccine is close to ' + num_citizens_not_vaccinated;

            console.log('Vaccination data refreshed');
        }
    });
});

census_tab.addEventListener('click', () => {
    $.ajax({
        url: '/government/refresh_census_data',
        type: 'GET',
        success: function (response) 
        {
            let years = response['years'];
            let population_male = response['population_male'];
            let population_female = response['population_female'];
            let births_male = response['births_male'];
            let births_female = response['births_female'];
            let deaths_male = response['deaths_male'];
            let deaths_female = response['deaths_female'];
            let marriages = response['marriages'];

            // update table rows with new data
            let table = document.getElementById('census-data-table');
            let table_rows = table.getElementsByTagName('tr');
            for (let i = 1; i < Math.min(years.length+1, table_rows.length); i++)
            {
                table_rows[i].getElementsByTagName('td')[0].innerHTML = years[i-1];
                table_rows[i].getElementsByTagName('td')[1].innerHTML = population_male[i-1];
                table_rows[i].getElementsByTagName('td')[2].innerHTML = population_female[i-1];
                table_rows[i].getElementsByTagName('td')[3].innerHTML = births_male[i-1];
                table_rows[i].getElementsByTagName('td')[4].innerHTML = births_female[i-1];
                table_rows[i].getElementsByTagName('td')[5].innerHTML = deaths_male[i-1];
                table_rows[i].getElementsByTagName('td')[6].innerHTML = deaths_female[i-1];
                table_rows[i].getElementsByTagName('td')[7].innerHTML = marriages[i-1];
            }

            // remove extra table rows if needed
            if (table_rows.length > years.length)
            {
                for (let i = table_rows.length - 1; i > years.length; i++)
                {
                    table.deleteRow(i);
                }
            }
            else {
                // add additonal table row tr elements if needed, i.e. if years.length > table_rows.length
                for (let i = table_rows.length; i <= years.length; i++)
                {
                    let new_row = table.insertRow(-1);
                    let cell1 = new_row.insertCell(0);
                    let cell2 = new_row.insertCell(1);
                    let cell3 = new_row.insertCell(2);
                    let cell4 = new_row.insertCell(3);
                    let cell5 = new_row.insertCell(4);
                    let cell6 = new_row.insertCell(5);
                    let cell7 = new_row.insertCell(6);
                    let cell8 = new_row.insertCell(7);
                    cell1.innerHTML = years[i-1];
                    cell2.innerHTML = population_male[i-1];
                    cell3.innerHTML = population_female[i-1];
                    cell4.innerHTML = births_male[i-1];
                    cell5.innerHTML = births_female[i-1];
                    cell6.innerHTML = deaths_male[i-1];
                    cell7.innerHTML = deaths_female[i-1];
                    cell8.innerHTML = marriages[i-1];
                }
            }

            console.log('Census data refreshed');
        }
    });
});

environment_tab.addEventListener('click', () => {
    $.ajax({
        url: '/government/refresh_environmental_data',
        type: 'GET',
        success: function (response) 
        {
            let dates = response['dates'];
            let air_quality_index = response['air_quality_index'];
            let water_quality_index = response['water_quality'];
            let sanitation = response['sanitation'];
            let air_dates = response['air_dates'];
            let air_quality_index_5 = response['air_quality_index_5'];

            // update table rows with new data
            let table = document.getElementById('last5-environmental-table');
            let table_rows = table.getElementsByTagName('tr');
            for (let i = 1; i < Math.min(dates.length+1, table_rows.length); i++)
            {
                table_rows[i].getElementsByTagName('td')[0].innerHTML = dates[i-1];
                table_rows[i].getElementsByTagName('td')[1].innerHTML = air_quality_index[i-1];
                table_rows[i].getElementsByTagName('td')[2].innerHTML = water_quality_index[i-1];
                table_rows[i].getElementsByTagName('td')[3].innerHTML = sanitation[i-1];
            }

            // remove extra table rows if needed
            if (table_rows.length > dates.length)
            {
                for (let i = table_rows.length - 1; i > dates.length; i++)
                {
                    table.deleteRow(i);
                }
            }
            else {
                // add additonal table row tr elements if needed, i.e. if dates.length > table_rows.length
                for (let i = table_rows.length; i <= dates.length; i++)
                {
                    let new_row = table.insertRow(-1);
                    let cell1 = new_row.insertCell(0);
                    let cell2 = new_row.insertCell(1);
                    let cell3 = new_row.insertCell(2);
                    let cell4 = new_row.insertCell(3);
                    cell1.innerHTML = dates[i-1];
                    cell2.innerHTML = air_quality_index[i-1];
                    cell3.innerHTML = water_quality_index[i-1];
                    cell4.innerHTML = sanitation[i-1];
                }
            }


            // update air quality index for the worst 5 days
            let table_air = document.getElementById('worst5-air-table');
            let table_rows_air = table_air.getElementsByTagName('tr');
            for (let i = 1; i < Math.min(air_dates.length+1, table_rows_air.length); i++)
            {
                table_rows_air[i].getElementsByTagName('td')[0].innerHTML = air_dates[i-1];
                table_rows_air[i].getElementsByTagName('td')[1].innerHTML = air_quality_index_5[i-1];
            }

            // remove extra table rows if needed
            if (table_rows_air.length > air_dates.length)
            {
                for (let i = table_rows_air.length - 1; i > air_dates.length; i++)
                {
                    table_air.deleteRow(i);
                }
            }
            else {
                // add additonal table row tr elements if needed, i.e. if air_dates.length > table_rows_air.length
                for (let i = table_rows_air.length; i <= air_dates.length; i++)
                {
                    let new_row = table_air.insertRow(-1);
                    let cell1 = new_row.insertCell(0);
                    let cell2 = new_row.insertCell(1);
                    cell1.innerHTML = air_dates[i-1];
                    cell2.innerHTML = air_quality_index_5[i-1];
                }
            }

            console.log('Environmental data refreshed');
        }
    });
});