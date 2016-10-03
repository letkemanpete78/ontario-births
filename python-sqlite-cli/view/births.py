import os
import sqlite3
class BIRTHS:

    # constructor
    def __init__( self):
        return

    # destructor
    def __del__(self):
        class_name = self.__class__.__name__
        #print ("Class '" + class_name + "' destroyed")

    def table_header(self):
        print("+---------------------------------------------------------+")
        print("|  AUTOID   |         CITY         | YEAR | MONTH | COUNT |")
        print("+---------------------------------------------------------+")

    def page_header(self,pagenum):
        print(" " * 12,"/","=" * 24,"\\")
        print(" " * 12,"|"," Ontario Births By Year ","|"," " * 4,"Page: " + str(pagenum).rjust(6))
        print(" " * 12,"\\","=" * 24,"/")

    def page_footer(self):
        print("+---------------------------------------------------------+")
        print("  {E}dit     | {D}elete | {A}dd      | {C}onfigure\n")
        print("  {P}revious | {N}ext   | {R}efresh  | {I}nit Data\n")
        print("  E{x}port   | {T}op 50 Records      | {Q}uit")
        action = input("\n  Action: ")
        return action.lower()

    def display_delete(self,row):
        retval = 0
        print ("  /---------------\\")
        print ("  |   Record View |")
        print ("  \\---------------/\n")
        print (" AutoID: " + str(row["autoID"]))
        print ("   City: " + row["theCity"])
        print ("   Year: " + str(row["theYear"]))
        print ("  Month: " + row["theMonth"])
        print ("  Count: " + str(row["theCount"]))
        delete_record = input(" Delete Record (y/n): ")
        if delete_record is None:
            retval = -1
        else:
            delete_record = delete_record.strip()
            if len(delete_record) < 1:
                retval = -1
            else:
                delete_record = delete_record[0:1].lower()
                if delete_record == "y":
                    retval = str(row["autoID"])
                else:
                    retval = -1
        return retval

    def display_insert(self):
        monthNum = 0
        monthOptions = {
            'jan': 1,
            'feb': 2,
            'mar': 3,
            'apr': 4,
            'may': 5,
            'jun': 6,
            'jul': 7,
            'aug': 8,
            'sep': 9,
            'oct': 10,
            'nov': 11,
            'dec': 12
        }

        # input values
        print ("  /---------------\\")
        print ("  |   Add Record  |")
        print ("  \\---------------/\n")
        theCity = input(" City (ex: Toronto) : ")
        theYear = input(" Year (ex: 2015): ")
        theMonth = input(" Month (ex: Jan): ")
        theCount = input(" Count (ex: 20: ")
        autoID = 0

        # validate inputs
        if theCity is None:
            theCity = ""

        if theYear is None:
            theYear = 0
        else:
            if len(theYear) < 1:
                theYear = 0
            else:
                if theYear.isnumeric():
                    theYear = theYear
                else:
                    theYear = 0

        if theMonth is None:
            theMonth = "Jan"
        theMonth = theMonth.strip()
        if len(theMonth) < 3:
            theMonth = "Jan"
        else:
            theMonth = theMonth[0:2]
        monthNum = monthOptions[theMonth.lower()]
        if monthNum == 0:
            monthNum = 1
            theMonth = "Jan"
        if theCount is None:
            theCount = 0
        else:
            theCount = theCount.strip()
            if len(theCount) < 1:
                theCount = 0
            else:
                if theCount.isnumeric():
                    theCount = theCount
                else:
                    theCount = int(row["theCount"])

        retval = {"theCity" : theCity,"theYear" : str(theYear),"theMonth" : theMonth,"theCount" : str(theCount),
                  "autoID" : str(autoID),"monthNum" :  str(monthNum)}
        return retval

    def display_edit(self,row):
        monthNum = 0
        monthOptions = {
            'jan': 1,
            'feb': 2,
            'mar': 3,
            'apr': 4,
            'may': 5,
            'jun': 6,
            'jul': 7,
            'aug': 8,
            'sep': 9,
            'oct': 10,
            'nov': 11,
            'dec': 12
        }

        # input values
        print ("  /---------------\\")
        print ("  |  Edit Record  |")
        print ("  \\---------------/\n")
        theCity = input(" City (" + row["theCity"] + "): ")
        theYear = input(" Year (" + str(row["theYear"]) + "): ")
        theMonth = input(" Month (" + row["theMonth"] + "): ")
        theCount = input(" Count (" + str(row["theCount"]) + "): ")
        autoID = row["autoID"]

        # validate inputs
        if theCity is None:
            theCity = row["theCity"]
        theCity = theCity.strip()
        if len(theCity) < 2:
            theCity = row["theCity"]

        if theYear is None:
            try:
                theYear = int(row["theYear"])
            except:
                theYear = 0
        else:
            theYear = theYear.strip()
            if len(theYear) < 1:
                theYear = int(row["theYear"])
            else:
                if theYear.isnumeric():
                    theYear = theYear
                else:
                    theYear = int(row["theYear"])
        if theMonth is None:
            theMonth = row["theMonth"]
        theMonth = theMonth.strip()
        if len(theMonth) < 3:
            theMonth = row["theMonth"]
        else:
            theMonth = theMonth[0:2]
        monthNum = monthOptions[theMonth.lower()]
        if monthNum == 0:
            theMonth = "Jan"
            monthNum = 1
        if theCount is None:
            try:
                theCount = int(row["theCount"])
            except:
                theCount = 0
        else:
            theCount = theCount.strip()
            if len(theCount) < 1:
                theCount = int(row["theCount"])
            else:
                if theCount.isnumeric():
                    theCount = theCount
                else:
                    theCount = int(row["theCount"])

        retval = {"theCity" : theCity,"theYear" : str(theYear),"theMonth" : theMonth,"theCount" : str(theCount),
                  "autoID" : str(autoID),"monthNum" :  str(monthNum)}
        return retval

    def display_list(self,rows,pagenum):
        if rows is None:
            action = "c"
            input ("Sorry, no records found. Please change search term.")
        else:
            if len(rows) == 0:
                action = "c"
                input ("Sorry, no records found. Please change search term.")
            else:
                self.page_header(pagenum)
                self.table_header()
                itemCounter = 0
                for row in rows:
                    print("|" + str(row["autoID"]).rjust(10) + " | " + row["theCity"].ljust(20) + " | " +
                          str(row["theYear"]).rjust(4) + " | " + row["theMonth"] + ".  | " + str(row["theCount"]).rjust(5) + " | ")
                    itemCounter = itemCounter + 1
                    if itemCounter % 10 == 0:
                        self.table_header()
                action = self.page_footer()
        retval = {"action":action,"pagenum":pagenum}
        return retval

    def display_summery(self,rows):
        for row in rows:
            cities = str(row["theCity"]).split(",")
            counts = str(row["theCount"]).split(",")
            print ("\n             TOP 50 RECORDS\n")
            print (" +=====+======================+=========+")
            print (" |     |         City         |  Count  |")
            print (" +=====+======================+=========+")
            for itemCounter in range(0,len(cities)):
                print(" | " + str(itemCounter+1).rjust(2) + ". | " + str(cities[itemCounter]).ljust(20) + " | " + str(counts[itemCounter]).rjust(7) + " |")
            print (" +=====+======================+=========+")
            input("\n Continue...")