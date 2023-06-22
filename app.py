from flask import Flask, request, jsonify, render_template
import json
import pymysql
app = Flask(__name__)


def db_connection():
    conn = None
    # try:
    conn = pymysql.connect(host='localhost',
                           #    host= 'sql12.freesqldatabase.com',
                                database='database_flask',
                                user='root',
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor
                           )
    # except pymysql.error as e:
    #     print(e)
    return conn


@app.route('/api/getEndpoint', methods=['GET'])
def users():

    conn = db_connection()
    cursor = conn.cursor()

    if request.method == 'GET':
        cursor.execute("SELECT * FROM dup_user_data")
        users = [
            dict(id=row['id'],
                 first_name=row['first_name'],
                 last_name=row['last_name'],
                 mobile_number=row['mobile_number'],
                 village=row['village'],
                 pincode=row['pincode'],
                 PrimaryFunction=row['PrimaryFunction'],
                 SecondaryFunction=row['SecondaryFunction'],
                 tehsil=row['tehsil'],
                 district=row['district'],
                 last_updated_at=row['last_updated_at'])

            for row in cursor.fetchall()
        ]
        if users is not None:
            return jsonify(users)


@app.route('/api/postData', methods=['POST'])
def add_data():

    conn = db_connection()
    cursor = conn.cursor()

    if request.is_json:
        data = request.get_json()

        first_name = data['first_name']
        last_name = data['last_name']
        mobile_number = data['mobile_number']
        village = data['village']
        pincode = data['pincode']
        PrimaryFunction = data['PrimaryFunction']
        SecondaryFunction = data['SecondaryFunction']
        tehsil = data['tehsil']
        district = data['district']

        query = "INSERT INTO dup_user_data (first_name, last_name, mobile_number, village, pincode, PrimaryFunction, SecondaryFunction, tehsil, district) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor = conn.cursor()
        cursor.execute(query, (first_name, last_name, mobile_number, village,
                       pincode, PrimaryFunction, SecondaryFunction, tehsil, district))
        conn.commit()
        cursor.close()
        conn.close()

        response = {'message': 'Success'}
        return jsonify(response), 200

    else:
        response = {'message': 'Invalid JSON data'}
        return jsonify(response), 400


@app.route('/district', methods=['GET', 'POST'])
def district():

    conn = db_connection()
    cursor = conn.cursor()

    if request.method == 'GET':
        # cursor.execute("SELECT * FROM r_district_data")
        query = "SELECT * FROM r_district_data WHERE id = '444' and district = 'Harda' order by tehsil, village asc;"
        cursor.execute(query)
        district = [
            dict(
                id=row['id'],
                village=row['village'],
                gram_panchayat=row['gram_panchayat'],
                tehsil=row['tehsil'],
                district=row['district'],
                state=row['state'],
                last_updated_at=row['last_updated_at'],
                pincode=row['pincode'],
                village_hindi=row['village_hindi'],
                tehsil_hindi=row['tehsil_hindi'],
                district_hindi=row['district_hindi'],
                state_hindi=row['state_hindi'],
            )

            for row in cursor.fetchall()
        ]

        if district is not None:
            return jsonify(district)


if __name__ == '__main__':
    app.run(debug=True)

