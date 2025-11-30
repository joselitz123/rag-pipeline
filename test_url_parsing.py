import urllib.parse

def parse_azure_uri(uri):
    parsed = urllib.parse.urlparse(uri)
    
    # Extract endpoint
    endpoint = f"{parsed.scheme}://{parsed.netloc}"
    
    # Extract deployment name
    path_parts = parsed.path.strip("/").split("/")
    try:
        deployments_index = path_parts.index("deployments")
        deployment_name = path_parts[deployments_index + 1]
    except (ValueError, IndexError):
        deployment_name = None
        
    # Extract API version
    query_params = urllib.parse.parse_qs(parsed.query)
    api_version = query_params.get("api-version", [None])[0]
    
    return {
        "endpoint": endpoint,
        "deployment_name": deployment_name,
        "api_version": api_version
    }

# Test case
uri = "https://my-project.cognitiveservices.azure.com/openai/deployments/gpt-5-nano/chat/completions?api-version=2024-05-01-preview"
result = parse_azure_uri(uri)

print(f"Input URI: {uri}")
print(f"Parsed Result: {result}")

expected = {
    "endpoint": "https://my-project.cognitiveservices.azure.com",
    "deployment_name": "gpt-5-nano",
    "api_version": "2024-05-01-preview"
}

assert result == expected, f"Expected {expected}, got {result}"
print("Test Passed!")
