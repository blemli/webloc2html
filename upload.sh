pytest
#abort if not all tests pass
if [ $? -ne 0 ]; then
  echo "Tests must pass before uploading to PyPI"
  exit 1
fi
#todo: update version in pyproject.toml
api_token=$(op item get "pypi api key" --field "Anmeldedaten")
python3 -m pip install --upgrade twine
python3 -m pip install --upgrade build
rm -rf dist/*
python3 -m build
python3 -m twine upload --repository pypi dist/* --user __token__ --password $api_token
pip install --upgrade $(basename $(pwd))