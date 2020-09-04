# ./manage.py covid19_statewide_update_db
from django.core.management.base import BaseCommand, CommandError
from time import time
from covid19_statewide.views import arc2pg, arc2pg_orange, arc2pg_fresno, arc2pg_pasadena, pbi2pg_alameda, pbi2pg_long_beach, arc2pg_sacramento_known_unknown, csv2pg, html2pg_tests_county
import json, redis

# LA Race Names
# "American Indian or Alaska Native"
# "Asian"
# "Black/African American"
# "Latino/Hispanic"
# "Native Hawaiian or Other Pacific Islander"
# "Other"
# "Unknown/Missing"
# "White"
# "Multiple Race"
# "Total"

# arc_url, database, schema, table, fieldmap
CONFIG = {
	'database': "covid19_race_class",
	'schema': "state_latest",
	'geographies': {
		'sacramento': {
			'table_cases': 'sacramento_race_cases_latest',
			'table_deaths': 'sacramento_race_deaths_latest',
			'table_known_unknown': 'sacramento_race_known_unknown_latest',
			'service_type': 'esri',
			'fieldmap_cases': {
				'Race_Ethnicity': 'race_ethn',
				'Cases': 'total',
				'Percent_': 'total_pct',
			},
			'fieldmap_deaths': {
				'Race_Ethnicity': 'race_ethn',
				'Cases': 'total',
				'Percent_': 'total_pct',
			},
			'fieldmap_known_unknown': {
				'Race_Ethnicity': 'race_ethn',
				'Cases': 'total',
				'Percent_': 'total_pct',
			},
			'racemap': {
				'AI/AN': 'American Indian or Alaska Native',
				'Hispanic': 'Latinx',
				'NHPI': 'Native Hawaiian or Other Pacific Islander',
				'Black': 'Black/African American',
				'Cases - Other/Multi/Unknown ': "Unknown/Missing",
				'Deaths - Other/Multi/Unknown ': "Unknown/Missing",	
			},
			'url_cases': 'https://services6.arcgis.com/yeTSZ1znt7H7iDG7/arcgis/rest/services/COVID19_Race_Ethnicity/FeatureServer/0/query?f=json&where=1%3D1&outFields=*', 
			'url_deaths': 'https://services6.arcgis.com/yeTSZ1znt7H7iDG7/arcgis/rest/services/COVID19_Deaths_by_Race_Ethnicity/FeatureServer/0/query?f=json&where=1%3D1&outFields=*', 
			'url_known_unknown': 'https://services6.arcgis.com/yeTSZ1znt7H7iDG7/ArcGIS/rest/services/COVID19_Race_Ethnicity_Known_Unknown/FeatureServer/0/query?where=1%3D1&outFields=*&f=json',
		},
		'riverside': {
			'table_cases': 'riverside_race_cases_latest',
			'table_deaths': '',
			'service_type': 'esri',
			'fieldmap_cases': {
				'Race': 'race_ethn',
				'Cases': 'total',
				'PctCases': 'total_pct',
				'Rate_100K': 'crude_rate',
				'Total': 'population',
			},
			'fieldmap_deaths': {},
			'racemap': {
				'AI/AN': 'American Indian/Alaska Native',
				'Hispanic/Latino': 'Latinx',
				'Native Hawaiian/Pacific Islander': 'Native Hawaiian or Other Pacific Islander',
				'Total Pop': 'Total',		
			},
			'url_cases': 'https://services1.arcgis.com/pWmBUdSlVpXStHU6/ArcGIS/rest/services/COVID19_Race_Graph/FeatureServer/0/query?where=race+is+not+null&outFields=*&f=json', 
			'url_deaths': None, 
		},
		'orange': {
			'table_cases': 'orange_race_cases_latest',
			'table_deaths': 'orange_race_deaths_latest',
			'service_type': 'esri_custom',
			'function': arc2pg_orange,
			'racemap': {
				'ai': 'American Indian or Alaska Native',
				'latinx': 'Latinx',
				'pi': 'Native Hawaiian or Other Pacific Islander',
				'unk': 'Unknown/Missing',
				'white': 'White',
				'asian': 'Asian',
				'aa': 'Black/African American',
				'mult_race': 'Multiple Race',
				'oth_race': 'Other',
			},
			'url_cases': 'https://services2.arcgis.com/LORzk2hk9xzHouw9/ArcGIS/rest/services/occovid_democase_csv/FeatureServer/0/query?where=1%3D1&outFields=*&f=json', 
			'url_deaths': 'https://services2.arcgis.com/LORzk2hk9xzHouw9/ArcGIS/rest/services/occovid_demodth_csv/FeatureServer/0/query?where=1%3D1&outFields=*&f=json', 
		},
		'fresno': {
			'table_cases': 'fresno_race_cases_latest',
			'table_deaths': '', # 'fresno_race_deaths_latest',
			'table_tests': 'fresno_race_testing_latest',
			'service_type': 'esri_custom',
			'function': arc2pg_fresno,
			'racemap': {
				'hispanic': 'Latinx',
				'white': 'White',
				'asian': 'Asian',
				'black': 'Black/African American',
				'other': 'Other',
			},
			'url_cases': 'https://services3.arcgis.com/ibgDyuD2DLBge82s/ArcGIS/rest/services/CoronavirusCases_ByEthnicity_Current/FeatureServer/0/query?where=1=1&outFields=*&f=json', 
			'url_deaths': '', 
			'url_tests': 'https://services3.arcgis.com/ibgDyuD2DLBge82s/ArcGIS/rest/services/CoronavirusCases_ByEthnicity_Current/FeatureServer/0/query?where=1=1&outFields=*&f=json', 
		},
		'san_joaquin': {
			'table_cases': 'san_joaquin_race_cases_latest',
			'table_deaths': 'san_joaquin_race_deaths_latest',
			'service_type': 'esri',
			'fieldmap_cases': {
				'Race_Ethnicity': 'race_ethn',
				'No_Cases': 'total',
				'Per_Cases': 'total_pct',
				'Per_Pop': 'population_pct',
			},
			'fieldmap_deaths': {
				'Race_Ethnicity': 'race_ethn',
				'No_Deaths': 'total',
				'Per_Deaths': 'total_pct',
				'Per_Pop': 'population_pct',
			},
			'racemap': {
				'Hispanic/Latino': 'Latinx',		
			},
			'url_cases': 'https://services6.arcgis.com/NtWO9krY7z9jd3mY/ArcGIS/rest/services/COVID_Race/FeatureServer/0/query?where=1%3D1&outFields=*&f=json', 
			'url_deaths': 'https://services6.arcgis.com/NtWO9krY7z9jd3mY/ArcGIS/rest/services/COVID_Race/FeatureServer/0/query?where=1%3D1&outFields=*&f=json', 
		},
		'pasadena': {
			'table_cases': 'pasadena_race_cases_latest',
			'table_deaths': 'pasadena_race_deaths_latest',
			'service_type': 'esri_custom',
			'function': arc2pg_pasadena,
			'racemap': {
				'latinx': 'Latinx',
				'raceunknown': 'Unknown/Missing',
				'racewhite': 'White',
				'raceasian': 'Asian',
				'raceblack': 'Black/African American',
				'raceother': 'Other',
			},
			'url_cases': 'https://services2.arcgis.com/zNjnZafDYCAJAbN0/ArcGIS/rest/services/PasadenaCACOVID19Cases/FeatureServer/0/query?where=1%3D1&outFields=*&f=json', 
			'url_deaths': 'https://services2.arcgis.com/zNjnZafDYCAJAbN0/ArcGIS/rest/services/PasadenaCACOVID19Cases/FeatureServer/0/query?where=1%3D1&outFields=*&f=json', 
		},
		'california': {
			'table_tests': 'cdph_testing_state_latest',
			'service_type': 'csv',
			'fieldmap_tests': {
				'tested': 'tests',
				'date': 'data_date',
			},
			'racemap': {},
			'url_tests': 'https://data.ca.gov/dataset/efd6b822-7312-477c-922b-bccb82025fbe/resource/b6648a0d-ff0a-4111-b80b-febda2ac9e09/download/statewide_testing.csv',
		},
	},
}

class Command(BaseCommand):
	help = 'Reload database tables for COVID-19 statewide analysis.  <config>'
	
	def add_arguments(self, parser):
		parser.add_argument('--geography', type=str, help='Optionally load just this geography (not yet active).')

	def handle(self, *args, **options):
		print ("Starting update...")
		t1 = time()

		database = CONFIG['database']
		schema = CONFIG['schema']
		geographies = CONFIG['geographies']

		# county-level testing, scrape the html table
		# try:
		# 	r = html2pg_tests_county(database, schema, 'cdph_testing_county_latest')
		# 	self.stdout.write(self.style.SUCCESS(r))
		# except Exception as e:
		# 	print (e)
		# 	self.stdout.write(self.style.ERROR('CDPH testing by county failed'))

		# Loop geographies
		for k, v in CONFIG['geographies'].items():
			try:
				if v['service_type'] == 'esri':
					# arc_url, database, schema, table, fieldmap, racemap
					# cases
					if 'url_cases' in v and v['url_cases']:
						r = arc2pg(v['url_cases'], database, schema, v['table_cases'], v['fieldmap_cases'], v['racemap'])
						self.stdout.write(self.style.SUCCESS(r))

					if 'url_deaths' in v and v['url_deaths']:
						r = arc2pg(v['url_deaths'], database, schema, v['table_deaths'], v['fieldmap_deaths'], v['racemap'])
						self.stdout.write(self.style.SUCCESS(r))

					if 'url_tests' in v:
						r = arc2pg(v['url_tests'], database, schema, v['table_tests'], v['fieldmap_tests'], v['racemap'])
						self.stdout.write(self.style.SUCCESS(r))

				elif v['service_type'] == 'esri_custom':
					if 'url_cases' in v and v['url_cases']:
						r = v['function'](v['url_cases'], database, schema, v['table_cases'], v['racemap'])
						self.stdout.write(self.style.SUCCESS(r))

					if 'url_deaths' in v and v['url_deaths']:
						r = v['function'](v['url_deaths'], database, schema, v['table_deaths'], v['racemap'])
						self.stdout.write(self.style.SUCCESS(r))

					if 'url_tests' in v and v['url_tests']:
						r = v['function'](v['url_tests'], database, schema, v['table_tests'], v['racemap'])
						self.stdout.write(self.style.SUCCESS(r))

				elif v['service_type'] == 'csv':
					if 'url_tests' in v and v['url_tests']:
						r = csv2pg(v['url_tests'], database, schema, v['table_tests'], v['fieldmap_tests'], v['racemap'])
						self.stdout.write(self.style.SUCCESS(r))
			except Exception as e:
				print (e)
				self.stdout.write(self.style.ERROR(str(k) + ' failed'))

		# known/unknown for sacramento is in separate service
		try:
			r = arc2pg_sacramento_known_unknown(geographies['sacramento']['url_known_unknown'], database, schema, geographies['sacramento']['fieldmap_known_unknown'], geographies['sacramento']['racemap'])
			self.stdout.write(self.style.SUCCESS(r))
		except Exception as e:
			print (e)
			self.stdout.write(self.style.ERROR('sacramento known/unknown failed'))

		# Power BI apps - alameda and long beach
		try:
			r = pbi2pg_alameda(database, schema)
			self.stdout.write(self.style.SUCCESS(r))
		except Exception as e:
			print (e)
			self.stdout.write(self.style.ERROR('Alameda failed'))

		try:
			r = pbi2pg_long_beach(database, schema)
			self.stdout.write(self.style.SUCCESS(r))
		except Exception as e:
			print (e)
			self.stdout.write(self.style.ERROR('Long Beach failed'))		

		print ("\nfinished! Elapsed time = " + str(round((time() - t1)/60, 2)) + " minutes")