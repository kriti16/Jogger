from flask_restful import Api as _Api

# some custom errors
class RoomDoesNotExist(Exception):
    pass

CUSTOM_ERRORS = {
'RoomDoesNotExist': {
        'message': "A room by that name does not exist.",
        'status': 404,
    },
}

class Api(_Api):
    def error_router(self, original_handler, e):
        """ Override original error_router to only custom errors and parsing error (from webargs)"""
        error_type = type(e).__name__.split(".")[-1] # extract the error class name as a string
        # if error can be handled by flask_restful's Api object, do so
        # otherwise, let Flask handle the error
        # the 'UnprocessableEntity' is included only because I'm also using webargs
        # feel free to omit it
        if self._has_fr_route() and error_type in list(CUSTOM_ERRORS) + ['UnprocessableEntity']:
            try:
                return self.handle_error(e)
            except Exception:
                pass  # Fall through to original handler

        return original_handler(e)

def init_api(app):
	api = Api(app, errors=CUSTOM_ERRORS)
	return api