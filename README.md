# WBH - Wordlists by history

```
╦ ╦╔╗ ╦ ╦
║║║╠╩╗╠═╣
╚╩╝╚═╝╩ ╩
Wordlists by history 0.1v
```

This script will create subdomains, files, parameters and domains wordlists based on your browser history.

*Works on Linux and Windows*
**Please close the browsers before running.**

*Idea came from this tweet: https://twitter.com/nil0x42/status/1318950787909849091*

## Usage

```
$ python3 wbh.py --help
usage: wbh.py [-h] [-d DIRECTORY] [-l LIMIT] [-c] [-f]

Create subdomains, files, parameters and domains wordlists from browser history

optional arguments:
  -h, --help            show this help message and exit
  -d DIRECTORY, --directory DIRECTORY
                        Directory to save the wordlists
  -l LIMIT, --limit LIMIT
                        Limit of characters. Default: 40
  -c, --chrome          Use Google Chrome to make the wordlists
  -f, --firefox         Use Firefox to make the wordlists

```

```
$ python3 wbh.py
10 subdomains found!
59 files found!
31 parameters found!
18 domains found!
``
