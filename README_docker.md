# Quick reference

-	**Maintained by**:  
	[Michal Chrobak](https://github.com/netrunn3r/pytbull-ng)

-	**Where to get help**:  
	[the pytbull-ng wiki](https://github.com/netrunn3r/pytbull-ng/wiki)

-	**Where to file issues**:  
	[https://github.com/netrunn3r/pytbull-ng/issues](https://github.com/netrunn3r/pytbull-ng/issues)

-	**Supported architectures**: ([more info](https://github.com/docker-library/official-images#architectures-other-than-amd64))  
	`amd64`, `arm/v7`, `arm64`, `i386`

# Supported tags and respective `Dockerfile` links

-	[`latest`]()
-	~~[`stable`]()~~ (to early for stable version)
-	[`dev`]()

# What is pytbull-ng?

Pytbull-ng is an IDS/IPS testing framework for any IDS/IPS.
Original version, pytbull, was developed by Sebastien Damaye (sebastien #dot# damaye #at# gmail #dot# com). Michal Chrobak continue development of this tool as pytbull-ng, making it more adapted to the current days, eg:
1. migrate to Python 3
2. refresh attacks types and payloads
3. dockerize it

It is shipped with about 300 tests grouped in 9 testing modules but you can easily write your own tests, and even your own modules. It supports full string based commands, string based commands using environment variables as well as the initial list-based syntax.

**It is under heavy development to refresh old pytbull to be truly next generation of pytbull. However current version (main branch / latest image) is fully operating and can be used**

![logo](https://raw.githubusercontent.com/netrunn3r/pytbull-ng/main/img/pytbull.png)

# How to use this image

## Running local to test how it works
On first console run:

```console
$ docker run --rm -it efigo/pytbull-ng -m victim
```

On second one:

```console
$ docker  run --rm -it efigo/pytbull -m attacker -t <ip from victim>
```

## Testing IDS/IPS
![network_architecture](https://raw.githubusercontent.com/netrunn3r/pytbull-ng/main/img/pytbull_arch.png)

On victim host run:

```console
$ docker network create -d macvlan --subnet=<host network> --gateway=<host gateway ip> -o parent=<host interface> net_pub
$ docker run --rm -it --network=net_pub --ip=<ip from host network> --name=pytbull-ng_victim efigo/pytbull-ng -m victim
```

On attacker host run:

```console
$ sysctl net.ipv4.ip_forward=1
$ docker run -it --rm -p 80:80 --name=pytbull-ng_attacker efigo/pytbull-ng -m attacker -t <pytbull-ng_victim ip> -l <host ip>
```


# Image Variants

The `pytbull-ng` images come in many flavors, each designed for a specific use case.

All images are based on the popular [Alpine Linux project](https://alpinelinux.org), available in [the `alpine` official image](https://hub.docker.com/_/alpine). Alpine Linux is much smaller than most distribution base images (~5MB), and thus leads to much slimmer images in general.

## `pytbull-ng:latest`

This image is based on *main* branch from github, which contains working, but not widely tested features.

## `pytbull-ng:stable`

This image is based on *stable* branch from github, which contains working and widely tested features.

## `pytbull-ng:dev`

This image is based on *dev* branch from github, which is under development and some features may not work, but there may be some new feature which are not present in *stable* or *master* branch.

# License

View [license information](https://github.com/netrunn3r/pytbull-ng/LICENSE.md) (GNU GPL v3) for the software contained in this image.

As with all Docker images, these likely also contain other software which may be under other licenses (such as Bash, etc from the base distribution, along with any direct or indirect dependencies of the primary software being contained).

As for any pre-built image usage, it is the image user's responsibility to ensure that any use of this image complies with any relevant licenses for all software contained within.
