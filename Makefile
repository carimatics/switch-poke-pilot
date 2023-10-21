install:
	pip install -r requirements.txt

run:
	python -m switchpokepilot

regenerate-pyinstaller-spec:
	flet pack switchpokepilot/__main__.py \
	  --name SwitchPokePilot \
	  --add-data "assets:assets"

pack:
	pyinstaller ./SwitchPokePilot.spec --noconfirm --clean
