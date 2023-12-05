from flask import Flask, request, render_template, redirect,send_from_directory,session,flash
import pandas as pd
import string
import os
import random
import mysql.connector
import numpy as np
from datetime import timedelta
import sys
from PIL import Image
import base64
import io
import re
import random
import secrets
from flask_mail import *
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

mydb = mysql.connector.connect(host="localhost", user="root", passwd="", port=3306, database="healthcare_sector")
cursor = mydb.cursor()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'the random string'
mail = Mail(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/doctor")
def doctor():
    a=random.randrange(10000, 999999)
    return render_template("doctor.html",a=a)

@app.route('/dlog', methods=['POST', 'GET'])
def dlog():
    if request.method == "POST":
        email = request.form['email']
        capt = request.form['capt']
        c1 = request.form['capt1']
        password1 = request.form['pwd']
        status = "Accepted"
        print(email, password1, status)
        sql = "SELECT * FROM doctor WHERE email=%s AND pwd=%s AND status=%s"
        values = (email, password1, status)
        cursor.execute(sql, values)
        results = cursor.fetchall()
        print(results)
        if capt == c1:
            if len(results) > 0:
                print('r')
                flash("Successfully Login to the Page", "primary")
                name = results[0][1]
                session['fname'] = name
                session['email'] = email
                return render_template('dhome.html', m="Login Success", msg=name)
            else:
                flash("Login Failure!!!", "primary")
                return render_template('doctor.html', msg="Login Failure!!!")
        else:
            return render_template('doctor.html', msg="Invalid value")
    return render_template('doctor.html')

@app.route("/admin",methods=['POST','GET'])
def admin():
    if request.method=='POST':
        email=request.form['email']
        Password=request.form["Password"]
        if email == 'admin@gmail.com' and Password == 'admin':
            session["email"]=email
            return render_template("adminhome.html",msg="success",email=email)
        else:
            return render_template("admin.html",msg="Failure")
    return render_template("admin.html")

@app.route("/viewdoctor")
def viewdoctor():
    print("Reading BLOB data from python_employee table")
    sql = "select * from doctor where status ='pending' "
    '''mycursor.execute(sql)
    x=mycursor.fetchall()'''
    x = pd.read_sql_query(sql, mydb)
    print(type(x))
    print(x)
    return render_template("viewdoctor.html", col_name=x.columns.values, row_val=x.values.tolist())

@app.route("/statusAccept/<id>")
def statusAccept(id):
    print(id)
    sql = "update doctor set status='Accepted' where id='%s'"%(id)
    cursor.execute(sql)
    mydb.commit()
    return redirect("/viewdoctor")

@app.route("/statusreject/<id>")
def statusreject(id):
    print(id)
    sql = "update doctor set status='Reject' where id='%s'"%(id)
    cursor.execute(sql)
    mydb.commit()
    return redirect("/viewdoctor")

@app.route("/viewpatient")
def viewpatient():
    print("Reading BLOB data from python_employee table")
    sql = "select * from patient where status ='pending' "
    '''mycursor.execute(sql)
    x=mycursor.fetchall()'''
    x = pd.read_sql_query(sql, mydb)
    print(type(x))
    print(x)
    x = x.drop(['pwd'], axis=1)
    return render_template("viewpatient.html", col_name=x.columns.values, row_val=x.values.tolist())

@app.route("/statuspAccept/<id>")
def statuspAccept(id):
    print(id)
    sql = "update patient set status='Accepted' where id='%s'"%(id)
    cursor.execute(sql)
    mydb.commit()
    return redirect("/viewpatient")

@app.route("/statuspreject/<id>")
def statuspreject(id):
    print(id)
    sql = "update patient set status='Reject' where id='%s'"%(id)
    cursor.execute(sql)
    mydb.commit()
    return redirect("/viewpatient")

@app.route("/dreg")
def dreg():
    return render_template("dreg.html")

@app.route('/dregback',methods=['POST','GET'])
def dregback():
    if request.method=='POST':
        fname=request.form['fname']
        lname=request.form['lname']
        email=request.form['email']
        role = request.form['role']
        pwd=request.form['pwd']
        addr=request.form['addr']
        cpwd=request.form['cpwd']
        ph=request.form['pno']
        area=request.form['area']
        sql="select * from doctor"
        result=pd.read_sql_query(sql,mydb)
        email1=result['email'].values
        print(email1)
        if email in email1:
            flash("email already existed","success")
            return render_template('dreg.html', msg="email existed")
        if(pwd==cpwd):
            sql = "INSERT INTO doctor (fname,lname,email,spe,pwd,area,addr,pno) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
            val = (fname,lname,email,role,pwd,area,addr,ph)
            cursor.execute(sql, val)
            mydb.commit()
            print("Successfully Registered")
            return render_template('dreg.html', msg="registered successfully")
        else:
            flash("Password and Confirm Password not same")
    return render_template('dreg.html',msg="somthing wrong")

@app.route("/dhome")
def dhome():
    return render_template("dhome.html")

@app.route("/feature")
def feature():
    sql = "select * from features"
    print(sql)
    x = pd.read_sql_query(sql, mydb)
    print(x)
    x = x.drop(['email'], axis=1)
    return render_template("feature.html", col_name=x.columns.values, row_val=x.values.tolist())

@app.route('/featureadd',methods=['POST','GET'])
def featureadd():
    if request.method=='POST':
        fname=request.form['fname']
        disp=request.form['disp']
        email = session.get('email')
        sql = "INSERT INTO features (email,fname,disp) VALUES (%s,%s,%s)"
        val = (email,fname,disp)
        cursor.execute(sql, val)
        mydb.commit()
        return render_template('feature.html')

@app.route("/update/<s1>/<s2>/<s3>")
def update(s1=0,s2='',s3=''):
    global n
    n = s1
    print(n)
    return render_template("update.html", n=n, s2=s2, s3=s3)

@app.route("/upback",methods=["POST","GET"])
def upback():
    if request.method=="POST":
        n = request.form['id']
        fname = request.form['fname']
        disp = request.form['disp']
    sql="update features set fname='%s' , disp='%s' where id='%s' " % (fname,disp,n)
    print(sql)
    cursor.execute(sql)
    mydb.commit()
    sql = "SELECT * from features where id='%s' " % (n)
    print(sql)
    result1 = pd.read_sql_query(sql, mydb)
    return render_template("feature.html")

@app.route("/delete/<s1>")
def delete(s1=0):
    print("delete items here")
    sql = "delete from features where id='"+s1+"' "
    '''mycursor.execute(sql)
    x=mycursor.fetchall()'''
    cursor.execute(sql)
    mydb.commit()
    '''print(type(x))
    print(x)
    x = x.drop(['photo'], axis=1)
    x["Delete"] = " "'''
    return render_template('delete.html', msg='item deleted successfully')

@app.route("/patient")
def patient():
    a=random.randrange(10000, 999999)
    return render_template("patient.html",a=a)

@app.route('/plog', methods=['POST', 'GET'])
def plog():
    if request.method == "POST":
        capt = request.form['capt']
        c1 = request.form['capt1']
        email = request.form['email']
        password1 = request.form['pwd']
        status = "Accepted"
        sql = "SELECT * FROM patient WHERE email=%s AND pwd=%s AND status=%s"
        values = (email, password1, status)
        cursor.execute(sql, values)
        results = cursor.fetchall()
        if capt == c1:
            if len(results) > 0:
                session['fname'] = results[0][1]
                session['email'] = email
                flash("Successfully Login to the Page", "primary")
                return render_template('phome.html', m="Login Success", msg=results[0][1])
            else:
                return render_template('patient.html', msg="Login Failure!!!")
        else:
            return render_template('patient.html', msg="Invalid value")
    return render_template('patient.html')

@app.route("/preg")
def preg():
    return render_template("preg.html")

@app.route('/pregback',methods=['POST','GET'])
def pregback():
    print("gekjhiuth")
    if request.method=='POST':
        print("gekjhiuth")
        fname=request.form['fname']
        lname=request.form['lname']
        email=request.form['email']
        pwd=request.form['pwd']
        addr=request.form['addr']
        cpwd=request.form['cpwd']
        ph=request.form['pno']
        print(ph)
        sql="select * from patient"
        result=pd.read_sql_query(sql,mydb)
        email1=result['email'].values
        print(email1)
        if email in email1:
            flash("email already existed","success")
            return render_template('preg.html', msg="email existed")
        if(pwd==cpwd):
            sql = "INSERT INTO patient(fname,lname,email,pwd,addr,pno) VALUES (%s,%s,%s,%s,%s,%s)"
            val = (fname,lname,email,pwd,addr,ph)
            cursor.execute(sql, val)
            mydb.commit()
            print("Successfully Registered")
            return render_template('preg.html', msg="registered successfully")
        else:
            flash("Password and Confirm Password not same")
    return render_template('preg.html',msg="somthing wrong")

@app.route("/vd")
def vd():
    print("Reading BLOB data from python_employee table")
    sql = "select * from doctor where status ='Accepted'  "
    '''mycursor.execute(sql)
    x=mycursor.fetchall()'''
    x = pd.read_sql_query(sql, mydb)
    print(type(x))
    print(x)
    x = x.drop(['pwd'], axis=1)
    x = x.drop(['id'], axis=1)
    x = x.drop(['lname'], axis=1)
    return render_template("vd.html", col_name=x.columns.values, row_val=x.values.tolist())

@app.route("/vd1/<s1>/<s2>")
def vd1(s1='',s2=''):
    global s
    s=s1
    sql = "select * from  features where email='%s'" % (s)
    x = pd.read_sql_query(sql, mydb)
    global n
    n = s2
    print(n)
    x = x.drop(['id'], axis=1)
    x = x.drop(['email'], axis=1)
    return render_template("vd1.html",n=n, col_name=x.columns.values, row_val=x.values.tolist())

@app.route("/vd2/<s1>/<s2>")
def vd2(s1='',s2=''):
    email = session.get('email')
    fname = session.get('fname')
    return render_template("vd2.html", s1=s1, s2=s2,e=email,n=fname)

@app.route('/vd2back',methods=['POST','GET'])
def vd2back():
    print("gekjhiuth")
    if request.method=='POST':
        print("gekjhiuth")
        dname=request.form['dname']
        pname=request.form['pname']
        demail=request.form['demail']
        pemail=request.form['pemail']
        sym=request.form['sym']
        date=request.form['date']
        sql = "INSERT INTO book_slot(dname,demail,pname,pemail,sym,date) VALUES (%s,%s,%s,%s,%s,%s)"
        val = (dname,demail,pname,pemail,sym,date)
        cursor.execute(sql, val)
        mydb.commit()
        return render_template('vd.html', msg="slot booking")
    return render_template('vd2.html',msg="somthing wrong")

@app.route("/appoint")
def appoint():
    print("Reading BLOB data from python_employee table")
    email = session.get('email')
    sql = "select * from book_slot where demail='%s' "%(email)
    x = pd.read_sql_query(sql, mydb)
    print(type(x))
    print(x)
    x = x.drop(['dname'], axis=1)
    x = x.drop(['demail'], axis=1)
    return render_template("appoint.html", col_name=x.columns.values, row_val=x.values.tolist())

@app.route("/sendreport/<s1>/<s2>/<s3>/<s4>/<s5>")
def sendreport(s1=0,s2='',s3='',s4='',s5=''):
    global s
    s=s1
    email = session.get('email')
    fname = session.get('fname')
    return render_template("sendreport.html",s=s,s2=s2,s3=s3,s4=s4,s5=s5,e=email,f=fname)

@app.route("/sendback",methods=["POST","GET"])
def sendback():
    if request.method=="POST":
        n = request.form['id']
        print(n)
        report = request.form['report']
        disp = request.form['disp']
        pname = request.form['pname']
        pemail = request.form['pemail']
        sym = request.form['sym']
        date = request.form['date']
        demail = request.form['demail']
        dname = request.form['dname']
        otp = random.randint(000000, 999999)
        skey = secrets.token_hex(4)
        k1=str(skey)
        print(type(k1))
        print("b")
        dd = "text file/" + report
        f = open(dd, "r")
        data = f.read()
        status="Uploaded"
        action="Close"
        sql1="update book_slot set status='Uploaded' where id='%s'"%(n)
        cursor.execute(sql1)
        mydb.commit()
        sql="INSERT INTO report(rid,pname,pemail,dname,demail,sym,disp,report,date,status,action,pkey) VALUES (%s,%s,%s,%s,%s,%s,%s,AES_ENCRYPT(%s,'lakshmi'),%s,%s,%s,%s)"
        val = (n,pname,pemail, dname,demail,sym,disp, data, date,status,action,k1)
        cursor.execute(sql, val)
        mydb.commit()
        m = "Your secret key is:"
        mail_content = m + ' ' + k1
        sender_address = 'saketh132002@gmail.com'
        sender_pass = 'avjjedkkqubxhohr'
        receiver_address = pemail
        message = MIMEMultipart()
        message['From'] = pemail
        message['To'] = receiver_address
        message['Subject'] = 'PLEASE FIND THE SECURITY KEY TO ACCESS PATIENT MEDICAL REPORTS'
        message.attach(MIMEText(mail_content, 'plain'))
        session = smtplib.SMTP('smtp.gmail.com', 587)
        session.starttls()
        session.login(sender_address, sender_pass)
        text = message.as_string()
        session.sendmail(sender_address, receiver_address, text)
        session.quit()
        return render_template("appoint.html", msg="sended report")

@app.route("/send/<s1>/<s2>/<s3>/<s4>/<s5>/<s6>/<s7>/<s8>/<s9>")
def send(s1=0,s2='',s3='',s4='',s5='',s6='',s7='',s8='',s9=''):
    global s
    s=s1
    m = "Your secret key is:"
    mail_content = m + ' ' + s9
    sender_address = 'saketh132002@gmail.com'
    sender_pass = 'avjjedkkqubxhohr'
    receiver_address = s3
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'PLEASE FIND THE SECURITY KEY TO ACCESS PATIENT MEDICAL REPORTS'
    message.attach(MIMEText(mail_content, 'plain'))
    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.starttls()
    session.login(sender_address, sender_pass)
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    
    sql1="update report set status='Complated' where status='Uploaded'"
    cursor.execute(sql1)
    mydb.commit()
    return redirect("/viewreport")

@app.route("/report")
def report():
    print("Reading BLOB data from python_employee table")
    email = session.get('email')
    sql = "select * from report where demail='%s' "%(email)
    x = pd.read_sql_query(sql, mydb)
    print(type(x))
    print(x)
    x = x.drop(['dname'], axis=1)
    x = x.drop(['demail'], axis=1)
    x = x.drop(['rid'], axis=1)
    x = x.drop(['report'], axis=1)
    x = x.drop(['pkey'], axis=1)
    return render_template("report.html", col_name=x.columns.values, row_val=x.values.tolist())

@app.route("/download/<s1>")
def download(s1=0):
    global p
    p=s1
    sql = "select count(*),AES_DECRYPT(report,'lakshmi') from report where id='"+p+"'"
    x = pd.read_sql_query(sql, mydb)
    count=x.values[0][0]
    print(count)
    asss=x.values[0][1]
    print(asss)
    if count==1:
        return render_template("hdfs.html", msg=asss)
    return render_template("report.html")

@app.route("/schedule")
def schedule():
    print("Reading BLOB data from python_employee table")
    email = session.get('email')
    sql = "select * from book_slot where pemail='%s' "%(email)
    x = pd.read_sql_query(sql, mydb)
    print(type(x))
    print(x)
    x = x.drop(['pname'], axis=1)
    x = x.drop(['pemail'], axis=1)
    x = x.drop(['id'], axis=1)
    return render_template("schedule.html", col_name=x.columns.values, row_val=x.values.tolist())

@app.route("/viewreport")
def viewreport():
    print("Reading BLOB data from python_employee table")
    email = session.get('email')
    sql = "select * from report"
    x = pd.read_sql_query(sql, mydb)
    print(type(x))
    print(x)
    x = x.drop(['action'], axis=1)
    x = x.drop(['rid'], axis=1)
    x = x.drop(['report'], axis=1)
    x = x.drop(['disp'], axis=1)
    return render_template("viewreport.html", col_name=x.columns.values, row_val=x.values.tolist())

@app.route("/re")
def re():
    print("Reading BLOB data from python_employee table")
    email = session.get('email')
    sql = "select * from report where pemail='%s' "%(email)
    x = pd.read_sql_query(sql, mydb)
    print(type(x))
    print(x)
    x = x.drop(['pname'], axis=1)
    x = x.drop(['pemail'], axis=1)
    x = x.drop(['rid'], axis=1)
    x = x.drop(['report'], axis=1)
    x = x.drop(['pkey'], axis=1)
    return render_template("re.html", col_name=x.columns.values, row_val=x.values.tolist())

@app.route("/filedown/<s1>")
def filedown(s1=0):
    global s
    s=s1
    return render_template("filedown.html",s=s)

@app.route("/filedownload",methods=["POST","GET"])
def filedownload():
    if request.method == "POST":
        n = request.form['id']
        print(n)
        pkey = request.form['pkey']
    sql = "select count(*),aes_decrypt(report,'lakshmi') from report where id='" + n + "' and pkey='" + pkey + "'"
    x = pd.read_sql_query(sql, mydb)
    count = x.values[0][0]
    print(count)
    asss = x.values[0][1]
    if count == 0:
        msg = "Enter valid key"
        return render_template("filedown.html", msg="invalid")
    if count == 1:
        return render_template("h1.html", msg=asss)
    return render_template("filedown.html")

if __name__ == "__main__":
    app.run(debug=True)