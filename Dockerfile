FROM python:3.8
COPY . /pet-hotel
WORKDIR /pet-hotel
RUN pip install -r requirements.txt
RUN python setup.py install
ENTRYPOINT ["python"]
CMD ["wsgi.py"]
