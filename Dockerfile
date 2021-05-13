FROM python:3
COPY requirements.txt /
RUN pip install gunicorn
RUN pip install -r requirements.txt
COPY gunicorn.conf.py /
COPY . /
CMD [ "gunicorn", "-c", "gunicorn.conf.py", "host_page:init_app" ]
