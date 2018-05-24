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
                time = p_g_j['result']['timeStamp']
                for obj in p_g_j['result']['uncles']:
                    miner = obj['miner'][2:]
                    reward = obj['blockreward']
                    ft.write("ethereum,"+miner+","+reward+","+time+","+temp[0])
                    ft.write("\n")
                #u_i_reward = p_g_j['result']['uncleInclusionReward']
                print("parsed block",temp[0])

def crawlUncleInclusionReward(fname_1,fname_2,apikey):
    url = 'https://api.etherscan.io/api?module=block&action=getblockreward&blockno='
    with open(fname_1,"a") as ft:
        with open(fname_2) as fs:
            for line in fs:
                temp = line.strip().split(",")
                if int(temp[0])>5326326:
                    url_c = url+temp[0]+"&apikey="+apikey
                    p_g = requests.get(url_c)
                    p_g_j = p_g.json()
                    sum_ = 0
                    time = p_g_j['result']['timeStamp']
                    u_i_reward = p_g_j['result']['uncleInclusionReward']
                    ft.write("ethereum,"+temp[1]+","+u_i_reward+","+time+","+temp[0])
                    ft.write("\n")
                    #print("ethereum,"+temp[1]+","+u_i_reward+","+time+","+temp[0])
                    print("parsed block",temp[0])


def crawlUncleRewardbyAPIrs(fname_1,fname_2,apikey):
    url = 'https://api.etherscan.io/api?module=block&action=getblockreward&blockno='
    with open(fname_1,"a") as ft:
        with open(fname_2) as fs:
            for line in fs:
                temp = line.strip().split(",")
                if int(temp[0])>5173420:
                    url_c = url+temp[0]+"&apikey="+apikey
                    p_g = requests.get(url_c)
                    p_g_j = p_g.json()
                    sum_ = 0
                    for obj in p_g_j['result']['uncles']:
                        sum_+=float(obj['blockreward'])
                    ft.write("ethereum,"+temp[1]+","+str(sum_)+",0,"+temp[0])
                    ft.write("\n")

                    print("parsed block",temp[0])
