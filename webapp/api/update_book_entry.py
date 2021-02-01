import json
import os
import random
import string

from webapp.api.Response import Response

def update_book_entry(new_entry, media):

    response = Response(True, 'Tutto a posto! Clicca su Chiudi per tornare ai messaggi.')

    folder_path = 'webapp/static/book_contents'
    path = f'{folder_path}/book.json'

    try:
        book_entry = json.loads(new_entry)
        book_data = {}

        if not os.path.exists(folder_path):
            os.mkdir(folder_path)

        if os.path.exists(path):
            with open(path) as json_file:  
                book_data = json.load(json_file)

        else:
            book_data['book_entries'] = []

        is_new = False

        existing_entry = next((entry for entry in book_data['book_entries'] if entry['id'] == book_entry['id']), None)

        if existing_entry is not None:
            # Stop execution and return exception if the edit key doesn't match
            if book_entry['edit_key'] != existing_entry['edit_key']:
                raise Exception('Il codice di modifica non corrisponde')

            existing_entry['author'] = book_entry['author']
            existing_entry['message'] = book_entry['message']
            existing_entry['video_path'] = book_entry['video_path']
            existing_entry['image_path'] = book_entry['image_path']

            if media is not None and 'video' in media:
                saved_video_path = save_media(media['video'], existing_entry['id'])
                
                if saved_video_path is not None:
                    existing_entry['video_path'] = saved_video_path

            if media is not None and 'image' in media:
                saved_image_path = save_media(media['image'], existing_entry['id'])
                
                if saved_image_path is not None:
                    existing_entry['image_path'] = saved_image_path

        else:
            is_new = True
            book_entry['id'] = assign_id(book_data['book_entries']);
            book_entry['edit_key'] = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))   
            
            if media is not None and 'video' in media:
                saved_video_path = save_media(media['video'], book_entry['id'])
                
                if saved_video_path is not None:
                    book_entry['video_path'] = saved_video_path

            if media is not None and 'image' in media:
                saved_image_path = save_media(media['image'], book_entry['id'])
                
                if saved_image_path is not None:
                    book_entry['image_path'] = saved_image_path

            book_data['book_entries'].append(book_entry)
           
       
        with open(path, 'w') as f:
            json.dump(book_data, f) 
            
        if is_new:           
            response.add('id', book_entry['id'])
            response.add('edit_key', book_entry['edit_key'])

        response.add('is_new', is_new)
        
    except Exception as e:
        response.status = False
        response.message = str(e)

    return response.compose()

def save_media(media, id):

    try:
        folder_path = 'webapp/static/book_contents'

        extension = media.filename.split('.')[-1]

        new_name = f'{str(id)}.{extension}'

        media.save(f'{folder_path}/{new_name}')

        return new_name

    except Exception as e:
        return None

def assign_id(book_entries):
    new_id = 1
    if len(book_entries) > 0:
        last_id = book_entries[-1]['id']
        new_id = last_id + 1

    return new_id