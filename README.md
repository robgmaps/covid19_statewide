# covid19_statewide
Django app to scrape data from California public health agencies.  Pulls data from Alameda, Sacramento, Riverside, Orange, Fresno, and San Joaquin counties, also Pasadena and Long Beach in LA.

### Requires:
* healthycity/rda_dev.util for database connections and query helpers
* Splash instance running on localhost:8050
* Python requests library

See statewide_county_tables.sql in /sql folder for database table definitions.

Scraping functions in views.py.  Pull data for all inlcuded geographies with:
`./manage.py covid19_statewide_update_db`
