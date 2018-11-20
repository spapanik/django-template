The following packages should be installed in the system before using the template.
* sassc
* postgres
* yarn
* npm
* poetry

In order to start a new django project, create a virtual environment and do the following. The creation of the virtual environment can be deferred until the make command

```bash
$ PROJ=<actual_project_name>
$ git clone git@github.com:spapanik/django-template.git $PROJ
$ cd $PROJ
$ rm -rf .git
$ find . ! -name "readme.md" -print0 | xargs -0 sed -i "s/{{project_name}}/$PROJ/g"
$ make install
```
