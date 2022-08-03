
1. 新开一个环境
conda create --name synology_download python=3.8 --channel https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/

2. 激活它
conda activate synology_download

3. 安装依赖

pip3 install synology-api

https://github.com/N4S4/synology-api

pip install fastapi
pip install "uvicorn[standard]"
pip install python-multipart
pip3 install python-dateutil

官方地址

	from synology_api import downloadstation

	# Initiate the classes DownloadStation & FileStation with (ip_address, port, username, password)
	# it will log in automatically 

	dwn = downloadstation.DownloadStation('192.168.50.232', '15001', 'lemonhall', 'xxxxx', secure=False, cert_verify=False, dsm_version=7, debug=True, otp_code=None)

	dwn.get_info()

4. 开始制作镜像

	sudo docker run -it lemonhall/xdp_demo bash

	dnf update

	mkdir ~/.venvs
	mkdir ~/.venvs/synology_download

	python3 -m venv ~/.venvs/synology_download
	source ~/.venvs/synology_download/bin/activate

	mkdir synology_download
	cd mkdir synology_download

	/root/.venvs/synology_download/bin/python3 -m pip install --upgrade pip

	pip3 install synology-api
	pip install fastapi
	pip install "uvicorn[standard]"
	pip install python-multipart
	pip3 install python-dateutil

太慢了

	pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

配置清华源

参考它的写法：

	docker run --rm -v `pwd`:/project mingc/android-build-box bash -c 'cd /project; ./gradlew build'

启动就是干三件事：

	cd /root/synology_download;
	source ~/.venvs/synology_download/bin/activate;
	uvicorn main:app --host 0.0.0.0

这只监听的是v4

	uvicorn main:app --host ::

脚本头部记得
#!/root/.venvs/synology_download/bin/python


### 试试

	sudo docker ps

	sudo docker commit -m "synology_downloader" -a "lemonhall" 029417ababbd lemonhall/synology_downloader

	sudo docker push lemonhall/synology_downloader

	sudo docker run -it lemonhall/synology_downloader bash


### 看了一眼ipv6的地址
	240e:3b4:303c:d970:3948:f89e:1892:19a1
	http://[240e:3b4:303c:d970:1000:242:ac10:c803]:8000/
	240e:3b4:303c:d970:1000:242:ac10:c803


ok，这样就可以了


### 启动
	sudo docker start synology_downloader bash -c 'cd /root/synology_download;source ~/.venvs/synology_download/bin/activate;uvicorn main:app --host ::'


### 关于传参
	application/json

	{"url":"magnet:?xxxxx"}

修改了一下源码：

	class Task(BaseModel):
	    url: str

	@app.post("/create_task")
	async def create_task(task:Task):
	    dwn = downloadstation.DownloadStation()
	    dwn.create_task(task.url)
	    print("server rev url:"+task.url)
	    return "OK=====>:"+task.url

FastAPI可以帮你自动解析

### 最终的启动参数，记得要重命名一下这个容器哈

	docker run -d lemonhall/synology_downloader bash -c 'cd /root/synology_download;source ~/.venvs/synology_download/bin/activate;uvicorn main:app --host ::'


性能问题
=======

运行后发现request非常慢

后来明白了，耗时的主要是loging过程

	class RepeatTimer(Timer):
	    def run(self):
	        while not self.finished.wait(self.interval):
	            self.function(*self.args, **self.kwargs)

	timer = RepeatTimer(60, task,args=('I am refersh login auth',))
	timer.start()

所以做了定时器来refresh login的凭据

	#global
	dwn = downloadstation.DownloadStation(）

	#重新登陆的
	def relogin():
	    global dwn

全局缓存这个操作句柄，定时更新

写插件开始
========

https://stackoverflow.com/questions/42800590/tampermonkey-right-click-menu


时区问题
======
	from datetime import datetime
	from dateutil import tz, zoneinfo

    tz_sh = tz.gettz('Asia/Shanghai')
    # datetime object containing current date and time
    now = datetime.now(tz=tz_sh)
    # dd/mm/YY H:M:S
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
    print(dt_string+"  : "+message)

启动参数
======

	'bash' '-c' 'cd /root/synology_download;source ~/.venvs/synology_download/bin/activate;uvicorn main:app --host ::'



