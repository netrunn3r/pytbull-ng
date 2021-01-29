FROM alpine:3.12 as builder
RUN echo "https://dl-cdn.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories && apk update \
    && apk --no-cache add \
    # Tools to build ncrack
    autoconf automake gcc g++ make musl-dev openssl-dev zlib-dev libssl1.1 libssh-dev python3-dev libffi-dev \
    # Tools to build snort3
    git cmake daq-dev libdnet-dev hwloc-dev luajit-dev libpcap-dev pcre-dev libunwind-dev libtirpc-dev libtool \
    # Build ncrack
    && wget https://nmap.org/ncrack/dist/ncrack-0.7.tar.gz \
    && tar -xzf ncrack-0.7.tar.gz \
    && cd ncrack-0.7 \    
    && ./configure \
    && make \
    && make install \
    # Build snort3
    && git clone git://github.com/snort3/libdaq.git \
    && cd libdaq \
    && ./bootstrap.sh \
    && ./configure \
    && make \
    && make install \
    && cd / \
    && git clone git://github.com/snort3/snort3.git \
    && cd snort3 \
    && ./configure_cmake.sh \
    && cd build \
    && make -j $(nproc) 

FROM alpine:3.12

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# For attacker to only publish port  80, not whole interface od host
EXPOSE 80

# Few tools are only in testing
RUN echo "https://dl-cdn.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories && apk update \
    && apk --no-cache add \
    # Install tools for pytbull
    python3 nmap nmap-nselibs nmap-scripts nikto apache2-utils scapy hping3 tcpreplay apache2 openssh-server vsftpd \
    # Install python requirements
    py3-feedparser py3-paramiko py3-requests py3-m2crypto py3-pip \
    && python3 -m pip install scapy cherrypy debugpy 

# Add files
ADD entrypoint.sh /pytbull/
ADD source/ /pytbull
ADD confs/vsftpd.conf /etc/vsftpd/vsftpd.conf
ADD confs/sshd_config /etc/ssh/sshd_config
ADD confs/httpd.conf /etc/apache2/httpd.conf
ADD clientsideattacks.tar.bz2 /var/www/localhost/htdocs/malicious/
ADD http://malc0de.com/bl/IP_Blacklist.txt /pytbull/data/

RUN chmod +x /pytbull/entrypoint.sh
    
# Add ncrack files from builder
COPY --from=builder /usr/local/share/ncrack/ /usr/local/share/ncrack/
COPY --from=builder /usr/local/bin/ncrack /usr/local/bin/ncrack

WORKDIR /pytbull

ENTRYPOINT [ "/pytbull/entrypoint.sh" ]
#CMD ["/bin/sh"]