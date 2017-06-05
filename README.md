## titanium_decrypt
titanium_decrypt extracts the encrypted Javascript source files from an Appcelarator Titanium android app.
This tool is based on [these blackhat conference slides](https://www.blackhat.com/docs/asia-15/materials/asia-15-Grassi-The-Nightmare-Behind-The-Cross-Platform-Mobile-Apps-Dream.pdf).

### Requirements
You need to install the following:

* Python 2 or 3
* pycrypto library
* jsbeautifier library
* apktool or other dex disassembler to smali

### Instalation
Run `pip install git+https://github.com/wiez/titanium_decrypt.git`

### Usage
First, disassemble the apk file to smali format. Using apktool execute `apktool d <appname.apk>`.

Find the AssetCryptImpl.smali file. If your app's package name is com.companyname.applicationname,
the file is located in `appname/smali/com/companyname/applicationname/`.

Finally, extract the encrypted source files using `titanium_decrypt <path to AssetCryptImpl.smali file>`.

The output path (default `output/`) can be set with the `-o` option.

Source files contain no whitespaces. If you want to format the files using jsbeautifier, pass the `-b` option.
