# crud
A Python web app that demonstrates Create Update Delete (CRUD) functions. This web based app demonstrates in a Pythonic way creating, updating and deleting structured information (that's why it's  called a 'CRUD' app). It allows users to sign in using a secure password and view a list of birds by their English  name. It displays other information about birds, as selected by the user, in an additional pane on the same page.

Some of the features of the app of interest to users are:

	Fully responsive user interface for mobile, tablet, or desktop
	Substring search of English name
	Paginated listing by English name
	Example data set includes more than 13,000 birds
	"Remember me" capable sign in


Some features more of interest to administrators:

	User authorization includes friendly/nickname
	Database initialization UI (no external tool required)
	Database initialization includes adding the Administrator user
	Only Salted and hashed passwords stored in a database
	Cross Site Subscription Forgery (CRSF) protection
	Cookie based sessions
	SQL Injection protection


Some languages, technologies, and frameworks employed are:

	Python - for all server implementaion
	Javascript - for all browser scripting
	SQL - for all database access
	SQLite disk based database storage, query, importing etc.
	SQLAlchemy database Object Request Manager (ORM) framework
	Flask - Python web container/server framework
	Jinja server side templating
	RESTful application interface
	Efficient, paginated, XHR data retreival in JSON format
	Bootstrap CSS
	Angular (1.x) Model, Views, and Controllers
	BCrypt encryption libraray with timing attack protection
	Sessions use cookies that are cryptographically signed
