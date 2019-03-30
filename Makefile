IMAGE=opengui
VERSION=0.1
ACCOUNT=gaf3
VOLUMES=-v ${PWD}/lib/:/opt/gaf3/lib/ \
		-v ${PWD}/test/:/opt/gaf3/test/

.PHONY: build shell test tag

build:
	docker build . -t $(ACCOUNT)/$(IMAGE):$(VERSION)

shell:
	docker run -it $(VOLUMES) $(ACCOUNT)/$(IMAGE):$(VERSION) sh

test:
	docker run -it $(VOLUMES) $(ACCOUNT)/$(IMAGE):$(VERSION) sh -c "coverage run -m unittest discover -v test && coverage report -m --include lib/*.py"

tag:
	git tag -a "v$(VERSION)" -m "Version $(VERSION)"
