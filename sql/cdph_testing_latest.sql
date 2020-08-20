create table state_latest.cdph_testing_latest (
	id serial primary key,
	tests int,
	data_date timestamp with time zone,
	row_date timestamp with time zone default now()
);

create index state_latest_cdph_testing_latest_data_date on state_latest.cdph_testing_latest (data_date);
create index state_latest_cdph_testing_latest_row_date on state_latest.cdph_testing_latest (row_date);

COMMENT on table state_latest.cdph_testing_latest is 'Daily California testing data from https://data.ca.gov/dataset/covid-19-testing/resource/b6648a0d-ff0a-4111-b80b-febda2ac9e09.';

COMMENT ON COLUMN state_latest.cdph_testing_latest.tests is 'Cumulative number of tests reported as pending from large laboratories.';
COMMENT ON COLUMN state_latest.cdph_testing_latest.data_date IS 'Date reported.';
COMMENT ON COLUMN state_latest.cdph_testing_latest.row_date is 'Date row was added to this table.';