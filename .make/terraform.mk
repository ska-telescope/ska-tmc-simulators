# include Makefile for Terraform related targets and variables

# do not declare targets if help had been invoked
ifneq (long-help,$(firstword $(MAKECMDGOALS)))
ifneq (help,$(firstword $(MAKECMDGOALS)))

MAKEFILE_PATH := $(abspath $(lastword $(MAKEFILE_LIST)))

SHELL=/usr/bin/env bash

TERRAFORM_SUPPORT := $(shell dirname $(abspath $(lastword $(MAKEFILE_LIST))))/.make-terraform-support

TERRAFORM_RUNNER ?= terraform

TERRAFORM_LINT_TARGET ?=

TERRAFORM_VARS_BEFORE_FMT ?=

TERRAFORM_SWITCHES_FOR_FMT ?= -diff -recursive

TERRAFORM_LINT_SWITCHES_FOR_INIT ?= -backend=false -compact-warnings

TERRAFORM_LINT_VARS_BEFORE_INIT ?=

TERRAFORM_LINT_SWITCHES_FOR_VALIDATE ?= -compact-warnings

TERRAFORM_LINT_VARS_BEFORE_VALIDATE ?=

TERRAFORM_TFLINT_RUNNER ?= tflint

TERRAFORM_SWITCHES_FOR_TFLINT ?=

TERRAFORM_VARS_BEFORE_TFLINT ?=

ifeq ($(TERRAFORM_LINT_TARGET),)
    TERRAFORM_LINT_TARGET := $(shell find . -name 'terraform.tf' | grep -v ".make" | sed 's/.terraform.tf//' | sort | uniq )
endif

.PHONY: terraform-format terraform-pre-format terraform-do-format terraform-post-format \
	terraform-lint terraform-pre-lint terraform-do-lint terraform-post-lint

terraform-format-target:
	$(TERRAFORM_VARS_BEFORE_FMT) $(TERRAFORM_RUNNER) fmt $(TERRAFORM_SWITCHES_FOR_FMT) $(TERRAFORM_LINT_TARGET)

terraform-pre-format:

terraform-post-format:

terraform-do-format:
	@for LINT_TARGET in $(TERRAFORM_LINT_TARGET); do \
		TERRAFORM_RUNNER="$(TERRAFORM_RUNNER)" \
		TERRAFORM_VARS_BEFORE_FMT="$(TERRAFORM_VARS_BEFORE_FMT)" \
		TERRAFORM_SWITCHES_FOR_FMT="$(TERRAFORM_SWITCHES_FOR_FMT)" \
		TERRAFORM_LINT_TARGET="$$LINT_TARGET" \
		make --no-print-directory terraform-format-target; \
	done;

## TARGET: terraform-format
## SYNOPSIS: make terraform-format
## HOOKS: terraform-pre-format, terraform-post-format, terraform-format-target
## VARS:
##       TERRAFORM_RUNNER=<terraform executor> - defaults to 'terraform', but could pass something like terragrunt
##       TERRAFORM_LINT_TARGET=<file or directory path to Terraform code> - defaults to empty and searches for modules
##       TERRAFORM_SWITCHES_FOR_FMT=<switches to pass to terraform fmt> - defaults to '-diff -recursive'
##       TERRAFORM_VARS_BEFORE_FMT=<env variables to pass to Terraform when calling fmt> - defaults to empty
##
##  Reformat project Terraform code in the given directories/files using terraform's fmt tool.

terraform-lint-target:
	@printf "\n\n ---- Linting $(TERRAFORM_LINT_TARGET) [$(TERRAFORM_LINT_TARGET_ID)] ---- \n\n"
	@. $(TERRAFORM_SUPPORT); \
	TERRAFORM_RUNNER="$(TERRAFORM_RUNNER)" \
	TERRAFORM_VARS_BEFORE_FMT="$(TERRAFORM_VARS_BEFORE_FMT)" \
	TERRAFORM_SWITCHES_FOR_FMT="$(TERRAFORM_SWITCHES_FOR_FMT)" \
	TERRAFORM_LINT_TARGET_ID="$(TERRAFORM_LINT_TARGET_ID)" \
	terraformCheckFormat $(TERRAFORM_LINT_TARGET) || \
	echo "$$TERRAFORM_LINT_TARGET" > build/results/$(TERRAFORM_LINT_TARGET_ID).format.failed
	@. $(TERRAFORM_SUPPORT); \
	TERRAFORM_RUNNER="$(TERRAFORM_RUNNER)" \
	TERRAFORM_VARS_BEFORE_FMT="$(TERRAFORM_VARS_BEFORE_FMT)" \
	TERRAFORM_SWITCHES_FOR_FMT="$(TERRAFORM_SWITCHES_FOR_FMT)" \
	TERRAFORM_LINT_VARS_BEFORE_INIT="$(TERRAFORM_LINT_VARS_BEFORE_INIT)" \
	TERRAFORM_LINT_SWITCHES_FOR_INIT="$(TERRAFORM_LINT_SWITCHES_FOR_INIT)" \
	TERRAFORM_LINT_VARS_BEFORE_VALIDATE="$(TERRAFORM_LINT_VARS_BEFORE_VALIDATE)" \
	TERRAFORM_LINT_SWITCHES_FOR_VALIDATE="$(TERRAFORM_LINT_SWITCHES_FOR_VALIDATE)" \
	TERRAFORM_LINT_TARGET_ID="$(TERRAFORM_LINT_TARGET_ID)" \
	terraformValidate $(TERRAFORM_LINT_TARGET) || \
	echo "$$TERRAFORM_LINT_TARGET" > build/results/$(TERRAFORM_LINT_TARGET_ID).validate.failed
	@. $(TERRAFORM_SUPPORT); \
	TERRAFORM_RUNNER="$(TERRAFORM_RUNNER)" \
	TERRAFORM_VARS_BEFORE_FMT="$(TERRAFORM_VARS_BEFORE_FMT)" \
	TERRAFORM_SWITCHES_FOR_FMT="$(TERRAFORM_SWITCHES_FOR_FMT)" \
	TERRAFORM_LINT_VARS_BEFORE_INIT="$(TERRAFORM_LINT_VARS_BEFORE_INIT)" \
	TERRAFORM_LINT_SWITCHES_FOR_INIT="$(TERRAFORM_LINT_SWITCHES_FOR_INIT)" \
	TERRAFORM_LINT_VARS_BEFORE_VALIDATE="$(TERRAFORM_LINT_VARS_BEFORE_VALIDATE)" \
	TERRAFORM_LINT_SWITCHES_FOR_VALIDATE="$(TERRAFORM_LINT_SWITCHES_FOR_VALIDATE)" \
	TERRAFORM_TFLINT_RUNNER="$(TERRAFORM_TFLINT_RUNNER)" \
	TERRAFORM_VARS_BEFORE_TFLINT="$(TERRAFORM_VARS_BEFORE_TFLINT)" \
	TERRAFORM_SWITCHES_FOR_TFLINT="$(TERRAFORM_SWITCHES_FOR_TFLINT)" \
	TERRAFORM_LINT_TARGET_ID="$(TERRAFORM_LINT_TARGET_ID)" \
	terraformLint $(TERRAFORM_LINT_TARGET) || \
	echo "$$TERRAFORM_LINT_TARGET" > build/results/$(TERRAFORM_LINT_TARGET_ID).tflint.failed

terraform-format: terraform-pre-format terraform-do-format terraform-post-format  ## format the Terraform code

terraform-pre-lint:

terraform-post-lint:

terraform-do-lint:
	@mkdir -p build/reports; rm -rf build/reports/linting-tf-*.xml;
	@rm -rf build/results; mkdir -p build/results;
	@for LINT_TARGET in $(TERRAFORM_LINT_TARGET); do \
		LINT_TARGET_ID="$$(basename $$LINT_TARGET)_mod"; \
		TERRAFORM_RUNNER="$(TERRAFORM_RUNNER)" \
		TERRAFORM_VARS_BEFORE_FMT="$(TERRAFORM_VARS_BEFORE_FMT)" \
		TERRAFORM_SWITCHES_FOR_FMT="$(TERRAFORM_SWITCHES_FOR_FMT)" \
		TERRAFORM_LINT_VARS_BEFORE_INIT="$(TERRAFORM_LINT_VARS_BEFORE_INIT)" \
		TERRAFORM_LINT_SWITCHES_FOR_INIT="$(TERRAFORM_LINT_SWITCHES_FOR_INIT)" \
		TERRAFORM_LINT_VARS_BEFORE_VALIDATE="$(TERRAFORM_LINT_VARS_BEFORE_VALIDATE)" \
		TERRAFORM_LINT_SWITCHES_FOR_VALIDATE="$(TERRAFORM_LINT_SWITCHES_FOR_VALIDATE)" \
		TERRAFORM_TFLINT_RUNNER="$(TERRAFORM_TFLINT_RUNNER)" \
		TERRAFORM_VARS_BEFORE_TFLINT="$(TERRAFORM_VARS_BEFORE_TFLINT)" \
		TERRAFORM_SWITCHES_FOR_TFLINT="$(TERRAFORM_SWITCHES_FOR_TFLINT)" \
		TERRAFORM_LINT_TARGET="$$LINT_TARGET" \
		TERRAFORM_LINT_TARGET_ID=$$LINT_TARGET_ID \
		make --no-print-directory -f $(MAKEFILE_PATH) terraform-lint-target; \
		if [ $$(ls build/results | grep "$$LINT_TARGET_ID.*.failed" | wc -l) -eq 0 ]; then echo "All good! ✨"; fi \
	done;
	@make --no-print-directory join-lint-reports || true
	@if [ $$(ls build/results | grep ".failed" | wc -l) -gt 0 ]; \
	then printf "\n\n--- \nLinting failed! ❌❌\n"; exit 1; \
	else printf "\n\n--- \nAll done! ✨ 🍰 ✨\n"; fi



## TARGET: terraform-lint
## SYNOPSIS: make terraform-lint
## HOOKS: terraform-pre-lint, terraform-post-lint, terraform-lint-target
## VARS:
##       TERRAFORM_RUNNER=<terraform executor> - defaults to 'terraform', but could pass something like terragrunt
##       TERRAFORM_LINT_TARGET=<file or directory path to Terraform code> - defaults to empty and searches for modules
##       TERRAFORM_SWITCHES_FOR_FMT=<switches to pass to terraform fmt> - defaults to '-diff -recursive'
##       TERRAFORM_VARS_BEFORE_FMT=<env variables to pass to Terraform when calling fmt> - defaults to empty
##       TERRAFORM_LINT_VARS_BEFORE_INIT=env variables to pass to Terraform when calling init> - defaults to empty
##       TERRAFORM_LINT_SWITCHES_FOR_INIT=<switches to pass to terraform fmt> - defaults to '-backend=false -compact-warnings'
##       TERRAFORM_LINT_VARS_BEFORE_VALIDATE=env variables to pass to Terraform when calling validate> - defaults to empty
##       TERRAFORM_LINT_SWITCHES_FOR_VALIDATE=<switches to pass to terraform fmt> - defaults to '-compact-warnings'
##       TERRAFORM_TFLINT_RUNNER=<tflint executor> - defaults to 'tflint'
##       TERRAFORM_VARS_BEFORE_TFLINT=<env variables to pass to tflint> - defaults to empty
##       TERRAFORM_SWITCHES_FOR_TFLINT=<switches to pass to terraform fmt> - defaults to empty
##
##  Lint Terraform code in the given directories/files using fmt and tflint.

terraform-lint: terraform-pre-lint terraform-do-lint terraform-post-lint  ## lint the Terraform code

endif
endif

