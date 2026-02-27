import azure.functions as func
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.core.credentials import AzureKeyCredential

def main(req: func.HttpRequest) -> func.HttpResponse:
    image_data = req.get_body()
    
    # 1. Initialize AI Client (credentials pulled from Environment Variables)
    client = ImageAnalysisClient(endpoint=AI_ENDPOINT, credential=AzureKeyCredential(AI_KEY))
    
    # 2. Analyze Image
    result = client.analyze(image_data, visual_features=["Tags", "Description"])
    
    # 3. Return results as JSON
    return func.HttpResponse(f"I see: {result.description.captions[0].text}")
    