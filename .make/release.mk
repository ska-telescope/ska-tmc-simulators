#
#   Copyright 2015  Xebia Nederland B.V.
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
ifeq ($(strip $(PROJECT)),)
  NAME=$(shell basename $(CURDIR))
else
  NAME=$(PROJECT)
endif

RELEASE_SUPPORT := $(shell dirname $(abspath $(lastword $(MAKEFILE_LIST))))/.make-release-support

ifeq ($(strip $(CAR_OCI_REGISTRY_HOST)),)
  CAR_OCI_REGISTRY_HOST = artefact.skao.int
endif

ifeq ($(strip $(CAR_OCI_REGISTRY_USER)),)
  CAR_OCI_REGISTRY_USER = ska-telescope
endif

IMAGE=$(CAR_OCI_REGISTRY_HOST)/$(CAR_OCI_REGISTRY_USER)/$(NAME)

VERSION=$(shell . $(RELEASE_SUPPORT) ; getVersion)
TAG=$(shell . $(RELEASE_SUPPORT); getTag)
SHELL=/bin/bash

DOCKER_BUILD_CONTEXT=.
DOCKER_FILE_PATH=Dockerfile

.PHONY: pre-build docker-build post-build build release patch-release minor-release major-release tag check-status check-release showver \
	push pre-push do-push post-push push-versioned-image create-tag create-publish-tag release-ska-tmc-simulators push-tag config-git \
	release-tmc-simulators delete-tmc-simulators-release delete-tag release-tmc-simulators-if-no-error

build: pre-build docker-build post-build  ## build the application image

pre-build:

post-build:

pre-push:

post-push:

docker-build: .release
	docker build $(DOCKER_BUILD_ARGS) -t $(IMAGE):$(VERSION) $(DOCKER_BUILD_CONTEXT) -f $(DOCKER_FILE_PATH) --build-arg CAR_OCI_REGISTRY_HOST=$(CAR_OCI_REGISTRY_HOST) --build-arg CAR_OCI_REGISTRY_USER=$(CAR_OCI_REGISTRY_USER)
	@DOCKER_MAJOR=$(shell docker -v | sed -e 's/.*version //' -e 's/,.*//' | cut -d\. -f1) ; \
	DOCKER_MINOR=$(shell docker -v | sed -e 's/.*version //' -e 's/,.*//' | cut -d\. -f2) ; \
	if [ $$DOCKER_MAJOR -eq 1 ] && [ $$DOCKER_MINOR -lt 10 ] ; then \
		echo docker tag -f $(IMAGE):$(VERSION) $(IMAGE):latest ;\
		docker tag -f $(IMAGE):$(VERSION) $(IMAGE):latest ;\
	else \
		echo docker tag $(IMAGE):$(VERSION) $(IMAGE):latest ;\
		docker tag $(IMAGE):$(VERSION) $(IMAGE):latest ; \
	fi

.release:
	@echo "release=0.0.0" > .release
	@echo "tag=$(NAME)-0.0.0" >> .release
	@echo INFO: .release created
	@cat .release
	@echo DESCRIPTION

release: check-status check-release build create-tag push

push: pre-push do-push post-push ## push the image to the Docker registry

do-push:
	docker push $(IMAGE):latest

snapshot: build push

showver: .release
	@. $(RELEASE_SUPPORT); getVersion

bump-patch-release: VERSION := $(shell . $(RELEASE_SUPPORT); nextPatchLevel)
bump-patch-release: .release tag

bump-minor-release: VERSION := $(shell . $(RELEASE_SUPPORT); nextMinorLevel)
bump-minor-release: .release tag

bump-major-release: VERSION := $(shell . $(RELEASE_SUPPORT); nextMajorLevel)
bump-major-release: .release tag

patch-release: tag-patch-release release
	@echo $(VERSION)

minor-release: tag-minor-release release
	@echo $(VERSION)

major-release: tag-major-release release
	@echo $(VERSION)

tag: TAG=$(shell . $(RELEASE_SUPPORT); getTag $(VERSION))
tag: check-status
#	@. $(RELEASE_SUPPORT) ; ! tagExists $(TAG) || (echo "ERROR: tag $(TAG) for version $(VERSION) already tagged in git" >&2 && exit 1) ;
	@. $(RELEASE_SUPPORT) ; setRelease $(VERSION)
#	git add .
#	git commit -m "bumped to version $(VERSION)" ;
#	git tag $(TAG) ;
#	@ if [ -n "$(shell git remote -v)" ] ; then git push --tags ; else echo 'no remote to push tags to' ; fi

check-status:
	@. $(RELEASE_SUPPORT) ; ! hasChanges || (echo "ERROR: there are still outstanding changes" >&2 && exit 1) ;

check-release: .release
	@. $(RELEASE_SUPPORT) ; tagExists $(TAG) || (echo "ERROR: version not yet tagged in git. make [minor,major,patch]-release." >&2 && exit 1) ;
	@. $(RELEASE_SUPPORT) ; ! differsFromRelease $(TAG) || (echo "ERROR: current directory differs from tagged $(TAG). make [minor,major,patch]-release." ; exit 1)

push-versioned-image:
	docker push $(IMAGE):$(VERSION)

create-tag: .release
	@. $(RELEASE_SUPPORT) ; createGitTag || (echo "ERROR: Some error in creating tag" >&2 && exit 1) ;

delete-image-from-nexus:
	@. $(RELEASE_SUPPORT) ; deleteImageFromNexus

push-tag: .release
	@. $(RELEASE_SUPPORT) ; gitPush

create-publish-tag: create-tag push-tag

config-git:
	git config --global user.email $(EMAILID)
	git config --global user.name $(USERNAME)

release-ska-tmc-simulators: config-git docker-build push-versioned-image create-publish-tag release-tmc-simulators-if-no-error

release-tmc-simulators: .release
	@. $(RELEASE_SUPPORT) ; releaseTMC-simulators

delete-tmc-simulators-release: .release
	@. $(RELEASE_SUPPORT) ; deleteTMC-simulatorsRelease

delete-tag: .release
	@. $(RELEASE_SUPPORT) ; deleteTag

release-tmc-simulators-if-no-error: .release
	@. $(RELEASE_SUPPORT) ; releasetmc-simulatorsIfNoError
