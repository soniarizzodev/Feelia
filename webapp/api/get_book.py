import json
import os

from webapp.api.Response import Response

def get_book(user):

    response = Response(True, 'Book retrieved successfully')

    path = 'webapp/static/book_contents/book.json'

    try:
        book_data = None

        if os.path.exists(path):
            with open(path) as json_file:  
                book_data = json.load(json_file)

        if book_data is not None:
            for entry in book_data['book_entries']:
                # Hide flagged entries for users with limited visibility
                if 'hide' in entry and user.role == 3:
                    book_data['book_entries'].remove(entry)
                    continue

                del entry['edit_key']

            response.add('book', book_data)

        else:
            response.status = False
            response.message = 'No book found'
        
    except Exception as e:
        response.status = False
        response.message = str(e)

    return response.compose()


