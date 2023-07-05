FROM python:3.11

ENV TZ=UTC
ENV DEBIAN_FRONTEND=noninteractive



COPY chromedriver.exe /usr/local/bin/chromedriver.exe
RUN chmod +x /usr/local/bin/chromedriver.exe
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libnss3 \
    libgconf-2-4 \
    libfontconfig1


# Copiar el código de la aplicación en la imagen
COPY . /app
WORKDIR /app

# Instalar las dependencias de Python
RUN pip install -r requirements.txt

CMD ["python", "3.py"]



