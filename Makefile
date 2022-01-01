run:
	python3 -uB ./app/app.py

new:
	rm -f ants.db
	python3 -uB ./app/app.py

docs:
	pdoc3 --html ./app/*.py
	mv ./html ./doc

scenarios:
	python3 -uB ./tests/test_scenarios.py

test-logic:
	python3 -uB ./tests/test_ants.py

pep8:
	pycodestyle test/*.py
	pycodestyle app/*.py

profile:
	python3 -m cProfile app/$(file).py > $(file)-profile.txt

clean:
	pyclean .
	rm -rf doc