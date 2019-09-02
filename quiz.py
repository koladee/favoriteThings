from cryptography.fernet import Fernet


def quiz():
    key = 'TluxwB3fV_GWuLkR1_BzGs1Zk90TYAuhNMZP_0q4WyM='

    # Oh no! The code is going over the edge! What are you going to do?
    message = b'gAAAAABdbQaJKitS3SO7uy4miEiRhnn6zegMWdZYEOJu2gNnIhC-jdZLjjjUMbqIUYNHFcs2jZzRsIHcxqNm9t5eAP'/
              b'XrosEXS0kJ5Wdt60Q3TBeIh1MECdBJfjCVvBbpEemrNKqzG3TzdhC_ZaNKaQ__MXGpinpotlcUATFPxtl2tAMUZxaJtlM='
    f = Fernet(key)
    r = f.decrypt(message)
    print(r)


if __name__ != "__main__":
    quiz()
