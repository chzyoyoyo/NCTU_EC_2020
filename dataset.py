import numpy as np
import csv
import time

def GetDataset(path):
    with open(path, encoding='utf-8-sig') as f:
        myData = csv.DictReader(f)
        result = []
        for data in myData:
            timestamp = TimeStampProcessing(data["日期"])
            close_price = NumericStringProcessing(data["收市"])
            open_price = NumericStringProcessing(data["開市"])
            highest = NumericStringProcessing(data["高"])
            lowest = NumericStringProcessing(data["低"])
            volume = VolumeProcessing(data["成交量"])
            result.append([timestamp,close_price , open_price , highest , lowest,volume])
        result = np.array(result)
    return result

def TimeStampProcessing(date): #2019年5月19號 -> 20190519 (int)
    timestamp = time.strptime(date,'%Y年%m月%d日')
    timestamp = float(time.strftime('%Y%m%d' , timestamp))
    return timestamp

def NumericStringProcessing(str):
    nums = str.split(',')
    result = 0
    for num in nums:
        result *= 1000
        result += float(num)
    return result

def VolumeProcessing(str):
    result = 0
    if str[-1] is 'M':
        result = float(str[:-1])*1000000
    elif str[-1] is 'K':
        result = float(str[:-1])*1000
    else:
        result = float(str)
    return result

def TransformToBinary(dataset):
    # data: 1 ~ -31 days, every day will compare to previous 1 day (5) and 30 days (5) and next day (1).
    # Hence, binary string will be (N-31)x(5+5+1) array
    size = dataset.shape[0]-31
    binary_string = np.zeros((size , 11) , dtype=np.int)

    for i in range(size):
        index = i + 1 # get the index of dataset

        thisday = dataset[index]
        nextday = dataset[index-1] #next day
        prvday = dataset[index+1] #previous day
        monthdata = dataset[index+1:index+31] #previous 30 days
        averagedata = np.sum(monthdata ,axis= 0)/30 #average of previous 30 days

        binary_string[i][:5] = thisday[1:] > prvday[1:] #represent the up and downs compared to previous day
        binary_string[i][5:10] = thisday[1:] > averagedata[1:] #represent the up and downs compared to prvious 30 days
        binary_string[i][-1] = nextday[1] > thisday[1]  # up and down

    return binary_string