"""MOBSF REST API Python wrapper"""

import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder

import logging

logger = logging.getLogger(__name__)

DEFAULT_SERVER = 'http://127.0.0.1:8000'


class MobSF:
    """Represents a MobSF instance."""

    def __init__(self, apikey, server=None):
        self.__server = server.rstrip('/') if server else DEFAULT_SERVER
        self.__apikey = apikey

    @property
    def server(self):
        return self.__server

    @property
    def apikey(self):
        return self.__apikey

    def upload(self, file):
        """Upload an app."""
        logger.debug(f"Uploading {file} to {self.__server}")

        multipart_data = MultipartEncoder(fields={'file': (file, open(file, 'rb'), 'application/octet-stream')})
        headers = {'Content-Type': multipart_data.content_type, 'Authorization': self.__apikey}

        r = requests.post(f'{self.__server}/api/v1/upload', data=multipart_data, headers=headers)

        return r.json()

    def scan(self, scantype, filename, scanhash, rescan=False):
        """Scan already uploaded file.

        If the file was not uploaded before you will have to do so first.
        """
        logger.debug(f"Requesting {self.__server} to scan {scanhash} ({filename}, {scantype})")

        post_dict = {'scan_type': scantype,
                     'file_name': filename,
                     'hash': scanhash,
                     're_scan': rescan}

        headers = {'Authorization': self.__apikey}

        r = requests.post(f'{self.__server}/api/v1/scan', data=post_dict, headers=headers)

        return r.json()

    def scans(self, page=1, page_size=100):
        """Show recent scans."""
        logger.debug(f'Requesting recent scans from {self.__server}')

        payload = {'page': page,
                   'page_size': page_size}
        headers = {'Authorization': self.__apikey}

        r = requests.get(f'{self.__server}/api/v1/scans', params=payload, headers=headers)

        return r.json()

    def report_pdf(self, scanhash, pdfname=None):
        """Retrieve and store a scan report as PDF."""
        pdfname = pdfname if pdfname else 'report.pdf'

        logger.debug(f'Requesting PDF report for scan {scanhash}')

        headers = {'Authorization': self.__apikey}
        data = {'hash': scanhash}

        r = requests.post(f'{self.__server}/api/v1/download_pdf', data=data, headers=headers, stream=True)

        logger.debug(f'Writing PDF report to {pdfname}')
        with open(pdfname, 'wb') as pdf:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    pdf.write(chunk)

        logger.info(f'Report saved as {pdfname}')

        return pdfname

    def report_json(self, scanhash):
        """Retrieve JSON report of a scan."""
        logger.debug(f'Requesting JSON report for scan {scanhash}')

        headers = {'Authorization': self.__apikey}
        data = {'hash': scanhash}

        r = requests.post(f'{self.__server}/api/v1/report_json', data=data, headers=headers)

        return r.json()

    def view_source(self, scantype, filename, scanhash):
        """Retrieve source files of a scan."""
        logger.debug(f'Requesting source files for {scanhash} ({filename}, {scantype})')

        headers = {'Authorization': self.__apikey}
        data = {'type': scantype,
                'hash': scanhash,
                'file': filename}

        r = requests.post(f'{self.__server}/api/v1/view_source', data=data, headers=headers)

        return r.json()

    def delete_scan(self, scanhash):
        """Delete a scan result."""
        logger.debug(f'Requesting {self.__server} to delete scan {scanhash}')

        headers = {'Authorization': self.__apikey}
        data = {'hash': scanhash}

        r = requests.post(f'{self.__server}/api/v1/delete_scan', data=data, headers=headers)

        return r.json()
