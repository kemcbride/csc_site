FROM jupyter/minimal-notebook

WORKDIR /csc_site

COPY requirements.txt .

RUN pip install peewee>=3.4.0

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "-m", "app"]

EXPOSE 25777
