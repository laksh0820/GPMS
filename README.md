# Gram Panchayat Management System

<h3>Group Members</h3>
<ul>
  <li>Aashirwad Mishra</li>
  <li>Dev Butani</li>
  <li>Kondapalli Mohan Balasubramanyam</li>
  <li>Lakshya Agrawal</li>
</ul>

<h2>Overview</h2>
<p>
    This project is a comprehensive web application designed for a village administration system. The system provides various functionalities for citizens, panchayat employees, system administrators, and government monitors to manage important services and data. Features include tax management, welfare schemes, vaccination updates, document services, and more, facilitating a better governance experience.
</p>

<h2>Functionalities</h2>

<h3>System Administrator</h3>
<ul>
    <li><strong>User Approval & Rejection</strong>: Approves or rejects new user registrations to ensure system security, including identifying potential scammers or phishers.</li>
    <li><strong>Full Access</strong>: Has access to all features and functionalities for all users in the system.</li>
</ul>

<h3>Panchayat Employees</h3>
<ul>
    <li><strong>Tax Management</strong>: View overdue taxes and mark taxes as paid for citizens.</li>
    <li><strong>Welfare Schemes</strong>: Revise, withdraw, or introduce new welfare schemes.</li>
    <li><strong>Vaccine Management</strong>: Update vaccine types, vaccination centers, and ensure safety for citizens.</li>
    <li><strong>Document Services</strong>: Manage the list of document services offered to citizens by adding, withdrawing, or revising services.</li>
    <li><strong>Expenses and Assets</strong>: Update records of panchayat expenses and asset installations, ensuring data is up-to-date.</li>
    <li><strong>Census and Environmental Data</strong>: Manage census data and environmental quality measures, including adding, updating, or removing records.</li>
</ul>

<h3>Citizens</h3>
<ul>
    <li><strong>Welfare Scheme Enrollment</strong>: Enroll in and monitor their welfare schemes.</li>
    <li><strong>Vaccination Requests</strong>: Request vaccines and view vaccination certificates.</li>
    <li><strong>Tax Status</strong>: Check and pay tax status to avoid penalties for tax evasion.</li>
    <li><strong>Government Services</strong>: Register for services like Aadhaar and Pan Card.</li>
    <li><strong>Service Monitoring</strong>: Keep track of enrolled services and ensure records are up-to-date.</li>
</ul>

<h3>Government Monitors</h3>
<ul>
    <li><strong>Data Analysis</strong>: Access various reports, including:
        <ul>
            <li><strong>Agricultural Data</strong>: Overview of village agriculture and citizen income.</li>
            <li><strong>Vaccination Reports</strong>: View vaccination statistics for the village.</li>
            <li><strong>Census Data</strong>: Analyze census data across multiple years.</li>
            <li><strong>Environmental Data</strong>: Get reports on environmental data and air quality indices.</li>
        </ul>
    </li>
</ul>

<h2>Login and Authentication</h2>
<ul>
    <li><strong>User Roles</strong>: Users can register with their respective roles (Citizen, Panchayat Employee, Government Monitor, or Admin) and must get their account verified by an admin after registration.</li>
    <li><strong>Security</strong>: The system implements a secure login mechanism with password hashing to ensure user privacy and system security.</li>
</ul>

<h2>Key Features</h2>

<h3>Automated Tax Updation</h3>
<p>Taxes are automatically assigned to users based on their income every month. A Panchayat employee can mark taxes as paid once the user pays, keeping the system updated.</p>

<h3>Password Hashing and Security</h3>
<p>Password hashes are securely saved before storing them in the database and validated during login to ensure data protection.</p>

<h3>Database Consistency</h3>
<p>To avoid data inconsistencies, all database updates are validated. Required fields are enforced in forms, and database attributes are set with NOT NULL constraints.</p>

<h2>Front-End Tools</h2>
<ul>
    <li><strong>Bootstrap 5.3.3</strong>: Used for styling HTML elements, ensuring a responsive and modern design.</li>
    <li><strong>CSS & JavaScript</strong>: Custom CSS and JS were added for page-specific functionality.</li>
    <li><strong>jQuery</strong>: Used for making HTTP GET requests to update data from the backend.</li>
</ul>

<h2>Back-End Tools</h2>
<ul>
    <li><strong>Flask</strong>: Flask was used as the web framework to support the front-end, including:
        <ul>
            <li><strong>User Authentication</strong>: Handled by Flask-Login for secure login and session management.</li>
            <li><strong>Template Rendering</strong>: Jinja2 templates render dynamic content based on user data.</li>
            <li><strong>Form Handling</strong>: WTForms used for handling form submission, validation, and CSRF protection.</li>
        </ul>
    </li>
</ul>

<h2>Installation and Setup</h2>

<h3>Prerequisites</h3>
<ul>
    <li>Python 3.x</li>
    <li>Flask</li>
    <li>jQuery</li>
    <li>Bootstrap</li>
    <li>PostgreSQL or any other relational database</li>
</ul>

<h3>Installation Steps</h3>
<ol>
    <li>Clone this repository.</li>
    <li>Install required Python libraries:
        <pre><code>pip install -r requirements.txt</code></pre>
    </li>
    <li>Set up the database and run the initialization scripts to create necessary tables.</li>
    <li>Configure the application with your database credentials.</li>
    <li>Run the application:
        <pre><code>python app.py</code></pre>
    </li>
</ol>

<h3>Running Locally</h3>
<p>Access the system by navigating to <a href="http://127.0.0.1:5000">http://127.0.0.1:5000</a> in your browser, or to the url provided in the generated logs if the host is on the same network as the one running the application.</p>
