# WBH - Wordlists by history
This script will create a subdomain and an files/path wordlist based on your browser history.

**Please close the browsers before running.**

*Idea came from this tweet: https://twitter.com/nil0x42/status/1318950787909849091*

## Usage

```
usage: wbh.py [-h] [-d DIRECTORY] [-l LIMIT] [-c] [-f]

Create subdomains and files wordlists from browser history

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
2753 subdomains found!
27367 paths found!
```
