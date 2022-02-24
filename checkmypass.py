#This is a password checker! Please run on your terminal the following code:
#checkmypass.py your_password_to_be_checked
#ps: This program allows you to check multiple passwords. You just need to separate them into spaces.

#Modules
import requests
import hashlib
import sys

#This function request pswnedpasswords.com API to check if your password was found on their database
def request_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching: {res.status_code}, check the API and try again.')
    return res

#Your password will be hashed (encrypted). This allow you to check your pass without giving it to their database
def get_password_leaks_count(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0

#The API just need a little piece of the hashed password to check. This function take the necessary part to make sure greater security.
def pwned_api_check(password):
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1password[:5], sha1password[5:]
    response = request_api_data(first5_char)
    return get_password_leaks_count(response, tail)

#Program output
def main(args):
    for password in args:
        count = pwned_api_check(password)
    if count:
        print(f'{password} was found {count} times... You should probably your password')
    else:
        print(f'{password} was not found. Carry on!')
    return 'done!'

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))