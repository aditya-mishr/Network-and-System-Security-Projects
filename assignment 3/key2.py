from Crypto import Random
import Crypto
from Crypto.PublicKey import RSA


def export_key_3(private_server):
        f = open('privatekeyserver.pem','wb')
        f.write(private_server.exportKey(format='PEM'))
        f.close()

def export_key_4(public_server):
        f = open('publickeyserver.pem','wb')
        f.write(public_server.exportKey(format='PEM'))
        f.close()



if __name__ == '__main__':

    rand = Random.new().read
    private_server=RSA.generate(1024,rand)
    print(private_server)
    public_server=private_server.publickey()
    print(public_server)
    export_key_3(private_server)
    export_key_4(public_server)
