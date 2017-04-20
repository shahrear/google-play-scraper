#!/usr/bin/python
import psycopg2
# note that we have to import the Psycopg2 extras library!
import psycopg2.extras
from math import exp


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

        cursor2 = conn.cursor()

        cursor.execute('SELECT feature_desc FROM table_features where table_name like \'apps_personal\'')

        for row in cursor:
            perm_all_comma = str(row[0]).replace('\"', '').split(',')

        perm_all_comma = sorted(perm_all_comma)

        # header_string = ''
        #
        # for i in range(0, len(perm_all_comma)):
        #     header_string += 'column' + str(i+1) + ','
        # header_string += 'review' + ',' + 'class'
        #
        # text_file.write(header_string + '\n')

        updated_rows = 0

        cursor.execute('SELECT id, vt_detection, tr_data FROM apps_personal')

        for row in cursor:
            feature_string = ''
            app_permissions = str(row['tr_data']).split(',')
            num_reviews = float(app_permissions.pop())
            review_score = float(app_permissions.pop())
            review_score_Q = 5000.0
            review_score_P = 0.7

            for perm in perm_all_comma:
                if perm in app_permissions:
                    feature_string += '1'
                else:
                    feature_string += '0'

                feature_string += ','

            weighted_review_score = ((review_score_P * review_score) + 5 * (1 - review_score_P) * (1 - exp(-(num_reviews/review_score_Q))) )

            feature_string += "{0:.2f}".format(weighted_review_score) + ','

            if int(row['vt_detection']) > 5:
                feature_string += '1'
            else:
                feature_string += '0'

            # text_file.write(feature_string + '\n')

            sql = """ UPDATE apps_personal SET tr_feature_values = %s WHERE id = %s"""

            cursor2.execute(sql, (feature_string, row['id']))
            updated_rows += cursor2.rowcount
            print updated_rows

        print updated_rows

        cursor.close()

        cursor2.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print error

    if conn is not None:
        conn.close()
        # text_file.close()


def main():
    createTrainingFeature()

if __name__ == "__main__":
    main()

