import requests
import hashlib


def request_api_data(query_char):
    url = "https://api.pwnedpasswords.com/range/" + str(query_char)

    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(
            f"Error fetching: {res.status_code} check the Api and try Again"
        )
    return res


def read_response(response):
    print(response.text)


def pwned_api_check(password):
    sha1password = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
    firts5_char, tail = sha1password[:5], sha1password[5:]
    response = request_api_data(firts5_char)
    # print(response)
    return read_response(response)


if __name__ == "__main__":

    pwned_api_check("123")
