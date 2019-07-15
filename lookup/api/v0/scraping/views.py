from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from scraping.scripts import license_lookup


class LicenseLookupView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, *args, **kwargs):

        first_name_p = request.query_params.get('first_name_p')
        last_name_p = request.query_params.get('last_name_p')
        state_p = request.query_params.get('state_p')
        county_p = request.query_params.get('county_p')
        cont_id = request.query_params.get('cont_id')

        if any(map(lambda x: x is None, [first_name_p, last_name_p, state_p, county_p, cont_id])):
            return Response(
                {'detail': 'Please, specify all query params (first_name_p, last_name_p, state_p, county_p, cont_id)'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            resp_data = license_lookup.run(first_name_p, last_name_p, state_p, county_p, cont_id)
        except:
            resp_data = {}

        return Response(resp_data)
