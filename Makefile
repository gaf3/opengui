IMAGE=opengui
VERSION=0.8.3
ACCOUNT=gaf3
TILT_PORT=27939
VOLUMES=-v ${PWD}/opengui.py:/opt/gaf3/opengui.py \
		-v ${PWD}/test_opengui.py:/opt/gaf3/test_opengui.py \
		-v ${PWD}/setup.py:/opt/gaf3/setup.py

.PHONY: build shell test tag

build:
	docker build . -t $(ACCOUNT)/$(IMAGE):$(VERSION)

shell:
	docker run -it $(VOLUMES) $(ACCOUNT)/$(IMAGE):$(VERSION) sh

test:
	docker run -it $(VOLUMES) $(ACCOUNT)/$(IMAGE):$(VERSION) sh -c "coverage run -m unittest -v test_opengui && coverage report -m"

up:
	kubectx docker-desktop
	tilt --port $(TILT_PORT) up

down:
	kubectx docker-desktop
	tilt down

tag:
	-git tag -a $(VERSION) -m "Version $(VERSION)"
	git push origin --tags

untag:
	-git tag -d $(VERSION)
	git push origin ":refs/tags/$(VERSION)"
