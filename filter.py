# this script filters transactions to a certain number of blocks
import re
import datetime

def filterbyBlock(block):
    fname = "transaction_till_"+str(block)+".csv"
    with open(fname,"w") as ft:
        with open("all_transactions.csv") as fs:
            for line in fs:
                if not re.match("from.*",line):
                    temp = line.strip().split(",")
                    if int(temp[4])<=block:
                        ft.write(line)


def filterbyTime(time):
    fname = "transaction_till_"+str(time)+".csv"
    with open(fname,"w") as ft:
        with open("all_transactions.csv") as fs:
            for line in fs:
                if not re.match("from.*",line):
                    temp = line.strip().split(",")
                    if int(temp[3])<=time:
                        ft.write(line)


def fromUnixtimetoDate(time):
    return(datetime.datetime.fromtimestamp(int(time)).strftime('%Y-%m-%d'))

    

if __name__=="__main__":
    year,month,day = map(int,fromUnixtimetoDate(1284101485).split('-'))
    print (year,month,day)
