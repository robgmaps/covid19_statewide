# covid19_statewide
Django app to scrape data from California public health agencies.  Pulls data from Alameda, Sacramento, Riverside, Orange, Fresno, and San Joaquin counties, also Pasadena and Long Beach in LA.  

### Requires:
* healthycity/rda_dev.util for database connections and query helpers
* Splash instance running on localhost:8050
* Python requests library

### File notes:

1. _sql/statewide_county_tables.sql_ -  database table definitions
2. _./views.py_ - functions for pulling and handling the data
3. _management/commands/covid19_statewide_update_db.py_ - set configuration and run scraping functions for each geography
	* See CONFIG variable for tables, endpoints, and race/ethnicity mapping for each geography
4. Pull data for all included geographies with:  
`./manage.py covid19_statewide_update_db`

App runs on [Healthy City](https://www.healthycity.org) by [Advancement Project California](https://www.advancementprojectca.org).