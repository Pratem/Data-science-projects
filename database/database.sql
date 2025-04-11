--TABLE Locations
CREATE TABLE Location_details(
    iso_code TEXT NOT NULL
    , last_observation_date TEXT
    , source_name TEXT
    , source_website TEXT
    , PRIMARY KEY (iso_code)
);

CREATE TABLE Locations
(
    location TEXT NOT NULL
    , iso_code TEXT NOT NULL
    , FOREIGN KEY (iso_code) REFERENCES Location_details(iso_code)
);
    

CREATE TABLE Locations_vaccines_list(
    iso_code TEXT NOT NULL
    , vaccines TEXT NOT NULL
    , PRIMARY KEY (vaccines, iso_code)
    ,FOREIGN KEY (iso_code) REFERENCES Location_details(iso_code)
);

--Table Country_vaccination
CREATE TABLE Country_vaccination_Details
(
    location TEXT NOT NULL 
    , date TEXT NOT NULL
    , source_url TEXT
    , total_vaccinations INT
    , people_vaccinated INT
    , people_fully_vaccinated INT
    , total_boosters INT
    , PRIMARY KEY (location, date)
);

CREATE TABLE Country_vaccinations(    
    location TEXT NOT NULL 
    , date TEXT NOT NULL
    , iso_code TEXT NOT NULL
    ,FOREIGN KEY (iso_code) REFERENCES Location_details(iso_code)
    ,FOREIGN KEY (location, date) REFERENCES Country_vaccination_Details(location, date)
);

CREATE TABLE Country_vaccines_list(
    location TEXT NOT NULL
    , date TEXT NOT NULL
    , vaccines TEXT NOT NULL
    , PRIMARY KEY (vaccines, location, date)
    ,FOREIGN KEY (location, date) REFERENCES Country_vaccination_Details(location, date)
);

--TABLE Vaccinations_by_age_group
CREATE TABLE Vaccinations_by_age_group_details(
    location TEXT NOT NULL
    , date TEXT NOT NULL
    , age_group TEXT NOT NULL
    , people_vaccinated_per_hundred REAL
    , people_fully_vaccinated_per_hundred REAL
    , people_with_booster_per_hundred REAL
    , PRIMARY KEY (location, date, age_group)
);

CREATE TABLE Vaccinations_by_age_group(
    location TEXT NOT NULL
    , date TEXT NOT NULL
    , age_group TEXT NOT NULL
    , iso_code TEXT NOT NULL
    , FOREIGN KEY (location, date, age_group) REFERENCES Vaccinations_by_age_group_details(location, date, age_group)
    , FOREIGN KEY (iso_code) REFERENCES Location_details(iso_code)
);

--TABLE State_vaccinations
CREATE TABLE State_vaccinations_details(
    location TEXT NOT NULL
    , date TEXT NOT NULL
    , state TEXT NOT NULL
    , total_vaccinations INT
    , total_distributed INT
    , people_vaccinated INT
    , people_fully_vaccinated_per_hundred REAL
    , total_vaccinations_per_hundred REAL
    , people_fully_vaccinated INT
    , people_vaccinated_per_hundred REAL
    , distributed_per_hundred REAL
    , daily_vaccinations_raw INT
    , daily_vaccinations INT
    , daily_vaccinations_per_million REAL
    , share_doses_used REAL
    , total_boosters INT
    , total_boosters_per_hundred REAL
    , PRIMARY KEY (location, date, state)
);

CREATE TABLE state_vaccinations(
    location TEXT NOT NULL
    , date TEXT NOT NULL
    , state TEXT NOT NULL
    , iso_code TEXT NOT NULL   
    , FOREIGN KEY (location, date, state) REFERENCES State_vaccinations_details(location, date, state)
    , FOREIGN KEY (iso_code) REFERENCES Location_details(iso_code)
);


--CREATE Vaccination_by_manufacturer
CREATE TABLE Vaccination_by_manufacturer_details(
    location TEXT NOT NULL
    , date TEXT NOT NULL
    , vaccine TEXT NOT NULL
    , total_vaccinations INT
    , PRIMARY KEY (location, date, vaccine)
);

CREATE TABLE Vaccination_by_manufacturer(
    location TEXT NOT NULL
    , date TEXT NOT NULL
    , vaccine TEXT NOT NULL
    , iso_code TEXT NOT NULL
    , FOREIGN KEY (location, date, vaccine) REFERENCES Vaccination_by_manufacturer_details(location, date, vaccine)
    , FOREIGN KEY (iso_code) REFERENCES Location_details(iso_code)
);

--Table vaccinations
CREATE TABLE Vaccination_details(
    location TEXT NOT NULL
    ,date TEXT NOT NULL
    ,total_vaccinations INT
    ,people_vaccinated INT
    ,people_fully_vaccinated INT
    ,total_boosters INT
    ,daily_vaccinations_raw INT
    ,daily_vaccinations INT
    ,total_vaccinations_per_hundred REAL
    ,people_vaccinated_per_hundred REAL
    ,people_fully_vaccinated_per_hundred REAL
    ,total_boosters_per_hundred REAL
    ,daily_vaccinations_per_million REAL
    ,daily_people_vaccinated REAL
    ,daily_people_vaccinated_per_hundred REAL
    , PRIMARY KEY (location, date)
);


CREATE TABLE Vaccination(
    location TEXT NOT NULL
    , date TEXT NOT NULL
    , iso_code TEXT NOT NULL
    , FOREIGN KEY (location ,date) REFERENCES Vaccination_details(location ,date) 
    , FOREIGN KEY (iso_code) REFERENCES Location_details(iso_code)
);

--Inserting Missing ISO_CODE
insert into location_details(iso_code, last_observation_date, source_name, source_website) 
values( 'OWID_SAM', NULL, NULL, NULL),
( 'OWID_NAM', NULL, NULL, NULL),
('OWID_ASI',  NULL, NULL, NULL) ,
( 'EU', NULL, NULL, NULL),
( 'OWID_OCE', NULL, NULL, NULL), 
('OWID_EUR', NULL, NULL, NULL),
( 'OWID_WRL', NULL, NULL, NULL),
( 'OWID_AFR', NULL, NULL, NULL);

--Inserting Missing ISO_CODE and correspnding Location Name
insert into locations(location, iso_code) 
values
( 'South America',  'OWID_SAM'), 
('European Union','EU'),
('Africa','OWID_AFR'), 
('Asia','OWID_ASI'),
('Europe','OWID_EUR'),
('North America','OWID_NAM'),
('Oceania','OWID_OCE'),
('World','OWID_WRL');