# 🤖 Smart Image Analysis API (Serverless & AI-Powered)
This project is a serverless API that uses Azure AI Vision to automatically describe and tag images. It is built with a "Security-First" mindset, utilizing Managed Identities to handle service-to-service communication without hardcoded keys.

# 🚀 Features
AI-Powered Analysis: Automatically generates captions and tags for uploaded images.

Infrastructure as Code (IaC): The entire cloud environment is defined using Azure Bicep.

CI/CD Pipeline: Fully automated deployments via GitHub Actions.

Serverless Scalability: Built on Azure Functions for cost-efficient, on-demand scaling.

# 🏗️ Architecture
The system follows a modern cloud-native workflow:

User sends a POST request with an image.

Azure Function (Python) processes the request.

Azure AI Vision analyzes the image content.

JSON Response is returned with a description, confidence score, and tags.

# 🛠️ Tech Stack
Cloud: Microsoft Azure

Language: Python 3.11

AI Service: Azure AI Vision (Cognitive Services)

DevOps: GitHub Actions, Bicep, Azure CLI

# ⚡ How to Use
Once deployed, you can test the API using curl or Postman:

Bash
curl -X POST https://your-app-name.azurewebsites.net/api/analyze \
  -H "Content-Type: application/octet-stream" \
  --data-binary "@photo.jpg"
Example Response (The Lotus Flower Test)
JSON
{
  "description": "a close up of a pink lotus flower with green leaves",
  "confidence": 0.985,
  "tags": ["flower", "pink", "lotus", "nature", "petal"]
}
