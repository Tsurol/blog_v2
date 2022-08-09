FROM python:3.7.5-slim-buster

WORKDIR /root/blog_v2

ADD ./requirements.txt /root/blog_v2

#RUN yum install mysql-devel gcc gcc-devel python-devel
#RUN apt-get install libmysqlclient-dev

RUN pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/ --trusted-host https://pypi.tuna.tsinghua.edu.cn

ADD ./ /root/blog_v2

CMD ["/bin/sh", "-c", "supervisord -c supervisord.conf -n"]