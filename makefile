default: run

setup:
	pip install -r requirements.txt --no-index --find-links=file:///$(DESTDIR)

run:
	python2 runserver.py

init-db:
	python2 scripts/init-db.py

.PHONY: no_targets__ list
no_targets__:
list:
	sh -c "$(MAKE) -p no_targets__ | awk -F':' '/^[a-zA-Z0-9][^\$$#\/\\t=]*:([^=]|$$)/ {split(\$$1,A,/ /);for(i in A)print A[i]}' | grep -v '__\$$' | sort"
