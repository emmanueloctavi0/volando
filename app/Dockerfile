FROM makinacorpus/geodjango:focal-3.8

WORKDIR /usr/src/app

# python dependencies
COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY ./ ./
