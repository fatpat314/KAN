FROM python:3.9-slim
RUN pip3 install --upgrade pip
WORKDIR /KAN
COPY . /KAN
COPY . /requirements.txt
RUN pip --no-cache-dir install -r requirements.txt
EXPOSE 8050
COPY . /python_proof
CMD ["python3", "main.py"]