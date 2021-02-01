import json
import os

from webapp.api.Response import Response

def delete_book_entry(book_entry_id, edit_key):

    response = Response(True, 'Messaggio cancellato! Clicca su Chiudi per tornare ai messaggi.')

    folder_path = 'webapp/static/book_contents'
    path = f'{folder_path}/book.json'

    try:
        book_data = {}        

        if os.path.exists(path):
            with open(path) as json_file:  
                book_data = json.load(json_file)
        else:
            raise Exception('No book found')        

        matching_entry = next((entry for entry in book_data['book_entries'] if entry['id'] == book_entry_id), None)

        if matching_entry is not None:
            # Stop execution and return exception if the edit key doesn't match
            if edit_key != matching_entry['edit_key']:
                raise Exception('Il codice di modifica non corrisponde')

            book_data['book_entries'].remove(matching_entry)

            with open(path, 'w') as f:
                json.dump(book_data, f) 
        
        
    except Exception as e:
        response.status = False
        response.message = str(e)

    return response.compose()


