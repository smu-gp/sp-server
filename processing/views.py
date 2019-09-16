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
    sentence_list=[]
    sentence=""
    
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
            for i in word_list:
                if(i != '.'):
                    sentence = sentence + i + " "
                else:
                    sentence_list.append(sentence)
                    sentence=""

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
            {"type": "text", "content": "Success!"},
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
