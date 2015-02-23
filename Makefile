.PHONY: clean tests upload-release

VERSION=$(shell cat s3_encryption/VERSION)

tests:
	@nosetests -vx

upload-release:
	@$(MAKE) tests
	@git tag $(VERSION)
	@git push --tags origin master
	@python setup.py sdist upload -r pypi
