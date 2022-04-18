FROM python:3.9 
WORKDIR /app # git https://github.com/PR0FESS0R-99/Open-Source
COPY . /app/ # /PR0FESS0R-99/Open-Source
RUN pip install -r requirements.txt
CMD ["python", "mt_botz.py"]

