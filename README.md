# pytbull-ng

![logo](https://github.com/netrunn3r/pytbull-ng/source/report/img/pytbull.png)

Pytbull-ng is an IDS/IPS testing framework for any IDS/IPS.
Original version, pytbull, was developed by Sebastien Damaye (sebastien #dot# damaye #at# gmail #dot# com). Michal Chrobak continue development of this tool as pytbull-ng, making it more adapted to the current days, eg:
1. migrate to Python 3
2. refresh attacks types and payloads
3. dockerize it

It is shipped with about 300 tests grouped in 9 testing modules but you can easily write your own tests, and even your own modules. It supports full string based commands, string based commands using environment variables as well as the initial list-based syntax.

Pytbull-ng development is focus on making docker images to easily deploy it in infrastructure. Images can be found on [Docker Hub](https://hub.docker.com/repository/docker/efigo/pytbull-ng).