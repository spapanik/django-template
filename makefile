COPYFLAGS = -n
SETTINGS_MODULE = settings.local
SETTINGS = --settings=$(SETTINGS_MODULE)
INPUT = --no-input
INTERACTIVE = --non-interactive
CSS_TYPE = nested

SCSS_FILES = $(wildcard */static/css/*.scss)
CSS_FILES = $(foreach name,$(basename $(SCSS_FILES)),$(name).css)
PO_FILES = $(wildcard locale/*/LC_MESSAGES/django.po)
MO_FILES = $(foreach po_file,$(basename $(PO_FILES)),$(po_file).mo)

# tl; dr version
# make install: Install project from scratch
# make update: Update requirements, migrations, translations, static files
# make fmt: Format the project using black
# make clean: Delete python caches, .orig files
# make static: Build the necessary .js and .css files
# make translations: Build the .mo files


.PHONY: update
update: requirements.txt migrations translations static

.PHONY: install
install: settings/local.py db update

.PHONY: fmt
fmt:
	black .

.PHONY: clean
clean:
	find . -type f -name "*.orig" -delete

settings/local.py: settings/local.py.template
	cp $(COPYFLAGS) $^ $@

.PHONY: db
db:
	createdb {{project_name}} 2> /dev/null || true

.PHONY: migrations
migrations:
	./manage.py migrate $(SETTINGS) $(INPUT)

poetry.lock: pyproject.toml
	poetry lock

requirements.txt: poetry.lock
	PIP_NO_BINARY="psycopg2" poetry install $(POETRY_EXTRA)
	poetry show | awk '{print $$1"=="$$2}' > $@

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
	python manage.py collectstatic $(SETTINGS) $(INPUT) -i "*.scss" $(STATIC_EXTRA)

.PHONY: static
static: js_requirements.txt css staticfiles

locale/%/LC_MESSAGES/django.mo: locale/%/LC_MESSAGES/django.po
	python manage.py compilemessages --locale=$*

.PHONY: translations
translations: $(MO_FILES)
