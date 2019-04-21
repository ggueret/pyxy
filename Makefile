run:
	docker run -p 127.0.0.1:3128:80 -v pyxy_cache:/data pyxy

build:
	docker build . -t pyxy
