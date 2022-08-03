#!/root/.venvs/synology_download/bin/python
from synology_api import downloadstation
from typing import Union
from fastapi import FastAPI, Form
import os
from pydantic import BaseModel
from threading import Timer
import signal
from datetime import datetime
from dateutil import tz, zoneinfo


app = FastAPI()

# def create_task(self, uri, additional_param=None):
#     api_name = 'SYNO.DownloadStation.Task'
#     info = self.download_list[api_name]
#     api_path = info['path']
#     req_param = {'version': info['maxVersion'], 'method': 'create', 'uri': uri}

#     if type(additional_param) is dict:
#         for key in additional_param.keys():
#             req_param[key] = additional_param[key]

#     return self.request_data(api_name, api_path, req_param)
class Task(BaseModel):
    url: str

#global
dwn = downloadstation.DownloadStation('192.168.50.232', '48602', 'lemonhall', "xxxxx", secure=True, cert_verify=False, dsm_version=7, debug=True, otp_code=None)

#重新登陆的
def relogin():
    global dwn
    dwn = downloadstation.DownloadStation('192.168.50.232', '48602', 'lemonhall', "xxxxx", secure=True, cert_verify=False, dsm_version=7, debug=True, otp_code=None)
    return True

# target task function
def task(message):
    tz_sh = tz.gettz('Asia/Shanghai')
    # datetime object containing current date and time
    now = datetime.now(tz=tz_sh)
    # dd/mm/YY H:M:S
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
    print(dt_string+"  : "+message)
    relogin()

class RepeatTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)

timer = RepeatTimer(600, task,args=('I am refersh login auth',))
timer.start()

def handler(signum, frame):
    msg = "Ctrl-c was pressed"
    print(msg, end="", flush=True)
    timer.cancel()
    exit(1)

signal.signal(signal.SIGINT, handler)


#用来测试系统存活性的
@app.get("/")
def test():
    return "I am OK~~~"

#真正干活的一个包装器，创建任务，去除登陆的过程其实非常快
@app.post("/create_task")
async def create_task(task:Task):
    global dwn
    try:
        dwn.create_task(task.url)
        print("server rev url:"+task.url)
    except Exception as e:
        print(e)
        relogin()
        dwn.create_task(task.url)
    return "OK=====>:"+task.url

#uvicorn main:app --host ::