import time
import mysql.connector
from datetime import datetime, timedelta, date
import pandas as pd


def main(parma_setting):
    mycursor = parma_setting["mysql_db"].cursor()
    #print(parma_setting["process_date"])


    st = time.time()
    while True:
        offset = parma_setting["num_per_page"] * parma_setting["page_counter"]
        mycursor.execute(
            """
            SELECT a.*
            from my_table as a 
            where a.id <> 00000
            order by a.date
            LIMIT %d, %d;
            """ % (offset, parma_setting["num_per_page"]))
        try:
            rows = mycursor.fetchall()
        except:
            parma_setting["page_counter"] += 1
            continue

        if len(rows) == 0:
            break

        field_names = [i[0] for i in mycursor.description]
        body = []
        for row in rows:
            data = {"engagement_lists": []}
            for index, value in enumerate(row):
                if "count" in field_names[index]:
                    try:
                        value = int(value)
                    except:
                        value = 0
                    data[field_names[index]] = value
                if field_names[index] == "mark":
                    continue
                elif field_names[index] == "content":
                    if value is not None:
                        if isinstance(value, bytes):
                            data["content"] = value.decode("utf-8")
                        elif isinstance(value, str):
                            data["content"] = value
                    else:
                        data[field_names[index]] = None
                elif field_names[index] == "date":
                    data[field_names[index]] = str(value)
                else:
                    data[field_names[index]] = value

            body.append(data)
            parma_setting["item_counter"] += 1


        parma_setting["page_counter"] += 1
        print("page: %d, total: %d, time used: %.2f" % (
            parma_setting["page_counter"],
            parma_setting["item_counter"],
            time.time() - st)
        )
        title = parma_setting["page_counter"]

        # add ur excel column names here
        df = pd.DataFrame(data=body,columns=['name', 'person_id', 'product_id', 'date','profit_ratio'])

        #df = (df.T)  
        #use page count for each excel file name
        df.to_excel('{}.xlsx'.format(str(title)))

    mycursor.close()


if __name__ == "__main__":

    mydb = mysql.connector.connect(
        host="your_database.rds.com",
        user="username",
        passwd="password",
        database="db1",
        use_pure=True
    )

    parma_setting = {
            "mysql_db": mydb,
            "page_counter": 0,
            "num_per_page": 10000,            #how many rows for each excel sheet
            "item_counter": 0
            #"process_date": _date.strftime("%Y%m%d") + "%"
        }

    current = datetime.now()
    print("[Time Log]" + str(current))
    main(parma_setting)
mydb.close()
