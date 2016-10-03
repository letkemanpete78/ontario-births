import sqlite3
import sys
import re
import datetime

class BIRTHS:

    # constructor
    def __init__( self, DBName = "births.db"):
        self.DBName = "births.db"
        self.dbConnect = sqlite3.connect(self.DBName)
        self.dbConnect.row_factory = sqlite3.Row
        self.dbCursor = self.dbConnect.cursor()

        # destructor
    def __del__(self):
        class_name = self.__class__.__name__
        self.dbCursor.close()
        self.dbConnect.close
        #print ("Class '" + class_name + "' destroyed")

    # insert one record
    # return autoID of record what was just inserted, otherwise return -1
    def insert_one(self,TheYear,TheMonth,TheCity,MonthNum,TheCount):
        ## sample call
        # temp = BirthsTable.BIRTHS()
        # retval = temp.insert_one(2012,"Apr","Toronto",4,10)
        # print(retval)

        retval = 0
        try:
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
            recordYear = 0
            recordMonth = ""
            recordMonthNum = 0
            recordCity = ""
            recordCount = 0
            if TheYear is not None:
                if TheYear.isnumeric():
                    recordYear = int(TheYear)
            if TheMonth is not None:
                recordMonth = TheMonth[0:2]
                recordMonthNum = monthOptions[recordMonth.lower()]
                if recordMonthNum == 0:
                    recordMonth = "Jan"
                    recordMonthNum = 1
            if TheCity is not None:
                recordCity = TheCity
            if TheCount is not None:
                if TheCount.isnumeric():
                    recordCount = int(TheCount)
            self.dbCursor.execute("INSERT INTO births (theYear,theMonth,theCity,theCount,monthNum) VALUES "
                                  "(:theYear,:theMonth,:theCity,:theCount,:monthNum)",
                                  {"theYear" :recordYear,"theMonth":recordMonth,"theCity":recordCity,
                                   "theCount":recordCount,"monthNum":recordMonthNum})
            retval = self.dbCursor.lastrowid
            self.dbConnect.commit()
        except:
            retval = -1
        return retval

    # update one record
    # return the number of records updated, otherwise return 0
    def update_one(self,autoID,TheYear,TheMonth,TheCity,MonthNum,TheCount):
        ## sample call
        # temp = BirthsTable.BIRTHS()
        # retval = temp.update_one(100,2012,"Apr","Toronto",4,10)
        # print(retval)

        retval = 0
        try:
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
            recordYear = 0
            recordMonth = ""
            recordMonthNum = 0
            recordCity = ""
            recordCount = 0
            if TheYear is not None:
                if TheYear.isnumeric():
                    recordYear = int(TheYear)
            if TheMonth is not None:
                recordMonth = TheMonth[0:2]
                recordMonthNum = monthOptions[recordMonth.lower()]
                if recordMonthNum == 0:
                    recordMonth = "Jan"
                    recordMonthNum = 1
            if TheCity is not None:
                recordCity = TheCity
            if TheCount is not None:
                if TheCount.isnumeric():
                    recordCount = int(TheCount)
            retval = self.dbCursor.execute("UPDATE births SET theYear=:theYear,theMonth=:theMonth,theCity=:theCity,"
                                           "theCount=:theCount,monthNum=:monthNum WHERE autoID=:autoID",
                                           {"theYear" :recordYear,"theMonth":recordMonth,"theCity":recordCity,
                                            "theCount":recordCount,"monthNum":recordMonthNum,"autoID":autoID}).rowcount
            self.dbConnect.commit()
        except:
            retval = -1
        return retval

    # retreive single record
    # return single record as a list object if record in database, otherwise return a value of NONE
    def get_single_record(self,autoID):
        ## sample call
        # temp = BirthsTable.BIRTHS()
        # retval = temp.get_single_record(100)
        # print(retval)

        retval = None
        try:
            if int(autoID) > 0:
                sqlString = "SELECT autoID,theYear,theMonth,theCity,theCount,monthNum FROM births WHERE autoID=" + str(autoID)
                self.dbCursor.execute (sqlString)
                row = self.dbCursor.fetchone()
                if row is not None:
                    retval = {"autoID":row["autoID"],"theYear":row["theYear"],"theMonth":row["theMonth"],
                              "theCity":row["theCity"],"theCount":row["theCount"],"monthNum":row["monthNum"]}
        except:
            retval = None
        return retval

    # retreive many records
    # return many records as a list of objects of records found in the database, otherwise return NONE
    def get_many_records(self,page_size,sort_field,sort_direction,current_page,search_fields,search_words):
        ## sample call
        # temp = BirthsTable.BIRTHS()
        # retval = temp.get_many_records(10,"theCity","ASC",1,"theMonth","2012")
        # for item in retval:
        #    print (item)

        retval = None
        record_start = 0
        record_size = 10
        record_page = 0
        order_by = "theCity"
        order_direction = "ASC"
        try:
            if int(current_page) < 1:
                record_page = 1
            else:
                record_page = current_page
        except:
            record_page = 1
        try:
            if int(page_size)  > 0 and int(page_size) < 100:
                record_size = int(page_size)
        except:
            record_size = 10
        if sort_field is None:
            order_by = "theCity"
        else:
            if len(sort_field) > 3:
                tempStr = ",autoid,theyear,themonth,thecity,thecount,monthnum,"
                if sort_field.lower() in tempStr:
                    order_by = sort_field
                else:
                    order_by = "theCity"
        if sort_direction is None:
            order_direction = "ASC"
        else:
            if sort_direction == "DESC":
                order_direction = "DESC"
            else:
                order_direction = "ASC"
        record_start = (int(record_page) -1) * int(record_size)
        query_words = {}
        query_fields = {}
        query_expression = ""
        if search_fields is not None:
            query_fields = search_fields.strip().split(",")
            if search_words is not None:
                query_words = search_words.lower().strip().split(" ")
                for qfield in query_fields:
                    for qword in query_words:
                        if qfield.strip() != "":
                            query_expression = query_expression + " (" + qfield + " LIKE '%" + qword.replace("'","''") \
                                               + "%') OR (" + qfield + " = '" + qword.replace("'","''") + "') OR"
                if len(query_expression) > 3:
                    if query_expression[-2:] == "OR":
                        query_expression = " WHERE " + query_expression[:-2]
        sqlString = "SELECT AutoID,TheYear,TheMonth,TheCity,MonthNum,theCount FROM births " + query_expression \
                    + " ORDER BY " + order_by + " " + order_direction + " LIMIT " + str(record_size) + " OFFSET " + str(record_start)
        self.dbCursor.execute(sqlString)
        self.current_page = int(current_page) + 1
        retval = self.dbCursor.fetchall()
        return retval

    # create a comma seperate list file with all the records in it
    # return filename
    def csv_file(self):
        sqlString = "SELECT AutoID,TheYear,TheMonth,TheCity,MonthNum,theCount FROM births"
        rows = self.dbCursor.execute(sqlString)
        filename = "workfile_" + datetime.datetime.today().strftime('%Y%m%d') + ".csv"
        outfile = open(filename, "w")
        outfile.write("ID,Year,Month,City,Month Num,Count\n")
        for row in rows:
            outfile.write(str(row["AutoID"]) + "," + str(row["TheYear"]) + "," + str(row["TheMonth"]) + "," +
                          str(row["TheCity"]) + "," + str(row["MonthNum"]) + "," + str(row["theCount"]) + "\n")
        return filename

    # delete records, autoID is comma seperated list
    # retval 0 if no records are deleted
    def delete(self,autoID):
        ## sample call
        # temp = BirthsTable.BIRTHS()
        # retval = temp.delete(101)
        # print (retval)

        retval = 0
        if autoID is None:
            retval = 0
        else:
            #dbConnect = sqlite3.connect(self.DBName)
            #dbConnect.row_factory = sqlite3.Row
            #dbCursor = dbConnect.cursor()
            sqlString = "DELETE FROM births WHERE autoID IN (" + str(autoID) + ")"
            retval = self.dbCursor.execute(sqlString).rowcount
            self.dbConnect.commit()
            #dbCursor.close()
            #dbConnect.close()
        return retval

    # load CSV file into the database
    # return number of records inserted
    def load_words(self,filename,resetDB):
        ## sample call
        # temp = BirthsTable.BIRTHS()
        # retval = temp.load_words("births_by_year_and_month_per_place_of_event_city_2010_0.csv",false)
        # print (retval)

        f = open(filename, 'r')
        lineCounter = 0
        if resetDB is not None:
            sqlString = "DROP TABLE IF EXISTS births"
            self.dbCursor.execute (sqlString)
            sqlString = "CREATE TABLE IF NOT EXISTS births (autoID INTEGER PRIMARY KEY AUTOINCREMENT, theYear INTEGER, " \
                    "theMonth TEXT, theCity TEXT, theCount INTEGER, monthNum INTEGER)"
        self.dbCursor.execute (sqlString)
        theYear = 0
        theMonth = ""
        theCity = ""
        theCount = 0
        monthNum = 0
        monthOptions = {
            'Jan': 1,
            'Feb': 2,
            'Mar': 3,
            'Apr': 4,
            'May': 5,
            'Jun': 6,
            'Jul': 7,
            'Aug': 8,
            'Sep': 9,
            'Oct': 10,
            'Nov': 11,
            'Dec': 12
        }
        ## ([\d]{4}),([A-Za-z ]*),([([\w\(\)\*;:\"\'.-\]*)\-\s]*),([\d]{1,4})
        ## 1912,Apr,TORONTO,6
        for line in f:   ## iterates over the lines of the file
            match = re.search(r'([\d]{4}),([A-Za-z ]*),([([\w\(\)\*;:\"\'.-\]*)\-\s]*),([\d]{1,4})',line)
            if match:
                lineCounter = lineCounter + 1
                theYear = match.group(1)
                theMonth = match.group(2)
                theCity = match.group(3)
                theCount = match.group(4)
                monthNum = monthOptions[theMonth]
                sqlString = "INSERT INTO births (theYear,theMonth,theCity,theCount,monthNum) VALUES (" \
                            + theYear + ",'" + theMonth + "','" + theCity.replace("'","''").title() + "'," + theCount \
                            + "," + str(monthNum) + ");"
                try:
                    self.dbCursor.execute (sqlString)
                except:
                    print (sqlString)
                sqlString = ""
        self.dbConnect.commit()
        f.close()
        return lineCounter

    # summary of the top X values
    def top_summary(self,limit_num):
        top_num = 50
        if limit_num is not None:
            if str(limit_num).isnumeric():
                if int(limit_num) > 10:
                    top_num = limit_num
        sqlString = "select group_concat(theCity) as theCity , group_concat(theCount)  as theCount from " \
                    "(select group_concat(theCity) as theCity, group_concat(theCount)  as theCount from " \
                    "(select  sum(theCount) as theCount, theCity from births group by theCity order by " \
                    "sum(theCount) desc limit " + str(int(top_num-1)) + ") UNION select 'Other' as theCity, " \
                    "sum(theCount) as theCount from (select sum(theCount) as thecount from births group by theCity " \
                    "order by sum(theCount) desc limit " + str(top_num) + ",2000000) ) order by  theCount, theCity;"
        rows = self.dbCursor.execute(sqlString)
        return rows


#        sqlString = "select group_concat(theCity) as theCity , group_concat(theCount)  as theCount from " \
#                    "(select group_concat(theCity) as theCity, group_concat(theCount)  as theCount from " \
#                    "(select  sum(theCount) as theCount, theCity from births group by theCity order by " \
#                    "sum(theCount) desc limit " + str(int(limit_num)-1) + ") UNION select 'Other' as theCity, " \
#                      "sum(theCount) as theCount from (select sum(theCount) as thecount from births group by theCity " \
#                      "order by sum(theCount) desc limit " + str(limit_num) + ",2000000) ) order by  theCount, theCity;"