import boto3
import json
from prompts.devops_prompt import get_devops_prompt


class BedrockService:

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
                    "maxTokens": 4000,
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

        def _clean_text(raw_text):
            cleaned = raw_text.strip()
            if cleaned.startswith("```json"):
                cleaned = cleaned.replace("```json", "", 1)
            if cleaned.startswith("```"):
                cleaned = cleaned[3:]
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]
            return cleaned.strip()

        def _normalize_artifact(item):
            if not isinstance(item, dict):
                return None
            return {
                "artifactType": item.get("artifactType", "Unknown"),
                "fileName": item.get("fileName", "generated.txt"),
                "code": item.get("code", "") or "",
                "explanation": item.get("explanation", "") or "",
                "compliance": item.get("compliance", []) or []
            }

        cleaned = _clean_text(text)
        artifacts = []

        try:
            data = json.loads(cleaned)

            if isinstance(data, dict) and isinstance(data.get("artifacts"), list):
                artifacts = [
                    _normalize_artifact(item)
                    for item in data["artifacts"]
                    if isinstance(item, dict)
                ]
            elif isinstance(data, list):
                artifacts = [
                    _normalize_artifact(item)
                    for item in data
                    if isinstance(item, dict)
                ]
            elif isinstance(data, dict):
                artifact = _normalize_artifact(data)
                if artifact:
                    artifacts = [artifact]
        except json.JSONDecodeError:
            decoder = json.JSONDecoder()
            index = 0
            text_len = len(cleaned)

            while index < text_len:
                while index < text_len and cleaned[index].isspace():
                    index += 1
                if index >= text_len:
                    break
                if cleaned[index] not in "[{":
                    next_obj = cleaned.find("{", index)
                    if next_obj == -1:
                        break
                    index = next_obj
                try:
                    obj, offset = decoder.raw_decode(cleaned[index:])
                    if isinstance(obj, dict) and isinstance(obj.get("artifacts"), list):
                        artifacts.extend([
                            _normalize_artifact(item)
                            for item in obj["artifacts"]
                            if isinstance(item, dict)
                        ])
                    elif isinstance(obj, list):
                        artifacts.extend([
                            _normalize_artifact(item)
                            for item in obj
                            if isinstance(item, dict)
                        ])
                    elif isinstance(obj, dict):
                        artifact = _normalize_artifact(obj)
                        if artifact:
                            artifacts.append(artifact)
                    index += offset
                except json.JSONDecodeError:
                    break

        if artifacts:
            return {"artifacts": artifacts}

        return {
            "artifacts": [
                {
                    "artifactType": "Raw Output",
                    "fileName": "output.txt",
                    "code": text,
                    "explanation": "JSON Parse Error: Failed to decode Bedrock response",
                    "compliance": []
                }
            ]
        }