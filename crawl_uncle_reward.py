import requests
from bs4 import BeautifulSoup
from multiprocessing import Process
import time

def parseReward(url_b):
    p_g = requests.get(url_b)
    soup = BeautifulSoup(p_g.text,"lxml")
    flag = 0
    for l in soup.find_all("table",{"class":"table nav-justified"}):
        for d in l.find_all("td"):
            if d.text.strip() == "Uncle Reward:":
                flag = 1
                continue
            if flag==1:
                val = d.text.strip().split(" ")
                return str(float(val[0])*1000000000000000000)

def crawlUncleReward(fname_1, fname_2, url):
    with open(fname_1,"w") as ft:
        with open(fname_2) as fs:
            for line in fs:
                temp = line.strip().split(",")
                for i in range(2,len(temp)):
                    u_b = temp[i]
                    url_b = url+u_b
                    reward = parseReward(url_b)
                try:
                    ft.write("ethereum"+","+temp[1]+","+reward+",0,"+temp[0])
                    ft.write("\n")
                except:
                    print("could not crawl:"+url_b)
                break

def crawlUncleRewardbyAPI(fname_1,fname_2,apikey):
    url = 'https://api.etherscan.io/api?module=block&action=getblockreward&blockno='
    with open(fname_1,"w") as ft:
        with open(fname_2) as fs:
            for line in fs:
                temp = line.strip().split(",")
                url_c = url+temp[0]+"&apikey="+apikey
                p_g = requests.get(url_c)
                p_g_j = p_g.json()
                sum_ = 0
                for obj in p_g_j['result']['uncles']:
                    sum_+=float(obj['blockreward'])
                ft.write("ethereum,"+temp[1]+","+str(sum_)+",0,"+temp[0])
                ft.write("\n")
                print("parsed block",temp[0])

if __name__=="__main__":

    apikey_1 = 'api key'
    apikey_2 = 'api key'

    jobs = []
    jobs.append(Process(target=crawlUncleRewardbyAPI, args=("uncle_r_1.csv","uncle_1",apikey_1,)))
    jobs.append(Process(target=crawlUncleRewardbyAPI, args=("uncle_r_2.csv","uncle_2",apikey_2,)))


    for j in jobs:
        j.start()

    for j in jobs:
        j.join()
