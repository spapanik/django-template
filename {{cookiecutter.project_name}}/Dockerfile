FROM spapanik/django-api:1.0.0

ENV DJANGO_USER=reinhardt
ENV WEBSERVER="/home/${DJANGO_USER}/volteras"
ENV DJANGO_SETTINGS_MODULE={{cookiecutter.project_name}}.settings
ENV webserver_netloc="0.0.0.0:8000"

USER ${DJANGO_USER}

COPY --chown=${DJANGO_USER}:${DJANGO_USER} . ${WEBSERVER}

WORKDIR ${WEBSERVER}

RUN yam -bf install_py

CMD yam -bf -r5 migrations && \
    yam -bf runserver
