"""Commandline interface for MobSF REST API"""

import argparse
import json
import logging
import os

from mobsfpy.mobsf import MobSF, DEFAULT_SERVER

__API_KEY_ENV_VAR = 'MOBSF_API_KEY'


def __cli_upload(args):
    mobsf = MobSF(args.apikey, args.server)
    result = mobsf.upload(args.file)

    print(result)


def __cli_scan(args):
    mobsf = MobSF(args.apikey, args.server)
    result = mobsf.scan(args.scantype, args.filename, args.hash, rescan=args.rescan)

    print(result)


def __cli_scans(args):
    mobsf = MobSF(args.apikey, args.server)
    result = mobsf.scans(args.page, args.pagesize)

    print(result)


def __cli_report_json(args):
    mobsf = MobSF(args.apikey, args.server)
    result = mobsf.report_json(args.hash)

    if args.output:
        if args.output is True:
            filename = f'report_{args.hash}.json'
        else:
            filename = args.output

        with open(filename, 'w') as f:
            json.dump(result, f, indent=4)
    else:
        print(json.dumps(result, indent=4))


def __cli_report_pdf(args):
    filename = args.output if args.output else f'report_{args.hash}.pdf'

    mobsf = MobSF(args.apikey, args.server)
    result = mobsf.report_pdf(args.hash, pdfname=filename)

    print(f'Wrote report to {result}')


def __cli_view_source(args):
    mobsf = MobSF(args.apikey, args.server)
    result = mobsf.scan(args.scantype, args.filename, args.hash)

    print(result)


def __cli_delete(args):
    mobsf = MobSF(args.apikey, args.server)
    result = mobsf.delete_scan(args.hash)

    print(result)


def __configure_logger(verbosity):
    logger = logging.getLogger()

    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    logger.setLevel(logging.WARNING)

    if verbosity == 1:
        logger.setLevel(logging.INFO)
    elif verbosity >= 2:
        logger.setLevel(logging.DEBUG)


def main():
    parser = argparse.ArgumentParser(prog='mobsf', description='CLI for using the MobSF REST-API')

    parser.add_argument('--server', '-s', default=DEFAULT_SERVER, type=str,
                        help=f"Server where MobSF is running. If not given, '{DEFAULT_SERVER}' is assumed.")
    parser.add_argument('--apikey', '-k', type=str, default=os.environ.get(__API_KEY_ENV_VAR),
                        help=f"The REST-API-Key for the MobSF instance. Can also be specified as environment variable "
                             f"using '{__API_KEY_ENV_VAR}'")
    parser.add_argument('--verbose', '-v', action='count', default=0, help='Increase verbosity')

    subparsers = parser.add_subparsers(title='Subcommands',
                                       description='This CLI supports a number of different subcommands which have to '
                                                   'be used.',
                                       help='Available subcommands',
                                       dest='command',
                                       required=True)

    parser_upload = subparsers.add_parser('upload', help='Upload a file to MobSF')
    parser_upload.add_argument('--noscan', action='store_true', help='Execute no scan after upload')
    parser_upload.add_argument('file', type=str, help='The file to upload')
    parser_upload.set_defaults(func=__cli_upload)

    parser_scan = subparsers.add_parser('scan', help='Scan a uploaded file with MobSF')
    parser_scan.add_argument('--rescan', '-r', action='store_true', help='Rescan the app, default is false')
    parser_scan.add_argument('scantype', type=str, choices=['apk', 'zip', 'ipa', 'appx'], help='Scan type')
    parser_scan.add_argument('filename', type=str, help='The file to scan')
    parser_scan.add_argument('hash', type=str, help='Hash of the scan')
    parser_scan.set_defaults(func=__cli_scan)

    parser_scans = subparsers.add_parser('scans', help='List recent scans')
    parser_scans.add_argument('--page', '-p', type=int, default=1)
    parser_scans.add_argument('--pagesize', '-s', type=int, default=100)
    parser_scans.set_defaults(func=__cli_scans)

    parser_report = subparsers.add_parser('report', help='Retrieve report of scan')
    parser_report.add_argument('hash', type=str, help='Hash of the scan')

    subparsers_report = parser_report.add_subparsers(title='Type',
                                                     description='The format which should be used for the report',
                                                     help='Type of report',
                                                     dest='report_type',
                                                     required=True)

    parser_report_json = subparsers_report.add_parser('json')
    parser_report_json.add_argument('--output', '-o', type=str, const=True, nargs='?',
                                    help="The file in which the report should be stored. If option is used wihtout "
                                         "specifying a file, 'report_<scanhash>.json' is assumed.")
    parser_report_json.set_defaults(func=__cli_report_json)

    parser_report_pdf = subparsers_report.add_parser('pdf')
    parser_report_pdf.add_argument('--output', '-o', type=str,
                                   help="The file in which the report should be stored. If not given, 'report.pdf' "
                                        "is assumed.")
    parser_report_pdf.set_defaults(func=__cli_report_pdf)

    parser_view_source = subparsers.add_parser('source', help='View source code of a scan')
    parser_view_source.add_argument('scantype', type=str, choices=['apk', 'zip', 'ipa', 'appx'], help='Scan type')
    parser_view_source.add_argument('filename', type=str, help='The file to scan')
    parser_view_source.add_argument('hash', type=str, help='Hash of the scan')
    parser_view_source.set_defaults(func=__cli_view_source)

    parser_delete = subparsers.add_parser('delete', help='Delete scan results')
    parser_delete.add_argument('hash', type=str, help='Hash of the scan')
    parser_delete.set_defaults(func=__cli_delete)

    args = parser.parse_args()
    print(args)

    if not args.apikey:
        parser.print_usage()
        exit(f"You have to give an API-Key using '--apikey' for MobSF or you have to define it in an environment "
             f"variable named '{__API_KEY_ENV_VAR}'.")

    __configure_logger(args.verbose)

    # Call the functions of the subparsers (previously definet by set_defaults())
    args.func(args)
