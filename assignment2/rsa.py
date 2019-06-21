def encrypt_rsa(m,key):
    [e,n]=key
    if e==1:
        return m % n
    elif e%2==1 :
        return ((encrypt_rsa(m,(int(e/2),n)) ** 2)* m)%n
    else :
        return (encrypt_rsa(m,(int(e/2),n)) ** 2)%n

def decrypt_rsa(m,key):
    [d,n]=key
    if d==1:
        return m % n
    elif d%2 ==1:
        return ((decrypt_rsa(m,(int(d/2),n))**2)*m)% n
    else:
        return (decrypt_rsa(m,(int(d/2),n))**2)% n

def encrypt(data,private_key):
    new_data=[]
    for d in data:
        new_data.append(encrypt_rsa(d,private_key))
    return new_data


def decrypt(data,public_key):
    new_data=[]
    for d in data:
        new_data.append(decrypt_rsa(d,public_key))
    return new_data


if __name__=="__main__":
    m=[125,111,100,9,90]
    c=encrypt(m,(7,187))
    m=decrypt(c,(23,187))
    print(m)
