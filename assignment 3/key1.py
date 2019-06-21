from Crypto import Random
import Crypto
from Crypto.PublicKey import RSA

def export_key_1(private_client):
        f = open('privatekeyclient.pem','wb')
        f.write(private_client.exportKey(format='PEM'))
        f.close()

def export_key_2(public_client):
        f = open('publickeyclient.pem','wb')
        f.write(public_client.exportKey(format='PEM'))
        f.close()


if __name__ == '__main__':
    rand = Random.new().read
    private_client=RSA.generate(1024,rand)
    print(private_client)
    public_client=private_client.publickey()
    print(public_client)
    export_key_1(private_client)
    export_key_2(public_client)
