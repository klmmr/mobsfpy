# MobSFpy

_Python CLI and wrapper for the Mobile Security Framework (MobSF) REST-API_ 

[Mobile Security Framework (MobSF)](https://github.com/MobSF/Mobile-Security-Framework-MobSF) is an automated framework
for security analysis of mobile apps.
It offers also a REST API which allows much flexibility.
The idea of this package is to allow for easier handling of MobSF when it is used on the command line.
It also allows integrating MobSF in your Python project.
With MobSFpy it should be easy to automate the analysis of many apps because you do not have to load them all manually
into MobSF. 


_WARNING:_ At the moment this package is work in progress.
So feedback is welcome!

## Installation

Currently, this package is not available via PyPI (maybe this will come at a later point of time).
But you can install directly from source on GitHub.  

Clone from GitHub and install using PIP:

    git clone https://github.com/klmmr/mobsfpy.git && cd mobsfpy
    pip install .
    
If you want to install it for development, you can also install with the `-e` option. 
(All changes in code are directly available.)

    pip install -e .

## Usage

`mobsfpy` can be used either as a standalone commandline tool or as a Python package which can be used in your own code.

### CLI

Hint: You will need an REST API key for your MobSF instance.
It is displayed in the logs of MobSF or can be retrieved from `http://<Server-IP/Hostname>:8000/api_docs`.
Best practice is to set the API-Key using `MOBSF_API_KEY` environment variable.



```bash
# Upload an app to MobSF
mobsf upload example.apk

# Upload if server is not running on http://127.0.0.1:8000/ and give REST API key explicit
mobsf -k 7e98...2a37 -s http://example.org upload example.apk

# Scan a file
mobsf scan apk example.apk <MD5 Hash of APK>

# Retrieve scan results
mobsf report <MD5 Hash of APK> json
# And save to file
mobsf report <MD5 Hash of APK> json -o result.json

# Getting help
mobsf -h
mobsf upload -h
```

You can get help everytime using the `-h` command.

### Python Package

You can import the package in your code and access the methods of the `mobsf` class.

```python
from mobsfpy import MobSF

# Give API key
mobsf = MobSF('7e98...2a37')

mobsf.upload('example.apk')
mobsf.scan('apk', 'example.apk', '<MD5 Hash of APK>')
mobsf.report_json('<MD5 Hash of APK>')
```

## License

This software is licensed under MIT license. For more information see `LICENSE` file.

## Acknowledgements

* [Ajin Abraham (@ajinabraham)](https://github.com/ajinabraham) and [many others](https://github.com/MobSF/Mobile-Security-Framework-MobSF#honorable-contributors) - For creating MobSF.
* This package is inspired by [this gist](https://gist.github.com/ajinabraham/0f5de3b0c7b7d3665e54740b9f536d81).
