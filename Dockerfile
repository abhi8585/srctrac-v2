FROM python:3.9
COPY setup.py /home/
COPY . /home/
WORKDIR /home
RUN pip3 install -r requirements.txt
ENTRYPOINT FLASK_APP=manage.py flask run --host=0.0.0.0
