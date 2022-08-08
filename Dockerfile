FROM python:3.7.5-slim-buster

WORKDIR /root/blog_v2

ADD ./requirements.txt /root/xintongyuan_backend

RUN pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com

ADD ./ /root/blog_v2

CMD ["/bin/sh", "-c", "supervisord -c supervisord.conf -n"]