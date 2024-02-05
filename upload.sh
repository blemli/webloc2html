pytest
api_token=$(op item get "pypi api key" --field "Anmeldedaten")
python3 -m pip install --upgrade twine
python3 -m pip install --upgrade build
rm -rf dist/*
python3 -m build
python3 -m twine upload --repository pypi dist/* --user __token__ --password $api_token
pip install --upgrade $(basename $(pwd))