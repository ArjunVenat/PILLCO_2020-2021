from flask import Flask, render_template
import mysql.connector

pillcodatabase = mysql.connector.connect(host = "localhost", user = "pillcouser", passwd = "pillco", database = "PILLCO")
my_cursor = pillcodatabase.cursor()

sqlstuff = "INSERT INTO CONTAINERINFO(Container_ID, PILL_NAME, NUMBER_OF_PILLS) VALUES(%s, %s, %s)"


app = Flask(__name__)

@app.route("/")
def sendinfo():
    my_cursor.execute("SELECT PILL_NAME FROM CONTAINERINFO WHERE CONTAINER_ID = 'A'")
    result = my_cursor.fetchall()
    for i in result:
        nameA = i[0]
    my_cursor.execute("SELECT PILL_NAME FROM CONTAINERINFO WHERE CONTAINER_ID = 'B'")
    result = my_cursor.fetchall()
    for i in result:
        nameB = i[0]
    my_cursor.execute("SELECT NUMBER_OF_PILLS FROM CONTAINERINFO WHERE CONTAINER_ID = 'A'")
    result = my_cursor.fetchall()
    for i in result:
        numA = i[0]
    my_cursor.execute("SELECT NUMBER_OF_PILLS FROM CONTAINERINFO WHERE CONTAINER_ID = 'B'")
    result = my_cursor.fetchall()
    for i in result:
        numB = i[0]

    return render_template('main.html', nameA = nameA, nameB = nameB, numA = numA, numB = numB)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5017, debug=True)
