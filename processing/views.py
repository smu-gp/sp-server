from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse

import io
import re

def detect_document(path):
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()
    
    with io.open(path,'rb') as image_file:
        content = image_file.read()
    image = vision.types.Image(content=content)

    response = client.document_text_detection(image=image)
    word_list=[]
    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            #print('\nBlock \n')
        
            for paragraph in block.paragraphs:
                #print('Paragraph ')
            
                for word in paragraph.words:
                    word_text=''.join([symbol.text for symbol in word.symbols])
                    #print('Word text: {} '.format(word_text))
                    word_list.append(word_text)

                    #for symbol in word.symbols:
                        #print('\tSymbol: {} '.format(symbol.text))
    return word_list




def process(request):
    if request.method == 'POST':
        image = request.FILES['image']
        fs = FileSystemStorage()
        saved_name = fs.save(image.name, image)
        image_url = fs.url(saved_name)
        path = (os.getcwd())
        word_list = detect_document(path + image_url)
        
        response = [
            {"type": "text", "content": "Success!"},
            {"type": "text", "content": "cropLeft: " + request.POST['cropLeft']},
            {"type": "text", "content": "cropTop: " + request.POST['cropTop']},
            {"type": "text", "content": "cropRight: " + request.POST['cropRight']},
            {"type": "text", "content": "cropBottom: " + request.POST['cropBottom']},
            {"type": "image", "content": image_url},
            {"type": "text", "content": word_list[0]},
        ]
        return JsonResponse(response, safe=False)
    else:
        return JsonResponse({'error': 'Please request post'})
