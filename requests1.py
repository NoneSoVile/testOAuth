import requests,sys

if len(sys.argv) > 1:
    url = sys.argv[1]
else:
    url = 'https://example.com'
response = requests.get(url)

print(response.status_code)  # Print the HTTP status code
print(response.text)         # Print the content of the response
