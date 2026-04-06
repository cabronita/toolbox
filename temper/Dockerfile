FROM rockylinux/rockylinux:10.1.20251123
ENV TZ='Europe/London'

WORKDIR /app
COPY requirements.txt temper.py .

RUN dnf install -y python3.12 python3-pip \
  && rm -rf /var/cache/dnf \
  && pip3 install --no-cache-dir -r requirements.txt

ENTRYPOINT [ "./temper.py"]
