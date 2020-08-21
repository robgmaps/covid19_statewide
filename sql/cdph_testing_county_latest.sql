-- Table: cdph_testing_county_latest
drop table if exists state_latest.cdph_testing_county_latest;
create table state_latest.cdph_testing_county_latest (
	id serial primary key,
	county varchar,
	avg_tests_per100k numeric,
	notes text,
	data_date date,
	row_date date default now()
);

create index state_latest_cdph_testing_county_latest_county on state_latest.cdph_testing_county_latest (county);
create index state_latest_cdph_testing_county_latest_data_date on state_latest.cdph_testing_county_latest (data_date);
create index state_latest_cdph_testing_county_latest_row_date on state_latest.cdph_testing_county_latest (row_date);

COMMENT on table state_latest.cdph_testing_county_latest is 'Average number of tests per day by County from table at https://www.cdph.ca.gov/Programs/CID/DCDC/Pages/COVID-19/COVID19CountyDataTable.aspx.  Auto-updates as data change.';

COMMENT on COLUMN state_latest.cdph_testing_county_latest.county is 'County name.';
COMMENT ON COLUMN state_latest.cdph_testing_county_latest.avg_tests_per100k is 'Avg # tests per day (per 100,000 population) (7 day average with a 7 day lag).';
COMMENT on COLUMN state_latest.cdph_testing_county_latest.notes is 'Notes on County Monitoring List status (asterisks in the source table).';
COMMENT ON COLUMN state_latest.cdph_testing_county_latest.data_date IS 'Date reported according to "Chart last updated on..." statement on source web page.';
COMMENT ON COLUMN state_latest.cdph_testing_county_latest.row_date is 'Date row was added to this table.';