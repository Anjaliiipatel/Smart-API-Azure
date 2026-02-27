import azure.functions as func
import logging
import os
import json
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential

app = func.FunctionApp()

@app.route(route="analyze", auth_level=func.AuthLevel.ANONYMOUS)
def smart_analyze(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Processing image analysis request.')

    try:
        # 1. Get image from request body
        image_data = req.get_body()
        if not image_data:
            return func.HttpResponse("Please upload an image in the request body.", status_code=400)

        # 2. Get credentials from Environment Variables (set by Bicep)
        endpoint = os.environ["VISION_ENDPOINT"]
        key = os.environ["VISION_KEY"]

        # 3. Initialize the AI Vision Client
        client = ImageAnalysisClient(
            endpoint=endpoint, 
            credential=AzureKeyCredential(key)
        )

        # 4. Analyze the image
        result = client.analyze(
            image_data=image_data,
            visual_features=[VisualFeatures.CAPTION, VisualFeatures.TAGS, VisualFeatures.OBJECTS],
        )

        # 5. Build a friendly response
        response_data = {
            "description": result.caption.text if result.caption else "No description found",
            "confidence": result.caption.confidence if result.caption else 0,
            "tags": [tag.name for tag in result.tags.list] if result.tags else []
        }

        return func.HttpResponse(
            json.dumps(response_data),
            mimetype="application/json",
            status_code=200
        )

    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return func.HttpResponse(f"Analysis failed: {str(e)}", status_code=500)