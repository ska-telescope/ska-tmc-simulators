#
# Project makefile for a ska-tmc-simulators project. You should normally only need to modify
# PROJECT below.
#
#
# CAR_OCI_REGISTRY_HOST and PROJECT are combined to define
# the Docker tag for this project. The definition below inherits the standard
# value for CAR_OCI_REGISTRY_HOST (artefact.skao.int) and overwrites
# CAR_OCI_REGISTRY_USER and PROJECT to give a final Docker tag of
# artefact.skao.int/ska-telescope/ska-tmc
#
CAR_OCI_REGISTRY_HOST:=artefact.skao.int
CAR_OCI_REGISTRY_USER:=ska-telescope
PROJECT = ska-tmc-simulators

# KUBE_NAMESPACE defines the Kubernetes Namespace that will be deployed to
# using Helm.  If this does not already exist it will be created
KUBE_NAMESPACE ?= ska-tmc-simulators-mid
DASHBOARD ?= webjive-dash.dump

# HELM_RELEASE is the release that all Kubernetes resources will be labelled
# with
HELM_RELEASE ?= test
HELM_CHARTS_TO_PUBLISH=

# F401 Ignore unused imports because of tagno protected sections
# W503 Ignore operator at beginning of line as conflicts with black
# stretch line length to 180 because of super long parameter assignments
PYTHON_LINT_TARGET = src/
PYTHON_SWITCHES_FOR_FLAKE8=--ignore=W503,N --max-line-length=180

# UMBRELLA_CHART_PATH Path of the umbrella chart to work with
HELM_CHART=ska-tmc-simulators-umbrella
UMBRELLA_CHART_PATH ?= charts/$(HELM_CHART)/
K8S_CHARTS ?= ska-tmc-simulators ska-tmc-simulators-umbrella## list of charts
K8S_CHART ?= $(HELM_CHART)

CI_PROJECT_DIR ?= .

XAUTHORITY ?= $(HOME)/.Xauthority
THIS_HOST := $(shell ip a 2> /dev/null | sed -En 's/127.0.0.1//;s/.*inet (addr:)?(([0-9]*\.){3}[0-9]*).*/\2/p' | head -n1)
DISPLAY ?= $(THIS_HOST):0
JIVE ?= false# Enable jive
TARANTA ?= false
MINIKUBE ?= true ## Minikube or not
FAKE_DEVICES ?= true ## Install fake devices or not
TANGO_HOST ?= tango-databaseds:10000## TANGO_HOST connection to the Tango DS
CI_PROJECT_PATH_SLUG ?= ska-tmc-simulators
CI_ENVIRONMENT_SLUG ?= ska-tmc-simulators
$(shell echo 'global:\n  annotations:\n    app.gitlab.com/app: $(CI_PROJECT_PATH_SLUG)\n    app.gitlab.com/env: $(CI_ENVIRONMENT_SLUG)' > gilab_values.yaml)

ITANGO_DOCKER_IMAGE = $(CAR_OCI_REGISTRY_HOST)/ska-tango-images-tango-itango:9.3.9

CI_REGISTRY ?= gitlab.com
CUSTOM_VALUES = --set tmcsim.image.tag=$(VERSION)
K8S_TEST_IMAGE_TO_TEST=$(CAR_OCI_REGISTRY_HOST)/$(PROJECT):$(VERSION)

-include .make/k8s.mk
-include .make/python.mk
-include .make/helm.mk
-include .make/oci.mk
-include .make/docs.mk
-include .make/release.mk
-include .make/make.mk
-include .make/help.mk
-include PrivateRules.mak

# flag this up for the oneshot /Dockerfile
OCI_IMAGES=ska-tmc-simulators

PYTHON_BUILD_TYPE = non_tag_setup

K8S_CHART_PARAMS = --set global.minikube=$(MINIKUBE) \
	--set global.tango_host=$(TANGO_HOST) \
	--set ska-tango-base.display=$(DISPLAY) \
	--set ska-tango-base.xauthority=$(XAUTHORITY) \
	--set ska-tango-base.jive.enabled=$(JIVE) \
	--set tmcsim.telescope=$(TELESCOPE) \
	$(CUSTOM_VALUES) \
	--values gilab_values.yaml
