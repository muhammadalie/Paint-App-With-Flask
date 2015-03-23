#!flask/bin/python
import sqlite3
from flask import Flask
app= Flask(__name__)
app.config.from_object('config')
from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.wtf import Form
import requests
import json
from flask import jsonify

@app.route('/', methods=['GET', 'POST'])
def home():
	try:
               c=sqlite3.connect('java.db')
               c.execute('CREATE TABLE PAINT(ID INTEGER PRIMARY KEY,NAME TEXT,COL BLOB,P1X BLOB,P1Y BLOB,P2X BLOB,P2Y BLOB);');

               c.commit()
               c.close()

        except:
               None
        try:
               c=sqlite3.connect('java.db')
               c.execute('CREATE TABLE REC(ID INTEGER PRIMARY KEY,NAME TEXT,COL BLOB,PX BLOB,PY BLOB,WIDTH BLOB,HEIGHT BLOB);');

               c.commit()
               c.close()
        except:
               None
        try:
               c=sqlite3.connect('java.db')
               c.execute('CREATE TABLE CIRC(ID INTEGER PRIMARY KEY,NAME TEXT,COL BLOB,PX BLOB,PY BLOB,RADIUS BLOB);');
               c.commit()
               c.close()
        except:
               None

	return render_template('test.html')

@app.route('/name')
def name():
    name = request.args.get('a')
    a=[]
    c=sqlite3.connect('java.db');
    rec=c.execute('SELECT * FROM REC WHERE NAME=?',[name]);
    for i in rec:
        a.append(i[1])

    cir=c.execute('SELECT * FROM CIRC WHERE NAME=?',[name]);
    for i in cir:
        a.append(i[1])

    pai=c.execute('SELECT * FROM PAINT WHERE NAME=?',[name]);
    for i in pai:
       a.append(i[1])


    c.commit()
    c.close()
    print a
    return jsonify(ln=len(a))


@app.route('/add')
def add_numbers():
    name = request.args.get('a')
    rectangle=[]
    circle=[]
    paint=[]
    
    c=sqlite3.connect('java.db');
    rec=c.execute('SELECT * FROM REC WHERE NAME=?',[name]);
    for i in rec:
        rectangle.append({"c":i[2],"p1":i[3],"p2":i[4],"w":i[5],"h":i[6]})

    cir=c.execute('SELECT * FROM CIRC WHERE NAME=?',[name]);
    for i in cir:
        circle.append({"c":i[2],"p1":i[3],"p2":i[4],"r":i[5]})

    pai=c.execute('SELECT * FROM PAINT WHERE NAME=?',[name]);
    for i in pai:
       paint.append({"c":i[2],"p1":i[3],"p2":i[4],"p3":i[5],"p4":i[6]})


    c.commit()
    c.close()
    return jsonify(p1=rectangle,p2=circle,p3=paint)



@app.route('/translate', methods=['GET', 'POST'])
def translate():
    names=[]	
    if request.method == 'POST':
               
  	name=request.json['name']
	data=request.json['data']

	mod= data['type']
	if(mod=="rect"):
  		point = data['p']
  		width = data['width']
		height = data['height']
		color=data['c']  
		c=sqlite3.connect('java.db');
		c.execute('INSERT INTO REC (NAME,COL,PX,PY,WIDTH,HEIGHT) VALUES(?,?,?,?,?,?)',[name,color,point[0],point[1],width,height]);
		c.commit()
		c.close()
	if(mod=="circ"):
                point = data['p']
                radius = data['radius']
		color=data['c']
                c=sqlite3.connect('java.db');
                c.execute('INSERT INTO CIRC (NAME,COL,PX,PY,RADIUS) VALUES(?,?,?,?,?)',[name,color,point[0],point[1],radius]);
                c.commit()
                c.close()
        if(mod=="paint"):
                p1 = data['p1']
                p2 = data['p2']
		color=data['c']
                c=sqlite3.connect('java.db');
                c.execute('INSERT INTO PAINT (NAME,COL,P1X,P1Y,P2X,P2Y) VALUES(?,?,?,?,?,?)',[name,color,p1[0],p1[1],p2[0],p2[1]]);
                c.commit()
                c.close()


	
app.run(debug=True)

