UNAME := $(shell uname -s)

project=chatbot
version=v1.0

image=${project}:${version}
image_tar=${project}-${version}.tar.gz


all: build setimagejs pkg clean

build:
	docker-compose build
	mkdir -p build/images
	docker save ${image} -o build/images/${image_tar}

setimagejs:
	echo "#!/bin/bash" > build/install.sh
	echo "docker load -i images/${image_tar}" >> build/install.sh
	chmod +x build/install.sh

pkg:
	tar -cvf build.tar.gz build

clean:
ifeq ($(UNAME),Darwin)
	rm -dRf build
else
	rm -f build
endif
