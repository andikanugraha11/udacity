NAME := fullstack-02

build:
	docker build -t ${NAME} .
stop:
	docker stop ${NAME}
run-dev:
	docker run --rm -it \
	-v ${PWD}:/usr/src/app \
	--dns 1.1.1.1 \
	-w /usr/src/app \
	-p 5000:5000 \
	--name ${NAME} -d ${NAME} tail -f /dev/null
restart:
	docker restart ${NAME}
