#!/usr/bin/python3
import os
import json
from flask import Flask,request,render_template
import time

app=Flask(__name__)


def dbGet(n):
    if os.path.exists("db/{}.txt".format(n)):
        with open("db/{}.txt".format(n),"r",encoding="UTF-8") as f:
            t=f.read()
            t=json.loads(t)
            return t
    else:
        with open("db/{}.txt".format(n),"w",encoding="UTF-8") as f:
            f.write("[]")
            return []

def dbWrite(n,t):
    with open("db/{}.txt".format(n),"w",encoding="UTF-8") as f:
        f.write(json.dumps(t))
        return t
        
@app.route("/api/do/doInOut/",methods={"POST"})
def doInOut():
    dict=json.loads(json.loads(request.data))
    users=dbGet("user")
    deviceDb=dbGet("device")
    op=dict['op']
    tp=dict['type']
    if not op in users:
        return json.dumps({"code":-1,"msg":"操作用户无效"})
    devicesToOp=dict['device']
    for t in devicesToOp:
        if tp=="back":
            thisdev=dbGet("devices/{}".format(t))
            thisdev.append({"time":time.time(),"from":deviceDb[t]['position'],"to":"仓库","op":op})
            dbWrite("devices/{}".format(t),thisdev)
            deviceDb[t]['stat']=1
            deviceDb[t]['position']='仓库'
        elif tp=="get":
            thisdev=dbGet("devices/{}".format(t))
            thisdev.append({"time":time.time(),"from":deviceDb[t]['position'],"to":op,"op":op})
            dbWrite("devices/{}".format(t),thisdev)
            deviceDb[t]['stat']=0
            deviceDb[t]['position']=op
        dbWrite("device",deviceDb)
    return json.dumps({"code":0})

@app.route("/api/get/statById/<deviceID>")
def returnStatByID(deviceID):
    db=dbGet("device")
    return db[int(deviceID)]
    
@app.route("/api/get/allDevice")
def returnAllDevice():
    db=dbGet("device")
    return json.dumps(db)
    
@app.route("/api/get/detailById/<id>")
def returnDetail(id):
    db=dbGet("devices/{}".format(id))
    return json.dumps(db)


# 页面部分
@app.route("/do/<deviceID>")
def handle_main(deviceID):
    return render_template("doAction.html",deviceID=deviceID)

@app.route("/stat/<deviceID>")
def detailPage(deviceID):
    return render_template("detail.html",deviceID=deviceID)
    
@app.route("/status/")
def mainx():
    return render_template("status.html")

if __name__=="__main__":
  app.run(host="0.0.0.0",port=1069,debug=False)
