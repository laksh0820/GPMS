from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_user,login_required,current_user,logout_user
from flask_wtf import FlaskForm
from Project.utils.db_utils import get_db_connection
government_bp = Blueprint('government',__name__,url_prefix='/government', template_folder='templates', static_folder='static')



# Wrapper to ensure that the user is a gvovernment monitor or a admin
def government_monitor_required(inner_func):
    def wrapped_function_government_monitor(*args,**kwargs):
        if current_user.is_authenticated and current_user.role != 'government' and current_user.role != 'admin':
            flash("Please log in as Government Monitor to access this page",'error')
            return redirect(url_for(f'{current_user.role}.base'))
        return inner_func(*args,**kwargs)
    wrapped_function_government_monitor.__name__ = inner_func.__name__
    return wrapped_function_government_monitor    

# Wrapper to ensure that the user in verified
def verification_required(inner_func):
    def wrapper(*args,**kwargs):
        if current_user.is_verified == False:
            flash("Please wait for 24 hours until Admin verifies you",'warning')
            return redirect(url_for('base'))
        return inner_func(*args,**kwargs)
    wrapper.__name__ = inner_func.__name__
    return wrapper





@government_bp.route('/')
@login_required
@government_monitor_required
@verification_required
def base():
    return render_template('base.html')





def fetch_agricultural_data():
    conn = get_db_connection()
    db = conn.cursor()

    # Gather Information of Land covered by each crop type and Average Land covered by each crop type
    db.execute("""
                SELECT crop_type, avg(area_acres), sum(area_acres)
                FROM land_record
                GROUP BY crop_type;
            """)
    res = db.fetchall()

    # Extracting relevant information
    crop_type = [row[0] for row in res]
    avg_area_acres = [row[1] for row in res]
    total_area_acres = [row[2] for row in res]


    # Gather Information of Average Land covered by a citizen in the village
    db.execute("""
                SELECT avg(area_acres)
                FROM land_record;
            """)
    res = db.fetchall()
    if (res == None or res[0][0] == None):
        avg_area_acres_per_citizen = 0
    else:
        avg_area_acres_per_citizen = res[0][0]
    

    # Gather Information of average income of a farmer in the village
    db.execute("""
                SELECT avg(income)
                FROM citizen JOIN land_record USING (citizen_id);
                """)
    res = db.fetchall()
    if res == None or res[0][0] == None:
        avg_income_per_farmer = 0
    else:
        avg_income_per_farmer = res[0][0]


    db.close()
    conn.close()

    return crop_type, avg_area_acres, total_area_acres, avg_area_acres_per_citizen, avg_income_per_farmer



def fetch_vaccination():
    conn = get_db_connection()
    db = conn.cursor()

    # Gather Information of the number of citizens vaccinated with each vaccine type
    db.execute("""
                SELECT vaccine_type, count(citizen_id)
                FROM Vaccination JOIN Vaccines USING (vaccine_id)
                GROUP BY vaccine_type;
                """)
    res = db.fetchall()
    vaccine_type = [row[0] for row in res]
    num_citizens = [row[1] for row in res]


    # Gather Information of the number of citizens who have been vaccinated (taken at least one vaccine)
    db.execute("""
                SELECT count(distinct citizen_id)
                FROM Vaccination;
                """)
    res = db.fetchall()
    num_citizens_vaccinated = len(res)


    # Gather Information of the number of citizens who have been vaccinated by all the available vaccine types
    db.execute("""
                SELECT count(citizen_id)
                FROM Vaccination
                GROUP BY citizen_id
                HAVING count(vaccine_id) = (SELECT count(vaccine_id) FROM Vaccines);
                """)
    res = db.fetchall()
    num_citizens_vaccinated_all = len(res)


    # Gather Information of the number of citizens who have not been vaccinated
    db.execute("""
                SELECT count(citizen_id)
                FROM Citizen
                WHERE citizen_id NOT IN (SELECT citizen_id FROM Vaccination);
                """)
    res = db.fetchall()
    num_citizens_not_vaccinated = len(res)


    # Gather Information of the top 5 centers with the most number of vaccinations
    db.execute("""
                SELECT centers
                FROM Vaccines
                GROUP BY centers
                ORDER BY count(vaccine_id) DESC
                LIMIT 5;
                """)
    res = db.fetchall()
    top_5_centers = [row[0] for row in res]


    db.close()
    conn.close()

    return vaccine_type, num_citizens, num_citizens_vaccinated, num_citizens_vaccinated_all, num_citizens_not_vaccinated, top_5_centers



def fetch_census_data():
    conn = get_db_connection()
    db = conn.cursor()

    # Gather Information about the census_data
    db.execute("""
                SELECT year, population_male, population_female, births_male, 
                births_female, deaths_male, deaths_female, marriages 
                FROM census_data;
                """)
    res = db.fetchall()
    years = [row[0] for row in res]
    population_male = [row[1] for row in res]
    population_female = [row[2] for row in res]
    births_male = [row[3] for row in res]
    births_female = [row[4] for row in res]
    deaths_male = [row[5] for row in res]
    deaths_female = [row[6] for row in res]
    marriages = [row[7] for row in res]

    db.close()
    conn.close()

    return years, population_male, population_female, births_male, births_female, deaths_male, deaths_female, marriages



def fetch_environmental_data():
    conn = get_db_connection()
    db = conn.cursor()

    # Gather Information about the last 5 days 
    db.execute("""
                SELECT date, air_quality_index, water_quality, sanitation
                FROM environmental_data
                ORDER BY date DESC
                LIMIT 5;
                """)
    res = db.fetchall()
    dates = [row[0] for row in res]
    air_quality_index = [row[1] for row in res]
    water_quality = [row[2] for row in res]
    sanitation = [row[3] for row in res]


    # Gather Information about the worst 5 days in terms of air quality index
    db.execute("""
                SELECT date, air_quality_index
                FROM environmental_data
                ORDER BY air_quality_index DESC
                LIMIT 5;
               """)
    res = db.fetchall()
    air_dates = [row[0] for row in res]
    air_quality_index_5 = [row[1] for row in res]


    db.close()
    conn.close()

    return dates, air_quality_index, water_quality, sanitation, air_dates, air_quality_index_5





@government_bp.route('/refresh_agricultural_data')
@login_required
@government_monitor_required
@verification_required
def refresh_agricultural_data():
    crop_type, avg_area_acres, total_area_acres, avg_area_acres_per_citizen, avg_income_per_farmer = fetch_agricultural_data()

    return jsonify({'crop_type':crop_type,
                    'avg_area_acres':avg_area_acres,
                    'total_area_acres':total_area_acres,
                    'avg_area_acres_per_citizen':avg_area_acres_per_citizen,
                    'avg_income_per_farmer':avg_income_per_farmer})



@government_bp.route('/refresh_vaccination')
@login_required
@government_monitor_required
@verification_required
def refresh_vaccination():
    vaccine_type, num_citizens, num_citizens_vaccinated, num_citizens_vaccinated_all, num_citizens_not_vaccinated, top_5_centers = fetch_vaccination()

    return jsonify({'vaccine_type':vaccine_type,
                    'num_citizens':num_citizens,
                    'num_citizens_vaccinated':num_citizens_vaccinated,
                    'num_citizens_vaccinated_all':num_citizens_vaccinated_all,
                    'num_citizens_not_vaccinated':num_citizens_not_vaccinated,
                    'top_5_centers':top_5_centers})



@government_bp.route('/refresh_census_data')
@login_required
@government_monitor_required
@verification_required
def refresh_census_data():
    years, population_male, population_female, births_male, births_female, deaths_male, deaths_female, marriages = fetch_census_data()

    return jsonify({'years':years,
                    'population_male':population_male,
                    'population_female':population_female,
                    'births_male':births_male,
                    'births_female':births_female,
                    'deaths_male':deaths_male,
                    'deaths_female':deaths_female,
                    'marriages':marriages})



@government_bp.route('/refresh_environmental_data')
@login_required
@government_monitor_required
@verification_required
def refresh_environmental_data():
    dates, air_quality_index, water_quality, sanitation, air_dates, air_quality_index_5 = fetch_environmental_data()

    return jsonify({'dates':dates,
                    'air_quality_index':air_quality_index,
                    'water_quality':water_quality,
                    'sanitation':sanitation,
                    'air_dates':air_dates,
                    'air_quality_index_5':air_quality_index_5})





@government_bp.route('/dashboard')
@login_required
@government_monitor_required
@verification_required
def dashboard():
    crop_type, avg_area_acres, total_area_acres, avg_area_acres_per_citizen, avg_income_per_farmer = fetch_agricultural_data()

    vaccine_type, num_citizens, num_citizens_vaccinated, num_citizens_vaccinated_all, num_citizens_not_vaccinated, top_5_centers = fetch_vaccination()

    years, population_male, population_female, births_male, births_female, deaths_male, deaths_female, marriages = fetch_census_data()

    dates, air_quality_index, water_quality, sanitation, air_dates, air_quality_index_5 = fetch_environmental_data()

    return render_template('Government/dashboard.html', 
                           crop_type=crop_type, 
                           avg_area_acres=avg_area_acres, 
                           total_area_acres=total_area_acres, 
                           avg_area_acres_per_citizen=avg_area_acres_per_citizen,
                           avg_income_per_farmer=avg_income_per_farmer,
                           vaccine_type=vaccine_type,
                           num_citizens=num_citizens,
                           num_citizens_vaccinated=num_citizens_vaccinated,
                           num_citizens_vaccinated_all=num_citizens_vaccinated_all,
                           num_citizens_not_vaccinated=num_citizens_not_vaccinated,
                           top_5_centers=top_5_centers,
                           years=years,
                           population_male=population_male,
                           population_female=population_female,
                           births_male=births_male,
                           births_female=births_female,
                           deaths_male=deaths_male,
                           deaths_female=deaths_female,
                           marriages=marriages,
                           date=dates,
                           air_quality_index=air_quality_index,
                           water_quality=water_quality,
                           sanitation=sanitation,
                           air_date=air_dates,
                           air_quality_index_5=air_quality_index_5)
