'''
Purpose:
    To determine the affect of weather, such as temperature, dew point, and 
    wind speed, on Chicago Marathon running performance.
    
Author: Hailey Reinhard
Date: December 9, 2024
CSCI 203, Fall 2024
'''
import matplotlib.pyplot as pyplot

weatherFile = 'Chicago Marathon Weather.csv'
raceFile = 'Chicago Marathon Results.csv'

def averageWeatherData(weatherData):
    '''
    Averages the 6AM, 9AM, and 12PM weather data points of a Chicago Marathon
    Race.

    Parameters:
        weatherData: A list, the three recorded weather data points throughout
        the marathon race.

    Return Value:
        avgWeatherData: A float, the average of the three data points throughout
        the Chicago Marathon Race. 
    '''
    sumData = 0
    
    # Sums the three recorded weather data points throughout the race.
    for data in weatherData:
        sumData += float(data)
        
    # Averages the sum of weather data, rounding to the tens place.
    avgWeatherData = round(sumData / len(weatherData), 1)
    
    return avgWeatherData

def weatherData(weatherFile, index1, index2, index3):
    '''
    Extracts weather data from the Chicago Marathon Weather CSV into a
    dictionary for a given date at a specific Chicago Marathon race.

    Parameters:
        weatherFile: A string, the name of the file that includes the date
        of the race and weather data throughout the race.
        index1: An integer, the column number corrosponding to various weather
        data at 6AM.
        index2: An integer, the column number corrosponding to various weather
        data at 9AM.
        index3: An integer, the column number corrosponding to various weather
        data at 12PM. 

    Return Value:
        weatherDictionary: A dictionary with the year of the race as the key,
        and a list of the average of weather data of the race as the value. 
    '''
    weatherDictionary = {}
    file = open(weatherFile, 'r', encoding = 'utf-8')
    file.readline()

    # Adds data from the weatherFile to weatherDictionary.
    for line in file:  
        line = line.rstrip()
        row = line.split(',')
        avgWeatherData = []
        year = row[0] # Assigns the key as the year of the race.
        
        # Creates a list of the three recorded weather data points during the
        #race.
        recordedData = [row[index1], row[index2], row[index3]]
        
        avgData = averageWeatherData(recordedData)
        avgWeatherData.append(avgData) 
        
        # Adds the key value pair (year, avgWeatherData) to the dictionary. 
        weatherDictionary[year] = avgWeatherData
        
    return weatherDictionary 

def convertResults2Seconds(time):
    '''
    Converts the final marathon time to seconds.

    Parameters:
        time: A string, the time it took for the corresponding runner to
        complete the marathon in hours:minutes:second format.

    Return Value:
        runTime: An integer, the marathon race time in seconds.
    '''
    timeList = time.split(':')
    
    # Adds together the hours in seconds, minutes in seconds, and
    # seconds to convert the run time to seconds.
    runTime = (int(timeList[0]) * 3600) + (int(timeList[1]) * 60)
    runTime = runTime + int(timeList[2])    
                                                                                        
    return runTime

def raceData(raceFile, gender):  
    '''
    Extracts race data from the Chicago Marathon Results CSV into a
    dictionary for a given year at a Chicago Marathon race. 

    Parameters:
        raceFile: A string, the name of the file that includes the date and
        final race times of runners from the Chicago Marathon each year.
        gender: A string, the gender of the racer. 

    Return Value:
        resultsDictionary: A dictionary that includes the year of the race as
        the key, and a list of the run time in seconds for the top 50 runners
        each year at the Chicago Marathon.
    '''
    file = open(raceFile, 'r', encoding = 'utf-8')
    resultsDictionary = {}
    file.readline()
    
    for line in file:
        line = line.rstrip()
        row = line.split(',')
        
        try:
            # Checks to ensure that the runner is a certain gender and from the
            #USA. 
            if row[3] == gender and row[5] == 'USA': 
                year = row[1] # Assigns the year as the key to the dictionary.
                
                if year in resultsDictionary:
                    # Assigns the converted marathon time in seconds to runTime.
                    runTime = convertResults2Seconds(row[7])  
                    resultsDictionary[year].append(runTime)
                    
                else:
                    runTimes = []
                    # Assigns the converted marathon time in seconds to runTime.
                    runTime = convertResults2Seconds(row[7])  
                    runTimes.append(runTime)
                    resultsDictionary[year] = runTimes
                    
        except: # For faulty data. 
            pass
    
    for year, runTimes in resultsDictionary.items():
        runTimes.sort()
        # Slices the sorted marathon times so that the runTimes include the
        # top 50 runners.
        top50M = runTimes[0:51]  
        resultsDictionary[year] = top50M

    return resultsDictionary

def averageRunTimes(runList):
    '''
    Averages the top 50 Chicago Marathon times in a given year.

    Parameters:
        runList: A list, the top 50 Chicago Marathon times

    Return Value:
        avgTime: A float, the average time of the top 50 Chicago Marathon
            runners.
    '''
    avgTime = sum(runList) / len(runList)
    
    return avgTime

def plotWeather(resultsDictionary, weatherDictionary, gender, weather):
    '''
    Plots the average weather throughout the race vs the times of the top 50
    runners in the Chicago Marathon each year as a scatter plot. 

    Parameters:
        resultsDictionary: A dictionary, includes the year of the race as the
            key and the run time for the top 50 runners as the value.
        weatherDictionary: A dictionary, includes the year of the race as the
            key and the average weather data as the value.
        gender: A string, the gender of the runners in resultsDictionary.
        weather: A string, the type of weather data (temperature, dew point, or
            wind speed). 

    Return Value:
        None.
    '''
    # Plots the list of average weather data vs the list of run
    # times for every year in resultsDictionary. 
    for year in resultsDictionary.keys():
        avgWeather = weatherDictionary[year]
        raceTimes = resultsDictionary[year]
        avgWeather = avgWeather * len(raceTimes)
        pyplot.scatter(avgWeather, raceTimes, s=10)
        
    pyplot.xlabel(f'Average {weather}')
    pyplot.ylabel(f'{gender} Marathon Time')
    pyplot.title(f'Average {weather} vs {gender} Marathon Time')
    pyplot.show()
    
def plotAvgWeather(resultsDictionary, weatherDictionary, gender, weather):
    '''
    Plots the average weather throughout the race vs the average time of the
    top 50 runners in the Chicago Marathon each year as a scatter plot. 

    Parameters:
        resultsDictionary: A dictionary, includes the year of the race as the
            key and the run time for the top 50 runners as the value.
        weatherDictionary: A dictionary, includes the year of the race as the
            key and the average weather data as the value.
        gender: A string, the gender of the runners in resultsDictionary.
        weather: A string, the type of weather data (temperature, dew point, or
            wind speed).

    Return Value:
        None.
    '''
    # Plots the list of average weather points vs the list of average run
    # time for every year in resultsDictionary.
    for year in resultsDictionary.keys():
        avgWeather = weatherDictionary[year]
        raceTimes = resultsDictionary[year]
        avgRaceTimes = averageRunTimes(raceTimes)
        pyplot.scatter(avgWeather, avgRaceTimes, s=10)
        
    pyplot.xlabel(f'Average {weather}')
    pyplot.ylabel(f'Average {gender} Marathon Time')
    pyplot.title(f'Average {weather} vs Average {gender} Marathon Time')
    pyplot.show()
        
def main():
    '''
    Runs all of the functions.

    Parameters:
        None.

    Return Value:
        None.
    '''
    
    # Creates a dictionary for temperature data.
    temperatureData = weatherData(weatherFile, 5, 8, 11)

    # Creates a dictionary for dew point data. 
    dewPointData = weatherData(weatherFile, 6, 9, 12)

    # Creates a dictionary for wind speed data.
    windData = weatherData(weatherFile, 7, 10, 13)

    # Creates a dictionary for female race data. 
    femaleResults = raceData(raceFile, 'F')

    # Creates a dictionary for male race data. 
    maleResults = raceData(raceFile, 'M')
    
    # Plots Average Temperature vs Female Run Times.
    plotWeather(femaleResults, temperatureData, 'Female', 'Temperature')
    # Plots Average Temperature vs Average Female Run Time.
    plotAvgWeather(femaleResults, temperatureData, 'Female', 'Temperature')

    # Plots Average Temperature vs Male Run Times.
    plotWeather(maleResults, temperatureData, 'Male', 'Temperature')
    # Plots Average Temperature vs Average Male Run Times.
    plotAvgWeather(maleResults, temperatureData, 'Male', 'Temperature')
    
    # Plots Average Dew Point vs Female Run Times.
    plotWeather(femaleResults, dewPointData, 'Female', 'Dew Point')
    # Plots Average Dew Point vs Average Female Run Times.
    plotAvgWeather(femaleResults, dewPointData, 'Female', 'Dew Point')

    # Plots Average Dew Point vs Male Run Times.
    plotWeather(maleResults, dewPointData, 'Male', 'Dew Point')
    # Plots Average Dew Point vs Average Male Run Times.
    plotAvgWeather(maleResults, dewPointData, 'Male', 'Dew Point')

    # Plots Average Wind Speed vs Female Run Times.
    plotWeather(femaleResults, windData, 'Female', 'Wind Speed')
    # Plots Average Wind Speed vs Average Female Run Times.
    plotAvgWeather(femaleResults, windData, 'Female', 'Wind Speed')

    # Plots Average Wind Speed vs Male Run Times.
    plotWeather(maleResults, windData, 'Male', 'Wind Speed')
    # Plots Average Wind Speed vs Average Male Run Times.
    plotAvgWeather(maleResults, windData, 'Male', 'Wind Speed')

main()
