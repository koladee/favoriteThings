from cryptography.fernet import Fernet


def quiz():
    key = 'TluxwB3fV_GWuLkR1_BzGs1Zk90TYAuhNMZP_0q4WyM='

    # Oh no! The code is going over the edge! What are you going to do?
    message = b'gAAAAABc-TORPfaj_2JPeQWNgNrHfxvio8ZaINBFH6NwdEsSfan12qHgpn9GBXhuQSQBHQso35N-qfnYbyDgg6S7BWZqZ-93' \
              b'JBnnWgVM4FOHEFcneVhTjc3LTvf3ksM-EthQb2f8uT3hLKihjVEkC53a9j4lZztI3qMBMT4mx17CsRpM6AhAqh0='

    f = Fernet(key)
    r = f.decrypt(message)
    print(r)


if __name__ != "__main__":
    quiz()
