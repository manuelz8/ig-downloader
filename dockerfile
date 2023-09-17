FROM python:3.8

# File Author / Maintainer
LABEL Chris G <chris@madhatterai.com>

# Google Chrome Repository for Selenium
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'

RUN apt update && \
    apt install --no-install-recommends -y build-essential gcc && \
    apt clean && rm -rf /var/lib/apt/lists/*

# Setup Chrome Driver
RUN apt -y update
RUN apt install -y google-chrome-stable

COPY . /app

# working directory
WORKDIR /app

# upgrade pip
RUN pip install --no-cache --upgrade pip
RUN pip install --upgrade setuptools

# install requirements
RUN pip install --no-cache -r requirements.txt

# port to view
EXPOSE 80

ENTRYPOINT ["python", "-m"]

CMD ["gunicorn", "--workers", "4", "--bind", "0.0.0.0:80", "wsgi:app"]