#!/bin/sh

# to get this url, do a search on leboncoin and copy/paste the url
url='https://www.leboncoin.fr/recherche/?category=55&locations=dn_75&price=50-200'
cookie="$(cat cookie)"

curl -s "$url" -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:76.0) Gecko/20100101 Firefox/76.0' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' -H 'Accept-Language: en-US,en;q=0.5' --compressed -H 'Referer: https://www.leboncoin.fr/' -H 'Connection: keep-alive' -H "Cookie: $cookie" -H 'Upgrade-Insecure-Requests: 1' -H 'Cache-Control: max-age=0' | fgrep 'window.__REDIAL_PROPS__ =' | sed -e 's/^  window\.__REDIAL_PROPS__ = \[null,null,null,null,null,//' -e 's/]$//'
