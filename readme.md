The following packages should be installed in the system before using the template.
* sassc
* postgres
* yarn
* npm
* poetry

* PROJ=<actual_project_name>
* git clone git@github.com:spapanik/django-template.git $PROJ
* cd $PROJ
* rm -rf .git
* find . ! -name "readme.md" -print0 | xargs -0 sed -i "s/{{project_name}}/$PROJ/g"
