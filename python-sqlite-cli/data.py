import sys
import re
import sqlite3
import numpy as np
import matplotlib.pyplot as plt

import controller.births as BirthController
import view.births as BirthView
import os

def clear():
    try:
        os.system("cls")
    except:
        os.system("clear")

def birth(page_size,sort_field,sort_direction,current_page):
    clear()
    action = "r"
    pg_num = current_page
    pg_size = page_size
    search_fields = "theYear"
    search_words = ""
    record_sort_field = sort_field
    record_sort_direction = sort_direction
    while action != "q":
        if action == "c":
            conf = searching_config(pg_num,search_fields,search_words,pg_size,record_sort_field,record_sort_direction)
            pg_num = conf["page_number"]
            pg_size = conf["page_size"]
            search_fields = conf["search_fields"]
            search_words = conf["search_words"]
            record_sort_field = conf["sort_field"]
            record_sort_direction = conf["sort_direction"]
        elif action == "n":
            pg_num = int(pg_num) + 1
        elif action == "p":
            pg_num = int(pg_num) - 1
            if int(pg_num) < 1:
                pg_num = 1
        tempval = process_action(action,pg_size,record_sort_field,record_sort_direction,pg_num,search_fields,search_words)
        if action is not None:
            action = action[0:1].lower()
        pagenum = tempval["pagenum"]

        action = tempval["action"]

def process_action(action,page_size,sort_field,sort_direction,current_page,search_fields,search_words):
    pg_num = current_page
    retval = None
    if action is not None:
        action = action.lower()
        if action == "e":
            autoID = input(" Enter AutoID Of Record To Edit: ")
            if autoID is not None:
                try:
                    autoID = int(autoID)
                except:
                    autoID = 0
            else:
                autoID = autoID.strip()
                if len(autoID) < 1:
                    theYear = 0
                else:
                    if autoID.isnumeric():
                        autoID = autoID
                    else:
                        autoID = 0
            if autoID > 0:
                clear()
                temp = BirthController.BIRTHS()
                row = temp.get_single_record(autoID)
                birth_view = BirthView.BIRTHS()
                temp_record = birth_view.display_edit(row)
                if temp_record is not None:
                    x = temp.update_one(temp_record["autoID"],temp_record["theYear"],temp_record["theMonth"],
                                        temp_record["theCity"],temp_record["monthNum"],temp_record["theCount"])
                    if int(x) > 0:
                        clear()
                        print(" " + str(x) + " Record(s) Updated")
                retval = {"action":"r","pagenum":pg_num}
        elif action == "t":
            clear()
            temp = BirthController.BIRTHS()
            rows = temp.top_summary(50)
            birth_view = BirthView.BIRTHS()
            birth_view.display_summery(rows)
            retval = {"action":"r","pagenum":1}
        elif action == "i":
            temp = BirthController.BIRTHS()
            print ("\n  Loading, takes a few moments...")
            retval = temp.load_words("births_by_year_and_month_per_place_of_event_city_2010_0.csv","true")
            input ("\n\n  " + str(retval) + " records imported.")
            retval = {"action":"r","pagenum":pg_num}
        elif action == "d":
            clear()
            autoID = input(" Enter AutoID Of Record To Delete: ")
            if autoID is not None:
                try:
                    autoID = int(autoID)
                except:
                    autoID = 0
            else:
                autoID = autoID.strip()
                if len(autoID) < 1:
                    theYear = 0
                else:
                    if autoID.isnumeric():
                        autoID = autoID
                    else:
                        autoID = 0
            if autoID > 0:
                temp = BirthController.BIRTHS()
                row = temp.get_single_record(autoID)
                if row is not None:
                    birth_view = BirthView.BIRTHS()
                    delete_autoID = birth_view.display_delete(row)
                    if int(delete_autoID) > 0:
                        x = temp.delete(delete_autoID)
                        if x > 0:
                            clear()
                            print (" Record Deleted")
                        else:
                            print (x)
                            sys.exit(0)
                    else:
                        clear()
                        if delete_autoID < 0:
                            print(" Record Not Deleted")
                            retval = {"action":"r","pagenum":pg_num}
                        else:
                            print(delete_autoID," Record Not Found")
                else:
                    clear()
                    print(" Record Not Found")
            retval = {"action":"r","pagenum":pg_num}
        elif action == "x":
            temp = BirthController.BIRTHS()
            filename = temp.csv_file()
            input ("\n\n " + filename + " created.")
            retval = {"action":"r","pagenum":pg_num}
        elif action == "a":
            birth_view = BirthView.BIRTHS()
            temp_record = birth_view.display_insert()
            if temp_record is not None:
                temp = BirthController.BIRTHS()
                x = temp.insert_one(temp_record["theYear"],temp_record["theMonth"],temp_record["theCity"],
                                    temp_record["monthNum"],temp_record["theCount"])
                if x > 0:
                    clear()
                    print(" Record Added")
            retval = {"action":"r","pagenum":pg_num}
        elif action == "p":
            temp = BirthController.BIRTHS()
            rows = temp.get_many_records(page_size,sort_field,sort_direction,pg_num,search_fields,search_words)
            birth_view = BirthView.BIRTHS()
            clear()
            retval = birth_view.display_list(rows,pg_num)
        elif action == "n":
            temp = BirthController.BIRTHS()
            rows = temp.get_many_records(page_size,sort_field,sort_direction,pg_num,search_fields,search_words)
            birth_view = BirthView.BIRTHS()
            clear()
            retval = birth_view.display_list(rows,pg_num)
        elif action == "q":
            clear()
            print("Good Bye")
            retval = {"action":action,"pagenum":pg_num}
        else:
            temp = BirthController.BIRTHS()
            rows = temp.get_many_records(page_size,sort_field,sort_direction,pg_num,search_fields,search_words)
            clear()
            birth_view = BirthView.BIRTHS()
            retval = birth_view.display_list(rows,pg_num)
    return retval

# display configuration/program options
def searching_config(page_number,search_fields,search_words,page_size,record_sort_field,record_sort_direction):
    retval = None
    pg_num = page_number
    pg_size = page_size
    search_fld = search_fields
    search_terms = search_words
    sort_field = record_sort_field
    sort_direction = record_sort_direction
    clear()
    print ("     /--------------------\\")
    print ("     |      Configure     |")
    print ("     \\--------------------/")
    print (" 1. Page Number (" + str(pg_num) + ") ")
    print (" 2. Page Size (" + str(pg_size) + ") ")
    print (" 3. Search Fields (" + search_fld + ") ")
    print (" 4. Search Terms (" + search_terms + ") ")
    print (" 5. Sort Field (" + sort_field + ") ")
    print (" 6. Sort Direction (" + sort_direction + ") ")
    print (" 7. Return")
    print (" 8. Exit")
    action = input ("\n Select Action: ")
    if action is not None:
        if action.isnumeric():
            action = int(action)
            if action == 1:
                print ("     /---------------------------------\\")
                print ("     |      Configure : Page Number    |")
                print ("     \\---------------------------------/")
                pg_num = input (" Enter New Page Number (" + str(pg_num) + "): ")
                if pg_num is not None:
                    if pg_num.isnumeric():
                        if int(pg_num) > 0:
                            pg_num = pg_num
                        else:
                            pg_num = page_number
                    else:
                        pg_num = page_number
                else:
                    pg_num = page_number
            elif action == 2:
                print ("     /-------------------------------\\")
                print ("     |      Configure : Page Size    |")
                print ("     \\-------------------------------/")
                pg_size = input (" Enter New Page Size (" + str(pg_size) + "): ")
                if pg_size is not None:
                    if pg_size.isnumeric():
                        if int(pg_size) > 1:
                            pg_size = pg_size
                        else:
                            pg_size = page_number
                    else:
                        pg_size = page_number
                else:
                    pg_size = page_number
            elif action == 3:
                print ("     /-------------------------------\\")
                print ("     |    Configure : Search Field   |")
                print ("     \\-------------------------------/")
                print(" 1 - AutoID | 2 - Year | 3 - Month | 4 - City | 5 - Count")
                search_fld = input (" Select Field For Searching (" + search_fld + "). e.g. 1,2 : ")
                if search_fld is not None:
                    temp_fld = ""
                    if "1" in search_fld:
                        temp_fld = temp_fld + "AutoID,"
                    if "2" in search_fld:
                        temp_fld = temp_fld + "TheYear,"
                    if "3" in search_fld:
                        temp_fld = temp_fld + "TheMonth,"
                    if "4" in search_fld:
                        temp_fld = temp_fld + "TheCity,"
                    if "5" in search_fld:
                        temp_fld = temp_fld + "TheCount,"
                    if temp_fld is not None:
                        if len(temp_fld) > 1:
                            if temp_fld[-1] == ",":
                                temp_fld = temp_fld[:-1]
                    if temp_fld is not None:
                        search_fld = temp_fld
                    else:
                        search_fld = search_fields
                else:
                    search_fld = search_fields
            elif action == 4:
                print ("     /---------------------------------\\")
                print ("     |      Configure : Search Term    |")
                print ("     \\---------------------------------/")
                search_terms = input(" Enter Search Terms: ")
                if search_terms is not None:
                    search_terms = search_terms
                else:
                    search_terms = search_words
            elif action == 5:
                print ("     /--------------------------------\\")
                print ("     |      Configure : Sort Field    |")
                print ("     \\--------------------------------/")
                print (" 1 - AutoID | 2 - Year | 3 - Month | 4 - City | 5 - Count")
                sort_field = input (" Cboose A Field: ")
                if sort_field is not None:
                    if sort_field == "1":
                        sort_field = "AutoID"
                    elif sort_field == "2":
                        sort_field = "TheYear"
                    elif sort_field == "3":
                        sort_field = "TheMonth"
                    elif sort_field == "4":
                        sort_field = "TheCity"
                    elif sort_field == "5":
                        sort_field = "TheCount"
                    else:
                        sort_field = record_sort_field
                else:
                    sort_field = record_sort_field
            elif action == 6:
                print ("     /------------------------------------\\")
                print ("     |      Configure : Sort Direction    |")
                print ("     \\------------------------------------/")
                sort_direction = input (" 1 - Ascending | 2 - Decending: ")
                if sort_direction is not None:
                    if sort_direction == "1":
                        sort_direction = "ASC"
                    elif sort_direction == "2":
                        sort_direction = "DESC"
                    else:
                        sort_direction = record_sort_direction
                else:
                    sort_direction = record_sort_direction
            elif action == 8:
                print (" Good Bye")
                sys.exit(0)
    retval = {"page_number":pg_num,"page_size":pg_size,"search_fields":search_fld,"search_words":search_terms,
              "sort_direction":sort_direction,"sort_field":sort_field}
    return retval

def PlotSummaryData():
    dbConnect = sqlite3.connect('births.db')
    dbConnect.row_factory = sqlite3.Row

    dbCursor = dbConnect.cursor()
    sqlString = "select group_concat(theCity) as theCity , group_concat(theCount)  as theCount from " \
                "(select group_concat(theCity) as theCity, group_concat(theCount)  as theCount from (select  sum(theCount) " \
                "as theCount, theCity from births group by theCity order by sum(theCount)  desc limit 49) UNION " \
                "select 'Other' as theCity, sum(theCount) as theCount from (select  sum(theCount) as thecount from births " \
                "group by theCity order by sum(theCount)  desc limit 50,2000) ) order by  theCount, theCity;"
    dbCursor.execute(sqlString)
    data = dbCursor.fetchone()
    if data is None:
        print('Empty')
    else:
        tempValues = data["theCity"]
        cities = tempValues.split(",")
        tempValues = data["theCount"]
        births = [int(k) for k in tempValues.split(',')]

        import matplotlib.pyplot as plt; plt.rcdefaults()
        import numpy as np
        import matplotlib.pyplot as plt

        y_pos = np.arange(len(cities))

        plt.bar(y_pos, births, align='center', alpha=0.5)
        plt.xticks(y_pos, cities)
        plt.ylabel('Births')
        plt.gcf().autofmt_xdate()

        plt.title('Births By City')

        plt.show()
    dbConnect.close()

def main():
    birth(10,"theCity","ASC",1)

if __name__ == '__main__':
    main()