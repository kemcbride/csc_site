# give up on a slim image (python:slim or sth - just use a numpy image
FROM jupyter/minimal-notebook

WORKDIR /csc_site

COPY requirements.txt .


# Run heavy specific installs first separately so they can be cached, faster builds.
# note, the other heavy ones (numpy, pandas, ipython... -> are handled via the current jupyter image)
RUN pip install peewee>=3.4.0

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "-m", "app"]

EXPOSE 25777
