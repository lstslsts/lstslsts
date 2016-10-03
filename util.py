"""
Authy has positioned itself as the clear rival to Google Authenticator, and right off the bat, 
it does have one clear advantage. It offers to back up all of your saved accounts, in case you have to wipe the phone,
or if you change phones. This is it does by encrypting the information and storing it in the cloud.

Authy also distinguishes itself by offering a desktop app, as well as the smartphone version. 
So you don’t have to be handcuffed to your phone if you don’t want to. Service name, it's length and 2-permutation should be used. 

Instead, you can get your codes directly from your desktop computer screen. 
If you don’t own a smartphone or tablet, Authy is particularly useful, allowing you
to finally use 2FA.
"""

import urllib
import urllib2
import time
import json

from urlparse import parse_qsl
import oauth2 as oauth
from httplib2 import RedirectLimit

class TumblrRequest(object):
    """
    A simple request object that lets us query the Tumblr API
    """

    __version = "0.0.7";

    def __init__(self, consumer_key, consumer_secret="", oauth_token="", oauth_secret="", host="https://api.tumblr.com"):
        self.host = host
        self.consumer = oauth.Consumer(key=consumer_key, secret=consumer_secret)
        self.token = oauth.Token(key=oauth_token, secret=oauth_secret)
        self.headers = {
            "User-Agent" : "pytumblr/" + self.__version
        }

    def get(self, url, params):
        """
        Issues a GET request against the API, properly formatting the params
        :param url: a string, the url you are requesting
        :param params: a dict, the key-value of all the paramaters needed
                       in the request
        :returns: a dict parsed of the JSON response
        """
        url = self.host + url
        if params:
            url = url + "?" + urllib.urlencode(params)

        client = oauth.Client(self.consumer, self.token)
        try:
            client.follow_redirects = False
            resp, content = client.request(url, method="GET", redirections=False, headers=self.headers)
        except RedirectLimit, e:
            resp, content = e.args

        return self.json_parse(content)

    def post(self, url, params={}, files=[]):
        """
        Issues a POST request against the API, allows for multipart data uploads
        :param url: a string, the url you are requesting
        :param params: a dict, the key-value of all the parameters needed
                       in the request
        :param files: a list, the list of tuples of files
        :returns: a dict parsed of the JSON response
        """
        url = self.host + url
        try:
            if files:
                return self.post_multipart(url, params, files)
            else:
                client = oauth.Client(self.consumer, self.token)
                resp, content = client.request(url, method="POST", body=urllib.urlencode(params), headers=self.headers)
                return self.json_parse(content)
        except urllib2.HTTPError, e:
            return self.json_parse(e.read())

    def json_parse(self, content):
        """
        Wraps and abstracts content validation and JSON parsing
        to make sure the user gets the correct response.
        
        :param content: The content returned from the web request to be parsed as json
        
        :returns: a dict of the json response
        """
        try:
            data = json.loads(content)
        except ValueError, e:
            data = {'meta': { 'status': 500, 'msg': 'Server Error'}, 'response': {"error": "Malformed JSON or HTML was returned."}}
        
        #We only really care about the response if we succeed
        #and the error if we fail
        if data['meta']['status'] in [200, 201, 301]:
            return data['response']
        else:
            return data

    def post_multipart(self, url, params, files):
        """
        Generates and issues a multipart request for data files
        :param url: a string, the url you are requesting
        :param params: a dict, a key-value of all the parameters
        :param files:  a list, the list of tuples for your data
        :returns: a dict parsed from the JSON response
        """
        #combine the parameters with the generated oauth params
        params = dict(params.items() + self.generate_oauth_params().items())
        faux_req = oauth.Request(method="POST", url=url, parameters=params)
        faux_req.sign_request(oauth.SignatureMethod_HMAC_SHA1(), self.consumer, self.token)
        params = dict(parse_qsl(faux_req.to_postdata()))

        content_type, body = self.encode_multipart_formdata(params, files)
        headers = {'Content-Type': content_type, 'Content-Length': str(len(body))}

        #Do a bytearray of the body and everything seems ok
        r = urllib2.Request(url, bytearray(body), headers)
        content = urllib2.urlopen(r).read()
        return self.json_parse(content)

    def encode_multipart_formdata(self, fields, files):
        """
        Properly encodes the multipart body of the request
        :param fields: a dict, the parameters used in the request
        :param files:  a list of tuples containing information about the files
        :returns: the content for the body and the content-type value
        """
        import mimetools
        import mimetypes
        BOUNDARY = mimetools.choose_boundary()
        CRLF = '\r\n'
        L = []
        for (key, value) in fields.items():
            L.append('--' + BOUNDARY)
            L.append('Content-Disposition: form-data; name="{0}"'.format(key))
            L.append('')
            L.append(value)
        for (key, filename, value) in files:
            L.append('--' + BOUNDARY)
            L.append('Content-Disposition: form-data; name="{0}"; filename="{1}"'.format(key, filename))
            L.append('Content-Type: {0}'.format(mimetypes.guess_type(filename)[0] or 'application/octet-stream'))
            L.append('Content-Transfer-Encoding: binary')
            L.append('')
            L.append(value)
        L.append('--' + BOUNDARY + '--')
        L.append('')
        body = CRLF.join(L)
        content_type = 'multipart/form-data; boundary={0}'.format(BOUNDARY)
        return content_type, body

    def generate_oauth_params(self):
        """
        Generates the oauth parameters needed for multipart/form requests
        :returns: a dictionary of the proper headers that can be used
                  in the request
        """
        params = {
            'oauth_version': "1.0",
            'oauth_nonce': oauth.generate_nonce(),
            'oauth_timestamp': int(time.time()),
            'oauth_token': self.token.key,
            'oauth_consumer_key': self.consumer.key
        }
return params

"""


========== кодо хостинги
гитхаб, битбакет

=========== free хостинги с ftp
нет таких в природе похоже

===веб хостинги
фри сайты с https?
https://infinityfree.net/ растет посещаемость, owncloud хапрещен
https://byet.host/

инсталяторы фантастико софтакулос закки

фантастико
эти 10 гб фри дают но адреса нет реселлеры?
https://squirrel-host.com/index.html

https://www.000webhost.com
оба! Fantastico/Softaculous
5000 алекса

весьма популярный
https://x10hosting.com/
30 000 алекса

http://runhosting.com/ =co.nf
170 000 ((

zacky installer v-сильно урезан по сравн с softaculous в кот есть owncloud 
http://biz.ht/
http://www.curhost.com/free-web-hosting.html


===================
1 гб
http://support.filesanywhere.com/entries/23427177-WebDAV-for-Windows-8-Users


https://www.free-hidrive.com/product/overview.html
5 gb дает webdove

webdove - фи
loudSafe provides WebDAV via SSL at port 443 only. WebDAV access via insecure http access at port 80 is blocked. Every user access to a safe uses a dedicated, unique URL, e.g. https://123456789.webdav.cloudsafe.com/


только http а хочется  https? -У НИХ НЕТ ФРИ -ОТ 1 ДОЛЛ В МЕС
https://www.cloudme.com/en/webdav/linux

этот не фри но имеет webdav -90 дней триал
https://www.myworkdrive.com/pricing-plans/

https://www.mydrive.ch/
100 Мб только для фри дает(

https://www.free-hidrive.com/product/overview.html
пароль до 20 симв!
5 гб вебдав
WebDAV (also via SSL) !!
быстрый!
Но дает для входа домен 5 уровня что плохо: https://твоёимя.webdav.hidrive.strato.com/

https://webdav.cubby.com/

5 gb free
https://webdav.opendrive.com/

https://my.powerfolder.com

дает на защищенный паролем (!) вход вида
https://длинная-случайна-строка.webdav.drivehq.com
и ограничение на файлы-100 мб

5 гб фри
https://www.idrivesync.com/webdav

https://cloud.zaclys.com/  1 гб но еще и некстклауд!!

1 gb free
https://hostiso.com/owncloud-hosting/

3 гб
https://www.blaucloud.de/en

2 г
https://www.blaucloud.de/en/singup-and-product-tableы

https://my.owndrive.com/remote.php/webdav/
1 гб

500 мб фри
https://woelkli.com/en

http://support.filesanywhere.com/entries/23427177-WebDAV-for-Windows-8-Users

webdav 5 гб
https://dav.idrivesync.com

7 гб
https://docs.live.net/35C151A17F6CBблабла


2Гб  и календарь дает.
https://www.cloudvault.ch/home#


========================== текст хостинги
хорошее место хранить что то простое под паролем ="запароленный текст-хостинг"
https://www.protectedtext.com/

этот позволяет без пароля залить текстовый файл потом его скачать! Но ссылку дает не запоминаемую
Uploading is easy using curl 
$ curl --upload-file ./hello.txt https://transfer.sh/hello.txt 
https://transfer.sh/66nb8/hello.txt 

http://pasted.co/register/
надо регится ибо ссылку дает неудобную для запоминания

http://textuploader.com/
просит регится, ссылка открыта

========== картинки

имгур выкладывает открытый скрипт для загрузки
http://askubuntu.com/questions/146888/software-for-imgur-image-upload

фри фотохостингов не много- фликр имгур и этот
https://unsplash.com/

===========хостинги скриншотов не годятся – он их делаес сам не позваоляя свое грузить


=== хранилища ключей
https://pgp.mit.edu/
https://sks-keyservers.net
https://pgp.key-server.io
http://keyserver.pgp.com






==== старт страницы
http://www.igoogleportal.com/ увы. Прекратили

http://www.netvibes.com
rss-ки и много виджетов по api к службам-напр можно поиск в твиттере или фб настроить

https://www.thedash.com/explore
много виджетов. экономика сша но все на англ.

почти все виджеты с популярных сервисов. море
http://www.cyfe.com/

==== страница всех радио с текущей передачей?
http://moskva.fm/radio/monte-karlo
http://www.moreradio.org/online_radio/monte_carlo_fm/
http://station.ru/stations/montecarlo
сетка передач http://echo.msk.ru/schedule/


==== rss from site
https://feed43.com/
 
http://www.makeuseof.com/tag/12-best-yahoo-pipes-alternatives-look/

http://feedity.com/builder.aspx
- с ростом в алекске
http://fetchrss.com/generator?url=meduza.io


=============блогохостинги ===
тумблер 500 K symbols limit (?) домен 3 уровня, как и soup.io
медиум гуд


===mail==
openmailbox.org
vfemail.com
inbx.lv
gmx.com

"""
