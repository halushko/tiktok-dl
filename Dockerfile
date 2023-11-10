FROM python:3.9-slim

WORKDIR /app
COPY tiktok-dl.py .
RUN mkdir /app/files

RUN pip install urllib3 argparse

ENTRYPOINT tail -f /dev/null
#CMD ["python", "main.py"]