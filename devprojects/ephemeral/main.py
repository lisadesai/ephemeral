import sys
import os
import json
from datetime import datetime, timezone, timedelta
venv_path = os.path.abspath("venv/lib/python3.10/site-packages")  
sys.path.insert(0, venv_path)  
import vedastro import calculate

#Get today's date and time. Location can be prime meridian meets equator.
def get_date():
   geo = vedastro.GeoLocation("Null Island", 00.0000, 00.0000)
   offset = timedelta(hours=-5)
 
   dt = datetime.now(timezone(offset))
   dt_yest = dt - timedelta(days=1)
   formatted_dt = dt.strftime("%H:%M %d/%m/%Y %z")
   formatted_dt_y = dt_yest.strftime("%H:%M %d/%m/%Y %z")
   formatted_dt = "12:00 20/05/2025 -05:00"  

   formatted_dt = formatted_dt[:-2] + ":" + formatted_dt[-2:]
   formatted_dt_y = formatted_dt_y[:-2] + ":" + formatted_dt_y[-2:]

   time_today = vedastro.Time(formatted_dt, geo)
   time_yest = vedastro.Time(formatted_dt_y, geo)
   return time_today, time_yest
   

#Get planet data   
def get_planet_info():
   calc = vedastro.Calculate()

   plts = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]
   planets = []
   today_dict = {}
   yest_dict = {}
   
   time_today, time_yest = get_date()
   for i in plts:
      planet = vedastro.PlanetName(i)
      planets.append(planet)
      today_data = calc.AllPlanetData(planet, time_today)
      yest_data = calc.AllPlanetData(planet, time_yest)

      retro_today = today_data.get("IsPlanetRetrograde")
      retro_yest = yest_data.get("IsPlanetRetrograde")
      flag = is_retro(retro_today, retro_yest)

      house = today_data.get("HousePlanetOccupiesBasedOnLongitudes")
      house_y = yest_data.get("HousePlanetOccupiesBasedOnLongitudes")

      house_e = vedastro.HouseName(house)
      house_ey = vedastro.HouseName(house_y)

      current_sign = str(calc.HouseZodiacSign(house_e, time_today).get("Name"))
      yest_sign = str(calc.HouseZodiacSign(house_ey, time_yest).get("Name"))
      if current_sign != yest_sign:
         print("---------- the sign has changed! ----------")

      today_dict[i] = today_data
      yest_dict[i] = yest_data

      #accounts for logic error 
      if i == "Rahu" or i=="Ketu":
         flag = "stays Retrograde"

      print("CURRENT sign: " + current_sign + " for planet: " + i)
      print("Yesterday's sign: " +  yest_sign + " for planet: " + i)
      print("This planet's directional motion "+ flag)
      print("\n")
      if i == "Jupiter":
         print(today_data)


#Get retro info
def is_retro(retro_today, retro_yest):   
   if retro_today != retro_yest:
      new_direction = retro_today
      if new_direction == "False":
         flag = "switched to Forward"
      else:
         flag = "switched to Retrograde"
   else:
      flag = "stays " + ("Forward" if retro_today == "False" else "Retrograde")
   return flag


get_planet_info()



