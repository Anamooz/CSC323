import os, time
from Crypto import Hash
from Crypto.Hash import SHA
from Crypto.Hash import HMAC as hmac
import sys


class HMAC:
    def __init__(self):
        self.key = os.urandom(SHA.digest_size)
        self.timeout = float(sys.argv[1])

    def hmac_sha1_sign(self, key, msg):
        h = hmac.new(key, msg, SHA)
        return h.digest()

    def hmac_sha1_verify(self, key, msg, tag):
        h = hmac.new(key, msg, SHA)
        tag_new = h.digest()
        # An obvious check
        if len(tag) != len(tag_new):
            return False
        # Now, for extra security, check each byte, one at a time
        for i in range(len(tag)):
            if tag[i] != tag_new[i]:
                return False
            else:
                print("Sleeping for 0.1 seconds")
                time.sleep(self.timeout)
        return True

    def verify_query(self, msg, tag):
        try:
            ret = self.hmac_sha1_verify(
                self.key, bytes(msg, "utf-8"), bytes.fromhex(tag)
            )
        except:
            ret = False
        return ret

    def mac_query(self, msg):
        return self.hmac_sha1_sign(self.key, msg).hex()
