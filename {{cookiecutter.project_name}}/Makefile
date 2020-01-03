SETTINGS = settings.local
PYTHONPATH = $(CURDIR)/src
ADMIN = DJANGO_SETTINGS_MODULE=$(SETTINGS) PYTHONPATH=$(PYTHONPATH) django-admin
INPUT = --no-input
INTERACTIVE = --non-interactive
CSS_TYPE = nested

TEST_FLAGS = -vv --reuse-db --cov=src
TEST_PATH = tests

DB_NAME = {{cookiecutter.db_name}}

SCSS_FILES = $(wildcard */static/css/*.scss)
CSS_FILES = $(foreach name,$(basename $(SCSS_FILES)),$(name).css)
PO_FILES = $(wildcard locale/*/LC_MESSAGES/django.po)
MO_FILES = $(foreach po_file,$(basename $(PO_FILES)),$(po_file).mo)

CONF = $(subst template.,local.,$(shell find . -type f -name "template.*"))

ifneq ("$(wildcard ./env.json)","")
    USE_ENV = -j env.json
endif

# tl; dr version
# make install: Install project from scratch
# make update: Update requirements, migrations, translations, static files
# make format: Format the project using black and isort
# make static: Build the necessary .js and .css files
# make translations: Build the .mo files

.PHONY: update
update: $(filter-out db, install)

.PHONY: install
install: requirements.txt configuration db migrations static

poetry.lock: pyproject.toml
	poetry lock

requirements.txt: poetry.lock
	poetry install $(POETRY_EXTRA)
	poetry export --without-hashes -f requirements.txt -o $@

.PHONY: format
format:
	isort --recursive .
	black .

.PHONY: lint
lint:
	flake8 .
	isort --check-only --recursive .
	black --check .

.PHONY: db
db:
	createdb $(DB_NAME) 2> /dev/null || true

.PHONY: migrations
migrations:
	$(ADMIN) migrate $(INPUT)

%.css: %.scss
	sassc -t $(CSS_TYPE) $^ $@

.PHONY: css
css: $(CSS_FILES)

yarn.lock: package.json
	yarn generate-lock-entry > $@

js_requirements.txt: yarn.lock
	yarn install $(INTERACTIVE) $(YARN_EXTRA)
	npm ls --depth=0 | awk 'NF {print $$2}' > $@

.PHONY: staticfiles
staticfiles:
	$(ADMIN) collectstatic $(INPUT) -i "*.scss" $(STATIC_EXTRA)

.PHONY: static
static: js_requirements.txt css staticfiles

.PHONY: configuration
configuration: $(CONF)

src/settings/local.%: src/settings/template.%
	test ! -f $@ || cp $@ $@.backup
	yashiro -t $^ $(USE_ENV) > $@

etc/nginx/servers/local.%: etc/nginx/servers/template.%
	yashiro -t $^ $(USE_ENV) > $@

etc/systemd/system/local.%: etc/systemd/system/template.%
	yashiro -t $^ $(USE_ENV) > $@

etc/tmpfiles.d/local.%: etc/tmpfiles.d/template.%
	yashiro -t $^ $(USE_ENV) > $@

locale/%/LC_MESSAGES/django.mo: locale/%/LC_MESSAGES/django.po
	$(ADMIN) compilemessages --locale=$*

.PHONY: translations
translations: $(MO_FILES)

.PHONY: tests
tests:
	py.test $(TEST_FLAGS) $(TEST_PATH)
