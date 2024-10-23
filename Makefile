IMAGE=opengui
INSTALL=python:3.8.5-alpine3.12
VERSION?=$(shell cat VERSION)
DEBUG_PORT=5678
ACCOUNT=gaf3
TILT_PORT=27939
TTY=$(shell if tty -s; then echo "-it"; fi)
VOLUMES=-v ${PWD}/opengui.py:/opt/service/opengui.py \
		-v ${PWD}/test_opengui.py:/opt/service/test_opengui.py \
		-v ${PWD}/.pylintrc:/opt/service/.pylintrc \
		-v ${PWD}/bin:/opt/service/bin \
		-v ${PWD}/VERSION:/opt/service/VERSION \
		-v ${PWD}/VERSION:/opt/service/README.md \
		-v ${PWD}/setup.py:/opt/service/setup.py \
		-v ${PWD}/docs:/opt/service/docs \
		-v ${PWD}/docs.py:/opt/service/docs.py
ENVIRONMENT=-e PYTHONDONTWRITEBYTECODE=1 \
			-e PYTHONUNBUFFERED=1 \
			-e test="python -m unittest -v" \
			-e debug="python -m ptvsd --host 0.0.0.0 --port 5678 --wait -m unittest -v"
PYPI=-v ${PWD}/LICENSE.txt:/opt/service/LICENSE.txt \
  	 -v ${HOME}/.pypirc:/opt/service/.pypirc

.PHONY: build shell test lint up down cli setup tag untag testpypi pypi sphinx docs html clean rtd

build:
	docker build . -t $(ACCOUNT)/$(IMAGE):$(VERSION)

shell:
	docker run $(TTY) $(VOLUMES) $(ENVIRONMENT) $(ACCOUNT)/$(IMAGE):$(VERSION) sh

debug:
	docker run $(TTY) $(VOLUMES) $(ENVIRONMENT) -p 127.0.0.1:$(DEBUG_PORT):5678 $(ACCOUNT)/$(IMAGE):$(VERSION) sh -c "python -m ptvsd --host 0.0.0.0 --port 5678 --wait -m unittest -v test_opengui"

test:
	docker run $(TTY) $(VOLUMES) $(ENVIRONMENT) $(ACCOUNT)/$(IMAGE):$(VERSION) sh -c "coverage run -m unittest -v test_opengui && coverage report -m"

lint:
	docker run $(TTY) $(VOLUMES) $(ENVIRONMENT) $(ACCOUNT)/$(IMAGE):$(VERSION) sh -c "pylint --rcfile=.pylintrc opengui.py"

up:
	kubectx docker-desktop
	tilt --port $(TILT_PORT) up

down:
	kubectx docker-desktop
	tilt down

cli:
	docker run $(TTY) $(VOLUMES) $(ENVIRONMENT) $(ACCOUNT)/$(IMAGE):$(VERSION) sh -c "python bin/cli.py"

setup:
	docker run $(TTY) $(VOLUMES) $(PYPI) $(INSTALL) sh -c "cp -r /opt/service /opt/install && cd /opt/install/ && \
	python setup.py install && \
	python -m opengui"

tag:
	-git tag -a $(VERSION) -m "Version $(VERSION)"
	git push origin --tags

untag:
	-git tag -d $(VERSION)
	git push origin ":refs/tags/$(VERSION)"

testpypi:
	docker run $(TTY) $(VOLUMES) $(PYPI) gaf3/pypi sh -c "cd /opt/service && \
	BUILD_VERSION='$(VERSION)' python -m build && \
	python -m twine upload -r testpypi --config-file=.pypirc dist/*"

pypi:
	docker run $(TTY) $(VOLUMES) $(PYPI) gaf3/pypi sh -c "cd /opt/service && \
	BUILD_VERSION='$(VERSION)' python -m build && \
	python -m twine upload --config-file=.pypirc dist/*"

sphinx:
	docker run $(TTY) $(VOLUMES) $(ENVIRONMENT) $(ACCOUNT)/$(IMAGE):$(VERSION) sh -c "sphinx-quickstart docs --sep -p $(IMAGE) -a 'George A. Fitch III (gaf3)' -r $(VERSION) -l en"

docs:
	docker run $(TTY) $(VOLUMES) $(ENVIRONMENT) $(ACCOUNT)/$(IMAGE):$(VERSION) sh -c "./docs.py"

html:
	docker run $(TTY) $(VOLUMES) $(ENVIRONMENT) $(ACCOUNT)/$(IMAGE):$(VERSION) sh -c "sphinx-build -b html docs/source/ docs/build/html"

clean:
	docker run $(TTY) $(VOLUMES) $(ENVIRONMENT) $(ACCOUNT)/$(IMAGE):$(VERSION) sh -c "rm -rf docs/build/html"

rtd: docs html
	open -a Firefox "file://$(PWD)/docs/build/html/index.html"
