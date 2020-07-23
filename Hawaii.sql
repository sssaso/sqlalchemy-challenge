-- Create a new table
CREATE TABLE measurements (
  station VARCHAR(30),
  date DATE,
  prcp NUMERIC,
  tobs INT
);

CREATE TABLE stations (
  station VARCHAR(30),
  name VARCHAR(30),
  latitude REAL,
  longitude REAL,
  elevation REAL
);