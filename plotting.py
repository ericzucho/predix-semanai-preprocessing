from scipy.stats import linregress
import csv

def checkEqual(iterator):
  try:
     iterator = iter(iterator)
     first = next(iterator)
     return all(first == rest for rest in iterator)
  except StopIteration:
     return True

routesTable = []
for selectedRoute in range(1,21):
    with open('routes.csv', 'rb') as fRoutes:
        readerRoutes = csv.reader(fRoutes, delimiter=',')
        currentRoute = []
        for rowRoute in readerRoutes:
            if rowRoute[selectedRoute - 1] != '':
                currentRoute.append(rowRoute[selectedRoute - 1])
        routesTable.append(currentRoute[0:len(currentRoute)-1])

finalTable = []
for engineNumber in range(700101,700198):
    with open("engines.csv", 'rb') as f:
        steps = []
        minutesAboveThreshold = []
        temperature = []
        numberOfMinutes = []
        reader = csv.DictReader(f)
        rows = [row for row in reader if row['EngineSerial'] == str(engineNumber)]
        counter = 1
        totalPlaneStep = 0
        acum = 0
        if len(rows) == 0:
            continue
        for row in rows:
            if row['Cancellation'] == 1:
                counter = 1
                acum = 0
            else:
                totalPlaneStep += 1
            steps.append(counter)
            if float(row['EngineTemperature']) >= 263:
                acum += float(row['EngineTemperatureTime'])
                minutesAboveThreshold.append(acum)
            else:
                minutesAboveThreshold.append(0.0)
            temperature.append(float((row['EngineTemperature'])))
            numberOfMinutes.append(float((row['EngineTemperatureTime'])))
            counter += 1
        currentCity = routesTable[int(row['EngineRoute'])-1][totalPlaneStep % len(routesTable[int(row['EngineRoute'])-1])]
        slope, intercept, r_value, p_value, std_err = (linregress(steps,minutesAboveThreshold))
        finalTable.append({'Engine':engineNumber,'CurrentCity':currentCity,'Route':"@".join(routesTable[int(row['EngineRoute'])-1]),'StepsSinceLastRepair':counter,'CurrentAcumulatedTime':acum,'MinutesAboveTemperatureSlope':slope,'MinutesAboveTemperatureIntercept':intercept})


keys = finalTable[0].keys()
with open('preprocessedEngines.csv', 'wb') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(finalTable)
        

