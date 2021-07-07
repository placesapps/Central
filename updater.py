from flask import Flask, redirect, url_for, render_template, request,session,flash
import sqlite3
import json
from datetime import datetime
from werkzeug.utils import append_slash_redirect
from hashing import Hashing
import random
import string
import base64
from passwordencryption import EncryptPass
from datetime import datetime
from datetime import timedelta
import time
from werkzeug.utils import secure_filename
from UnpackUpdate import Update
import os
brandinfo={}
year = datetime.now().strftime('%Y')
langname="zh-HK.langpck"
with open("branding"+os.sep+"branding.json") as file:
    brandinfo = json.load(file)
    productname = brandinfo["Vendor"]+" "+brandinfo["ProductName"]
    lc=brandinfo["License"]
    print(productname)
    file.close()
with open("lang"+os.sep+"zh-HK.json",encoding="utf-8") as file:
    lang = json.load(file)
    file.close()
with open(lc,encoding="utf-8") as file:
    license1=file.readlines()
    file.close()
app = Flask(__name__)
langname="zh-HK.langpck"
def langpack_rd():
    global productname
    with open(f"langpck"+os.sep+f"{langname}"+os.sep+"strings.sf.json","r", encoding='utf-8') as f:
        jl=json.loads(f.read())
        ovr=jl["overrideproductname"]
        if ovr == "1":
            productname=jl["0"]
langpack_rd()
def langpack(strcode):
    global langname
    with open(f"langpck"+os.sep+f"{langname}"+os.sep+"strings.sf.json","r", encoding='utf-8') as f:
        strings=json.loads(f.read())[str(strcode)]
    return strings
app.jinja_env.globals.update(strings=langpack)
@app.route('/',methods=['POST','GET'])
def stepui():
    if request.method=="POST":
        f = request.files['file']
        f.save(secure_filename("updates_"+f.filename))
        UD=Update()
        a=UD.update("updates_"+f.filename.replace(".cudp",""))
        return render_template("nano/complete.html",version=a)
    else:
        return render_template("nano/upload.html",productname=productname,year=year)
    
if __name__ == "__main__":
	app.run(port=8888, debug=True)