-- Create Table for India
CREATE TABLE Table_Ind (
    Customer_Name VARCHAR(255) NOT NULL,
    Customer_Id INT PRIMARY KEY,
    Open_Date DATE NOT NULL,
    Last_Consulted_Date DATE,
    Vaccination_Id CHAR(5),
    Dr_Name VARCHAR(255),
    State CHAR(5),
    Country CHAR(5),
    DOB DATE NOT NULL,
    Is_Active CHAR(1),
    Age INT,  -- Will be updated via trigger
    Days_Since_Last_Consulted INT  -- Will be updated via trigger
);

-- Create Table for USA
CREATE TABLE Table_USA (
    Customer_Name VARCHAR(255) NOT NULL,
    Customer_Id INT PRIMARY KEY,
    Open_Date DATE NOT NULL,
    Last_Consulted_Date DATE,
    Vaccination_Id CHAR(5),
    Dr_Name VARCHAR(255),
    State CHAR(5),
    Country CHAR(5),
    DOB DATE NOT NULL,
    Is_Active CHAR(1),
    Age INT,  -- Will be updated via trigger
    Days_Since_Last_Consulted INT  -- Will be updated via trigger
);
--CREATE TABLE FOR AUSTRALIA
	CREATE TABLE Table_AU (
	Customer_Name VARCHAR(255) NOT NULL,
    Customer_ID VARCHAR(18) PRIMARY KEY,
    Open_Date DATE NOT NULL,
    Last_Consulted_Date DATE,
    Vaccination_Id  CHAR(5),
    Dr_Name CHAR(255),
    State CHAR(5),
    Country CHAR(5),
    DOB DATE NOT NULL,
	Is_Active CHAR(1),
    FLAG CHAR(1),
    Age INT,   -- Will be updated via trigger
    Days_Since_Last_Consulted INT   -- Will be updated via trigger
);
--CREATE TABLE NYC
CREATE TABLE Table_NYC(
	Customer_Name VARCHAR(255) NOT NULL,
	Customer_ID VARCHAR(18) PRIMARY KEY,
    Open_Date DATE NOT NULL,
    Last_Consulted_Date DATE, 
    Vaccination_Id  CHAR(5),
    Dr_Name CHAR(255),
    State CHAR(5),
    Country CHAR(5),
    DOB DATE NOT NULL,
	Is_Active CHAR(1),
    FLAG CHAR(1),
    Age INT ,  -- Will be updated via trigger
    Days_Since_Last_Consulted INT  -- Will be updated via trigger
);

--CREATE TABLE PHIL
CREATE TABLE Table_PHIL(
	Customer_Name VARCHAR(255) NOT NULL,
	Customer_Id  VARCHAR(18) PRIMARY KEY,
    Open_Date DATE NOT NULL,
    Last_Consulted_Date  DATE,
    Vaccination_Id CHAR(5),
    Dr_Name CHAR(255),
    State CHAR(5),
    Country CHAR(5),
    DOB DATE NOT NULL,
	Is_Active CHAR(1),
    FLAG CHAR(1),
    Age INT ,  -- Will be updated via trigger
    Days_Since_Last_Consulted INT   -- Will be updated via trigger
);


----CREATE TRIGGERS
CREATE OR REPLACE FUNCTION update_age_and_days() RETURNS TRIGGER AS $$
BEGIN
 
    NEW.Age := EXTRACT(YEAR FROM age(NEW.DOB));

 
    IF NEW.Last_Consulted_Date IS NOT NULL THEN
        NEW.Days_Since_Last_Consulted := CURRENT_DATE - NEW.Last_Consulted_Date;
    ELSE
        NEW.Days_Since_Last_Consulted := NULL;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

---Trigger for table India
CREATE TRIGGER age_and_days_trigger_India
BEFORE INSERT OR UPDATE ON Table_Ind
FOR EACH ROW EXECUTE FUNCTION update_age_and_days();

-- Trigger for USA
CREATE TRIGGER age_and_days_trigger_USA
BEFORE INSERT OR UPDATE ON Table_USA 
FOR EACH ROW EXECUTE FUNCTION update_age_and_days();

--Trigger for Australia
CREATE TRIGGER age_and_days_trigger_AU
BEFORE INSERT OR UPDATE ON Table_AU 
FOR EACH ROW EXECUTE FUNCTION update_age_and_days();

--Trigger for Phillipines
CREATE TRIGGER age_and_days_trigger_PHIL
BEFORE INSERT OR UPDATE ON Table_PHIL 
FOR EACH ROW EXECUTE FUNCTION update_age_and_days();

--Trigger for NYC
CREATE TRIGGER age_and_days_trigger_NYC
BEFORE INSERT OR UPDATE ON Table_NYC
FOR EACH ROW EXECUTE FUNCTION update_age_and_days();

select * from Table_ind