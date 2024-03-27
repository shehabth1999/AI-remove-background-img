from django.shortcuts import render
from django.http import JsonResponse
from rm_bg.models import ProcessedImage
from rest_framework.decorators import api_view
import requests
from django.core.files.base import ContentFile
import os

PROCESSED_IMAGE = 'processed_image.png' 

def remove_processed_image_from_root():
    processed_image_path = PROCESSED_IMAGE
    if os.path.exists(processed_image_path):
        os.remove(processed_image_path)
        print(f"Processed image '{processed_image_path}' removed successfully from the root directory.")
    else:
        print(f"Processed image '{processed_image_path}' does not exist in the root directory.")



@api_view(['POST'])
def process_image(request):
    if request.method == 'POST':
        image_file = request.FILES.get('image')
        if image_file:
            api_key = 'g4k388JgSSt3B9a8zpMaNsj7'
            api_endpoint = 'https://api.remove.bg/v1.0/removebg'

            # Send POST request to Remove.bg API
            response = requests.post(
                api_endpoint,
                files={'image_file': image_file},
                data={'size': 'auto'},
                headers={'X-Api-Key': api_key},
            )
            if response.status_code == requests.codes.ok:
                processed_image_data = response.content

                processed_image_path = PROCESSED_IMAGE
                with open(processed_image_path, 'wb') as out:
                    out.write(processed_image_data)
                
                processed_image = ProcessedImage.objects.create(image=image_file)
                
                # Set the result_image field to the processed image data
                processed_image.result_image.save(PROCESSED_IMAGE, ContentFile(processed_image_data))

                # Return the URL of the processed image
                remove_processed_image_from_root()
                domain = request.get_host()
                return JsonResponse({'processed_image_url' : f'{request.scheme}://{domain}{processed_image.result_image.url}'})
            else:
                return JsonResponse({'error': 'Failed to process image'}, status=response.status_code)
        else:
            return JsonResponse({'error': 'Empty image file'}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)