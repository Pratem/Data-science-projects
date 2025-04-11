--D.1)
SELECT
    location AS "Country Name (CN)",
    ROW_NUMBER() OVER (PARTITION BY location ORDER BY date) - 1 AS "Day Number",
    SUM(people_vaccinated) OVER (PARTITION BY location ORDER BY date) AS "Total Injected People"
FROM Vaccination_details
ORDER BY location, date;

--D.2)
SELECT location AS Country, MAX(total_vaccinations) AS "Cumulative Doses"
FROM Vaccination_details
GROUP BY location
HAVING "Cumulative Doses" != ""
ORDER BY "Cumulative Doses" DESC;

--D,3
SELECT 
    DISTINCT vaccines as "Vaccine Type"
    ,location as "Country"
from  Country_vaccines_list
GROUP BY vaccines, location;

--D.4
SELECT
  source_url AS "Source Name (URL)",
  MAX(total_vaccinations) AS "Largest total Administered Vaccines"
FROM Country_Vaccination_details
GROUP BY source_url
HAVING "Largest total Administered Vaccines" IS NOT NULL
ORDER BY source_url DESC;
  
--D.5
SELECT
    strftime('%Y-%m', date) AS Month,
    MAX(CASE WHEN location = 'Australia' THEN people_fully_vaccinated END) AS Australia,
    MAX(CASE WHEN location = 'United States' THEN people_fully_vaccinated END) AS 'United States',
    MAX(CASE WHEN location = 'England' THEN people_fully_vaccinated END) AS England,
    MAX(CASE WHEN location = 'New Zealand' THEN people_fully_vaccinated END) AS 'New Zealand'
FROM  Vaccination_details
WHERE date BETWEEN '2022-01-01' AND '2022-12-31'
GROUP BY Month
ORDER BY Month;