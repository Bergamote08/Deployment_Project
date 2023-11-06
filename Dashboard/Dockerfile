FROM python:3.10  

WORKDIR /home/app  

RUN apt-get update
RUN apt install curl -y  
RUN curl -fsSL https://get.deta.dev/cli.sh | sh

COPY . /home/app  
COPY requirements.txt /dependencies/requirements.txt 

RUN pip install --upgrade pip
RUN pip install -r /dependencies/requirements.txt 
 
EXPOSE 8051  

CMD streamlit run --server.port $PORT 8051 app.py
