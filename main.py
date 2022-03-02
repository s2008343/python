#!/usr/bin/python
import csv
import os

import mysql.connector
from mysql.connector import Error
from members import Member
from perDag import Dag
import matplotlib.pyplot as plt
from lijsten import Lijsten
#wordlcloud
from wordcloud import WordCloud
import seaborn as sns

#boxplot
import numpy as np

# Treemap
import squarify
import pandas as pd
from kleur import Kleur

import time

# user='Cas',
# password='hNZtYCDk7xk81XUPKPT6')

lijst = Lijsten()
kleur = ['#913074','#53297A','#5357C6','#271B50','#D2B3E6','#DD98D3','#E3C7AB','#993533','#1B4250','#5357C6','#122536','#B4523C','#88D7C0']
global bierTotaal
bierTotaal = 0
def importMembers():
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='presentatie',
                                             user='root',
                                             password='root')
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("You're connected to database: ", record)

    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            sql_select_Query = "select id, login from members"
            cursur = connection.cursor()
            cursur.execute(sql_select_Query)
            records = cursor.fetchall()
            print("Total number of rows in table", cursor.rowcount)

            for row in records:
                mem = Member()
                mem.name = row[1]
                mem.id = row[0]
                lijst.member.append(mem)

            cursur.close()
            cursor.close()
            connection.close()
            print("MySQL connection is closed")




def aantalBier():
    global bierTotaal
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='presentatie',
                                             user='root',
                                             password='root')
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("You're connected to database: ", record)
            cursor.close()
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursur = connection.cursor()
            totaal = 0
            for mem in lijst.member:
                id = mem.id
                sql_select_Query = "select sum(aantal)  from streeplijsten where memberid like %s"%id;
                cursur.execute(sql_select_Query)
                record = cursur.fetchone()
                record = record[0]

                if (type(record) != type(None) ):
                    mem.aantal = record
                    lijst.kopie.append(mem)
                    bierTotaal += record
                    print(str(mem.name)+" "+str(mem.aantal))
            cursur.close()
            connection.close()

def createPieChart():
    pieLabels = []
    pieData = []
    pieLijst = lijst.member

    # sort list
    def getAantal(e):
        return e.aantal
    pieLijst.sort(key=getAantal)



    for mem in pieLijst:
        if  mem.aantal > 99:
            pieLabels.append(mem.name)
            pieData.append(mem.aantal)
    figureObject, axesObject = plt.subplots()

    explode = [0]*int(len(pieData))
    explode[len(explode)-1] = 0.1
    wedge_props = {"linewidth":1,"edgecolor": "None"}
    text_props = {"weight": "bold"}

    axesObject.pie(pieData, labels=pieLabels,colors=kleur, autopct='%1.0f', startangle=225, shadow=False,
                   explode=explode, wedgeprops=wedge_props, textprops=text_props,rotatelabels=True)


    axesObject.axis('equal')
    '''
    plt.savefig("pie.png",
                bbox_inches="tight",
                pad_inches=1,
                transparent=True,
                orientation='landscape')
    '''
    plt.show()

def createWordCloud():
    pieLijst = lijst.member

    # sort list
    def getAantal(e):
        return e.aantal
    pieLijst.sort(key=getAantal)
    text = ""
    for mem in pieLijst:
        text +=" "
        text +=str(mem.name)

    wordcloud = WordCloud(width=480,height=480,margin=0).generate(text)
    plt.imshow(wordcloud,interpolation='bilinear')
    plt.axis('off')
    plt.margins(x=0,y=0)
    plt.show()

def createTreemap():
    Labels = []
    Data = []
    treeLijst = naamCorrectie(lijst.member)

    # sort list
    def getAantal(e):
        return e.aantal

    treeLijst.sort(key=getAantal)

    for mem in treeLijst:
        if mem.aantal > 99:
            #print(bierTotaal)
            percentage = round(mem.aantal/bierTotaal,2)
            s = mem.name
            s +=" "
            s +=str(percentage)
            Labels.append(s)
            Data.append(float(mem.aantal))

    df = pd.DataFrame({'size': Data,'name': Labels})

    #plot
    squarify.plot(sizes=df['size'],label=df['name'],alpha=.6,color=kleur)
    plt.axis('off')
    plt.show()


def naamCorrectie(member):
    for mem in member:
        match mem.name:
            case 'davidpouw':
                mem.name = 'Koen'
            case 'justin':
                mem.name = 'Justin'
            case 'stijnkolkman':
                mem.name = 'Stinna'
            case 'cas':
                mem.name = 'Cas'
            case 'jorrit':
                mem.name = 'Jorrit'
            case 'basonck':
                mem.name = 'Bas'
            case 'marcel':
                mem.name = 'Marcel'
            case 'dino':
                mem.name = "Dino"
            case 'Michael':
                mem.name = 'Hop'
            case 'stevenvogt':
                mem.name = "Vogt"
    return member


## Split and create sql table where date and time are split

def createDayTimeTable(memberLijst):
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='presentatie',
                                             user='root',
                                             password='root')
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("You're connected to database: ", record)
            cursor.close()
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursur = connection.cursor()
            sql_select_Query = "select id, memberid, time, aantal, ladingid from streeplijsten";
            cursur.execute(sql_select_Query)
            record = cursur.fetchall()
            record2 = record.copy()
            record2.clear()
            if (type(record) != type(None) ):
               # print(type(record))
              #  print(record[0])
             #   print(type(record[0]))

                for entry in record:
                    e = ["1", "2", 3, 4, 5,6]
                    e1 = id2name(entry[1],memberLijst)
                    e2 = entry[2]
                    e3 = e2.year
                    e4 = e2.month
                    e5 = e2.day
                    e6 = e2.hour
                    e7 = e2.minute
                    e[0] = str(e1)
                    e[1] = str(e3)
                    e[2] = int(e4)
                    e[3] = int(e5)
                    e[4] = int(e6)
                    e[5] = int(e7)
                    record2.append(e)
                record3 = record2.copy()
                record3.clear()
                for mem in memberLijst:
                    name = mem.name
                    cwd = os.getcwd()
                    filepath = cwd+"\\data\\"+name+".csv"
                    with open (filepath,'a',newline='') as f:
                        write = csv.writer(f)
                        for entry in record2:
                            if(entry[0] == name):
                                write.writerow(entry)




            cursur.close()
            connection.close()

def createBoxplot(member):
    X = list()
    for mem in member:
        name = mem.name
        cwd = os.getcwd()
        filepath = cwd + "\\data\\" + name + ".csv"
        with open(filepath,newline='') as f:
            reader = csv.reader(f)
            data = list(reader)
        f.close()
        x = list()
        data = filter(None, data)
        for entry in data:
            #print(entry)
            hour = int(entry[4])
            minute = int(entry[5])



            if(hour<12):
                x.append(hour+24)
                X.append((hour+24)*60+minute)
            else:
                x.append(hour)
                X.append(hour*60+minute)

        fig, ax = plt.subplots(figsize=(3, 6))

        ax.set_title(name)
        ax.set_ylim([12, (24+11)])
        def_tick =  [12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35]
        my_tick=    [12,13,14,15,16,17,18,19,20,21,22,23,24,1,2,3,4,5,6,7,8,9,10,11]
        plt.yticks(def_tick,my_tick)
        plt.boxplot(x)
        savename = name + "png"
        #plt.savefig(savename)
        plt.show()

    fig, ax = plt.subplots(figsize=(3, 6))
    name = "Bentrot"
    ax.set_title(name)
    ax.set_ylim([12*60, (24+11)*60+59])
    plt.boxplot(X)
    savename = name + "png"
    plt.savefig(savename)
    plt.show()





def id2name(id,member):
    for mem in member:
        if(mem.id==id):
            return mem.name
    return "kanker"


def saveByDay(memberLijst):
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='presentatie',
                                             user='root',
                                             password='root')
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("You're connected to database: ", record)
            cursor.close()
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursur = connection.cursor()
            sql_select_Query = "select id, memberid, time, aantal, ladingid from streeplijsten";
            cursur.execute(sql_select_Query)
            record = cursur.fetchall()
            record2 = record.copy()
            record2.clear()
            if (type(record) != type(None) ):
               # print(type(record))
              #  print(record[0])
             #   print(type(record[0]))

                for entry in record:
                    e = ["1", "2", 3, 4, 5,6]
                    e1 = id2name(entry[1],memberLijst)
                    e2 = entry[2]
                    e3 = e2.year
                    e4 = e2.month
                    e5 = e2.day
                    e6 = e2.hour
                    e7 = entry[3]
                    e[0] = str(e1) # naam
                    e[1] = str(e3) # yaar
                    e[2] = int(e4) # maand
                    e[3] = int(e5) # dag
                    e[4] = int(e6) # uur
                    e[5] = int(e7) # aantal
                    record2.append(e)
                record3 = record2.copy()
                datums = list()

                for entry in record2:
                    datum = str(entry[1])+str(entry[2])+str(entry[3]) # yearmonthday

                    for d in datums:
                        x = 0
                        if(d == datum):
                            x = 1
                        if(x==0):
                            dag = Dag()
                            dag.datum = datum
                            datums.append(dag)
                            break

                for entry in record2:
                    for dag in datums:
                        if dag.datum==str(entry[1])+str(entry[2])+str(entry[3]):
                            dag.aantal = dag.aantal+entry[5]

            cursur.close()
            connection.close()
            return datums

def simpleDagTest(perdag):
    x = list()
    y = list()
    for dag in perdag:
        x.append(int(dag.datum))
        y.append(dag.aantal)
    i = 0
    for i in range(len(x)):
        print(str(x[0])+";"+str(y[0]))







def main():
    importMembers()
    aantalBier()
    lijst.member = lijst.kopie
   # createPieChart()
    #createWordCloud()
    #createTreemap()
    df = sns.load_dataset('diamonds')
    #createDayTimeTable(naamCorrectie(lijst.member))
   # createBoxplot(naamCorrectie(lijst.member))
    print("hoi")
    perdag = list()
    perdag = saveByDay(naamCorrectie(lijst.member))
    simpleDagTest(perdag)
    print("doei")
if __name__ == "__main__":
    main()