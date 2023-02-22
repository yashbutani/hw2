"""
FILE: skeleton_parser.py
------------------
Author: Firas Abuzaid (fabuzaid@stanford.edu)
Author: Perth Charernwattanagul (puch@stanford.edu)
Modified: 04/21/2014

Skeleton parser for CS564 programming project 1. Has useful imports and
functions for parsing, including:

1) Directory handling -- the parser takes a list of eBay json files
and opens each file inside of a loop. You just need to fill in the rest.
2) Dollar value conversions -- the json files store dollar value amounts in
a string like $3,453.23 -- we provide a function to convert it to a string
like XXXXX.xx.
3) Date/time conversions -- the json files store dates/ times in the form
Mon-DD-YY HH:MM:SS -- we wrote a function (transformDttm) that converts to the
for YYYY-MM-DD HH:MM:SS, which will sort chronologically in SQL.

Your job is to implement the parseJson function, which is invoked on each file by
the main function. We create the initial Python dictionary object of items for
you; the rest is up to you!
Happy parsing!
"""

import sys
from json import loads
from re import sub

columnSeparator = "|"

# Dictionary of months used for date transformation
MONTHS = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06',\
        'Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}

"""
Returns true if a file ends in .json
"""
def isJson(f):
    return len(f) > 5 and f[-5:] == '.json'

"""
Converts month to a number, e.g. 'Dec' to '12'
"""
def transformMonth(mon):
    if mon in MONTHS:
        return MONTHS[mon]
    else:
        return mon

"""
Transforms a timestamp from Mon-DD-YY HH:MM:SS to YYYY-MM-DD HH:MM:SS
"""
def transformDttm(dttm):
    dttm = dttm.strip().split(' ')
    dt = dttm[0].split('-')
    date = '20' + dt[2] + '-'
    date += transformMonth(dt[0]) + '-' + dt[1]
    return date + ' ' + dttm[1]

"""
Transform a dollar value amount from a string like $3,453.23 to XXXXX.xx
"""

def transformDollar(money):
    if money == None or len(money) == 0:
        return money
    return sub(r'[^\d.]', '', money)

"""
Parses a single json file. Currently, there's a loop that iterates over each
item in the data set. Your job is to extend this functionality to create all
of the necessary SQL tables for your database.
"""
def parseJson(json_file):
    with open(json_file, 'r') as f:
        items = loads(f.read())['Items'] # creates a Python dictionary of Items for the supplied json file
        
        """
        TODO: traverse the items dictionary to extract information from the
        given `json_file' and generate the necessary .dat files to generate
        the SQL tables based on your relation design
        """
        
        items_file = open("items.dat", "w+")
        category = open("category.dat", "w+")
        users = open("users.dat", "w+")
        bids = open("bids.dat", "w+")
         
        keys = ["ItemID", "Name", "Category", "Currently", "First_Bid", "Number_of_Bids", "Bids", "Location", "Country", "Started", "Ends", 
                "Seller", "Description"]
        
        fullset = set() #string = \" + string.replace('\"', '\"\"') + \"

        for item in items:
            
            #item: ItemID (int), SellerID (str), Name (str), Currently (float/$), First Bid (float/$), Number of Bids (int), Started (date-time), Ends (date-time), Description (str)
            item_id = "NULL"
            user_id = "NULL"
            items_t = ""
            
            if item["ItemID"] == None:
                items_t += "NULL"
            else:
                item_id = item["ItemID"]
                items_t += item["ItemID"]
                
            if item["Seller"]["UserID"] == None:
                items_t += "|" + "NULL"
            else:
                items_t += "|" + "\"" + item["Seller"]["UserID"].replace('\"', '\"\"') + "\""
                user_id = item["Seller"]["UserID"]
            
            if item["Name"] == None:
                items_t += "|" + "NULL"   
            else:
                items_t += "|" + "\"" + item["Name"].replace('\"', '\"\"') + "\""
                
            if item["Currently"] == None:
                items_t += "|" + "NULL"
            else:
                items_t += "|" + transformDollar(item["Currently"])
                
            if item["First_Bid"] == None:
                items_t += "|" + "NULL"
            else:
                items_t += "|" + transformDollar(item["First_Bid"])
            
            if item["Number_of_Bids"] == None:
                items_t += "|" + "NULL"
            else:
                items_t += "|" +  item["Number_of_Bids"]
            
            if item["Started"] == None:
                items_t += "|" + "NULL"
            else:
                items_t += "|" + transformDttm(item["Started"])
                
            if item["Ends"] == None:
                items_t += "|" + "NULL"
            else:
                items_t += "|" + transformDttm(item["Ends"])
            
            if item["Description"] == None:
                items_t += "|" + "NULL"
            else:
                items_t += "|" + "\"" + item["Description"].replace('\"', '\"\"') + "\""
     
            items_t += "\n"
            if items_t not in fullset:
                fullset.add(items_t)
                items_file.write(items_t)
            
            #categories: ItemID (int), Category (str)
            for element in item["Category"]:
                category_t = "" + item_id + "|" + "\"" + element.replace('\"', '\"\"') + "\"" + "\n"
                if category_t not in fullset:
                    fullset.add(category_t)
                    category.write(category_t)
                    
            #user (seller): UserID (str), Rating (int), Location (str), Country (str)
            users_t = ""
            
            users_t += "\"" + item["Seller"]["UserID"].replace('\"', '\"\"') + "\""
            
            if item["Seller"]["Rating"] == None:
                users_t += "|" + "NULL"
            else:
                users_t += "|" + item["Seller"]["Rating"]
            
            if item["Location"] == None:
                users_t += "|" + "NULL"
            else:
                users_t += "|" + "\"" + item["Location"].replace('\"', '\"\"') + "\""
            
            if item["Country"] == None:
                users_t += "|" + "NULL"
            else:
                users_t += "|" + "\"" + item["Country"].replace('\"', '\"\"') + "\""
                
            users_t += "\n"
            
            if users_t not in fullset:
                fullset.add(users_t)
                users.write(users_t)
            
            #bids: ItemID (int), UserID (str), Time (date-time), Amount (float/$)
            if not item["Bids"] == None:
                for bidder in item["Bids"]:
                    bid_tv = item_id
                    bid = bidder["Bid"]["Bidder"]

                    if bid["UserID"] == None:
                        bid_tv += "|" + "NULL"
                    else:
                        bid_tv += "|" + "\"" + bid["UserID"].replace('\"', '\"\"') + "\""

                    if bidder["Bid"]["Time"] == None:
                        bid_tv += "|" + "NULL"
                    else:
                        bid_tv += "|" + transformDttm(bidder["Bid"]["Time"])

                    if bidder["Bid"]["Amount"] == None:
                        bid_tv += "|" + "NULL"
                    else:
                        bid_tv += "|" + transformDollar(bidder["Bid"]["Amount"])

                    bid_tv += "\n"

                    if bid_tv not in fullset:
                        fullset.add(bid_tv)
                        bids.write(bid_tv)
                
            #get bidders for users table
            if not item["Bids"] == None:
                for bidder in item["Bids"]:
                    bid_t = ""
                    bid = bidder["Bid"]["Bidder"]
                    if bid["UserID"] == None:
                        bid_t += "NULL"
                    else:
                        bid_t += "\"" + bid["UserID"].replace('\"', '\"\"') + "\""

                    if bid["Rating"] == None:
                        bid_t += "|" + "NULL"
                    else:
                        bid_t += "|" + bid["Rating"]

                    if "Location" not in bid.keys() or bid["Location"] == None:
                        bid_t += "|" + "NULL"
                    else:
                        bid_t += "|" + "\"" + bid["Location"].replace('\"', '\"\"') + "\""

                    if "Country" not in bid.keys() or bid["Country"] == None:
                        bid_t += "|" + "NULL"
                    else:
                        bid_t += "|" + "\"" + bid["Country"].replace('\"', '\"\"') + "\""

                    bid_t += "\n"

                    if bid_t not in fullset:
                        fullset.add(bid_t)
                        users.write(bid_t)
                    
            #break #####DELETE
                
        items_file.close()
        category.close()
        users.close()
        bids.close()

"""
Loops through each json files provided on the command line and passes each file
to the parser
"""
def main(argv):
    if len(argv) < 2:
        print >> sys.stderr, 'Usage: python skeleton_json_parser.py <path to json files>'
        sys.exit(1)
    # loops over all .json files in the argument
    for f in argv[1:]:
        if isJson(f):
            parseJson(f)
            print("Success parsing " + f)

if __name__ == '__main__':
    main(sys.argv)