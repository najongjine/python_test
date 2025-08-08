from inference_sdk import InferenceHTTPClient

CLIENT = InferenceHTTPClient(
    api_url="https://serverless.roboflow.com",
    api_key="iWXvPKU6wZG4gB4PEeuIaaaa"
)

result = CLIENT.infer("healthy1.jpg", model_id="plants-disease-2599r/1")
print(result)