install:
	pip install .

run:
	python -m switchpokepilot

regenerate-pyinstaller-spec:
	flet pack switchpokepilot/__main__.py \
	  --name SwitchPokePilot

pack:
	pyinstaller ./SwitchPokePilot.spec --noconfirm --clean
	rm -f ./dist/SwitchPokePilot
	cp -R ./examples/SwitchPokePilot ./dist/SwitchPokePilot
