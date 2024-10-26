FROM python:3.12-slim
WORKDIR /usr/scrapp/

USER root

COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT ["python3", "/usr/scrapp/run_all.py", "/usr/scrapp_volume/"]
