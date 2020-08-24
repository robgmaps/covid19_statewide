# covid19_statewide
Django app to scrape data from California public health agencies.  Pulls data from Alameda, Sacramento, Riverside, Orange, Fresno, and San Joaquin counties, also Pasadena and Long Beach in LA.

### Requires:
* healthycity/rda_dev.util for database connections and query helpers
* Splash instance running on localhost:8050
* Python requests library

See statewide_county_tables.sql in /sql folder for database table definitions.

*_./views.py_* - functions for handling the data

*_management/commands/covid19_statewide_update_db.py_* - set configuration and run scraping functions for each geography

See *CONFIG* variable in *_covid19_statewide_update_db.py_* for tables, endpoints, and race/ethnicity mapping for each geography


Scraping functions in views.py.  Pull data for all included geographies with:  
`./manage.py covid19_statewide_update_db`
