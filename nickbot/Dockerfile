FROM python:2

WORKDIR /usr/src/app
COPY requirements2.txt ./
RUN pip install --no-cache-dir -r requirements2.txt

COPY . .

CMD [ "python", "./nickbot.py" ]
