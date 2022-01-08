#!/usr/bin/python
import mysql.connector
from mysql.connector import Error
from members import Member
import matplotlib.pyplot as plt
from lijsten import Lijsten
#wordlcloud
from wordcloud import WordCloud
import seaborn as sns


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
            print(bierTotaal)
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

def main():
    print("Hello World!")
    importMembers()
    aantalBier()
    lijst.member = lijst.kopie
    createPieChart()
    createWordCloud()
    createTreemap()
    df = sns.load_dataset('diamonds')


if __name__ == "__main__":
    main()