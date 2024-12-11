# Modified server.py for testing without secret.py

MENU = '''
YALM (Yet Another Lost Modulus):

1. Get secret
2. Test encryption
3. Exit
'''

class YALM:

    def __init__(self):
        self.e = 3
        # Placeholder value for N (use a large number for testing)
        self.n = 1234567890123456789012345678901234567890
        # Placeholder flag message for testing
        self.flag = "TEST_FLAG{This_is_a_test_flag}"

    def get_secret(self):
        message = f'Hey! This is my secret... it is secure because RSA is extremely strong and very hard to break... Here you go: {self.flag}'
        m = int(message.encode().hex(), 16)
        c = pow(m, self.e, self.n)

        return hex(c)

    def test_encryption(self):
        plaintext = input('Plaintext: ').strip()

        m = int(plaintext, 16)
        cs = []

        while m:
            c = pow(m, self.e, self.n)
            cs.append(c)
            m //= self.n

        if len(cs) > 1:
            return 'Too many messages!'

        return 'Thanks for the message!'


def main():
    yalm = YALM()

    while True:
        print(MENU)

        try:
            option = int(input('Option: '))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if option == 1:
            print(f'Ciphertext: {yalm.get_secret()}')
        elif option == 2:
            print(yalm.test_encryption())
        else:
            print("Exiting.")
            break


if __name__ == '__main__':
    main()

