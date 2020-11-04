FROM alpine:latest

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# For attacker to only publish port  80, not whole interface od host
EXPOSE 80

# Add files
ADD requirements.txt .
ADD entrypoint.sh /pytbull/
ADD source/ /pytbull
ADD confs/vsftpd.conf /etc/vsftpd/vsftpd.conf
ADD confs/sshd_config /etc/ssh/sshd_config
ADD confs/httpd.conf /etc/apache2/httpd.conf
ADD clientsideattacks.tar.bz2 /var/www/localhost/htdocs/malicious/
ADD http://malc0de.com/bl/IP_Blacklist.txt /pytbull/data/

# Few tools are only in testing
RUN echo "https://dl-cdn.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories && apk update \
    && apk --no-cache add \
    # Install tools for pytbull
    python3 nmap nmap-nselibs nmap-scripts nikto apache2-utils scapy hping3 py3-m2crypto py3-pip tcpreplay apache2 openssh-server vsftpd \
    # Tools to build ncrack and python dependencies
    autoconf automake gcc g++ make musl-dev openssl-dev zlib-dev libssl1.1 libssh-dev python3-dev libffi-dev \
    # Install pip requirements
    && python3 -m pip install -r requirements.txt \
    # Download and  build ncrack
    && wget https://nmap.org/ncrack/dist/ncrack-0.7.tar.gz \
    && tar -xzf ncrack-0.7.tar.gz \
    && cd ncrack-0.7 \    
    && ./configure \
    && make \
    && make install \
    && cd / \
    # Clean up
    && rm -r ncrack-0.7* \
    && apk del autoconf automake gcc g++ make musl-dev openssl-dev zlib-dev libssl1.1 libssh-dev python3-dev libffi-dev \
    # Make entrypoint.sh executable
    && chmod +x /pytbull/entrypoint.sh
    
# Install dev packages (python3-dev libffi-dev for python packages from pip)    
#RUN apk --no-cache add autoconf automake gcc g++ make musl-dev openssl-dev zlib-dev libssl1.1 libssh-dev python3-dev libffi-dev

# RUN wget https://nmap.org/ncrack/dist/ncrack-0.7.tar.gz \
#     && tar -xzf ncrack-0.7.tar.gz \
#     && cd ncrack-0.7 \    
#     && ./configure \
#     && make \
#     && make install \
#     && cd / \
#     && rm -r ncrack-0.7*

# Install pip requirements
# ADD requirements.txt .
# RUN python3 -m pip install -r requirements.txt

# Delete dev packages
# RUN apk del autoconf automake gcc g++ make musl-dev openssl-dev zlib-dev libssl1.1 libssh-dev python3-dev libffi-dev

WORKDIR /pytbull

# ADD entrypoint.sh /pytbull/
# RUN chmod +x /pytbull/entrypoint.sh
ENTRYPOINT [ "/pytbull/entrypoint.sh" ]
#CMD ["/bin/sh"]
