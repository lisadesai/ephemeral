import sys
import os
import json

venv_path = os.path.abspath("venv/lib/python3.10/site-packages")  

if venv_path not in sys.path:
    sys.path.insert(0, venv_path)  

import vedastro  
from datetime import datetime, timezone, timedelta
 

#Get today's date and time. Location can be staid.
geo = vedastro.GeoLocation("Dallas, USA", 96.808891, 32.779167)
offset = timedelta(hours=-5)
 
dt = datetime.now(timezone(offset))
dt_yest = dt - timedelta(days=1)

formatted_dt = dt.strftime("%H:%M %d/%m/%Y %z")
formatted_dt = "12:00 01/06/2025 -05:00"
formatted_dt_y = dt_yest.strftime("%H:%M %d/%m/%Y %z")

formatted_dt = formatted_dt[:-2] + ":" + formatted_dt[-2:]
formatted_dt_y = formatted_dt_y[:-2] + ":" + formatted_dt_y[-2:]

print("Formatted date today: "+ formatted_dt + " and formatted date yesterday " + formatted_dt_y)

time_today = vedastro.Time(formatted_dt, geo)
time_yest = vedastro.Time(formatted_dt_y, geo)
 
calc = vedastro.Calculate()
plt = "Jupiter"
planet = vedastro.PlanetName(plt)
ls= calc.AllPlanetData(planet, time_today)
ls_y = calc.AllPlanetData(planet, time_yest)

retro_today = ls.get("IsPlanetRetrograde")
retro_yest = ls_y.get("IsPlanetRetrograde")

if retro_today != retro_yest:
   new_direction = retro_today
   if new_direction == "False":
      flag = "Forward"
   else:
      flag = "Retrograde"
   print("this planet has switched orientation to " + flag)

house = ls.get("HousePlanetOccupiesBasedOnLongitudes")
house_y = ls_y.get("HousePlanetOccupiesBasedOnLongitudes")

house_e = vedastro.HouseName(house)
house_ey = vedastro.HouseName(house_y)

current_sign = str(calc.HouseZodiacSign(house_e, time_today).get("Name"))
yest_sign = str(calc.HouseZodiacSign(house_ey, time_yest).get("Name"))

print("current sign: " + current_sign + " for planet: " + plt)
print("yesterday's sign: " +  yest_sign + " for planet: " + plt)



