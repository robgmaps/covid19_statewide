------------------------------------------------------------------------------
-- SACRAMENTO
------------------------------------------------------------------------------

	-- CASES

		-- table state_latest.sacramento_race_cases_latest
		drop table if exists state_latest.sacramento_race_cases_latest;
		create table state_latest.sacramento_race_cases_latest (
			id serial primary key,
			race_ethn varchar,
			total int,
			total_pct numeric,
			data_date timestamp with time zone,
			row_date timestamp with time zone default now()
		);

		create index state_latest_sacramento_race_cases_latest_race_ethn on state_latest.sacramento_race_cases_latest (race_ethn);
		create index state_latest_sacramento_race_cases_latest_data_date on state_latest.sacramento_race_cases_latest (data_date);
		create index state_latest_sacramento_race_cases_latest_row_date on state_latest.sacramento_race_cases_latest (row_date);

		comment on table state_latest.sacramento_race_cases_latest is 'Cases by race/ethnicity from Sacramento County DPH ArcGIS feature server layer COVID19_Race_Ethnicity.  Layer information at https://services6.arcgis.com/yeTSZ1znt7H7iDG7/ArcGIS/rest/services/COVID19_Race_Ethnicity/FeatureServer/0.  Updates daily with new data from query endpoint.  See data_date column for data vintage and row_date for when data were loaded.

		ArcGIS endpoint for data: https://services6.arcgis.com/yeTSZ1znt7H7iDG7/arcgis/rest/services/COVID19_Race_Ethnicity/FeatureServer/0/query?f=json&where=1%3D1&outFields=*

		ArcGIS endpoint for race known/unknown: https://services6.arcgis.com/yeTSZ1znt7H7iDG7/ArcGIS/rest/services/COVID19_Race_Ethnicity_Known_Unknown/FeatureServer/0/query?where=1%3D1&outFields=*&f=json';

		COMMENT ON COLUMN state_latest.sacramento_race_cases_latest.race_ethn IS 'Race/Ethnicity.';
		COMMENT ON COLUMN state_latest.sacramento_race_cases_latest.total IS 'Cumulative cases.';
		COMMENT ON COLUMN state_latest.sacramento_race_cases_latest.total_pct IS 'Percent of cumulative cases.';
		COMMENT ON COLUMN state_latest.sacramento_race_cases_latest.data_date IS 'Last updated date of data according to layer metadata page at https://services6.arcgis.com/yeTSZ1znt7H7iDG7/ArcGIS/rest/services/COVID19_Race_Ethnicity/FeatureServer/0.';
		COMMENT ON COLUMN state_latest.sacramento_race_cases_latest.row_date is 'Date row was added to this table.';

	------------------------------------------------------------------------------

	-- DEATHS

		-- table state_latest.sacramento_race_deaths_latest
		drop table if exists state_latest.sacramento_race_deaths_latest;
		create table state_latest.sacramento_race_deaths_latest (
			id serial primary key,
			race_ethn varchar,
			total int,
			total_pct numeric,
			data_date timestamp with time zone,
			row_date timestamp with time zone default now()
		);

		create index state_latest_sacramento_race_deaths_latest_race_ethn on state_latest.sacramento_race_deaths_latest (race_ethn);
		create index state_latest_sacramento_race_deaths_latest_data_date on state_latest.sacramento_race_deaths_latest (data_date);
		create index state_latest_sacramento_race_deaths_latest_row_date on state_latest.sacramento_race_deaths_latest (row_date);

		comment on table state_latest.sacramento_race_deaths_latest is 'Deaths by race/ethnicity from Sacramento County DPH ArcGIS feature server layer COVID19_Deaths_by_Race_Ethnicity.  Layer information at https://services6.arcgis.com/yeTSZ1znt7H7iDG7/ArcGIS/rest/services/COVID19_Deaths_by_Race_Ethnicity/FeatureServer/0.  Updates daily with new data from query endpoint.  See data_date column for data vintage and row_date for when data were loaded.

		ArcGIS endpoint for race data: https://services6.arcgis.com/yeTSZ1znt7H7iDG7/arcgis/rest/services/COVID19_Deaths_by_Race_Ethnicity/FeatureServer/0/query?f=json&where=1%3D1&outFields=*

		ArcGIS endpoint for race known/unknown: https://services6.arcgis.com/yeTSZ1znt7H7iDG7/ArcGIS/rest/services/COVID19_Race_Ethnicity_Known_Unknown/FeatureServer/0/query?where=1%3D1&outFields=*&f=json';

		COMMENT ON COLUMN state_latest.sacramento_race_deaths_latest.race_ethn IS 'Race/Ethnicity.';
		COMMENT ON COLUMN state_latest.sacramento_race_deaths_latest.total IS 'Cumulative deaths.';
		COMMENT ON COLUMN state_latest.sacramento_race_deaths_latest.total_pct IS 'Percent of cumulative deaths.';
		COMMENT ON COLUMN state_latest.sacramento_race_deaths_latest.data_date IS 'Last updated date of data according to layer metadata page at https://services6.arcgis.com/yeTSZ1znt7H7iDG7/ArcGIS/rest/services/COVID19_Deaths_by_Race_Ethnicity/FeatureServer/0.';
		COMMENT ON COLUMN state_latest.sacramento_race_deaths_latest.row_date is 'Date row was added to this table.';

	------------------------------------------------------------------------------

	-- RACE KNOWN/UNKNOWN

		-- table state_latest.sacramento_race_known_unknown_latest
		drop table if exists state_latest.sacramento_race_known_unknown_latest;
		create table state_latest.sacramento_race_known_unknown_latest (
			id serial primary key,
			race_ethn varchar,
			total int,
			total_pct numeric,
			data_date timestamp with time zone,
			row_date timestamp with time zone default now()
		);

		create index state_latest_sacramento_race_known_unknown_latest_race_ethn on state_latest.sacramento_race_known_unknown_latest (race_ethn);
		create index state_latest_sacramento_race_known_unknown_latest_data_date on state_latest.sacramento_race_known_unknown_latest (data_date);
		create index state_latest_sacramento_race_known_unknown_latest_row_date on state_latest.sacramento_race_known_unknown_latest (row_date);

		comment on table state_latest.sacramento_race_known_unknown_latest is 'Cases and deaths with known vs. unknown race/ethnicity from Sacramento County DPH ArcGIS feature server layer COVID19_Race_Ethnicity_Known_Unknown.  Layer information at https://services6.arcgis.com/yeTSZ1znt7H7iDG7/ArcGIS/rest/services/COVID19_Race_Ethnicity_Known_Unknown/FeatureServer/0.  Updates daily with new data from query endpoint.  See data_date column for data vintage and row_date for when data were loaded.

		ArcGIS endpoint for data: https://services6.arcgis.com/yeTSZ1znt7H7iDG7/ArcGIS/rest/services/COVID19_Race_Ethnicity_Known_Unknown/FeatureServer/0/query?where=1%3D1&outFields=*&f=json';

		COMMENT ON COLUMN state_latest.sacramento_race_known_unknown_latest.race_ethn IS 'Cases/deaths known or unknown.';
		COMMENT ON COLUMN state_latest.sacramento_race_known_unknown_latest.total IS 'Cumulative cases or deaths in race_ethn category.';
		COMMENT ON COLUMN state_latest.sacramento_race_known_unknown_latest.total_pct IS 'Percent of cases or deaths in race_ethn category.';
		COMMENT ON COLUMN state_latest.sacramento_race_known_unknown_latest.data_date IS 'Last updated date of data according to layer metadata page at https://services6.arcgis.com/yeTSZ1znt7H7iDG7/ArcGIS/rest/services/COVID19_Race_Ethnicity_Known_Unknown/FeatureServer/0.';
		COMMENT ON COLUMN state_latest.sacramento_race_known_unknown_latest.row_date is 'Date row was added to this table.';

	------------------------------------------------------------------------------

	-- TESTING

		-- not available

	------------------------------------------------------------------------------

------------------------------------------------------------------------------
-- RIVERSIDE
------------------------------------------------------------------------------

	-- CASES

		-- table state_latest.riverside_race_cases_latest
		drop table if exists state_latest.riverside_race_cases_latest;
		create table state_latest.riverside_race_cases_latest (
			id serial primary key,
			race_ethn varchar,
			total int,
			total_pct numeric,
			crude_rate numeric,
			population int,
			data_date timestamp with time zone,
			row_date timestamp with time zone default now()
		);

		create index state_latest_riverside_race_cases_latest_race_ethn on state_latest.riverside_race_cases_latest (race_ethn);
		create index state_latest_riverside_race_cases_latest_data_date on state_latest.riverside_race_cases_latest (data_date);
		create index state_latest_riverside_race_cases_latest_row_date on state_latest.riverside_race_cases_latest (row_date);

		comment on table state_latest.riverside_race_cases_latest is 'Cases by race/ethnicity from Riverside County DPH ArcGIS feature server layer COVID19_Race_Ethnicity.  Layer information at https://services1.arcgis.com/pWmBUdSlVpXStHU6/ArcGIS/rest/services/COVID19_Race_Graph/FeatureServer/0.  Updates daily with new data from query endpoint.  See data_date column for data vintage and row_date for when data were loaded.

		ArcGIS endpoint for data: https://services1.arcgis.com/pWmBUdSlVpXStHU6/ArcGIS/rest/services/COVID19_Race_Graph/FeatureServer/0/query?where=race+is+not+null&outFields=*&f=json';

		COMMENT ON COLUMN state_latest.riverside_race_cases_latest.race_ethn IS 'Race/Ethnicity.';
		COMMENT ON COLUMN state_latest.riverside_race_cases_latest.total IS 'Cumulative cases.';
		COMMENT ON COLUMN state_latest.riverside_race_cases_latest.total_pct IS 'Percent of cumulative cases.';
		COMMENT ON COLUMN state_latest.riverside_race_cases_latest.crude_rate IS 'Case rate per 100k.';
		COMMENT ON COLUMN state_latest.riverside_race_cases_latest.population IS 'Population.';
		COMMENT ON COLUMN state_latest.riverside_race_cases_latest.data_date IS 'Last updated date of data according to layer metadata page at https://services1.arcgis.com/pWmBUdSlVpXStHU6/ArcGIS/rest/services/COVID19_Race_Graph/FeatureServer/0.';
		COMMENT ON COLUMN state_latest.riverside_race_cases_latest.row_date is 'Date row was added to this table.';

		------------------------------------------------------------------------------

		-- DEATHS

		-- not available

		------------------------------------------------------------------------------

		-- TESTING

		-- see it on their dashboard but not in their data, still searching

		------------------------------------------------------------------------------

------------------------------------------------------------------------------
-- ORANGE
------------------------------------------------------------------------------

	-- CASES

		-- table state_latest.orange_race_cases_latest
		drop table if exists state_latest.orange_race_cases_latest;
		create table state_latest.orange_race_cases_latest (
			id serial primary key,
			race_ethn varchar,
			total int,
			total_pct numeric,
			population_pct numeric,
			data_date timestamp with time zone,
			row_date timestamp with time zone default now()
		);

		create index state_latest_orange_race_cases_latest_race_ethn on state_latest.orange_race_cases_latest (race_ethn);
		create index state_latest_orange_race_cases_latest_data_date on state_latest.orange_race_cases_latest (data_date);
		create index state_latest_orange_race_cases_latest_row_date on state_latest.orange_race_cases_latest (row_date);

		comment on table state_latest.orange_race_cases_latest is 'Cases by race/ethnicity from Orange County DPH ArcGIS feature server layer occovid_democase_csv.  Layer information at https://services2.arcgis.com/LORzk2hk9xzHouw9/ArcGIS/rest/services/occovid_democase_csv/FeatureServer/0.  Updates daily with new data from query endpoint.  See data_date column for data vintage and row_date for when data were loaded.

		ArcGIS endpoint for data: https://services2.arcgis.com/LORzk2hk9xzHouw9/ArcGIS/rest/services/occovid_democase_csv/FeatureServer/0/query?where=1%3D1&outFields=*&f=json';

		COMMENT ON COLUMN state_latest.orange_race_cases_latest.race_ethn IS 'Race/Ethnicity.';
		COMMENT ON COLUMN state_latest.orange_race_cases_latest.total IS 'Cumulative cases.';
		COMMENT ON COLUMN state_latest.orange_race_cases_latest.total_pct IS 'Percent of cumulative cases.';
		COMMENT ON COLUMN state_latest.orange_race_cases_latest.population_pct IS 'Percent of total population.';
		COMMENT ON COLUMN state_latest.orange_race_cases_latest.data_date IS 'Last updated date of data according to layer metadata page at https://services2.arcgis.com/LORzk2hk9xzHouw9/ArcGIS/rest/services/occovid_democase_csv/FeatureServer/0.';
		COMMENT ON COLUMN state_latest.orange_race_cases_latest.row_date is 'Date row was added to this table.';

	------------------------------------------------------------------------------

	-- DEATHS

		-- table state_latest.orange_race_deaths_latest
		drop table if exists state_latest.orange_race_deaths_latest;
		create table state_latest.orange_race_deaths_latest (
			id serial primary key,
			race_ethn varchar,
			total int,
			total_pct numeric,
			population_pct numeric,
			data_date timestamp with time zone,
			row_date timestamp with time zone default now()
		);

		create index state_latest_orange_race_deaths_latest_race_ethn on state_latest.orange_race_deaths_latest (race_ethn);
		create index state_latest_orange_race_deaths_latest_data_date on state_latest.orange_race_deaths_latest (data_date);
		create index state_latest_orange_race_deaths_latest_row_date on state_latest.orange_race_deaths_latest (row_date);

		comment on table state_latest.orange_race_deaths_latest is 'Deaths by race/ethnicity from Orange County DPH ArcGIS feature server layer occovid_democase_csv.  Layer information at https://services2.arcgis.com/LORzk2hk9xzHouw9/ArcGIS/rest/services/occovid_demodth_csv/FeatureServer/0.  Updates daily with new data from query endpoint.  See data_date column for data vintage and row_date for when data were loaded.

		ArcGIS endpoint for data: https://services2.arcgis.com/LORzk2hk9xzHouw9/ArcGIS/rest/services/occovid_demodth_csv/FeatureServer/0/query?where=1%3D1&outFields=*&f=json';

		COMMENT ON COLUMN state_latest.orange_race_deaths_latest.race_ethn IS 'Race/Ethnicity.';
		COMMENT ON COLUMN state_latest.orange_race_deaths_latest.total IS 'Cumulative deaths.';
		COMMENT ON COLUMN state_latest.orange_race_deaths_latest.total_pct IS 'Percent of cumulative deaths.';
		COMMENT ON COLUMN state_latest.orange_race_deaths_latest.population_pct IS 'Percent of total population.';
		COMMENT ON COLUMN state_latest.orange_race_deaths_latest.data_date IS 'Last updated date of data according to layer metadata page at https://services2.arcgis.com/LORzk2hk9xzHouw9/ArcGIS/rest/services/occovid_demodth_csv/FeatureServer/0.';
		COMMENT ON COLUMN state_latest.orange_race_deaths_latest.row_date is 'Date row was added to this table.';

	------------------------------------------------------------------------------

	-- TESTING

		-- They have it (pcr and sero), come back to

	------------------------------------------------------------------------------

------------------------------------------------------------------------------
-- FRESNO
------------------------------------------------------------------------------

	-- CASES

		-- table state_latest.fresno_race_cases_latest
		drop table if exists state_latest.fresno_race_cases_latest;
		create table state_latest.fresno_race_cases_latest (
			id serial primary key,
			race_ethn varchar,
			crude_rate numeric,
			data_date timestamp with time zone,
			row_date timestamp with time zone default now()
		);

		create index state_latest_fresno_race_cases_latest_race_ethn on state_latest.fresno_race_cases_latest (race_ethn);
		create index state_latest_fresno_race_cases_latest_data_date on state_latest.fresno_race_cases_latest (data_date);
		create index state_latest_fresno_race_cases_latest_row_date on state_latest.fresno_race_cases_latest (row_date);

		comment on table state_latest.fresno_race_cases_latest is 'Cases by race/ethnicity from Fresno County DPH ArcGIS feature server layer CoronavirusCases_ByEthnicity_Current.  Layer information at https://services3.arcgis.com/ibgDyuD2DLBge82s/ArcGIS/rest/services/CoronavirusCases_ByEthnicity_Current/FeatureServer/0.  Updates daily with new data from query endpoint.  See data_date column for data vintage and row_date for when data were loaded.

		ArcGIS endpoint for data: https://services3.arcgis.com/ibgDyuD2DLBge82s/ArcGIS/rest/services/CoronavirusCases_ByEthnicity_Current/FeatureServer/0/query?where=1=1&outFields=*&f=json';

		COMMENT ON COLUMN state_latest.fresno_race_cases_latest.race_ethn IS 'Race/Ethnicity.';
		COMMENT ON COLUMN state_latest.fresno_race_cases_latest.crude_rate IS 'Case rate per 100k.';
		COMMENT ON COLUMN state_latest.fresno_race_cases_latest.data_date IS 'Last updated date of data according to layer metadata page at https://services3.arcgis.com/ibgDyuD2DLBge82s/ArcGIS/rest/services/CoronavirusCases_ByEthnicity_Current/FeatureServer/0.';
		COMMENT ON COLUMN state_latest.fresno_race_cases_latest.row_date is 'Date row was added to this table.';

	------------------------------------------------------------------------------

	-- DEATHS

		-- table state_latest.fresno_race_deaths_latest
		drop table if exists state_latest.fresno_race_deaths_latest;
		create table state_latest.fresno_race_deaths_latest (
			id serial primary key,
			race_ethn varchar,
			crude_rate numeric,
			data_date timestamp with time zone,
			row_date timestamp with time zone default now()
		);

		create index state_latest_fresno_race_deaths_latest_race_ethn on state_latest.fresno_race_deaths_latest (race_ethn);
		create index state_latest_fresno_race_deaths_latest_data_date on state_latest.fresno_race_deaths_latest (data_date);
		create index state_latest_fresno_race_deaths_latest_row_date on state_latest.fresno_race_deaths_latest (row_date);

		comment on table state_latest.fresno_race_deaths_latest is 'Deaths by race/ethnicity from Fresno County DPH ArcGIS feature server layer CoronavirusCases_ByEthnicity_Current.  Layer information at https://services3.arcgis.com/ibgDyuD2DLBge82s/ArcGIS/rest/services/CoronavirusCases_ByEthnicity_Current/FeatureServer/0.  Updates daily with new data from query endpoint.  See data_date column for data vintage and row_date for when data were loaded.

		ArcGIS endpoint for data: https://services3.arcgis.com/ibgDyuD2DLBge82s/ArcGIS/rest/services/CoronavirusCases_ByEthnicity_Current/FeatureServer/0/query?where=1=1&outFields=*&f=json';

		COMMENT ON COLUMN state_latest.fresno_race_deaths_latest.race_ethn IS 'Race/Ethnicity.';
		COMMENT ON COLUMN state_latest.fresno_race_deaths_latest.crude_rate IS 'Case rate per 100k.';
		COMMENT ON COLUMN state_latest.fresno_race_deaths_latest.data_date IS 'Last updated date of data according to layer metadata page at https://services3.arcgis.com/ibgDyuD2DLBge82s/ArcGIS/rest/services/CoronavirusCases_ByEthnicity_Current/FeatureServer/0.';
		COMMENT ON COLUMN state_latest.fresno_race_deaths_latest.row_date is 'Date row was added to this table.';

	------------------------------------------------------------------------------

	-- TESTING

		-- table state_latest.fresno_race_testing_latest
		drop table if exists state_latest.fresno_race_testing_latest;
		create table state_latest.fresno_race_testing_latest (
			id serial primary key,
			race_ethn varchar,
			total int,
			data_date timestamp with time zone,
			row_date timestamp with time zone default now()
		);

		create index state_latest_fresno_race_testing_latest_race_ethn on state_latest.fresno_race_testing_latest (race_ethn);
		create index state_latest_fresno_race_testing_latest_data_date on state_latest.fresno_race_testing_latest (data_date);
		create index state_latest_fresno_race_testing_latest_row_date on state_latest.fresno_race_testing_latest (row_date);

		comment on table state_latest.fresno_race_testing_latest is 'Testing by race/ethnicity from Fresno County DPH ArcGIS feature server layer CoronavirusCases_ByEthnicity_Current.  Layer information at https://services3.arcgis.com/ibgDyuD2DLBge82s/ArcGIS/rest/services/CoronavirusCases_ByEthnicity_Current/FeatureServer/0.  Updates daily with new data from query endpoint.  See data_date column for data vintage and row_date for when data were loaded.

		ArcGIS endpoint for data: https://services3.arcgis.com/ibgDyuD2DLBge82s/ArcGIS/rest/services/CoronavirusCases_ByEthnicity_Current/FeatureServer/0/query?where=1=1&outFields=*&f=json';

		COMMENT ON COLUMN state_latest.fresno_race_testing_latest.race_ethn IS 'Race/Ethnicity.';
		COMMENT ON COLUMN state_latest.fresno_race_testing_latest.total IS 'Cumulative tests.';
		COMMENT ON COLUMN state_latest.fresno_race_testing_latest.data_date IS 'Last updated date of data according to layer metadata page at https://services3.arcgis.com/ibgDyuD2DLBge82s/ArcGIS/rest/services/CoronavirusCases_ByEthnicity_Current/FeatureServer/0.';
		COMMENT ON COLUMN state_latest.fresno_race_testing_latest.row_date is 'Date row was added to this table.';

		-- also has hospitalizations by race, though all nulls other than "other"

------------------------------------------------------------------------------
-- ALAMEDA
------------------------------------------------------------------------------

	-- CASES

		-- Power BI, looks like there is an endpoint though... need to research more
		-- CASES

		-- table state_latest.alameda_race_cases_latest
		drop table if exists state_latest.alameda_race_cases_latest;
		create table state_latest.alameda_race_cases_latest (
			id serial primary key,
			race_ethn varchar,
			total int,
			crude_rate numeric,
			data_date timestamp with time zone,
			row_date timestamp with time zone default now()
		);

		create index state_latest_alameda_race_cases_latest_race_ethn on state_latest.alameda_race_cases_latest (race_ethn);
		create index state_latest_alameda_race_cases_latest_data_date on state_latest.alameda_race_cases_latest (data_date);
		create index state_latest_alameda_race_cases_latest_row_date on state_latest.alameda_race_cases_latest (row_date);

		comment on table state_latest.alameda_race_cases_latest is 'Cases by race/ethnicity from Alameda County DPH Power BI app.  Updates daily with new data from page charts.  See data_date column for data vintage and row_date for when data were loaded.

		Data dashboard at: https://app.powerbigov.us/view?r=eyJrIjoiM2EyMmNiMjMtY2YxYS00MzZlLTlhMzMtNTExZDJlZGMyOWYzIiwidCI6IjMyZmRmZjJjLWY4NmUtNGJhMy1hNDdkLTZhNDRhN2Y0NWE2NCJ9&pageName=ReportSection';

		COMMENT ON COLUMN state_latest.alameda_race_cases_latest.race_ethn IS 'Race/Ethnicity.';
		COMMENT ON COLUMN state_latest.alameda_race_cases_latest.total IS 'Cumulative cases.';
		COMMENT ON COLUMN state_latest.alameda_race_cases_latest.crude_rate IS 'Case rate per 100k.';
		COMMENT ON COLUMN state_latest.alameda_race_cases_latest.data_date IS 'Last updated date of data according to response metadata.';
		COMMENT ON COLUMN state_latest.alameda_race_cases_latest.row_date is 'Date row was added to this table.';

	------------------------------------------------------------------------------

	-- DEATHS

		-- table state_latest.alameda_race_deaths_latest
		drop table if exists state_latest.alameda_race_deaths_latest;
		create table state_latest.alameda_race_deaths_latest (
			id serial primary key,
			race_ethn varchar,
			total int,
			crude_rate numeric,
			data_date timestamp with time zone,
			row_date timestamp with time zone default now()
		);

		create index state_latest_alameda_race_deaths_latest_race_ethn on state_latest.alameda_race_deaths_latest (race_ethn);
		create index state_latest_alameda_race_deaths_latest_data_date on state_latest.alameda_race_deaths_latest (data_date);
		create index state_latest_alameda_race_deaths_latest_row_date on state_latest.alameda_race_deaths_latest (row_date);

		comment on table state_latest.alameda_race_deaths_latest is 'Deaths by race/ethnicity from Alameda County DPH Power BI app.  Updates daily with new data from page charts.  See data_date column for data vintage and row_date for when data were loaded.

		Data dashboard at: https://app.powerbigov.us/view?r=eyJrIjoiM2EyMmNiMjMtY2YxYS00MzZlLTlhMzMtNTExZDJlZGMyOWYzIiwidCI6IjMyZmRmZjJjLWY4NmUtNGJhMy1hNDdkLTZhNDRhN2Y0NWE2NCJ9&pageName=ReportSection';

		COMMENT ON COLUMN state_latest.alameda_race_deaths_latest.race_ethn IS 'Race/Ethnicity.';
		COMMENT ON COLUMN state_latest.alameda_race_deaths_latest.total IS 'Cumulative deaths.';
		COMMENT ON COLUMN state_latest.alameda_race_deaths_latest.crude_rate IS 'Death rate per 100k.';
		COMMENT ON COLUMN state_latest.alameda_race_deaths_latest.data_date IS 'Last updated date of data according to response metadata.';
		COMMENT ON COLUMN state_latest.fresno_race_deaths_latest.row_date is 'Date row was added to this table.';

	------------------------------------------------------------------------------

	-- TESTING

	------------------------------------------------------------------------------

------------------------------------------------------------------------------
-- SAN JOAQUIN
------------------------------------------------------------------------------

	-- CASES

		-- table state_latest.san_joaquin_race_cases_latest
		drop table if exists state_latest.san_joaquin_race_cases_latest;
		create table state_latest.san_joaquin_race_cases_latest (
			id serial primary key,
			race_ethn varchar,
			total int,
			total_pct numeric,
			population_pct numeric,
			data_date timestamp with time zone,
			row_date timestamp with time zone default now()
		);

		create index state_latest_san_joaquin_race_cases_latest_race_ethn on state_latest.san_joaquin_race_cases_latest (race_ethn);
		create index state_latest_san_joaquin_race_cases_latest_data_date on state_latest.san_joaquin_race_cases_latest (data_date);
		create index state_latest_san_joaquin_race_cases_latest_row_date on state_latest.san_joaquin_race_cases_latest (row_date);

		comment on table state_latest.san_joaquin_race_cases_latest is 'Cases by race/ethnicity from San Joaquin County DPH ArcGIS feature server layer COVID_Race.  Layer information at https://services6.arcgis.com/NtWO9krY7z9jd3mY/ArcGIS/rest/services/COVID_Race/FeatureServer/0.  Updates daily with new data from query endpoint.  See data_date column for data vintage and row_date for when data were loaded.

		ArcGIS endpoint for data: https://services6.arcgis.com/NtWO9krY7z9jd3mY/ArcGIS/rest/services/COVID_Race/FeatureServer/0/query?where=1%3D1&outFields=*&f=json';

		COMMENT ON COLUMN state_latest.san_joaquin_race_cases_latest.race_ethn IS 'Race/Ethnicity.';
		COMMENT ON COLUMN state_latest.san_joaquin_race_cases_latest.total IS 'Cumulative cases.';
		COMMENT ON COLUMN state_latest.san_joaquin_race_cases_latest.total_pct IS 'Percent of cumulative cases.';
		COMMENT ON COLUMN state_latest.san_joaquin_race_cases_latest.population_pct IS 'Percent of total population.';
		COMMENT ON COLUMN state_latest.san_joaquin_race_cases_latest.data_date IS 'Last updated date of data according to layer metadata page at https://services6.arcgis.com/NtWO9krY7z9jd3mY/ArcGIS/rest/services/COVID_Race/FeatureServer/0.';
		COMMENT ON COLUMN state_latest.san_joaquin_race_cases_latest.row_date is 'Date row was added to this table.';

	------------------------------------------------------------------------------

	-- DEATHS

		-- table state_latest.san_joaquin_race_deaths_latest
		drop table if exists state_latest.san_joaquin_race_deaths_latest;
		create table state_latest.san_joaquin_race_deaths_latest (
			id serial primary key,
			race_ethn varchar,
			total int,
			total_pct numeric,
			population_pct numeric,
			data_date timestamp with time zone,
			row_date timestamp with time zone default now()
		);

		create index state_latest_san_joaquin_race_deaths_latest_race_ethn on state_latest.san_joaquin_race_deaths_latest (race_ethn);
		create index state_latest_san_joaquin_race_deaths_latest_data_date on state_latest.san_joaquin_race_deaths_latest (data_date);
		create index state_latest_san_joaquin_race_deaths_latest_row_date on state_latest.san_joaquin_race_deaths_latest (row_date);

		comment on table state_latest.san_joaquin_race_deaths_latest is 'Deaths by race/ethnicity from San Joaquin County DPH ArcGIS feature server layer COVID_Race.  Layer information at https://services6.arcgis.com/NtWO9krY7z9jd3mY/ArcGIS/rest/services/COVID_Race/FeatureServer/0.  Updates daily with new data from query endpoint.  See data_date column for data vintage and row_date for when data were loaded.

		ArcGIS endpoint for data: https://services6.arcgis.com/NtWO9krY7z9jd3mY/ArcGIS/rest/services/COVID_Race/FeatureServer/0/query?where=1%3D1&outFields=*&f=json';

		COMMENT ON COLUMN state_latest.san_joaquin_race_deaths_latest.race_ethn IS 'Race/Ethnicity.';
		COMMENT ON COLUMN state_latest.san_joaquin_race_deaths_latest.total IS 'Cumulative deaths.';
		COMMENT ON COLUMN state_latest.san_joaquin_race_deaths_latest.total_pct IS 'Percent of cumulative deaths.';
		COMMENT ON COLUMN state_latest.san_joaquin_race_deaths_latest.population_pct IS 'Percent of total population.';
		COMMENT ON COLUMN state_latest.san_joaquin_race_deaths_latest.data_date IS 'Last updated date of data according to layer metadata page at https://services6.arcgis.com/NtWO9krY7z9jd3mY/ArcGIS/rest/services/COVID_Race/FeatureServer/0.';
		COMMENT ON COLUMN state_latest.san_joaquin_race_deaths_latest.row_date is 'Date row was added to this table.';

	------------------------------------------------------------------------------

	-- TESTING



	------------------------------------------------------------------------------

------------------------------------------------------------------------------
-- PASADENA
------------------------------------------------------------------------------

	-- CASES

		-- table state_latest.pasadena_race_cases_latest
		drop table if exists state_latest.pasadena_race_cases_latest;
		create table state_latest.pasadena_race_cases_latest (
			id serial primary key,
			race_ethn varchar,
			total int,
			data_date timestamp with time zone,
			row_date timestamp with time zone default now()
		);

		create index state_latest_pasadena_race_cases_latest_race_ethn on state_latest.pasadena_race_cases_latest (race_ethn);
		create index state_latest_pasadena_race_cases_latest_data_date on state_latest.pasadena_race_cases_latest (data_date);
		create index state_latest_pasadena_race_cases_latest_row_date on state_latest.pasadena_race_cases_latest (row_date);

		comment on table state_latest.pasadena_race_cases_latest is 'Cases by race/ethnicity from Pasadena DPH ArcGIS feature server layer PasadenaCACOVID19Cases.  Layer information at https://services2.arcgis.com/zNjnZafDYCAJAbN0/ArcGIS/rest/services/PasadenaCACOVID19Cases/FeatureServer/0.  Updates daily with new data from query endpoint.  See data_date column for data vintage and row_date for when data were loaded.

		ArcGIS endpoint for data: https://services2.arcgis.com/zNjnZafDYCAJAbN0/ArcGIS/rest/services/PasadenaCACOVID19Cases/FeatureServer/0/query?where=1%3D1&outFields=*&f=json';

		COMMENT ON COLUMN state_latest.pasadena_race_cases_latest.race_ethn IS 'Race/Ethnicity.';
		COMMENT ON COLUMN state_latest.pasadena_race_cases_latest.total IS 'Cumulative cases.';
		COMMENT ON COLUMN state_latest.pasadena_race_cases_latest.data_date IS 'Last updated date of data according to layer metadata page at https://services2.arcgis.com/zNjnZafDYCAJAbN0/ArcGIS/rest/services/PasadenaCACOVID19Cases/FeatureServer/0.';
		COMMENT ON COLUMN state_latest.pasadena_race_cases_latest.row_date is 'Date row was added to this table.';

	------------------------------------------------------------------------------

	-- DEATHS

		-- table state_latest.pasadena_race_deaths_latest
		drop table if exists state_latest.pasadena_race_deaths_latest;
		create table state_latest.pasadena_race_deaths_latest (
			id serial primary key,
			race_ethn varchar,
			total int,
			data_date timestamp with time zone,
			row_date timestamp with time zone default now()
		);

		create index state_latest_pasadena_race_deaths_latest_race_ethn on state_latest.pasadena_race_deaths_latest (race_ethn);
		create index state_latest_pasadena_race_deaths_latest_data_date on state_latest.pasadena_race_deaths_latest (data_date);
		create index state_latest_pasadena_race_deaths_latest_row_date on state_latest.pasadena_race_deaths_latest (row_date);

		comment on table state_latest.pasadena_race_deaths_latest is 'Deaths by race/ethnicity from Pasadena DPH ArcGIS feature server layer PasadenaCACOVID19Cases.  Layer information at https://services2.arcgis.com/zNjnZafDYCAJAbN0/ArcGIS/rest/services/PasadenaCACOVID19Cases/FeatureServer/0.  Updates daily with new data from query endpoint.  See data_date column for data vintage and row_date for when data were loaded.

		ArcGIS endpoint for data: https://services2.arcgis.com/zNjnZafDYCAJAbN0/ArcGIS/rest/services/PasadenaCACOVID19Cases/FeatureServer/0/query?where=1%3D1&outFields=*&f=json';

		COMMENT ON COLUMN state_latest.pasadena_race_deaths_latest.race_ethn IS 'Race/Ethnicity.';
		COMMENT ON COLUMN state_latest.pasadena_race_deaths_latest.total IS 'Cumulative deaths.';
		COMMENT ON COLUMN state_latest.pasadena_race_deaths_latest.data_date IS 'Last updated date of data according to layer metadata page at https://services2.arcgis.com/zNjnZafDYCAJAbN0/ArcGIS/rest/services/PasadenaCACOVID19Cases/FeatureServer/0.';
		COMMENT ON COLUMN state_latest.pasadena_race_deaths_latest.row_date is 'Date row was added to this table.';

	------------------------------------------------------------------------------

	-- TESTING



	------------------------------------------------------------------------------

------------------------------------------------------------------------------
-- LONG BEACH
------------------------------------------------------------------------------

	-- CASES
		-- by race/ethn and age group - % cases, % pop

		-- table state_latest.long_beach_race_cases_latest
		drop table if exists state_latest.long_beach_race_cases_latest;
		create table state_latest.long_beach_race_cases_latest (
			id serial primary key,
			race_ethn varchar,
			total_pct numeric,
			population_pct numeric,
			data_date timestamp with time zone,
			row_date timestamp with time zone default now()
		);

		create index state_latest_long_beach_race_cases_latest_race_ethn on state_latest.long_beach_race_cases_latest (race_ethn);
		create index state_latest_long_beach_race_cases_latest_data_date on state_latest.long_beach_race_cases_latest (data_date);
		create index state_latest_long_beach_race_cases_latest_row_date on state_latest.long_beach_race_cases_latest (row_date);

		comment on table state_latest.long_beach_race_cases_latest is 'Cases by race/ethnicity from Long Beach DPH Power BI app.  Updates daily with new data from page charts.  See data_date column for data vintage and row_date for when data were loaded.

		Data dashboard at: https://app.powerbigov.us/view?r=eyJrIjoiM2EyMmNiMjMtY2YxYS00MzZlLTlhMzMtNTExZDJlZGMyOWYzIiwidCI6IjMyZmRmZjJjLWY4NmUtNGJhMy1hNDdkLTZhNDRhN2Y0NWE2NCJ9&pageName=ReportSection';

		COMMENT ON COLUMN state_latest.long_beach_race_cases_latest.race_ethn IS 'Race/Ethnicity.';
		COMMENT ON COLUMN state_latest.long_beach_race_cases_latest.total_pct IS 'Percent of cumulative cases.';
		COMMENT ON COLUMN state_latest.long_beach_race_cases_latest.population_pct IS 'Percent of total population.';
		COMMENT ON COLUMN state_latest.long_beach_race_cases_latest.data_date IS 'Last updated date of data according to response metadata.';
		COMMENT ON COLUMN state_latest.long_beach_race_cases_latest.row_date is 'Date row was added to this table.';

	------------------------------------------------------------------------------

	-- DEATHS

		-- table state_latest.long_beach_race_deaths_latest
		drop table if exists state_latest.long_beach_race_deaths_latest;
		create table state_latest.long_beach_race_deaths_latest (
			id serial primary key,
			race_ethn varchar,
			total_pct numeric,
			population_pct numeric,
			data_date timestamp with time zone,
			row_date timestamp with time zone default now()
		);

		create index state_latest_long_beach_race_deaths_latest_race_ethn on state_latest.long_beach_race_deaths_latest (race_ethn);
		create index state_latest_long_beach_race_deaths_latest_data_date on state_latest.long_beach_race_deaths_latest (data_date);
		create index state_latest_long_beach_race_deaths_latest_row_date on state_latest.long_beach_race_deaths_latest (row_date);

		comment on table state_latest.long_beach_race_deaths_latest is 'Deaths by race/ethnicity from Long Beach DPH Power BI app.  Updates daily with new data from page charts.  See data_date column for data vintage and row_date for when data were loaded.

		Data dashboard at: https://app.powerbigov.us/view?r=eyJrIjoiM2EyMmNiMjMtY2YxYS00MzZlLTlhMzMtNTExZDJlZGMyOWYzIiwidCI6IjMyZmRmZjJjLWY4NmUtNGJhMy1hNDdkLTZhNDRhN2Y0NWE2NCJ9&pageName=ReportSection';

		COMMENT ON COLUMN state_latest.long_beach_race_deaths_latest.race_ethn IS 'Race/Ethnicity.';
		COMMENT ON COLUMN state_latest.long_beach_race_deaths_latest.total_pct IS 'Percent of cumulative deaths.';
		COMMENT ON COLUMN state_latest.long_beach_race_deaths_latest.population_pct IS 'Percent of total population.';
		COMMENT ON COLUMN state_latest.long_beach_race_deaths_latest.data_date IS 'Last updated date of data according to response metadata.';
		COMMENT ON COLUMN state_latest.long_beach_race_deaths_latest.row_date is 'Date row was added to this table.';

	------------------------------------------------------------------------------

	-- TESTING



	------------------------------------------------------------------------------

