import requests

def make_post_request(url, data=None, headers=None, timeout=10):
   
    try:
        # Set default headers if not provided
        if headers is None:
            headers = {"Content-Type": "application/json"}
            
        # Make the POST request
        response = requests.post(url, json=data, headers=headers, timeout=timeout)
        
        # Raise an exception for 4XX/5XX status codes
        response.raise_for_status()
        
        # Try to return JSON, otherwise return text
        try:
            return response.json()
        except ValueError:
            return response.text
            
    except requests.RequestException as e:
        print(f"Error making POST request: {e}")
        raise

# Example usage with parameters:
def restart_esp(ip, port=8080, api_key="poqob"):
    url = f"http://{ip}:{port}/restart"
    data = {"api_key": api_key}
    
    try:
        result = make_post_request(url, data)
        return result
    except Exception as e:
        print(f"Error restarting ESP: {e}")
        return None