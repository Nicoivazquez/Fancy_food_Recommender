def ReadAsin(lst_of_AID):
    # AsinList = csv.DictReader(open(os.path.join(os.path.dirname(__file__),"Asinfeed.csv")))
    AsinList = lst_of_AID
        #['B001E4KFG0',
#     'B00813GRG4',
#     'B00GJYCIVK',]
    
    for i in AsinList:
        url = "http://www.amazon.com/dp/"+i
        print("Processing: "+url)
        extracted_data.append(AmzonParser(url))
        sleep(5)
    with open('data.json','w') as f:
        json.dump(extracted_data,f,indent=4)
    return extracted_data,f
 
data = ReadAsin(amazon_id[:1000])
data
