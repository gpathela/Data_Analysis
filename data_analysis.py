import csv
import statistics
#this method reads the data from a csv file and returns  
#a list of cases for each month and each year
#number of valid records
#number of invalid reords
def parse_data(filename):
    #list of valid years
    validYear = [2010,2011,2012,2013,2014]
    #list of valid months
    validMonth = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
    #making an list for each month and year. 
    caseList = [[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0]]
    validRecord = 0
    invalidRecord = 0
    #opening and looping through the file
    file = open(filename,'r')
    reader = csv.reader(file, delimiter=',')
    next(reader)    #Just ignoring headers
    #loop to read all records line by line
    for line in reader:
        line[0] = int(line[0]) 
        if line[0] in validYear:
            if line[1] in validMonth:
                validRecord = validRecord + 1
                x = validYear.index(line[0]) #finding year
                y = validMonth.index(line[1]) #fininging month
                caseList[x][y] += 1
            else:
                invalidRecord = invalidRecord + 1
        else:
            invalidRecord = invalidRecord + 1
    return (caseList, validRecord, invalidRecord)

#this is a method to align case counts
#It take a list as l and split number as num
#It just split the list from num parameter and then just add the remaining part in end
def shift(l, n):
    return l[n:] + l[:n]

#this method is to align the maximum number of cases
#It will shift the data to left or right to align it under mean  month
def align_counts(raw_counts):
    # declaring month list
    validMonth = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
    maxIndex = []
    maxMonth = []
    #loop to find max month and its index
    for each in raw_counts:
        maxIndex.append(each.index(max(each)))
        maxMonth.append(validMonth[each.index(max(each))])
    #variabel to store how many number of times a month had max 
    seen = []
    for month in validMonth:
        seen.append(maxMonth.count(month))
    #Mean month index represents the month like if it is 6 it means month is JUN
    meanMonthIndex = seen.index(max(seen))
    meanMonth = validMonth[meanMonthIndex]
    alignedList = []    #a variable to store aligned list
    for i in range(0,5):
        num = maxIndex[i] - meanMonthIndex  #Fnding how many months it needs to aligned
        alignedList.append(shift(raw_counts[i],num))
    return alignedList

#This method tests the level of alert
#It uses mean and standard deviation to calculate the threshold level
def calculate_alert_levels(aligned_counts):
    zipped = zip(aligned_counts[0],aligned_counts[1],aligned_counts[2],aligned_counts[3],aligned_counts[4])
    monthlyMean = []    #To store mean of each month
    monthlyTreshold = []    #To store treshold for each month
    GIVENCONSTANT = 1.645
    for each in zipped:
        eachMean = statistics.mean(each)
        eachSD = statistics.stdev(each)
        eachTreshold = eachMean + (GIVENCONSTANT * eachSD)
        monthlyMean.append(eachMean)
        monthlyTreshold.append(eachTreshold)

    return(monthlyMean, monthlyTreshold)

#This method is to test the threshold level
#This methid wil take a list of current counts and will compare it with thresholds
#parameter num_months is to decide how many months should count increase thresholds
def test_alert(thresholds, counts, num_months=2):
    validMonth = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC',-1]
    trigger = -1
    countExceds = 0
    for i in range(0,len(counts)):
        if(counts[i] > thresholds[i]):
            countExceds += 1
        else:
            countExceds = 0
           
        if(countExceds >= num_months):
            trigger = i
            break
    return validMonth[trigger]

raw_data = parse_data("case_list.csv")
aligned_counts = align_counts(raw_data[0])
thresholds = calculate_alert_levels(aligned_counts)
print(test_alert(thresholds[1], [0,10,23,30]))
print(test_alert(thresholds[1], [10,1,5,45,93]))

