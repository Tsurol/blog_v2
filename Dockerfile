FROM python:3.7.5-slim-buster

WORKDIR /root/blog_v2

ADD ./requirements.txt /root/blog_v2

RUN pip3 install --upgrade pip -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com

RUN pip3 install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com

ADD ./ /root/blog_v2

CMD ["/bin/sh", "-c", "supervisord -c supervisord.conf -n"]