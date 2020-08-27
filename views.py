# COVID-19 Statewide Analysis
# Data scraping functions - cases, deaths, and testing as available
# See ./manage.py covid19_statewide_update_db for config endpoints and fieldmaps

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404
from rda_dev.views import pgdata2_data, pgdata_column_info_data
from rda_dev.util.pg_connect import pg_connect, pg_disconnect, run_sql_select_query
from collections import OrderedDict
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from datetime import datetime
from lxml import html
import redis, json, requests, time, copy, re, pyexcel as pe

# generic take an ArcGIS endpoint and load into a postgres table
def arc2pg(arc_url, database, schema, table, fieldmap, racemap):
	print ("\nStarting %s.%s" % (schema, table))

	# get metadata for the endpoint
	meta_url = arc_url.split('/query?')[0] + '?f=json'
	metadata = arc_meta(meta_url)
	
	# last edit date
	last_edit_date = timezone.make_aware(datetime.fromtimestamp(metadata['editingInfo']['lastEditDate'] / 1000))
	
	# db connect
	dbconn = pg_connect(database)
	conn = dbconn['conn']
	cur = dbconn['cur']

	# check whether data are current
	sql = "SELECT max(data_date) as dt from %s.%s;" % (schema, table)
	dt = run_sql_select_query(cur=cur, sql=sql)[0]['dt']
	print ('last edit', last_edit_date, '\ndata date', dt)
	if dt and dt >= last_edit_date:
		pg_disconnect(conn, cur)
		return "No new data for %s.%s" % (schema, table)	

	# get the data
	req = requests.get(arc_url)
	data = json.loads(req.content.decode('utf-8'))

	# insert into db
	print ('inserting records')
	fieldlist = fieldmap.items()
	columns = [ v for k, v in fieldlist ]
	sql = "INSERT into %s.%s (%s, data_date) values " % (schema, table, ", ".join(columns))
	for f in data['features']:
		slist = [ "%s" for c in columns ] + [ "%s" ]
		sql_r = sql + "({});".format(", ".join(slist))
		values = [ f['attributes'][k] if v != 'race_ethn' else (racemap[f['attributes'][k]] if f['attributes'][k] in racemap else f['attributes'][k]) for k, v in fieldlist ] + [ last_edit_date ]
		cur.execute(sql_r, (*values, ))
		
	# commit inserts
	conn.commit()

	# vacuum analyze
	print ('cleaning up')
	conn.autocommit = True
	cur.execute("VACUUM ANALYZE {}.{};".format(schema, table))
	conn.autocommit = False

	# close db conn
	pg_disconnect(conn, cur)
	return "Updated %s.%s" % (schema, table)

# custom scraping functions for complicated endpoints
def arc2pg_orange(arc_url, database, schema, table, racemap):
	print ("\nStarting %s.%s" % (schema, table))

	# get metadata for the endpoint
	meta_url = arc_url.split('/query?')[0] + '?f=json'
	metadata = arc_meta(meta_url)

	# whether cases, deaths, or tests
	table_type = 'cases' if '_cases_' in table else ('deaths' if '_deaths_' in table else 'tests')
	
	# last edit date
	last_edit_date = timezone.make_aware(datetime.fromtimestamp(metadata['editingInfo']['lastEditDate'] / 1000))
	
	# db connect
	dbconn = pg_connect(database)
	conn = dbconn['conn']
	cur = dbconn['cur']

	# check whether data are current
	sql = "SELECT max(data_date) as dt from %s.%s;" % (schema, table)
	dt = run_sql_select_query(cur=cur, sql=sql)[0]['dt']
	print ('last edit', last_edit_date, '\ndata date', dt)
	if dt and dt >= last_edit_date:
		pg_disconnect(conn, cur)
		return "No new data for %s.%s" % (schema, table)	

	# get the data
	req = requests.get(arc_url)
	data = json.loads(req.content.decode('utf-8'))

	# insert into db
	print ('inserting records')
	a = data['features'][0]['attributes']
	data_prefix = 'case_' if table_type == 'cases' else 'dth_'
	data_total = "total_%s" % table_type if table_type == 'cases' else 'total_dth'
	columns = [ 'race_ethn', 'total', 'total_pct', 'population_pct', 'data_date', ]
	sql = "INSERT into %s.%s (%s) values " % (schema, table, ", ".join(columns))
	# total row 
	slist = [ "%s" for c in columns ]
	sql_r = sql + "({});".format(", ".join(slist))
	values = [ 'Total', a[data_total], 100, 100, last_edit_date, ]
	cur.execute(sql_r, (*values, ))
	# each race
	for k, v in racemap.items():
		values = [
			v,
			a[data_prefix + k],
			a[data_prefix + k + '_perc'],
		]
		if k == 'mult_race':
			values += [ a['multi_pop_perc'] ]
		elif k == 'oth_race':
			values += [ a['other_pop_perc'] ]
		elif k + '_pop_perc' in a:
			values += [ a[k + '_pop_perc'] ]
		else:
			values += [ None ]
		values += [ last_edit_date, ]
		cur.execute(sql_r, (*values, ))
		
	# commit inserts
	conn.commit()

	# vacuum analyze
	print ('cleaning up')
	conn.autocommit = True
	cur.execute("VACUUM ANALYZE {}.{};".format(schema, table))
	conn.autocommit = False

	# close db conn
	pg_disconnect(conn, cur)
	return "Updated %s.%s" % (schema, table)

def arc2pg_fresno(arc_url, database, schema, table, racemap):
	print ("\nStarting %s.%s" % (schema, table))

	# get metadata for the endpoint
	meta_url = arc_url.split('/query?')[0] + '?f=json'
	metadata = arc_meta(meta_url)

	# whether cases, deaths, or tests
	table_type = 'cases' if '_cases_' in table else ('deaths' if '_deaths_' in table else 'tests')
	
	# db connect
	dbconn = pg_connect(database)
	conn = dbconn['conn']
	cur = dbconn['cur']

	# get the data
	req = requests.get(arc_url)
	data = json.loads(req.content.decode('utf-8'))
	a = data['features'][0]['attributes']

	# check whether our data are current
	sql = "SELECT max(data_date) as dt from %s.%s;" % (schema, table)
	dt = run_sql_select_query(cur=cur, sql=sql)[0]['dt']

	# last edit date
	last_edit_date = timezone.make_aware(datetime.fromtimestamp(a['reportdt'] / 1000))

	print ('last edit', last_edit_date, '\ndata date', dt)
	if dt and dt >= last_edit_date:
		pg_disconnect(conn, cur)
		return "No new data for %s.%s" % (schema, table)	

	# insert into db
	print ('inserting records')
	# set up sql
	columns = [ 'race_ethn', 'crude_rate' if table_type != 'tests' else 'total', 'data_date', ]
	sql = "INSERT into %s.%s (%s) values " % (schema, table, ", ".join(columns))
	slist = [ "%s" for c in columns ]
	sql_r = sql + "({});".format(", ".join(slist))
	
	# each race
	for k, v in racemap.items():
		values = [
			v,
			a[k + table_type],
			last_edit_date,
		]
		cur.execute(sql_r, (*values, ))
		
	# commit inserts
	conn.commit()

	# vacuum analyze
	print ('cleaning up')
	conn.autocommit = True
	cur.execute("VACUUM ANALYZE {}.{};".format(schema, table))
	conn.autocommit = False

	# close db conn
	pg_disconnect(conn, cur)
	return "Updated %s.%s" % (schema, table)

def arc2pg_pasadena(arc_url, database, schema, table, racemap):
	print ("\nStarting %s.%s" % (schema, table))

	# get metadata for the endpoint
	meta_url = arc_url.split('/query?')[0] + '?f=json'
	metadata = arc_meta(meta_url)

	# whether cases, deaths, or tests
	table_type = 'cases' if '_cases_' in table else ('deaths' if '_deaths_' in table else 'tests')
	
	# db connect
	dbconn = pg_connect(database)
	conn = dbconn['conn']
	cur = dbconn['cur']

	# get the data
	req = requests.get(arc_url)
	data = json.loads(req.content.decode('utf-8'))
	a = data['features'][0]['attributes']

	# check whether our data are current
	sql = "SELECT max(data_date) as dt from %s.%s;" % (schema, table)
	dt = run_sql_select_query(cur=cur, sql=sql)[0]['dt']

	# last edit date
	last_edit_date = timezone.make_aware(datetime.fromtimestamp(a['reportdt'] / 1000))

	print ('last edit', last_edit_date, '\ndata date', dt)
	if dt and dt >= last_edit_date:
		pg_disconnect(conn, cur)
		return "No new data for %s.%s" % (schema, table)	

	# insert into db
	print ('inserting records')
	# set up sql
	columns = [ 'race_ethn', 'total', 'data_date', ]
	sql = "INSERT into %s.%s (%s) values " % (schema, table, ", ".join(columns))
	slist = [ "%s" for c in columns ]
	sql_r = sql + "({});".format(", ".join(slist))
	
	# each race
	for k, v in racemap.items():
		values = [
			v,
			a[table_type + k],
			last_edit_date,
		]
		cur.execute(sql_r, (*values, ))
		
	# commit inserts
	conn.commit()

	# vacuum analyze
	print ('cleaning up')
	conn.autocommit = True
	cur.execute("VACUUM ANALYZE {}.{};".format(schema, table))
	conn.autocommit = False

	# close db conn
	pg_disconnect(conn, cur)
	return "Updated %s.%s" % (schema, table)

def arc2pg_sacramento_known_unknown(arc_url, database, schema, fieldmap, racemap):
	print ("\nStarting Sacramento known/Unknown")

	# get metadata for the endpoint
	meta_url = arc_url.split('/query?')[0] + '?f=json'
	metadata = arc_meta(meta_url)
	
	# last edit date
	last_edit_date = timezone.make_aware(datetime.fromtimestamp(metadata['editingInfo']['lastEditDate'] / 1000)).date()

	# db connect
	dbconn = pg_connect(database)
	conn = dbconn['conn']
	cur = dbconn['cur']

	# check whether data are current
	table = 'sacramento_race_cases_latest'
	sql = "SELECT max(data_date)::date as dt from %s.%s;" % (schema, table)
	dt = run_sql_select_query(cur=cur, sql=sql)[0]['dt']
	print ('last edit', last_edit_date, '\ndata date', dt)
	if dt and dt >= last_edit_date:
		# check if data for known/unknown yet
		sql = "SELECT id from {}.{} where data_date::date = %(data_date)s and substr(race_ethn, 0, 8) = 'Cases -';".format(schema, table)
		known_unknown = run_sql_select_query(cur=cur, sql=sql, params={ 'data_date': last_edit_date })
		if len(known_unknown):
			pg_disconnect(conn, cur)
			return "No new data for Sacramento known/unknown"	

	# get the data
	req = requests.get(arc_url)
	data = json.loads(req.content.decode('utf-8'))

	# insert into db
	print ('inserting records')
	fieldlist = fieldmap.items()
	columns = [ v for k, v in fieldlist ]
	for f in data['features']:
		table = 'sacramento_race_cases_latest' if f['attributes']['Race_Ethnicity'].startswith('Cases -') else 'sacramento_race_deaths_latest'
		sql = "INSERT into %s.%s (%s, data_date) values " % (schema, table, ", ".join(columns))
		slist = [ "%s" for c in columns ] + [ "%s" ]
		sql_r = sql + "({});".format(", ".join(slist))
		values = [ f['attributes'][k] if v != 'race_ethn' else (racemap[f['attributes'][k]] if f['attributes'][k] in racemap else f['attributes'][k]) for k, v in fieldlist ] + [ last_edit_date ]
		cur.execute(sql_r, (*values, ))
		
	# commit inserts
	conn.commit()

	# vacuum analyze
	print ('cleaning up')
	conn.autocommit = True
	cur.execute("VACUUM ANALYZE {}.{};".format(schema, table))
	conn.autocommit = False

	# close db conn
	pg_disconnect(conn, cur)
	return "Updated %s.%s" % (schema, table)

def pbi2pg_alameda(database, schema):

	# base URL for requests
	dashboard_url = "https://app.powerbigov.us/view?r=eyJrIjoiM2EyMmNiMjMtY2YxYS00MzZlLTlhMzMtNTExZDJlZGMyOWYzIiwidCI6IjMyZmRmZjJjLWY4NmUtNGJhMy1hNDdkLTZhNDRhN2Y0NWE2NCJ9&pageName=ReportSection"
	data_url = "https://wabi-us-gov-iowa-api.analysis.usgovcloudapi.net/public/reports/querydata?synchronous=true"

	# JSON for postdata
	postdata = {
		'cases': {
			'counts': {
				"version":"1.0.0",
				"queries":[{
					"Query":{
						"Commands":[{
							"SemanticQueryDataShapeCommand":{
								"Query":{
									"Version":2,
									"From":[{"Name":"v","Entity":"V_RaceEth_Rates","Type":0}],
									"Select":[{"Column":{"Expression":{"SourceRef":{"Source":"v"}},"Property":"RaceEth"},"Name":"V_RaceEth_Rates.RaceEth"},{"Aggregation":{"Expression":{"Column":{"Expression":{"SourceRef":{"Source":"v"}},"Property":"Cases"}},"Function":0},"Name":"Sum(V_RaceEth_Rates.Cases)"}],
									"Where":[{
										"Condition":{"Not":{"Expression":{"In":{"Expressions":[{"Column":{"Expression":{"SourceRef":{"Source":"v"}},"Property":"RaceEth"}}],"Values":[[{"Literal":{"Value":"'Overall Known Race/Ethnicity'"}}],[{"Literal":{"Value":"'Overall'"}}]]}}}}},{
										"Condition":{"Comparison":{"ComparisonKind":2,"Left":{"Aggregation":{"Expression":{"Column":{"Expression":{"SourceRef":{"Source":"v"}},"Property":"Cases"}},"Function":0}},"Right":{"Literal":{"Value":"10L"}}}},"Target":[{"Column":{"Expression":{"SourceRef":{"Source":"v"}},"Property":"RaceEth"}}]}],
									"OrderBy":[{"Direction":1,"Expression":{"Column":{"Expression":{"SourceRef":{"Source":"v"}},"Property":"RaceEth"}}}]
								},
								"Binding":{"Primary":{"Groupings":[{"Projections":[0,1]}]},"DataReduction":{"DataVolume":4,"Primary":{"Window":{"Count":1000}}},"Version":1}
							}
						}]
					},
					"QueryId":"",
					"ApplicationContext":{"DatasetId":"d4923c43-5fc4-444c-aa95-8ecf0d15f562","Sources":[{"ReportId":"5080f005-6411-4a22-88b0-ff13c00d140f"}]}
				}],
				"cancelQueries":[],
				"modelId":295360,
			},
			'rates': {
				"version":"1.0.0",
				"queries":[{
					"Query": {
						"Commands": [{
							"SemanticQueryDataShapeCommand": {
								"Query": {
									"Version": 2,
									"From": [{"Name":"v","Entity":"V_RaceEth_Rates","Type":0}],
									"Select": [
										{"Column":{"Expression":{"SourceRef":{"Source":"v"}},"Property":"RaceEth"},"Name":"V_RaceEth_Rates.RaceEth"},
										{"Aggregation":{"Expression":{"Column":{"Expression":{"SourceRef":{"Source":"v"}},"Property":"CaseRates"}},"Function":0},"Name":"Sum(V_RaceEth_Rates.CaseRates)"}
									],
									"OrderBy": [{"Direction":1,"Expression":{"Column":{"Expression":{"SourceRef":{"Source":"v"}},"Property":"RaceEth"}}}]
								}, 
								"Binding": {"Primary":{"Groupings":[{"Projections":[0,1]}]},"DataReduction":{"DataVolume":4,"Primary":{"Window":{"Count":1000}}},"Version":1}
							}
						}]
					}, 
					"QueryId":"",
					"ApplicationContext": {"DatasetId":"d4923c43-5fc4-444c-aa95-8ecf0d15f562","Sources":[{"ReportId":"5080f005-6411-4a22-88b0-ff13c00d140f"}]}
				}],
				"cancelQueries":[],
				"modelId":295360,
			},
		},
		'deaths': {
			'counts': {
				"version":"1.0.0",
				"queries":[{
					"Query":{
						"Commands":[{
							"SemanticQueryDataShapeCommand":{
								"Query":{"Version":2,"From":[{"Name":"v","Entity":"V_RaceEth_Rates","Type":0}],"Select":[{"Column":{"Expression":{"SourceRef":{"Source":"v"}},"Property":"RaceEth"},"Name":"V_RaceEth_Rates.RaceEth"},{"Aggregation":{"Expression":{"Column":{"Expression":{"SourceRef":{"Source":"v"}},"Property":"Deaths"}},"Function":0},"Name":"Sum(V_RaceEth_Rates.Deaths)"}],"Where":[{"Condition":{"Not":{"Expression":{"In":{"Expressions":[{"Column":{"Expression":{"SourceRef":{"Source":"v"}},"Property":"RaceEth"}}],"Values":[[{"Literal":{"Value":"'Overall Known Race/Ethnicity'"}}],[{"Literal":{"Value":"'Overall'"}}]]}}}}},{"Condition":{"Comparison":{"ComparisonKind":2,"Left":{"Aggregation":{"Expression":{"Column":{"Expression":{"SourceRef":{"Source":"v"}},"Property":"Deaths"}},"Function":0}},"Right":{"Literal":{"Value":"10L"}}}},"Target":[{"Column":{"Expression":{"SourceRef":{"Source":"v"}},"Property":"RaceEth"}}]}],"OrderBy":[{"Direction":1,"Expression":{"Column":{"Expression":{"SourceRef":{"Source":"v"}},"Property":"RaceEth"}}}]},
								"Binding":{"Primary":{"Groupings":[{"Projections":[0,1]}]},"DataReduction":{"DataVolume":4,"Primary":{"Window":{"Count":1000}}},"Version":1}
							}
					}]},
					"QueryId":"",
					"ApplicationContext":{"DatasetId":"d4923c43-5fc4-444c-aa95-8ecf0d15f562","Sources":[{"ReportId":"5080f005-6411-4a22-88b0-ff13c00d140f"}]}
				}],
				"cancelQueries":[],
				"modelId":295360,
			},
			'rates': {
				"version":"1.0.0",
				"queries":[{
					"Query":{
						"Commands":[{
							"SemanticQueryDataShapeCommand":{
								"Query":{"Version":2,"From":[{"Name":"v","Entity":"V_RaceEth_Rates","Type":0}],"Select":[{"Column":{"Expression":{"SourceRef":{"Source":"v"}},"Property":"RaceEth"},"Name":"V_RaceEth_Rates.RaceEth"},{"Aggregation":{"Expression":{"Column":{"Expression":{"SourceRef":{"Source":"v"}},"Property":"DeathRates"}},"Function":0},"Name":"Sum(V_RaceEth_Rates.DeathRates)"}],"Where":[{"Condition":{"Comparison":{"ComparisonKind":2,"Left":{"Column":{"Expression":{"SourceRef":{"Source":"v"}},"Property":"Deaths"}},"Right":{"Literal":{"Value":"10L"}}}}}],"OrderBy":[{"Direction":1,"Expression":{"Column":{"Expression":{"SourceRef":{"Source":"v"}},"Property":"RaceEth"}}}]},
								"Binding":{"Primary":{"Groupings":[{"Projections":[0,1]}]},"DataReduction":{"DataVolume":4,"Primary":{"Window":{"Count":1000}}},"Version":1}
							}
						}]
					},
					"QueryId":"",
					"ApplicationContext":{"DatasetId":"d4923c43-5fc4-444c-aa95-8ecf0d15f562","Sources":[{"ReportId":"5080f005-6411-4a22-88b0-ff13c00d140f"}]}
				}],
				"cancelQueries":[],
				"modelId":295360,
			},
		},
	}

	# racemap - data_race => db_race
	racemap = {
		'Hispanic/Latino': "Latinx",
		'African American/Black': "Black/African American",
		'Pacific Islander': "Native Hawaiian or Other Pacific Islander", 
		'Native American': "American Indian or Alaska Native", 
		'Multirace': "Multiple Race", 
		'Overall': "Total",
		'Unknown': "Unknown/Missing",
	}

	# get the data
	session = requests.Session()

	# get the ActivityID header using splash/lua
	print ('\nsplash script to get download url (up to 90sec)')
	script = """
		assert(splash:go(args.url))
		assert(splash:wait(5))
		local activityId = splash:evaljs('window.telemetrySessionId')
		return {
			activityId = activityId, 
		}
	"""

	sr = session.post('http://localhost:8050/run', json={
		'lua_source': script,
		'url': dashboard_url,
		'timeout': 90,
		'resource_timeout': 40
	})
	src = json.loads(sr.content.decode('utf-8'))
	print ('\nsrc: ', src)

	if 'error' in src:
		print ('error getting page', src['error'])

	# post for the response
	headers = { 
	 	'ActivityId': src['activityId'],
	 	'X-PowerBI-ResourceKey': '3a22cb23-cf1a-436e-9a33-511d2edc29f3', 
	}

	# last update
	meta_url = 'https://wabi-us-gov-iowa-api.analysis.usgovcloudapi.net/public/reports/3a22cb23-cf1a-436e-9a33-511d2edc29f3/modelsAndExploration?preferReadOnlySession=true'
	sr = session.get(meta_url, headers=headers)
	metadata = json.loads(sr.content.decode('utf-8'))
	last_edit_date = timezone.make_aware(parse_datetime(metadata['models'][0]['LastRefreshTime']))
	print ('Last updated: ', last_edit_date)

	# db connect
	dbconn = pg_connect(database)
	conn = dbconn['conn']
	cur = dbconn['cur']

	# get the data
	tabledata = {}
	for k, v in postdata.items():
		# check whether data are current
		table = "alameda_race_%s_latest" % k
		sql = "SELECT max(data_date) as dt from %s.%s;" % (schema, table)
		dt = run_sql_select_query(cur=cur, sql=sql)[0]['dt']
		print (k, 'last edit', last_edit_date, '\n%s' % k, 'data date', dt)
		if dt and dt >= last_edit_date:
			pg_disconnect(conn, cur)
			return "No new data for Alameda County"

		# whether to insert or update
		insert_or_update = 'update' if dt.date() == last_edit_date.date() else 'insert'

		tabledata[k] = {}
		for typ, p in v.items():
			sr = session.post(data_url, json=p, headers=headers)
			d = json.loads(sr.content.decode('utf-8'))
			racelist = d['results'][0]['result']['data']['dsr']['DS'][0]['ValueDicts']['D0']
			valueslist = d['results'][0]['result']['data']['dsr']['DS'][0]['PH'][0]['DM0']
			for i, r in enumerate(racelist):
				race_ethn = racemap[r] if r in racemap else r
				if race_ethn not in tabledata[k]:
					tabledata[k][race_ethn] = {}

				if len(valueslist[i]['C']) == 1 and 'R' in valueslist[i]:
					# not sure this part is right, but currently matches what they display on their site... double check at next update
					# seems like if they don't include data but include an 'R' property then it's a repeat of the previous value
					print (k, race_ethn, typ, '\n\n', valueslist, '\n\n', i, valueslist[i])
					tabledata[k][race_ethn][typ] = valueslist[i-1]['C'][1]
				else:
					tabledata[k][race_ethn][typ] = valueslist[i]['C'][1]				

	# insert into db
	print ('inserting records')
	for k, t in tabledata.items():
		table = "alameda_race_%s_latest" % k
		if insert_or_update == 'insert':
			# add a new row
			columns = [ 'race_ethn', 'total', 'crude_rate', 'data_date', ]
			sql = "INSERT into %s.%s (%s) values " % (schema, table, ", ".join(columns))
			slist = [ "%s" for c in columns ]
			sql_r = sql + "({});".format(", ".join(slist))
			# each race
			for r, v in t.items():
				values = [
					r,
					v['counts'] if 'counts' in v else None,
					v['rates'] if 'rates' in v else None,
					last_edit_date,
				]
				cur.execute(sql_r, (*values, ))
		else: 
			# update the current row
			sql = "UPDATE %s.%s set " % (schema, table)
			sql_r = sql + "total = %s, crude_rate = %s, data_date = %s, row_date = now() where race_ethn = %s and data_date::date = %s;"
			# each race
			for r, v in t.items():
				values = [
					v['counts'] if 'counts' in v else None,
					v['rates'] if 'rates' in v else None,
					last_edit_date,
					r,
					last_edit_date.date(),					
				]
				cur.execute(sql_r, (*values, ))
		
		# commit and vacuum analyze
		conn.commit()
		conn.autocommit = True
		cur.execute("VACUUM ANALYZE {}.{};".format(schema, table))
		conn.autocommit = False

	# close db conn
	pg_disconnect(conn, cur)
	return "Updated Alameda County"

def pbi2pg_long_beach(database, schema):

	# base URL for requests
	dashboard_url = "https://app.powerbigov.us/view?r=eyJrIjoiMDNmNWM3ZjgtNjA2OS00YTEyLThhMjUtNTQyMTU1ZWM3Yjk5IiwidCI6IjMxM2YxMWMzLTQyNjgtNGY2YS04ZDNiLWM3ZTY1MDE4M2U3OCJ9"
	data_url = "https://wabi-us-gov-iowa-api.analysis.usgovcloudapi.net/public/reports/querydata?synchronous=true"


	# JSON for postdata
	postdata = {
		'cases': {"version":"1.0.0","queries":[{"Query":{"Commands":[{"SemanticQueryDataShapeCommand":{"Query":{"Version":2,"From":[{"Name":"h","Entity":"Case-Race","Type":0},{"Name":"c","Entity":"city_demographic","Type":0}],"Select":[{"Aggregation":{"Expression":{"Column":{"Expression":{"SourceRef":{"Source":"c"}},"Property":"Percent"}},"Function":0},"Name":"Sum(city_demographic.Percent)"},{"Aggregation":{"Expression":{"Column":{"Expression":{"SourceRef":{"Source":"h"}},"Property":"Percentage"}},"Function":0},"Name":"Sum(Case-Race.Percentage)"},{"Aggregation":{"Expression":{"Column":{"Expression":{"SourceRef":{"Source":"h"}},"Property":"orderid"}},"Function":0},"Name":"Sum(Case-Race.orderid)"},{"Column":{"Expression":{"SourceRef":{"Source":"h"}},"Property":"table_race"},"Name":"Case-Race.race_table"}],"OrderBy":[{"Direction":1,"Expression":{"Aggregation":{"Expression":{"Column":{"Expression":{"SourceRef":{"Source":"h"}},"Property":"orderid"}},"Function":0}}}]},"Binding":{"Primary":{"Groupings":[{"Projections":[0,1,2,3]}]},"DataReduction":{"DataVolume":4,"Primary":{"Window":{"Count":1000}}},"SuppressedJoinPredicates":[2],"Version":1}}}]},"QueryId":"","ApplicationContext":{"DatasetId":"38141830-4b1b-4309-b51e-da91c50f22ee","Sources":[{"ReportId":"cef91e37-b89d-4967-8130-dc528ff1d964"}]}}],"cancelQueries":[],"modelId":276737
		},
		'deaths': {"version":"1.0.0","queries":[{"Query":{"Commands":[{"SemanticQueryDataShapeCommand":{"Query":{"Version":2,"From":[{"Name":"h1","Entity":"health_processed_death_by_race_output","Type":0},{"Name":"c","Entity":"city_demographic_death_option","Type":0},{"Name":"h","Entity":"Hosp-Race","Type":0}],"Select":[{"Column":{"Expression":{"SourceRef":{"Source":"h1"}},"Property":"Race"},"Name":"health_processed_death_by_race_output.Race"},{"Aggregation":{"Expression":{"Column":{"Expression":{"SourceRef":{"Source":"h1"}},"Property":"Orderid"}},"Function":3},"Name":"Min(health_processed_death_by_race_output.Orderid)"},{"Aggregation":{"Expression":{"Column":{"Expression":{"SourceRef":{"Source":"h1"}},"Property":"Percentage"}},"Function":0},"Name":"Sum(health_processed_death_by_race_output.Percentage)"},{"Aggregation":{"Expression":{"Column":{"Expression":{"SourceRef":{"Source":"c"}},"Property":"Percent"}},"Function":0},"Name":"Sum(city_demographic_death_option.Percent)"}],"Where":[{"Condition":{"In":{"Expressions":[{"Column":{"Expression":{"SourceRef":{"Source":"h"}},"Property":"Race"}}],"Values":[[{"Literal":{"Value":"'Asian'"}}],[{"Literal":{"Value":"'Hispanic or Latino'"}}],[{"Literal":{"Value":"'Other'"}}],[{"Literal":{"Value":"'Pacific Islander'"}}],[{"Literal":{"Value":"'White'"}}],[{"Literal":{"Value":"'Hawaiian or Islander'"}}],[{"Literal":{"Value":"'Black'"}}]]}}}],"OrderBy":[{"Direction":1,"Expression":{"Aggregation":{"Expression":{"Column":{"Expression":{"SourceRef":{"Source":"h1"}},"Property":"Orderid"}},"Function":3}}}]},"Binding":{"Primary":{"Groupings":[{"Projections":[0,1,2,3]}]},"DataReduction":{"DataVolume":4,"Primary":{"Window":{"Count":1000}}},"SuppressedJoinPredicates":[1],"Version":1}}}]},"QueryId":"","ApplicationContext":{"DatasetId":"38141830-4b1b-4309-b51e-da91c50f22ee","Sources":[{"ReportId":"cef91e37-b89d-4967-8130-dc528ff1d964"}]}}],"cancelQueries":[],"modelId":276737}
	}

	# racemap - data_race => db_race
	racemap = {
		'Hispanic or Latino': "Latinx",
		'Black': "Black/African American",
		'Pacific Islander': "Native Hawaiian or Other Pacific Islander",
		'Unreported': "Unknown/Missing",
	}

	# get the data
	session = requests.Session()

	# get the ActivityID header using splash/lua
	print ('\nsplash script to get download url (up to 90sec)')
	script = """
		assert(splash:go(args.url))
		assert(splash:wait(5))
		local activityId = splash:evaljs('window.telemetrySessionId')
		return {
			activityId = activityId, 
		}
	"""

	sr = session.post('http://localhost:8050/run', json={
		'lua_source': script,
		'url': dashboard_url,
		'timeout': 90,
		'resource_timeout': 40
	})
	src = json.loads(sr.content.decode('utf-8'))
	print ('\nsrc: ', src)

	if 'error' in src:
		print ('error getting page', src['error'])

	# post for the response
	headers = { 
	 	'ActivityId': src['activityId'],
	 	'X-PowerBI-ResourceKey': '03f5c7f8-6069-4a12-8a25-542155ec7b99', 
	}

	# last update
	meta_url = 'https://wabi-us-gov-iowa-api.analysis.usgovcloudapi.net/public/reports/03f5c7f8-6069-4a12-8a25-542155ec7b99/modelsAndExploration?preferReadOnlySession=true'
	sr = session.get(meta_url, headers=headers)
	metadata = json.loads(sr.content.decode('utf-8'))
	last_edit_date = timezone.make_aware(parse_datetime(metadata['models'][0]['LastRefreshTime']))
	print ('Last updated: ', last_edit_date)

	# db connect
	dbconn = pg_connect(database)
	conn = dbconn['conn']
	cur = dbconn['cur']

	# get the data
	tabledata = {}
	for k, v in postdata.items():
		# check whether data are current
		table = "long_beach_race_%s_latest" % k
		sql = "SELECT max(data_date) as dt from %s.%s;" % (schema, table)
		dt = run_sql_select_query(cur=cur, sql=sql)[0]['dt']
		print (k, 'last edit', last_edit_date, '\n%s' % k, 'data date', dt)
		if dt and dt >= last_edit_date:
			pg_disconnect(conn, cur)
			return "No new data for Long Beach"

		# whether to insert or update
		insert_or_update = 'update' if dt.date() == last_edit_date.date() else 'insert'

		# response data
		sr = session.post(data_url, json=v, headers=headers)
		d = json.loads(sr.content.decode('utf-8'))
		valueslist = d['results'][0]['result']['data']['dsr']['DS'][0]['PH'][0]['DM0']

		# insert into db
		print ('inserting records for %s' % k)

		# different for update or insert
		if insert_or_update == 'insert':
			# add a new row
			columns = [ 'race_ethn', 'total_pct', 'population_pct', 'data_date', ]
			sql = "INSERT into %s.%s (%s) values " % (schema, table, ", ".join(columns))
			slist = [ "%s" for c in columns ]
			sql_r = sql + "({});".format(", ".join(slist))
			# each race
			# different for cases and deaths
			if k == 'cases':
				for v in valueslist:
					r = v['C']
					race_ethn = racemap[r[0]] if r[0] in racemap else r[0]
					population_pct = r[1]
					total_pct = r[2]
					values = [
						race_ethn,
						total_pct,
						population_pct,
						last_edit_date,
					]
					cur.execute(sql_r, (*values, ))
			else:
				for v in valueslist:
					r = v['C']
					race_ethn = racemap[r[0]] if r[0] in racemap else r[0]
					total_pct = r[2]
					population_pct = r[3]
					values = [
						race_ethn,
						total_pct,
						population_pct,
						last_edit_date,
					]
					cur.execute(sql_r, (*values, ))
		else: 
			# update the current row
			sql = "UPDATE %s.%s set " % (schema, table)
			sql_r = sql + "total_pct = %s, population_pct = %s, data_date = %s, row_date = now() where race_ethn = %s and data_date::date = %s;"
			# each race
			# different for cases and deaths
			if k == 'cases':
				for v in valueslist:
					r = v['C']
					race_ethn = racemap[r[0]] if r[0] in racemap else r[0]
					population_pct = r[1]
					total_pct = r[2]
					values = [
						total_pct,
						population_pct,
						last_edit_date,
						race_ethn,
						last_edit_date.date(),
					]
					cur.execute(sql_r, (*values, ))
			else:
				for v in valueslist:
					r = v['C']
					race_ethn = racemap[r[0]] if r[0] in racemap else r[0]
					total_pct = r[2]
					population_pct = r[3]
					values = [
						total_pct,
						population_pct,
						last_edit_date,
						race_ethn,
						last_edit_date.date(),
					]
					cur.execute(sql_r, (*values, ))		

		# commit and vacuum analyze
		conn.commit()
		conn.autocommit = True
		cur.execute("VACUUM ANALYZE {}.{};".format(schema, table))
		conn.autocommit = False

	# close db conn
	pg_disconnect(conn, cur)
	return "Updated Long Beach"

# metadata for an ArcGIS endpoint
def arc_meta(arc_url):
	# get data from source
	req = requests.get(arc_url, params={})
	data = json.loads(req.content.decode('utf-8'))
	return data

# generic csv to postgres
def csv2pg(data_url, database, schema, table, fieldmap, racemap={}):
	print ('\nstarting %s.%s' % (schema, table))

	# get data from source
	req = requests.get(data_url, params={})
	records = pe.get_records(file_stream=req.content, file_type='csv')
	if not len(records):
		return # abort

	# db connect
	dbconn = pg_connect('covid19_race_class')
	conn = dbconn['conn']
	cur = dbconn['cur']

	# delete from the current table
	sql = "DELETE from {}.{};".format(schema, table)
	cur.execute(sql)

	# reset the gids so they don't get too huge
	sql = "ALTER SEQUENCE {}.{}_id_seq restart;".format(schema, table)
	cur.execute(sql)

	# load data into table
	fieldlist = fieldmap.items()
	columns = [ v for k, v in fieldlist ]
	sql = "INSERT into %s.%s (%s) values " % (schema, table, ", ".join(columns))
	for r in records:
		slist = [ "%s" for c in columns ]
		sql_r = sql + "({});".format(", ".join(slist))
		values = [ r[k] for k, v in fieldlist ]
		cur.execute(sql_r, (*values, ))

	# commit changes
	conn.commit()

	# commit changes to end transaction
	conn.commit()

	# vacuum analyze
	conn.autocommit = True
	cur.execute("VACUUM ANALYZE {}.{}".format(schema, table))

	# close db conn
	pg_disconnect(conn, cur)
	return "Updated %s.%s" % (schema, table)

# custom html endpoints
def html2pg_tests_county(database, schema, table):
	print ('\nstarting testing by county')
	# table loads with the html, don't see any API endpoint for getting the data
	# pull the page html
	page_url = 'https://www.cdph.ca.gov/Programs/CID/DCDC/Pages/COVID-19/COVID19CountyDataTable.aspx'
	req = requests.get(page_url, params={})
	root = html.fromstring(req.content.decode('utf-8'))
	
	# check last updated date
	last_edit_date = root.xpath("//*[contains(text(), 'Chart last updated on ')]//text()")[0].replace('Chart last updated on ', '')
	last_edit_date = datetime.strptime(last_edit_date, '%B %d, %Y').date()

	# db connect
	dbconn = pg_connect(database)
	conn = dbconn['conn']
	cur = dbconn['cur']

	# check whether data are current
	sql = "SELECT max(data_date) as dt from %s.%s;" % (schema, table)
	dt = run_sql_select_query(cur=cur, sql=sql)[0]['dt']
	print ('last edit', last_edit_date, '\ndata date', dt)
	if dt and dt >= last_edit_date:
		pg_disconnect(conn, cur)
		return "No new data for %s.%s" % (schema, table)

	# get the table rows (there is just one table on the page)
	rows = []
	for r in root.xpath("//table")[0].xpath(".//tr")[3:]:
		rows.append(r.xpath('.//td/text()'))

	noteslist = [ r.replace('\r\n', '') for r in root.xpath("//table")[1].xpath(".//tr/td//*/text()") ]

	# insert into db
	print ('inserting records')
	columns = [ 'county', 'avg_tests_per100k', 'notes', 'data_date', ]
	sql = "INSERT into %s.%s (%s) values " % (schema, table, ", ".join(columns))
	for r in rows:
		slist = [ "%s" for c in columns ]
		sql_r = sql + "({});".format(", ".join(slist))
		county_sp = r[0].split('*')
		values = [
			county_sp[0].replace('*', ''), 
			r[1], 
			noteslist[len(county_sp) - 2] if len(county_sp) > 1 else None, 
			last_edit_date,
		]
		cur.execute(sql_r, (*values, ))
		
	# commit inserts
	conn.commit()

	# vacuum analyze
	print ('cleaning up')
	conn.autocommit = True
	cur.execute("VACUUM ANALYZE {}.{};".format(schema, table))
	conn.autocommit = False

	# close db conn
	pg_disconnect(conn, cur)
	return 'finished %s.%s' % (schema, table)