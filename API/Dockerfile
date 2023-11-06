FROM python:3.10  

WORKDIR /home/app  

RUN apt-get update
RUN apt install curl -y  
RUN curl -fsSL https://get.deta.dev/cli.sh | sh

COPY . /home/app  
COPY requirements.txt /dependencies/requirements.txt 

RUN pip install --upgrade pip
RUN pip install -r /dependencies/requirements.txt 

EXPOSE 8000

CMD gunicorn apitest:app -b 0.0.0.0:8000 -k uvicorn.workers.UvicornWorker