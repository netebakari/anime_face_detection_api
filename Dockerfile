FROM python:3.11
RUN mkdir /app
WORKDIR /app
COPY requirements.txt /app
RUN pip install -r requirements.txt
RUN apt update && apt install -y libgl1-mesa-dev
COPY . /app
CMD ["python", "face_d_api_server.py"]
EXPOSE 80
