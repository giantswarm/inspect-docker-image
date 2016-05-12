FROM python:2.7-alpine
ENV PYTHON_UNBUFFERED 1
RUN pip install --upgrade pip
ADD requirements.txt /
RUN pip install -r /requirements.txt
ADD imageinspector.py /
ADD service.py /
ENTRYPOINT ["python", "/imageinspector.py"]
