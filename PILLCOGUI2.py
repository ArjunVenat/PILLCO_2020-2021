from tkinter import *
import mysql.connector
from flask import Flask, render_template
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
ControlPin = [7, 11, 13, 15]
for pin in ControlPin():
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 0)
seq = [
[1, 0, 0, 0],
[1, 1, 0, 0],
[0, 1, 0, 0],
[0, 1, 1, 0],
[0, 0, 1, 0],
[0, 0, 1, 1],
[0, 0, 0, 1],
[1, 0, 0, 1],
]

def rotate(n):
    intpart = int(n)/10
    remainderpart = n%10
    total = int(n*51.2)
    for i in range(total):
        for halfstep in range(8):
            for pin in range(4):
                GPIO.output(ControlPin[pin], seq[halfstep][pin])
            time.sleep(0.001)
    GPIO.cleanup()


security_code = 1237647
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


root = Tk()
screen1frame = LabelFrame(root)
screen2frame =  LabelFrame(root)
screen3frame = LabelFrame(root)
screen3andhalfframe =  LabelFrame(root)
screen4frame = LabelFrame(root)

screen1frame.pack()
screen2frame.pack()
screen3frame.pack()
screen3andhalfframe.pack()
screen4frame.pack()

counter = 0

def screen1buttonclick():
    global counter
    entered_code = int(screen1_textbox.get())
    screen1_textbox.delete(0, 'end')


    global screen1_wrongcode
    if(counter == 0):
        screen1_wrongcode = Label()

    #print(entered_code == security_code)
    if(entered_code == security_code):
        screen2()
    else:
        screen1_wrongcode.destroy()
        screen1_wrongcode = Label(screen1frame, text = "Incorrect Security Code, please enter the correct code")
        screen1_wrongcode.pack(side = RIGHT)
        counter += 1

def screen2():
    global screen2frame

    screen1frame.destroy()
    screen3frame.destroy()
    screen3andhalfframe.destroy()
    screen4frame.destroy()
    screen2frame.destroy()
    screen2frame = LabelFrame(root)
    screen2frame.pack()

    screen2_title = Label(screen2frame, text = "Would you like to")
    screen2_title.pack()
    screen2A = Label(screen2frame, text = "A) Dispense pills/Remove pills from Inventory")
    screen2B = Label(screen2frame, text = "B) Add pills through Inventory")
    screen2C = Label(screen2frame, text = "C) Assign a container to a new pill brand")
    screen2A.pack()
    screen2B.pack()
    screen2C.pack()

    screen2_buttonA = Button(screen2frame, text = "A", command = screen3)
    screen2_buttonB = Button(screen2frame, text = "B", command = screen3andhalf)
    screen2_buttonC = Button(screen2frame, text = "C", command = screen4)
    newline = Label(screen2frame, text = "\n\n")
    newline.pack()
    screen2_buttonA.pack(side = LEFT)
    screen2_buttonB.pack(side = LEFT)
    screen2_buttonC.pack(side = LEFT)

def screen3buttonclick():
    global my_cursor
    global AName, BName, ANum, BNum, numberA, numberB
    containerChoice3 = clicked3.get()

    if(int(screen3_numpillsbox.get())<0):
        screen2()
    my_cursor.execute("SELECT NUMBER_OF_PILLS FROM CONTAINERINFO WHERE CONTAINER_ID = 'A'")
    result = my_cursor.fetchall()
    for i in result:
        numberA = i[0]
    my_cursor.execute("SELECT NUMBER_OF_PILLS FROM CONTAINERINFO WHERE CONTAINER_ID = 'B'")
    result = my_cursor.fetchall()
    for i in result:
        numberB = i[0]

    if(containerChoice3 == 'A'):
        if(numberA-int(screen3_numpillsbox.get()) < 0):
            screen2()
    if(containerChoice3 == 'B'):
        if(numberB-int(screen3_numpillsbox.get()) < 0):
            screen2()

    numpills3 = int(screen3_numpillsbox.get())
    newnumpills = 0
    my_cursor.execute("SELECT NUMBER_OF_PILLS FROM CONTAINERINFO WHERE CONTAINER_ID = \'" + containerChoice3 + "\'")
    result = my_cursor.fetchall()
    for i in result:
        newnumpills = i[0]
    newnumpills = newnumpills - numpills3
    pillcoupdate = "UPDATE CONTAINERINFO SET NUMBER_OF_PILLS = " + str(newnumpills) + " WHERE CONTAINER_ID = \'" + containerChoice3 + "\'"
    my_cursor.execute(pillcoupdate)
    pillcodatabase.commit()

    my_cursor.execute("SELECT PILL_NAME FROM CONTAINERINFO WHERE CONTAINER_ID = 'A'")
    result = my_cursor.fetchall()
    for i in result:
        AName = i[0]
    my_cursor.execute("SELECT PILL_NAME FROM CONTAINERINFO WHERE CONTAINER_ID = 'B'")
    result = my_cursor.fetchall()
    for i in result:
        BName = i[0]
    my_cursor.execute("SELECT NUMBER_OF_PILLS FROM CONTAINERINFO WHERE CONTAINER_ID = 'A'")
    result = my_cursor.fetchall()
    for i in result:
        ANum = i[0]
    my_cursor.execute("SELECT NUMBER_OF_PILLS FROM CONTAINERINFO WHERE CONTAINER_ID = 'B'")
    result = my_cursor.fetchall()
    for i in result:
        BNum = i[0]
    #newnumpills = newnumpills-numpills3
    #pillcoupdate = "UPDATE CONTAINERINFO SET NUMBER_OF_PILLS = " + str(newnumpills) + " WHERE CONTAINER_ID = " + str(containerChoice3)
    #pillcodatabase.commit()
    #print("Dispensing " + str(numpills3) + " pills from " + containerChoice3)
    #dispensingmessage = Label(screen3frame, text = "Please place your container under the nozzle")
    #dispensingmessage.pack()
    #time.sleep(5)
    rotate(numpills3)
    screen2()

def screen3andhalfbuttonclick():
    global my_cursor
    if(int(screen3andhalf_numpillsbox.get())<0):
        screen2()

    containerChoice3andhalf = clicked3andhalf.get()
    numpills3andhalf = int(screen3andhalf_numpillsbox.get())
    newnumpills = 0
    my_cursor.execute("SELECT NUMBER_OF_PILLS FROM CONTAINERINFO WHERE CONTAINER_ID = \'" + containerChoice3andhalf + "\'")
    result = my_cursor.fetchall()
    for i in result:
        newnumpills = i[0]
    newnumpills = newnumpills + numpills3andhalf
    pillcoupdate = "UPDATE CONTAINERINFO SET NUMBER_OF_PILLS = " + str(newnumpills) + " WHERE CONTAINER_ID = \'" + containerChoice3andhalf + "\'"
    my_cursor.execute(pillcoupdate)
    pillcodatabase.commit()

    my_cursor.execute("SELECT PILL_NAME FROM CONTAINERINFO WHERE CONTAINER_ID = 'A'")
    result = my_cursor.fetchall()
    for i in result:
        AName = i[0]
    my_cursor.execute("SELECT PILL_NAME FROM CONTAINERINFO WHERE CONTAINER_ID = 'B'")
    result = my_cursor.fetchall()
    for i in result:
        BName = i[0]
    my_cursor.execute("SELECT NUMBER_OF_PILLS FROM CONTAINERINFO WHERE CONTAINER_ID = 'A'")
    result = my_cursor.fetchall()
    for i in result:
        ANum = i[0]
    my_cursor.execute("SELECT NUMBER_OF_PILLS FROM CONTAINERINFO WHERE CONTAINER_ID = 'B'")
    result = my_cursor.fetchall()
    for i in result:
        BNum = i[0]

    screen2()




def screen4buttonclick():
    if(int(screen4_numpillsbox.get())<0):
        screen2()
    containerChoice4 = clicked4.get()
    numpills4 = int(screen4_numpillsbox.get())
    brandname = screen4_brandname_box.get()
    pillcoupdate = "UPDATE CONTAINERINFO SET NUMBER_OF_PILLS = " + str(numpills4) + " WHERE CONTAINER_ID = \'" + containerChoice4 + "\'"
    my_cursor.execute(pillcoupdate)
    pillcoupdate = "UPDATE CONTAINERINFO SET PILL_NAME = \'" + brandname + "\' WHERE CONTAINER_ID = \'" + containerChoice4 + "\'"
    my_cursor.execute(pillcoupdate)
    pillcodatabase.commit()

    my_cursor.execute("SELECT PILL_NAME FROM CONTAINERINFO WHERE CONTAINER_ID = 'A'")
    result = my_cursor.fetchall()
    for i in result:
        AName = i[0]
    my_cursor.execute("SELECT PILL_NAME FROM CONTAINERINFO WHERE CONTAINER_ID = 'B'")
    result = my_cursor.fetchall()
    for i in result:
        BName = i[0]
    my_cursor.execute("SELECT NUMBER_OF_PILLS FROM CONTAINERINFO WHERE CONTAINER_ID = 'A'")
    result = my_cursor.fetchall()
    for i in result:
        ANum = i[0]
    my_cursor.execute("SELECT NUMBER_OF_PILLS FROM CONTAINERINFO WHERE CONTAINER_ID = 'B'")
    result = my_cursor.fetchall()
    for i in result:
        BNum = i[0]
    #dispensingmessage = Label(screen4frame, text = "Please place your container under the nozzle")
    #dispensingmessage.pack()
    #time.sleep(5)
    screen2()

def screen3():
    global screen3frame
    global screen3_numpillsbox
    screen2frame.destroy()
    screen3frame = LabelFrame(root)
    screen3frame.pack()

    screen3_button = Button(screen3frame, text = "<--", command = screen2)
    screen3_button.place(x = 0, y = 0)
    newline = Label(screen3frame, text = "\n")
    newline.pack()
    newline.pack()
    screen3_containers_message = Label(screen3frame, text = "Which Container?")
    screen3_containers_message.pack()

    global clicked3
    clicked3 = StringVar()
    clicked3.set("A")
    screen3_dropdown = OptionMenu (screen3frame, clicked3, "A", "B")
    screen3_dropdown.pack()
    newline.pack()
    screen3_numpillsmessage = Label(screen3frame, text = "How many pills would you like to dispense?")
    screen3_numpillsbox = Entry(screen3frame)
    screen3_numpillsmessage.pack()
    screen3_numpillsbox.pack()


    screen3_button = Button(screen3frame, text = "Done ✓", command = screen3buttonclick)
    screen3_button.pack()



def screen3andhalf():
    global screen3andhalfframe
    global screen3andhalf_numpillsbox
    screen2frame.destroy()
    screen3andhalfframe = LabelFrame(root)
    screen3andhalfframe.pack()

    screen3andhalf_button = Button(screen3andhalfframe, text = "<--", command = screen2)
    screen3andhalf_button.place(x = 0, y = 0)
    newline = Label(screen3andhalfframe, text = "\n")
    newline.pack()
    screen3andhalf_containers_message = Label(screen3andhalfframe, text = "Select A Container")
    screen3andhalf_containers_message.pack()

    global clicked3andhalf
    clicked3andhalf = StringVar()
    clicked3andhalf.set("A")
    screen3andhalf_dropdown = OptionMenu (screen3andhalfframe, clicked3andhalf, "A", "B")
    screen3andhalf_dropdown.pack()
    newline.pack()
    screen3andhalf_numpillsmessage = Label(screen3andhalfframe, text = "How many pills would you like to add?")
    screen3andhalf_numpillsbox = Entry(screen3andhalfframe)
    screen3andhalf_numpillsmessage.pack()
    screen3andhalf_numpillsbox.pack()


    screen3andhalf_button = Button(screen3andhalfframe, text = "Done ✓", command = screen3andhalfbuttonclick)
    screen3andhalf_button.pack()



def screen4():
    global screen4frame
    global screen4_numpillsbox
    global screen4_brandname_box
    screen2frame.destroy()
    screen4frame = LabelFrame(root)
    screen4frame.pack()

    screen4_button = Button(screen4frame, text = "<--", command = screen2)
    screen4_button.place(x = 0, y = 0)
    newline = Label(screen4frame, text = "\n")
    newline.pack()
    newline.pack()
    screen4_containers_message = Label(screen4frame, text = "Which Container?")
    screen4_containers_message.pack()

    global clicked4
    clicked4 = StringVar()
    clicked4.set("A")
    screen4_dropdown = OptionMenu (screen4frame, clicked4, "A", "B")
    screen4_dropdown.pack()
    newline.pack()

    screen4_brandname_message = Label(screen4frame, text = "What is the name of the new pill brand?")
    screen4_brandname_box = Entry(screen4frame)
    screen4_numpillsmessage = Label(screen4frame, text = "How many pills are being added to the selected container?")
    screen4_numpillsbox = Entry(screen4frame)

    screen4_brandname_message.pack()
    screen4_brandname_box.pack()
    screen4_numpillsmessage.pack()
    screen4_numpillsbox.pack()

    screen4_button = Button(screen4frame, text = "Done ✓", command = screen4buttonclick)
    screen4_button.pack()


screen1_title = Label(screen1frame, text = "Welcome to PILLCO")
screen1_sec_code_message = Label(screen1frame, text = "Please Enter your Security Code")
screen1_title.pack()
screen1_sec_code_message.pack()

screen1_textbox = Entry(screen1frame)
screen1_textbox.pack()
screen1_button = Button(screen1frame, text = "Done ✓", command = screen1buttonclick)
screen1_button.pack(side = LEFT)


root.mainloop()
