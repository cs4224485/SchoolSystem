import hashlib, requests, random, string, json
from django.conf import settings


class UserService(object):
    @staticmethod
    def geneAuthCode(bond_info=None):
        m = hashlib.md5()
        str = "%s-%s-%s" % (bond_info.id, bond_info.salt, bond_info.status)
        m.update(str.encode("utf-8"))
        return m.hexdigest()

    @staticmethod
    def geneSalt(length=16):
        keylist = [random.choice((string.ascii_letters + string.digits)) for i in range(length)]
        return ("".join(keylist))

    @staticmethod
    def getWeChatOpenId(code):
        url = "https://api.weixin.qq.com/sns/jscode2session?appid={0}&secret={1}&js_code={2}&grant_type=authorization_code" \
            .format(settings.MINA_APP['appid'], settings.MINA_APP['appkey'], code)
        r = requests.get(url)
        res = json.loads(r.text)
        openid = None
        if 'openid' in res:
            openid = res['openid']
        return openid
