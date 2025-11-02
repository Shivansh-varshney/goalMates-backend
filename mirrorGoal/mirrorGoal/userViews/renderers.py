import json
from rest_framework.renderers import JSONRenderer
from django.core.serializers.json import DjangoJSONEncoder

class UserRenderer(JSONRenderer):
    charset='utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        if 'ErrorDetail' in str(data):
            if 'messages' in str(data):
                response = json.dumps({
                    'status': 'error',
                    'message': data['messages'][0]['message']
                })
            else:
                response = json.dumps({
                'status':'error',
                'message': data
                })
        else:
            response = json.dumps(data, cls=DjangoJSONEncoder)

        return response