FROM python:3.11
RUN mkdir -p /app/weights
WORKDIR /app
COPY requirements.txt /app
RUN pip install -r requirements.txt
RUN apt update && apt install -y libgl1-mesa-dev
RUN curl -L 'https://huggingface.co/UZUKI/anime-face-detection/resolve/main/ssd_best8.pth?download=true' -o weights/ssd_best8.pth
COPY . /app
CMD ["python", "face_d_api_server.py"]
EXPOSE 80
