#!/usr/bin/python
import psycopg2
# note that we have to import the Psycopg2 extras library!
import psycopg2.extras
import json
from datetime import datetime


def createTrainingData():
    conn_string = "host='130.15.1.82' dbname='androzoo' user='shahrear' password='$Obscure123'"
    # print the connection string we will use to connect
    print "Connecting to database\n	->%s" % conn_string

    try:
        conn = psycopg2.connect(conn_string)
        conn.autocommit = True

    except:
        print "Cannot connect to db"

    try:
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute('SELECT id, app_permissions, app_details FROM apps_personal')
        cursor2 = conn.cursor()
        permissions_all = set()
        updated_rows = 0
        for row in cursor:

            app_permissions = json.loads(row['app_permissions'])  # returns list of dict
            permstring = ''
            for permdict in app_permissions:
                permissions_all.add(permdict['permission'])
                permstring = permstring + permdict['permission'] + ','

            app_details = json.loads(row['app_details'])

            permstring = permstring + str(app_details['score']) + ',' + str(app_details['reviews'])

            sql = """ UPDATE apps_personal SET tr_data = %s WHERE id = %s"""

            cursor2.execute(sql, (permstring, row['id']))
            updated_rows += cursor2.rowcount

        perm_all_comma = sorted(permissions_all)
        print perm_all_comma
        print len(perm_all_comma)
        print updated_rows

        cursor.close()
        sql = """ UPDATE table_features SET feature_desc = %s, date_added = %s WHERE table_name = %s"""

        cursor2.execute(sql, (perm_all_comma, datetime.now(), 'apps_personal'))

        cursor2.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print error

    if conn is not None:
        conn.close()


def main():
    createTrainingData()

if __name__ == "__main__":
    main()

