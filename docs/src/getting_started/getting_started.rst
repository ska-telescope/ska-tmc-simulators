===============
Getting started
===============

This page contains instructions for software developers who want to get
started with usage and development of the Simulators.

Background
----------
Detailed information on how the SKA Software development
community works is available at the `SKA software developer portal <https://developer.skao.int/en/latest/>`_.
There you will find guidelines, policies, standards and a range of other
documentation.

Set up your development environment
-----------------------------------
This project is structured to use k8s for development and testing so that the build environment, test environment and test results are all completely reproducible and are independent of host environment. It uses ``make`` to provide a consistent UI (run ``make help`` for targets documentation).
