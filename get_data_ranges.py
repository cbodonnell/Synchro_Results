def get_data_ranges(results):
    #Loops through results array and returns start and end indicies
    #of each intersection's data
    numInts = 0
    lastIntersection = 0
    for line in results:
        try:
            if len(line[0]) > 0:
                isIntersection = int(line[0][0])
                intNumber = int(line[0].split(':')[0])
                if intNumber != lastIntersection:
                    lastIntersection = intNumber
                    numInts += 1
        except ValueError or IndexError:
            None       
    lastIntersection = 0
    lastIndex = 0
    intCounter = 1
    intDataRanges = []
    for line in results:
        try:
            if len(line[0]) > 0:
                isIntersection = int(line[0][0])
                intNumber = int(line[0].split(':')[0])
                if intNumber != lastIntersection:
                    intName = line[0].split(':')[1].lstrip()
                    intIndex = results.index(line)
                    lastIntersection = intNumber
                    if intCounter == 1:
                        lastIndex = intIndex
                        intCounter += 1                    
                    elif intCounter < numInts:
                        intDataRange = [lastIndex, intIndex]
                        lastIndex = intIndex
                        intDataRanges.append(intDataRange)
                        intCounter += 1  
                    else:
                        intDataRange = [lastIndex, intIndex]
                        lastDataRange = [intIndex, len(results)]                    
                        intDataRanges.append(intDataRange)
                        intDataRanges.append(lastDataRange)             
        except ValueError or IndexError:
            None
    return intDataRanges
