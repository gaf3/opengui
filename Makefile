IMAGE=opengui
INSTALL=python:3.8.5-alpine3.12
VERSION=0.8.8
ACCOUNT=gaf3
TILT_PORT=27939
TTY=$(shell if tty -s; then echo "-it"; fi)
VOLUMES=-v ${PWD}/opengui.py:/opt/service/opengui.py \
		-v ${PWD}/test_opengui.py:/opt/service/test_opengui.py \
		-v ${PWD}/setup.py:/opt/service/setup.py
PIPY=-v ${PWD}/LICENSE.txt:/opt/service/LICENSE.txt \
	-v ${PWD}/PYPI.md:/opt/service/README.md \
	-v ${HOME}/.pypirc:/opt/service/.pypirc

.PHONY: build shell test up down setup tag untag testpypi pypi

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

setup:
	docker run $(TTY) $(VOLUMES) $(INSTALL) sh -c "cp -r /opt/service /opt/install && cd /opt/install/ && \
	python setup.py install && \
	python -m opengui"

tag:
	-git tag -a $(VERSION) -m "Version $(VERSION)"
	git push origin --tags

untag:
	-git tag -d $(VERSION)
	git push origin ":refs/tags/$(VERSION)"

testpypi:
	docker run $(TTY) $(VOLUMES) $(PIPY) gaf3/pypi sh -c "cd /opt/service && \
	python -m build && \
	python -m twine upload -r testpypi --config-file=.pypirc dist/*"

pypi:
	docker run $(TTY) $(VOLUMES) $(PIPY) gaf3/pypi sh -c "cd /opt/service && \
	python -m build && \
	python -m twine upload --config-file=.pypirc dist/*"
