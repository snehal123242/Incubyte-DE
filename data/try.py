import pandas as pd

# Define your data in CSV format
data = """H,Customer_Name,Customer_Id,Open_Date,Last_Consulted_Date,Vaccination_Id,Dr_Name,State,Country,DOB,Is_Active
D,Alex,123457,20101012,20121013,MVD,Paul,SA,USA,06031987,A
D,John,123458,20101012,20121013,MVD,Paul,TN,India,06031987,A
D,Mary,123459,20101115,20121116,MVD,James,CA,USA,04121990,A
D,Lucas,123460,20100918,20120919,MRV,Chris,NY,USA,12011985,A
D,Emma,123461,20101220,20121221,TTD,David,NSW,AU,09101992,A
D,Liam,123462,20100825,20120826,MVD,Robert,QLD,AU,01081988,A
D,Sophia,123463,20101102,20121103,MVD,Mary,MH,India,05111991,A
D,James,123464,20100713,20120714,TTD,Michael,PH,PHIL,11021986,A
D,Isabella,123465,20100907,20120908,MVD,Luke,NY,NYC,04051993,A
D,Michael,123466,20101125,20121126,MVD,Paul,SA,USA,02121989,A
D,Olivia,123467,20100104,20120105,MRV,Chris,CA,USA,05071990,A
D,Daniel,123468,20100517,20120518,MVD,Robert,TN,India,10011985,A
D,Grace,123469,20100721,20120722,MVD,James,PH,PHIL,09251991,A
D,Matthew,123470,20100930,20120931,TTD,David,NSW,AU,08071989,A
D,Ethan,123471,20100211,20120212,MVD,Mary,MH,India,11031987,A
D,Charlotte,123472,20100322,20120323,MVD,Paul,SA,USA,02051992,A
D,Benjamin,123473,20100425,20120426,MRV,Chris,NY,USA,12071990,A"""

# Read the data into a pandas DataFrame
df = pd.read_csv(pd.io.common.StringIO(data))

# Convert 'Open_Date' and 'Last_Consulted_Date' to datetime format
df['Open_Date'] = pd.to_datetime(df['Open_Date'], format='%Y%m%d')

# Display the result
print(df[['Customer_Name', 'Open_Date']])
