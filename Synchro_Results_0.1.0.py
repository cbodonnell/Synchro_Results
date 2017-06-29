#Synchro Results Reader
#Craig O'Donnell
#Last Updated: 02/08/2017


#DIRECTIONS:
# 1. Run script
# 2. Type number of iterations (number of reports to read)
# 3. CSV files will be created in the same directory as the read reports


#Import modules and functions
#need to be in the same directory unless paths are given
import time, csv
from classes import Intersection, Approach, Lanegroup
from browse_for_path import browse_for_path
from txt_to_array import txt_to_array
from get_data_ranges import get_data_ranges


#Returns an array of project data objects
def synchroReader(results):

    #Notes starting time
    start_time = time.time()
    
    #ENABLE THIS CODE AFTER DEVELOPMENT
    
    #Allows user to select the .txt report
    file = results.split('/')[-1]
    path = ('/'.join(results.split('/')[0:-1])) + '/'
    periodIdentifier = file.split('_')[0]
    results = txt_to_array(results)

    #QUICKER TESTING PURPOSES ONLY (disable after development)
    '''
    results = txt_to_array(
        'C:\\Users\\codonnell\\Desktop\\Tools\\Python\\Synchro Results\\' +
        'SampleReport_Synchro_HCMSig_HCMUnsig.txt'
        )
    '''

    #Finds the start and end position of each intersection's data
    data_ranges = get_data_ranges(results)

    #Goes through data intersection by intersection
    projectData = []
    for int_data_range in data_ranges:
        
        #Isolates the data array for the intersection
        int_data = results[int_data_range[0]:int_data_range[1]]

        #Isolates Synchro and HCM data
        for line in int_data:
            if line[0] == '':
                splitter = int_data.index(line)
        intSynchroData = int_data[0:splitter]
        intHCMData = int_data[splitter + 1:]

        #Gets intersection name and number
        intName = intSynchroData[0][0].split(': ')[1]
        intNumber = float(intSynchroData[0][0].split(': ')[0])

        #Gets intersection control type
        for line in intSynchroData:
            if 'Control Type' in line[0]:
                intControlType = line[0].split(': ')[1]

        #Gets intersection overall delay and vc ratio
        intDelay = '-'
        intVC = '-'
        if intControlType == 'Pretimed':
            for line in intHCMData:
                if line[0] == 'HCM 2000 Control Delay':
                    for item in line:
                        if item == 'HCM 2000 Level of Service':
                            delayIndex = line.index(item) - 1
                            intDelay = line[delayIndex]
                elif line[0] == 'HCM 2000 Volume to Capacity ratio':
                    intVC = line[-1]
        elif intControlType == 'Unsignalized':
            for line in intHCMData:
                if (
                    line[0] == 'Average Delay' or
                    line[0] == 'Delay'
                    ):
                    intDelay = line[-1]

        #Gets intersection approaches (this is not the object parameter!!)
        approaches = []
        lanegroupsIndex = 0
        configurationIndicies = []
        for line in intSynchroData:
            if line[0] == 'Lane Group':
                lanegroupsIndex = intSynchroData.index(line)
            if line[0] == 'Lane Configurations':
                for index, item in enumerate(line):
                    if (
                        item != '0' and
                        item != 'Lane Configurations' and
                        item != ''
                        ):
                        configurationIndicies.append(index)
        for index in configurationIndicies:
            approach = intSynchroData[lanegroupsIndex][index][:2]
            if approach not in approaches:
                approaches.append(approach)

        #Iterates through approaches and gets relevant data
        approachObjects = []
        for app in approaches:
            
            #Get approach name
            appName = app

            #Get column indicies for the approach
            appIndicies = []
            for line in intHCMData:
                if line[0] == 'Movement':
                    for index, item in enumerate(line):
                        if app in item:
                            appIndicies.append(index)

            #Get approach delay
            appDelay = '-'
            #For signalized intersections
            if intControlType == 'Pretimed':
                for line in intHCMData:
                    if line[0] == 'Approach Delay (s)':
                        for index in appIndicies:
                            if line[index] != '':
                                appDelay = line[index]
            #For unsignalized intersections
            if intControlType == 'Unsignalized':
                appDelayIndex = 0
                for line in intHCMData:
                    if line[0] == 'Direction, Lane #':
                        for index, item in enumerate(line):
                            if app in item:
                                appDelayIndex = index
                    elif line[0] == 'Approach Delay (s)':
                        appDelay = line[appDelayIndex]

            #Get approach lanegroups (this is not the object parameter!!)
            lanegroups = []
            lanegroupIndicies = []
            mvtIndicies = []
            for line in intSynchroData:
                if 'Traffic Volume' in line[0]:
                    for index in appIndicies:
                        if line[index] != '':
                            if int(line[index]) > 0:
                                mvtIndicies.append(index)

            #Gets lanegroup results
            laneNames = [] #ADD CODE TO CLEAN UP THE LANEGROUP NAMES
            delays = []
            vc_ratios = []

            #For signalized intersections
            if intControlType == 'Pretimed':
                resultIndicies = []
                for line in intHCMData:
                    if line[0] == 'Delay (s)':
                        for mvt in appIndicies:
                            if line[mvt] != '':
                                resultIndicies.append(mvt)
                                delays.append(line[mvt])
                for line in intHCMData:
                    if line[0] == 'Movement':
                        for index in resultIndicies:
                            lanegroup = line[index].replace(app, '')
                            lanegroups.append(lanegroup)
                    if line[0] == 'v/c Ratio':
                        for index in resultIndicies:
                            vc_ratios.append(line[index])

            #For unsignalized intersections
            if intControlType == 'Unsignalized':
                resultIndicies = []
                for line in intHCMData:
                    if line[0] == 'Direction, Lane #':
                        for index, item in enumerate(line):
                            if app in item[:2]:
                                resultIndicies.append(index)
                                laneNames.append(item)
                    vc_ratios.append('-')
                    if line[0] == 'Control Delay (s)':
                        for index in resultIndicies:
                            delays.append(line[index])

            #Makes lanegroup objects
            lanegroupObjects = []

            if intControlType == 'Pretimed':
                for index, lane in enumerate(lanegroups):
                    lanegroupObject = Lanegroup(lane, vc_ratios[index],
                                                delays[index])
                    lanegroupObjects.append(lanegroupObject)

            if intControlType == 'Unsignalized':
                if len(delays) > 0:
                    for index, lane in enumerate(laneNames):
                        lanegroupObject = Lanegroup(lane, vc_ratios[index],
                                                    delays[index])
                        lanegroupObjects.append(lanegroupObject)

            #Makes approach objects
            approachObject = Approach(appName, appDelay, lanegroupObjects)
            approachObjects.append(approachObject)
            
        #Makes intersection objects
        intersectionObject = Intersection(intName, intNumber, intControlType,
                                          intDelay, intVC, approachObjects)
        projectData.append(intersectionObject)

    #Puts results into formatted array
    results_array = [['id', 'Intersection',
                      'Overall v/c', 'Overall Delay',
                      'Approach', 'Lanegroup',
                      'v/c Ratio', 'Delay']]
    for i in projectData:
        int_count = 0
        for j in i.approaches:
            app_count = 0
            for k in j.lanegroups:
                int_num = i.number
                int_name = i.name
                int_delay = i.overall_delay
                int_vc_ratio = i.overall_vc
                app_name = j.name
                if int_count > 0:
                    int_num += 0.1 * int_count
                    int_name = ''
                    int_delay = ''
                    int_vc_ratio = ''
                if app_count > 0:
                    app_name = ''
                int_count += 1
                app_count += 1
                data = [int_num, int_name,
                        int_vc_ratio, int_delay,
                        app_name, k.name,
                        k.vc_ratio, k.delay]
                results_array.append(data)

    #Writes results to .csv file for use in other programs    
    with open((path + periodIdentifier + '_results.csv'),
              'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(results_array)

    #Displays elapsed time
    elapsed_time = round(time.time() - start_time,3)
    print('Process completed in ' + str(elapsed_time) + ' seconds.')
    print('See %s_results.csv for analysis results.' % periodIdentifier)
    

#Main function
if __name__ == "__main__":
    numIter = int(input('Number of iterations: '))
    allConditions = []
    for _ in range(numIter):
        txt_report = browse_for_path()
        allConditions.append(txt_report)
    for condition in allConditions:
        synchroReader(condition)
