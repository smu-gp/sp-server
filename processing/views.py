from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse

import io
import re
import os
from google.oauth2 import service_account

def detect_document(path):
    from google.cloud import vision
    credentials = service_account.Credentials.from_service_account_file('/home/pmp/myoungjin/balmy-particle-246206-23eecc6f950a.json')
    client = vision.ImageAnnotatorClient()
    
    with io.open(path,'rb') as image_file:
        content = image_file.read()
        
    image = vision.types.Image(content=content)

    response = client.document_text_detection(image=image)
    
    text=""
    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    for symbol in word.symbols:
                        text+=symbol.text
                        if(symbol.property.detected_break.type == 1):
                            text+=' '
                        if(symbol.property.detected_break.type == 2):
                            text+='\t'
                        if(symbol.property.detected_break.type == 3):
                            text+='\n'
                        if(symbol.property.detected_break.type == 5):
                            text+='\n'
                            
    sentence_list = text.split('\n')
    sentence_list.pop()
    return sentence_list




def process(request):
    if request.method == 'POST':
        image = request.FILES['image']
        fs = FileSystemStorage()
        saved_name = fs.save(image.name, image)
        image_url = fs.url(saved_name)
        path = (os.getcwd())
        sentence_list = detect_document(path + image_url)
        
        response = [
            #{"type": "image", "content": image_url},
            #{"type": "text", "content": word_list[0]},
        ]
        
        for n in sentence_list:
            response.append({"type": "text", "content": n})
        
        if os.path.isfile(path+image_url):
           os.remove(path+image_url)
           print(path+image_url+" delete complete!")
        
        return JsonResponse(response, safe=False)
    else:
        return JsonResponse({'error': 'Please request post'})
