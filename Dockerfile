FROM python:3-alpine3.12
WORKDIR ./app
add  requirements.txt /app
COPY . /app
RUN export PYTHONPATH=/usr/bin/python
RUN pip install -r requirements.txt
EXPOSE 5000
CMD python . /app.py
