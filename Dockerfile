FROM winamd64/python:3

WORKDIR /usr/src/budget_interface


COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./main.py" ]