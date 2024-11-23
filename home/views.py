from django.shortcuts import render
import requests
import json

def index(request):
    return render(request, 'home/index.html')

def index_form(request):
    if request.method == 'POST':
        long_url = request.POST.get('long_url')
        if long_url:
            new_url = shorten_url(long_url)
            print(f"Shortened URL: {new_url}")
            return render(request, "home/new_url.html", context={'url': new_url})
        else:
            # Handle empty URL input
            return render(request, "home/index.html", context={'error': 'Please provide a URL to shorten.'})
    return render(request, 'home/index.html')

# Function to shorten the URL
def shorten_url(url):
    headers = {
        'Authorization': 'Bearer 5bd0675cfdd98b4b4d25a80d1e02e2fc68d96404',  # Ensure this token is valid
        'Content-Type': 'application/json',  # Correct header for content type
    }

    data_dict = {'long_url': url, 'domain': 'bit.ly'}
    data = json.dumps(data_dict)  # Convert the dictionary to JSON format

    # Sending POST request to Bitly API
    response = requests.post('https://api-ssl.bitly.com/v4/shorten', headers=headers, data=data)

    if response.status_code == 200:
        # If request is successful, parse the response and return the shortened URL
        response_dict = response.json()  # .json() is a built-in method for parsing JSON response
        return response_dict.get('link', 'Error: Link not found in response.')
    else:
        # If there's an error, print the error message or return a default error message
        print(f"Error: {response.status_code} - {response.text}")
        return 'Error: Unable to shorten URL. Please try again later.'

