import os
import shutil

from webloc2html import convert_all,convert

def webloc(url, filename):
    """

    :param url:
    :param filename:
    :return:
    """
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, 'w') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">\n')
        f.write('<plist version="1.0">\n')
        f.write('<dict>\n')
        f.write('    <key>URL</key>\n')
        f.write('    <string>' + url + '</string>\n')
        f.write('</dict>\n')
        f.write('</plist>\n')
        print('Created:', filename)

def test_includes_subdirectories():
    # create a webloc file inside a subdirectory
    webloc('https://google.com','tests/fixtures/subdirectory/google.webloc')
    convert_all(path='tests/fixtures',silent=True)
    assert os.path.exists('tests/fixtures/subdirectory/google.html')
    #shutil.rmtree('tests/fixtures')

def test_url_doesnt_change():
    # create a webloc file inside a subdirectory
    webloc('https://google.com','tests/fixtures/google.webloc')
    convert('tests/fixtures/google.webloc')
    with open('tests/fixtures/google.html') as f:
        data = f.read()
    assert 'https://google.com' in data
    #shutil.rmtree('tests/fixtures')


def test_weird_url():
    # create a webloc file inside a subdirectory
    webloc('http://user:pw@localhost:8080','tests/fixtures/localhost.webloc')
    convert('tests/fixtures/localhost.webloc')
    with open('tests/fixtures/localhost.html') as f:
        data = f.read()
    assert 'http://user:pw@localhost:8080' in data
    #shutil.rmtree('tests/fixtures')

def test_ask_before_overwriting_existing_html():
    pass
    #todo: how to implement?


def test_deletes_webloc():
    # create a webloc file inside a subdirectory
    webloc('https://google.com','tests/fixtures/google.webloc')
    convert('tests/fixtures/google.webloc')
    assert not os.path.exists('tests/fixtures/google.webloc')
    #shutil.rmtree('tests/fixtures')

def test_deletes_webloc_subdirectory():
    # create a webloc file inside a subdirectory
    webloc('https://google.com','tests/fixtures/subdirectory/google.webloc')
    convert('tests/fixtures/subdirectory/google.webloc')
    assert not os.path.exists('tests/fixtures/subdirectory/google.webloc')
    #shutil.rmtree('tests/fixtures')


def test_relative_path_outside_cwd():
    # Setup: Determine an outside directory and create a webloc file there
    outside_dir = '../../outside_test_directory'
    webloc_url = 'https://example.com'
    filename = 'outside_relative_path_test.webloc'
    full_path = os.path.join(outside_dir, filename)

    # Ensure the outside directory exists
    os.makedirs(outside_dir, exist_ok=True)

    # Create a webloc file at the calculated relative path
    webloc(webloc_url, full_path)

    # Act: Convert the .webloc file using its relative path from the current working directory
    convert(full_path)

    # Assert: Check if the corresponding .html file exists in the same outside directory
    expected_html_path = os.path.join(outside_dir, 'outside_relative_path_test.html')
    assert os.path.exists(expected_html_path), f"{expected_html_path} should exist after conversion."

    # Optional: Read the .html file to check if it contains the correct URL
    with open(expected_html_path) as f:
        data = f.read()
    assert webloc_url in data, f"The URL in the converted file should be {webloc_url}."

    # Cleanup: Optionally remove the test files and directory to clean up the test environment
    # os.remove(full_path)
    # os.remove(expected_html_path)
    # os.rmdir(outside_dir)  # Make sure the directory is empty before removing it
