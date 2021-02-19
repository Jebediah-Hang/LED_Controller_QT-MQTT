import paho.mqtt.client as mqtt
import wiringpi
import tkinter
import time

ledR = 24
ledG = 25
ledB = 27
key1 = 22
key2 = 21
key3 = 7
selection = 1
ledRv = 0
ledGv = 0
ledBv = 0

wiringpi.wiringPiSetup()
wiringpi.pinMode(key1, wiringpi.GPIO.INPUT)
wiringpi.pullUpDnControl(key1, wiringpi.GPIO.PUD_UP)
wiringpi.pinMode(key2, wiringpi.GPIO.INPUT)
wiringpi.pullUpDnControl(key1, wiringpi.GPIO.PUD_UP)
wiringpi.pinMode(key3, wiringpi.GPIO.INPUT)
wiringpi.pullUpDnControl(key1, wiringpi.GPIO.PUD_UP)

wiringpi.softPwmCreate(ledR, 0, 100)
wiringpi.softPwmCreate(ledG, 0, 100)
wiringpi.softPwmCreate(ledB, 0, 100)

top = tkinter.Tk()
top.title("Demo")
top.geometry('700x400')
textSl = tkinter.StringVar()
textRv = tkinter.StringVar()
textGv = tkinter.StringVar()
textBv = tkinter.StringVar()
textLog = tkinter.StringVar()

def logwrite(op):
    newinst = time.strftime("%Y-%m-%d,%H:%M:%S,", time.localtime()) + op + "\n"
    fo = open("log.txt", "r+")
    odf = fo.read()
    newtext = newinst + odf
    fo.seek(0)
    fo.write(newtext)
    fo.close()

def localcontral():
    global selection
    global ledRv
    global ledGv
    global ledBv
    k1s = wiringpi.digitalRead(key1)
    k2s = wiringpi.digitalRead(key2)
    k3s = wiringpi.digitalRead(key3)
    
    if k1s==0:
        if selection==1:
            if ledRv==100:
                ledRv = 0
            else:
                ledRv += 1
            client.publish("ctrlpub", payload="Ra", qos=0)
            logwrite("Key,Red+")
        if selection==2:
            if ledGv==100:
                ledGv = 0
            else:
                ledGv += 1
            client.publish("ctrlpub", payload="Ga", qos=0)
            logwrite("Key,Green+")
        if selection==3:
            if ledBv==100:
                ledBv = 0
            else:
                ledBv += 1
            client.publish("ctrlpub", payload="Ba", qos=0)
            logwrite("Key,Blue+")
        wiringpi.delay(50)
        textGv.set(ledGv)
        textBv.set(ledBv)
        textRv.set(ledRv)
        wiringpi.softPwmWrite(ledR, ledRv)
        wiringpi.softPwmWrite(ledG, ledGv)
        wiringpi.softPwmWrite(ledB, ledBv)
    if k2s==0:
        if selection==1:
            if ledRv==0:
                ledRv = 100
            else:
                ledRv -= 1
            client.publish("ctrlpub", payload="Rd", qos=0)
            logwrite("Key,Red-")
        if selection==2:
            if ledGv==0:
                ledGv = 100
            else:
                ledGv -= 1
            client.publish("ctrlpub", payload="Gd", qos=0)
            logwrite("Key,Green-")
        if selection==3:
            if ledBv==0:
                ledBv = 100
            else:
                ledBv -= 1
            client.publish("ctrlpub", payload="Bd", qos=0)
            logwrite("Key,Blue-")
        wiringpi.delay(50)
        textGv.set(ledGv)
        textBv.set(ledBv)
        textRv.set(ledRv)
        wiringpi.softPwmWrite(ledR, ledRv)
        wiringpi.softPwmWrite(ledG, ledGv)
        wiringpi.softPwmWrite(ledB, ledBv)
    if k3s==0:
        if selection==3:
            selection = 1
        else:
            selection += 1
        wiringpi.delay(200)
        textSl.set(selection)
    top.after(100, localcontral)

def btncRa():
    global ledRv
    if ledRv==100:
        ledRv = 0
    else:
        ledRv += 1
    textRv.set(ledRv)
    client.publish("ctrlpub", payload="Ra", qos=0)
    logwrite("Local,Red+")
    wiringpi.softPwmWrite(ledR, ledRv)

def btncRd():
    global ledRv
    if ledRv==0:
        ledRv = 100
    else:
        ledRv -= 1
    textRv.set(ledRv)
    client.publish("ctrlpub", payload="Rd", qos=0)
    logwrite("Local,Red-")
    wiringpi.softPwmWrite(ledR, ledRv)

def btncGa():
    global ledGv
    if ledGv==100:
        ledGv = 0
    else:
        ledGv += 1
    textGv.set(ledGv)
    client.publish("ctrlpub", payload="Ga", qos=0)
    logwrite("Local,Green+")
    wiringpi.softPwmWrite(ledG, ledGv)

def btncGd():
    global ledGv
    if ledGv==0:
        ledGv = 100
    else:
        ledGv -= 1
    textGv.set(ledGv)
    client.publish("ctrlpub", payload="Gd", qos=0)
    logwrite("Local,Green-")
    wiringpi.softPwmWrite(ledG, ledGv)

def btncBa():
    global ledBv
    if ledBv==100:
        ledBv = 0
    else:
        ledBv += 1
    textBv.set(ledBv)
    client.publish("ctrlpub", payload="Ba", qos=0)
    logwrite("Local,Blue+")
    wiringpi.softPwmWrite(ledB, ledBv)

def btncBd():
    global ledBv
    if ledBv==0:
        ledBv = 100
    else:
        ledBv -= 1
    textBv.set(ledBv)
    client.publish("ctrlpub", payload="Bd", qos=0)
    logwrite("Local,Blue-")
    wiringpi.softPwmWrite(ledB, ledBv)

def btncLog():
    fo = open("log.txt", "r+")
    log = fo.readline()
    textLog.set(log)
    fo.close()

def on_connect(client, userdata, flags, rc):
    client.subscribe("ctrlsub")

def on_message(client, userdata, msg):
    rec = str(msg.payload)[2:4]
    global ledRv
    global ledGv
    global ledBv
    if rec=="Ra":
        if ledRv==100:
            ledRv = 0
        else:
            ledRv += 1
        textRv.set(ledRv)
        logwrite("Server,Red+")
        wiringpi.softPwmWrite(ledR, ledRv)
    elif rec=="Rd":
        if ledRv==0:
            ledRv = 100
        else:
            ledRv -= 1
        textRv.set(ledRv)
        logwrite("Server,Red-")
        wiringpi.softPwmWrite(ledR, ledRv)
    elif rec=="Ga":
        if ledGv==100:
            ledGv = 0
        else:
            ledGv += 1
        textGv.set(ledGv)
        logwrite("Server,Green+")
        wiringpi.softPwmWrite(ledG, ledGv)
    elif rec=="Gd":
        if ledGv==0:
            ledGv = 100
        else:
            ledGv -= 1
        textGv.set(ledGv)
        logwrite("Server,Green-")
        wiringpi.softPwmWrite(ledG, ledGv)
    elif rec=="Ba":
        if ledBv==100:
            ledBv = 0
        else:
            ledBv += 1
        textBv.set(ledBv)
        logwrite("Server,Blue+")
        wiringpi.softPwmWrite(ledB, ledBv)
    elif rec=="Bd":
        if ledBv==0:
            ledBv = 100
        else:
            ledBv -= 1
        textBv.set(ledBv)
        logwrite("Server,Blue-")
        wiringpi.softPwmWrite(ledB, ledBv)
    else:
        wiringpi.softPwmWrite(ledR, ledRv)
        wiringpi.softPwmWrite(ledG, ledGv)
        wiringpi.softPwmWrite(ledB, ledBv)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

labS = tkinter.Label(top, text="Selection")
labR = tkinter.Label(top, text="Red")
labG = tkinter.Label(top, text="Green")
labB = tkinter.Label(top, text="Blue")
labSl = tkinter.Label(top, textvariable=textSl)
labRv = tkinter.Label(top, textvariable=textRv)
labGv = tkinter.Label(top, textvariable=textGv)
labBv = tkinter.Label(top, textvariable=textBv)
labLog = tkinter.Label(top, textvariable=textLog)
btnRa = tkinter.Button(top, height=1, width=2, text='+', command=btncRa)
btnRd = tkinter.Button(top, height=1, width=2, text='-', command=btncRd)
btnGa = tkinter.Button(top, height=1, width=2, text='+', command=btncGa)
btnGd = tkinter.Button(top, height=1, width=2, text='-', command=btncGd)
btnBa = tkinter.Button(top, height=1, width=2, text='+', command=btncBa)
btnBd = tkinter.Button(top, height=1, width=2, text='-', command=btncBd)
btnLog = tkinter.Button(top, height=1, width=2, text='Log', command=btncLog)
textSl.set(selection)
textGv.set(ledGv)
textBv.set(ledBv)
textRv.set(ledRv)
textLog.set("")

labS.place(x=50,y=50)
labR.place(x=50,y=100)
labG.place(x=50,y=150)
labB.place(x=50,y=200)
labSl.place(x=200,y=50)

btnRd.place(x=140,y=95)
labRv.place(x=200,y=100)
btnRa.place(x=230,y=95)

btnGd.place(x=140,y=145)
labGv.place(x=200,y=150)
btnGa.place(x=230,y=145)

btnBd.place(x=140,y=195)
labBv.place(x=200,y=200)
btnBa.place(x=230,y=195)

labLog.place(x=100,y=300)
btnLog.place(x=50,y=300)

client.connect("49.232.128.246", 1883, 60)
client.loop_start()

top.after(100, localcontral)
top.mainloop()

