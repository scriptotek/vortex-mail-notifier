Enkelt script for epostvarsling når det kommer en ny Vortex-side i en WebDav-mappe.

`config.ini`-eksempel:

```
[webdav]
host=dav.myserver.com
username=gollum
password=verysecret

[mailgun]
domain=myserver.com
key=some-long-key

[page]
path=/path/to/folder
body=New page just appeared at http://url.to/folder
subject=Wow!
sender=Gollum <gollum@myserver.com>
recipient=sauron@myserver.com
```
