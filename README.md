## redgifs-dl
A command line tool to download videos from redgifs.com

# Installation

```shell
git clone https://github.com/boobfuck/redgifs-dl/blob/main/redgifs.py
chmod +x redgifs.py
./redgifs
```
```console
usage: redgifs.py [-h] [-f] [-q | -w  | -ns]
                  [url]

Download videos from redgifs.com
Version: 1.2.0

positional arguments:
  url             The gif URL. If you want
                  to use [--file] flag then
                  this is can be omitted.

optional arguments:
  -h, --help      show this help message and
                  exit
  -f , --file     File path of the URLs to
                  download. A file need to
                  be passed when using this
                  flag.
  -q, --quite     No verbose outputs.
  -w, --wait      Wait for some seconds
                  between each request
                  (while using -f). Default:
                  6.9
  -ns, --no-save  Don't save the video, just
                  return the MP4 URL.
```

## Quick tutorial

To download a single video using its URL.
```console
$ ./redgifs.py [url]
```

Example:
```console
$ ./redgifs.py https://redgifs.com/TheFooBars
```

### `--file <file>`

To download multiple videos, the URLs should be added to a file.  

-----
- File: `urls.txt`
```
https://redgifs.com/TheFooBars
https://www.redgifs.com/PythonGoodJavaBad
...
```
-----

Then use the `--file` flag and specify the file.  

Example:
```console
$ ./redgifs.py --file urls.txt
```

### `--wait <seconds>`
By default, the script waits for 6.9 seconds between each request to the URLs when using `--file`. If you want to change this, use this flag.

Example:
```console
$ # to wait for 4.20 seconds between each requests
$ ./redgifs.py --file urls.txt --wait 4.20
```

### `--no-save`
When `--no-save` flag is used it returns the MP4 URL of the video/videos instead of downloading it.

### `--quite`
Using this flag does not show verbose outputs.
