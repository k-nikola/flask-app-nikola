# Interstellar vacation booking app 🌌🚀👩‍🚀
![Bootstrap](https://img.shields.io/badge/bootstrap-%23563D7C.svg?style=for-the-badge&logo=bootstrap&logoColor=white) ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)  ![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white) ![Kubernetes](https://img.shields.io/badge/kubernetes-%23326ce5.svg?style=for-the-badge&logo=kubernetes&logoColor=white) 

This app frontend uses bootstrap 5.0.2. Backend uses Flask framework.
The basic prerequisite to running this app is having pythong 3.9.2 installed.
```
└─$ python --version     
Python 3.9.2
```
All the required packages are listed in the requirements.txt file in this repo, and can be installed in your virtual environment with pip.
```
pip3 install -r .\requirements.txt
```
This app needs a secret key and a database, in which it can store information about users and reservations. These two are referenced with the environment variables of the operating system the app runs on.
```
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('db_uri')
app.config["SECRET_KEY"] = os.getenv('secret_key')
```
The database URI and secret key need to be stored in env variables that have the same names as the arguments passed in the getenv method above. After setting the envinronment variables, app can be run with:
```
python run.py
```
The Dockerfile inside this repo can also be used to create a docker image with all the prerequisites needed to run the app. It is important to pass the database uri and secret key through environment variables inside the container created from that image.

This Dockerfile is used to create docker images and push them to a public repository every time a change has been made in the code. Main.yml file inside the github workflows folder contains the steps that make this possible, with GitHub Actions. Those docker images can later be used inside the pods of a kubernetes cluster. All of the files inside the webapp-deployment folder can be used to spin up a local kubernetes cluster, such as minikube and test this out.
```
└─$ minikube version                                 
minikube version: v1.19.0
```
All of the files can be applied with the command:
```
kubectl apply -f ./webapp-deployment
```
Every container inside the pod will be able to reach the database inside the cluster as the uri is passed to it via an env variable upon creation.
```
env:
- name: db_uri
    valueFrom:
    secretKeyRef:
        name: flask-mysql-secrets
        key: db_uri
- name: secret_key
    valueFrom:
    secretKeyRef:
        name: flask-mysql-secrets
        key: secret_key
```
The values of database uri and secret key are stored within secrets.yml file.
The number of pods inside the cluster is based on the utilization of the CPU of the pods. Horizontal Pod Autoscaler makes sure to have at least 2 pod replicas running at all times, scaling up to 10, based on the beforementioned CPU utilization.
To track CPU and other metrics, it is necessary to install kube metrics server. In minikube this can be achieved with:
```
minikube addons enable metrics-server
```
CPU and Memory utilization of the pods can be checked with kubectl top pods command. The output should be something similar to:
```
└─$ kubectl top pods -n flaskapp-nikola
NAME                                   CPU(cores)   MEMORY(bytes)   
flaskapp-deployment-7bfc6999f7-hvm6k   5m           74Mi            
flaskapp-deployment-7bfc6999f7-jpz2k   5m           73Mi            
mysql-8f56489f5-qtfxg                  3m           381Mi   
```
As Pods don't use nearly enough of computational power or memory specified in their requests and limits, HPA makes sure it keeps only 2 replicas running.
This can also be checked with kubectl describe command:
```
─$ kubectl describe  hpa -n flaskapp-nikola
Name:                                                  flaskapp-hpa
Namespace:                                             flaskapp-nikola
CreationTimestamp:                                     Wed, 11 Aug 2021 08:39:41 -0400
Reference:                                             Deployment/flaskapp-deployment
Metrics:                                               ( current / target )
  resource cpu on pods  (as a percentage of request):  10% (5m) / 80%
Min replicas:                                          2
Max replicas:                                          10
Deployment pods:                                       2 current / 2 desired
```
We can generate some traffic via shell, to test the horizontal pod autoscaler and see if the number of pods increases based on CPU ultilization:
```
while true; do wget -q -O- http://192.168.49.2:31614 ; done 
```
The IP address used in this command is the address of the flask-service, used to expose pods inside the cluster, which can be obtained through `minikube service flask-service -n flaskapp-nikola` command. Re-running the commands from before should result in a different output:
```
└─$ kubectl top pods -n flaskapp-nikola     
NAME                                   CPU(cores)   MEMORY(bytes)   
flaskapp-deployment-7bfc6999f7-hvm6k   96m          74Mi            
flaskapp-deployment-7bfc6999f7-jpz2k   94m          73Mi            
mysql-8f56489f5-qtfxg                  3m           381Mi   
└─$ kubectl describe  hpa -n flaskapp-nikola
Name:                                                  flaskapp-hpa
Namespace:                                             flaskapp-nikola
CreationTimestamp:                                     Wed, 11 Aug 2021 08:39:41 -0400
Reference:                                             Deployment/flaskapp-deployment
Metrics:                                               ( current / target )
  resource cpu on pods  (as a percentage of request):  190% (95m) / 80%
Min replicas:                                          2
Max replicas:                                          10
Deployment pods:                                       2 current / 4 desired
```
Very quickly HPA will detect the load on the pods and schedule new ones to run. Running the same top pods command will yet again give different output, this time there should be more pods running:
```
└─$ kubectl top pods -n flaskapp-nikola
NAME                                   CPU(cores)   MEMORY(bytes)   
flaskapp-deployment-7bfc6999f7-9jbf8   53m          72Mi            
flaskapp-deployment-7bfc6999f7-hqkf4   55m          70Mi            
flaskapp-deployment-7bfc6999f7-hvm6k   57m          74Mi            
flaskapp-deployment-7bfc6999f7-jpz2k   66m          73Mi            
flaskapp-deployment-7bfc6999f7-zppjj   84m          70Mi            
mysql-8f56489f5-qtfxg                  3m           381Mi   
```
It might take some time, but after stopping the shell loop, HPA will once again change the number of pods inside the deployment to optimal state, which will be 2. Here is the example of HPA events that can be seen in the describe hpa command output:
```
Events:
  Type    Reason             Age                    From                       Message
  ----    ------             ----                   ----                       -------
  Normal  SuccessfulRescale  6m49s (x4 over 5h46m)  horizontal-pod-autoscaler  New size: 4; reason: cpu resource utilization (percentage of request) above target
  Normal  SuccessfulRescale  6m33s (x2 over 4h57m)  horizontal-pod-autoscaler  New size: 5; reason: cpu resource utilization (percentage of request) above target
  Normal  SuccessfulRescale  5m32s                  horizontal-pod-autoscaler  New size: 9; reason: cpu resource utilization (percentage of request) above target
  Normal  SuccessfulRescale  27s                    horizontal-pod-autoscaler  New size: 7; reason: All metrics below target
  Normal  SuccessfulRescale  12s (x4 over 5h38m)    horizontal-pod-autoscaler  New size: 2; reason: All metrics below target
```
Accessing the flask-service via web browser should give the following result:
![flaskapp](https://user-images.githubusercontent.com/81910142/129585520-7caba96d-1bec-4b85-aa22-63bf6a4f42bb.PNG)