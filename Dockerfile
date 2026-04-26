FROM python:3.12-slim

# Install postgres + GIS libs
RUN apt-get update && apt-get install -y \
    postgresql \
    postgresql-contrib \
    postgis \
    postgresql-15-postgis-3 \
    gdal-bin \
    libgdal-dev \
    libgeos-dev \
    libproj-dev \
    && rm -rf /var/lib/apt/lists/*

# create postgres data dir
RUN mkdir -p /data/postgres

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

COPY start.sh /start.sh
RUN chmod +x /start.sh

EXPOSE 8000

CMD ["/start.sh"]