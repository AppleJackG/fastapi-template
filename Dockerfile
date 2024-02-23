FROM python:3.11
RUN mkdir /fastapi_auth
WORKDIR /fastapi_auth
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# CMD gunicorn src.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000
RUN chmod a+x docker/*sh