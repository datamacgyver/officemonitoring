FROM arm32v7/python:3

RUN apt-get update

#1. Install dependencies for PyODBC and tds
RUN apt-get install -y tdsodbc unixodbc-dev
RUN apt install unixodbc-bin -y
RUN apt-get clean -y

#2. Edit /etc/odbcinst.ini
RUN echo "[FreeTDS]\n\
Description = FreeTDS unixODBC Driver\n\
Driver = /usr/lib/arm-linux-gnueabi/odbc/libtdsodbc.so\n\
Setup = /usr/lib/arm-linux-gnueabi/odbc/libtdsS.so" >> /etc/odbcinst.ini

#3. Install requirements (contains pyodbc)
COPY ../requirements.txt /usr/src/app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

#Copy and run my app
COPY .. .
CMD [ "python", "app.py"]
