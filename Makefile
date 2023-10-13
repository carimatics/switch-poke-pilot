install:
	pip install -r requirements.txt

run:
	SWITCH_POKE_PILOT_PACKED=false python -m switchpokepilot

regenerate-pyinstaller-spec:
	flet pack switchpokepilot/__main__.py \
	  --name SwitchPokePilot \
	  --add-data "assets:assets"

pack:
	pyinstaller ./SwitchPokePilot.spec --noconfirm --clean
