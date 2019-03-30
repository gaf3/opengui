IMAGE=opengui
VERSION=0.1
ACCOUNT=gaf3
VOLUMES=-v ${PWD}/opengui.py:/opt/gaf3/lib/opengui.py \
		-v ${PWD}/test_opengui.py:/opt/gaf3/test_opengui.py \
		-v ${PWD}/setup.py:/opt/gaf3/setup.py

.PHONY: build shell test tag

build:
	docker build . -t $(ACCOUNT)/$(IMAGE):$(VERSION)

shell:
	docker run -it $(VOLUMES) $(ACCOUNT)/$(IMAGE):$(VERSION) sh

test:
	docker run -it $(VOLUMES) $(ACCOUNT)/$(IMAGE):$(VERSION) sh -c "coverage run -m unittest -v test_opengui && coverage report -m"

tag:
	git tag -a "v$(VERSION)" -m "Version $(VERSION)"
