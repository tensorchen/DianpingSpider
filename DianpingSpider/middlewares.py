import base64
import random

from settings import PROXIES
from settings import USER_AGENTS

class RandomUserAgent(object):


    def process_request(self, request, spider):
        request.headers.setdefault('User-Agent', random.choice(USER_AGENTS))


class ProxyMiddleware(object):

    def process_request(self, request, spider):
        request.meta['proxy'] = "http://%s" % random.choice(PROXIES)
#        proxy_user_pass = "tensor:92598866"

#        encode_user_pass = base64.encodestring(proxy_user_pass)
#        request.headers['Proxy-Authorization'] = 'Basic' + proxy_user_pass
