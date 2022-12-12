FROM python:3

WORKDIR /usr/src/app

RUN apt-get update -y && \
	apt-get install openssh-server -y

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000
EXPOSE 22

#ssh config
RUN sed -ri 's/^#?PermitRootLogin\s+.*/PermitRootLogin yes/' /etc/ssh/sshd_config && \
    sed -ri 's/UsePAM yes/#UsePAM yes/g' /etc/ssh/sshd_config

RUN service ssh start
CMD ["/usr/sbin/sshd", "-D"]

