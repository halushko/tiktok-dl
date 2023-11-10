FROM python:3.9-slim

WORKDIR /app
COPY tiktok-dl.py .
RUN mkdir /app/files

RUN pip install sys re urllib3 argparse urllib.request

ENTRYPOINT tail -f /dev/null
#CMD ["python", "main.py"]