#!/usr/bin/env python

import argparse
import os
import re
import sys
import jsbeautifier
from Crypto.Cipher import AES


class AssetCryptImplFile:
    def __init__(self, file):
        if '.source "AssetCryptImpl.java"\n' not in file:
            raise ValueError
        self.file = file
        self.asset_ranges = self._read_asset_ranges()
        self.encrypted_data = self._read_encrypted_data()
        self.cipher = AES.new(key=self.encrypted_data[-0x10:], mode=AES.MODE_ECB)

    def get_asset_list(self):
        return list(self.asset_ranges.keys())

    def get_asset_data(self, asset):
        range = self.asset_ranges[asset]
        decrypted = self.cipher.decrypt(self.encrypted_data[range[0]:range[0] + range[1]]).decode('utf-8')
        return decrypted[:-ord(decrypted[-1])]  # Removes padding

    def _read_asset_ranges(self):
        asset_list = {}
        for match in re.finditer('invoke-direct \{v\d+, v(\d+), v(\d+)\}, L(.+)/(.+)/(.+)/AssetCryptImpl\$Range;-><init>', self.file):
            sub_file = self.file[:match.start()]
            file_name = re.findall('const-string v1, "(.+)"', sub_file)[-1]
            start = re.findall('const(/\d+)? v%d, 0x([0-9a-fA-F]+)' % int(match.group(1)), sub_file)[-1][1]
            length = re.findall('const(/\d+)? v%d, 0x([0-9a-fA-F]+)' % int(match.group(2)), sub_file)[-1][1]
            asset_list[file_name] = (int(start, 16), int(length, 16))
        return asset_list

    def _read_encrypted_data(self):
        encrypted_data = ''.join(re.findall('const-string v1, "(.+)"\s+invoke-virtual \{v0, v1\}, Ljava/nio/CharBuffer;->append', self.file))
        return encrypted_data.encode('utf-8').decode('unicode_escape').encode('iso-8859-1')


def main():
    parser = argparse.ArgumentParser(description='extracts encrypted javascript source files from a Appcelerator Titanium android app')
    parser.add_argument('inputfile', help='path to AssetCryptImpl.smali file', type=argparse.FileType('r'))
    parser.add_argument('-o', '--output', help='path to output directory', default='output')
    parser.add_argument('-b', '--beautify', help='beautify javascript files', action='store_true', default=False)
    parser.add_argument('-q', '--quiet', help='hide file list', action='store_true', default=False)
    args = vars(parser.parse_args())

    try:
        acif = AssetCryptImplFile(args['inputfile'].read())
    except ValueError:
        sys.exit('invalid input file')

    output_path = os.path.normpath(args['output']) + '/'
    if not os.path.isdir(output_path):
        os.makedirs(output_path)
    elif os.listdir(output_path):
        sys.exit('output directory not empty')

    for asset in acif.get_asset_list():
        asset_data = acif.get_asset_data(asset)
        dir_path = output_path + os.path.dirname(asset)
        if not os.path.isdir(dir_path):
            os.makedirs(dir_path)
        with open(output_path + asset, 'wb') as file:
            if args['beautify']:
                asset_data = jsbeautifier.beautify(asset_data)
            file.write(asset_data.encode('utf-8'))
        if not args['quiet']:
            print(asset)

if __name__ == '__main__':
    main()