import boto3
import json
from prompts.devops_prompt import get_devops_prompt

class BedrockService:

````
def __init__(self, region_name="us-east-1"):
    self.client = boto3.client(
        service_name="bedrock-runtime",
        region_name=region_name
    )

    self.model_id = "amazon.nova-pro-v1:0"

def generate_artifact(self, user_prompt):

    try:
        prompt = get_devops_prompt(user_prompt)

        request_body = {
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "text": prompt
                        }
                    ]
                }
            ],
            "inferenceConfig": {
                "maxNewTokens": 4000,
                "temperature": 0.1,
                "topP": 0.9
            }
        }

        response = self.client.invoke_model(
            modelId=self.model_id,
            body=json.dumps(request_body),
            accept="application/json",
            contentType="application/json"
        )

        response_body = json.loads(
            response["body"].read().decode("utf-8")
        )

        print("BEDROCK RESPONSE")
        print(json.dumps(response_body, indent=2))

        generated_text = response_body["output"]["message"]["content"][0]["text"]

        return self._parse_response(generated_text)

    except Exception as e:

        import traceback

        traceback.print_exc()

        return {
            "type": "Bedrock Error",
            "file_name": "error.txt",
            "code": str(e),
            "explanation": "Failed to invoke Bedrock model",
            "compliance": ""
        }

def _parse_response(self, text):

    try:

        cleaned = text.strip()

        if cleaned.startswith("```json"):
            cleaned = cleaned.replace("```json", "")
            cleaned = cleaned.replace("```", "")

        data = json.loads(cleaned)

        return {
            "type": data.get("artifactType", "Unknown"),
            "file_name": data.get("fileName", "generated.txt"),
            "code": data.get("code", ""),
            "explanation": data.get("explanation", ""),
            "compliance": "\n".join(
                data.get("compliance", [])
            )
        }

    except Exception as e:

        return {
            "type": "Raw Output",
            "file_name": "output.txt",
            "code": text,
            "explanation": f"JSON Parse Error: {str(e)}",
            "compliance": ""
        }
````
