#!/bin/sh

usage() { 
    echo "Usage: docker run --rm -it <image> (-m attacker -t <ip to attack> [-l <local ip>]) | (-m victim)" 1>&2 
    exit 1
}

while getopts ":m:t:l:d" o; do
    case "${o}" in
        m)
            m=${OPTARG}
            if [ "${m}" != "attacker" -a "${m}" != "victim" ]; then
                echo "Mode can be only attacker or victim"
                usage
            fi
            ;;
        t)
            t=${OPTARG}
            ;;
        l)
            ip=${OPTARG}
            ;;
        d)
            debug="-m debugpy --listen 0.0.0.0:5678 --wait-for-client"
            ;;
        *)
            echo "Unknown parameters"
            usage
            ;;
    esac
done
shift $((OPTIND-1))

if [ -z "${m}" ]; then
    echo "No mode selected"
    usage
fi

if [ "${m}" = "victim" -a -n "${t}" ]; then
    echo "Victim mode need not parameters"
    usage
fi

if [ "${m}" = "attacker" -a -z "${t}" ]; then
    echo "No victim IP"
    usage
fi

start_date=$(date)

int=$(ip l | grep eth | head -n 1 | cut -d '@' -f 1 | egrep -o -e '[a-z]+[0-9]+')
if [ -z "${ip}" ]; then
    ip=$(ip a | grep eth | tail -n 1 | egrep -o '[0-9.]*/' | cut -d '/' -f 1)
    mask="/$(ip a | grep eth | tail -n 1 | egrep -o '[0-9.]*/[0-9]{2}' | cut -d '/' -f 2)"
fi
sed -i "s/PYTBULL_IP/${ip}/" /pytbull/conf/config.cfg
sed -i "s/PYTBULL_INT/${int}/" /pytbull/conf/config.cfg


# Add local user
if [ "${m}" = "victim" ]; then
    ftp_user=$(openssl rand -base64 24 | tr -d /=+ | head -c 12)
    ftp_pass=$(openssl rand -base64 40 | tr -d /=+ | head -c 20)
    adduser ${ftp_user} -D
    mkdir /var/www/localhost/htdocs/2bjPrECZWqJC
    echo -n "${ftp_user}:${ftp_pass}" | chpasswd 2>/dev/null
    echo -n "${ftp_user}:${ftp_pass}" > /var/www/localhost/htdocs/2bjPrECZWqJC/WSR79Fc1XGIo
    htpasswd -cBb /pytbull/htpasswd dQWiwjxce0uR rca985co9mWw 2>/dev/null
elif [ "${m}" = "attacker" ]; then
    user_pass=$(wget http://dQWiwjxce0uR:rca985co9mWw@${t}:80/2bjPrECZWqJC/WSR79Fc1XGIo -O - 2>/dev/null)
    ftp_user=$(echo ${user_pass} | cut -d ':' -f 1)
    ftp_pass=$(echo ${user_pass} | cut -d ':' -f 2)
fi

sed -i "s/PYTBULL_FTP_USER/${ftp_user}/" /pytbull/conf/config.cfg
sed -i "s/PYTBULL_FTP_PASS/${ftp_pass}/" /pytbull/conf/config.cfg
echo "FTP user: ${ftp_user}:${ftp_pass}"

if [ "${m}" = "attacker" ]; then
    sed -i "s#PYTBULL_MALWARE_URL#http://${ip}/malicious/#" /pytbull/conf/config.cfg
fi

echo "Mode: ${m}"
echo "Host IP: ${ip}${mask}"
if [ "${m}" = "attacker" -a -n "${t}" ]; then
    echo "Victim IP: ${t}"
fi

if ! command -v sudo &> /dev/null; then
    sed -i "s/PYTBULL_SUDO//" /pytbull/conf/config.cfg
else
    sed -i "s#PYTBULL_SUDO#/usr/bin/sudo#" /pytbull/conf/config.cfg  # change to locate
fi

if [ "${m}" = "attacker" ]; then
    httpd 2>/dev/null
    netstat -tlpn
    if [ -z "${debug}" ]; then
        time python3 /pytbull/pytbull -t ${t} -r --offline
    else
        time python3 ${debug} /pytbull/pytbull -t ${t} -r --offline
    fi
elif [ "${m}" = "victim" ]; then
    vsftpd /etc/vsftpd/vsftpd.conf &
    ssh-keygen -f /etc/ssh/ssh_host_rsa_key -q -N "" 
    /usr/sbin/sshd 
    httpd 2>/dev/null
    netstat -tlpn
    if [ -z "${debug}" ]; then
        python3 /pytbull/server/pytbull-server.py
    else
        python3 ${debug} /pytbull/server/pytbull-server.py
    fi
fi 

echo -e "\nStart: ${start_date}"
echo -n "End:   "; date