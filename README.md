This repository contains steps and key notes to develop and deploy a simple Fast API application on an EC2 instance<br>
The architecture of the application is as follows:<br>
![CC-Project1-Part1-Architecture](https://github.com/husainasad/Cloud-Computing-1-1/assets/32503674/ab43e9ce-1b40-4081-93dd-8d457e2b3af6)

## Step 1: Create Fast API application
Fast API is supported on python 3.8+ versions </br>
The application can either be run using uvicorn. Command:
```
uvicorn {server file name}:app --host 0.0.0.0 --port 8000 --reload --workers=k
```
--host parameter (optional): binds the application server with machine IP (especially useful for EC2) </br>
--port number: port to run the application on </br>
--reload (optional): useful for development purposes, behaves as an auto server start on code change </br>
--workers (optional): can specify number of workers for concurrency </br>

Another way is to use Gunicorn. Command:
```
gunicorn main:app --workers=10 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## Step 2: Test with Fast API doc
The created APIs can be tested on https://url:port/docs

## Steps 3: Test with Workload Generator
Workload Generator simulates a client side and sends requests to the server. The code matches the server responses and helps in verifying the correctness and speed of code logic. </br>
Command to test:
```
python ./Resources/workload_generator/workload_generator.py --num_request 100  --url http://127.0.0.1:8000/ --image_folder "./Resources/dataset/face_images_1000/"  --prediction_file "./Resources/dataset/Classification Results on Face Dataset (1000 images).csv"
```
More information on workload generator can be found in the associated readme.

## Create EC2 instance
The EC2 instance can be created automatically by running the 'createEC2.py' script. </br>

## Project setup in EC2
Setting up the project in EC2 involves updating existing packages, pulling project from GitHub, creating virtual environment, installing relevant libraries before running the server code. </br>
To make this process automatic, the setup commands are saved in the 'cc-startup-script' and passed to the EC2 creation script as user data. </br>

The startup script is explained in the next section.

## Start up Script for EC2 instance
By default, the user data is run as root user. However, in this project, we run the script as a non-root user since we eventually use the user data created folders and access them as a non-root user. </br>
Also, when connecting to the instance through ssh, we login as non-root user. </br>

The script can be divided into three parts:

### Initial Set Up
This section sets up the project folders and installs the required packages inside a virtual environment. </br>
At an initial stage, this is sufficient for user data. </br>

```
sudo apt-get update -y
sudo apt install python3.10-venv -y
python3 -m venv ccprojectenv
source ccprojectenv/bin/activate
sudo apt-get update -y
git clone -q https://github.com/husainasad/Cloud-Computing.git
pip install --upgrade pip
pip install --upgrade setuptools
pip install "fastapi[all]"
pip install pandas python-multipart
```

### Add sever running command to boot files
We want that the server runs even when the instance is rebooted for any reason. For this, we can add a script inside the ec2 boot files. </br>
```
echo "[Unit]
Description=My Uvicorn server
After=multi-user.target
StartLimitIntervalSec=0

[Service]
Type=simple
ExecStart=/home/ubuntu/ccprojectenv/bin/python -m uvicorn app:app --host 0.0.0.0 --port 8000
WorkingDirectory=/home/ubuntu/Cloud-Computing
User=ubuntu
Restart=always
RestartSec=1

[Install]
WantedBy=multi-user.target" | sudo tee /etc/systemd/system/uvicorn-server.service
```

### Save boot file and enable script
Once the script is added to the system files, we run and enable the files:
```
sudo chmod 644 /etc/systemd/system/uvicorn-server.service
sudo systemctl start uvicorn-server
sudo systemctl enable uvicorn-server
```
The details on the the boot file script can be found in 'reboot-script'

## Deployed Application
The 'createEC2' script creates an ec2 instance and runs the server automatically. </br>
Furthermore, since the command to run the server is added inside the boot files, the server will run automatically even after every bootup. </br>
This will save us an extra step to SSH into the instance and manually start the server and keep the process running. </br>
This way we are able to create a constantly running server without any need for manual server set up. </br>

We can test the API using either Fast API docs or running workload generator on a different machine. </br>
