#!/usr/bin/python
import psycopg2
# note that we have to import the Psycopg2 extras library!
import psycopg2.extras
from collections import Counter


def createTrainingFeature():
    conn_string = "host='130.15.1.82' dbname='androzoo' user='shahrear' password='$Obscure123'"
    # print the connection string we will use to connect
    print "Connecting to database\n	->%s" % conn_string

    try:
        conn = psycopg2.connect(conn_string)
        conn.autocommit = True

    except:
        print "Cannot connect to db"

    # text_file = open("perm_v.txt", "w")

    try:
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        #cursor.execute('SELECT id, vt_detection, tr_data FROM apps_personal where (id between 1 and 100) or (id between 11000 and 11100)')
        cursor.execute('SELECT id, vt_detection, tr_data FROM apps_personal')

        good_list = []
        bad_list = []

        for row in cursor:
            app_permissions = str(row['tr_data']).split(',')
            app_permissions.pop()
            app_permissions.pop()

            if int(row['vt_detection']) > 5:
                bad_list.extend(app_permissions)
            else:
                good_list.extend(app_permissions)

        good_dict = Counter(good_list)
        bad_dict = Counter(bad_list)

        good_common = good_dict.most_common(30)
        bad_common = bad_dict.keys()

        good_common_list = [i[0] for i in good_common]


        bad_perm_list = list(set(bad_common) - set(good_common_list))

        print good_common
        print bad_common
        print bad_perm_list

        cursor.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print error

    if conn is not None:
        conn.close()
        # text_file.close()


def main():
    createTrainingFeature()

if __name__ == "__main__":
    main()

