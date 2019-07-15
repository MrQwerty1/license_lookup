from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from scraping.scripts import license_lookup


class LicenseLookupView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, *args, **kwargs):

        fname = request.query_params.get('fname')
        lname = request.query_params.get('lname')
        state = request.query_params.get('state')
        county = request.query_params.get('county')
        cont_id = request.query_params.get('cont_id')

        if any(map(lambda x: x is None, [fname, lname, state, county, cont_id])):
            return Response(
                {'detail': 'Please, specify all query params (fname, lname, state, county, cont_id)'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # http://127.0.0.1:8000/api/v0/test/?fname=robert&lname=garcia&state=nevada&county=clark&cont_id=
        try:
            resp_data = license_lookup.run(fname, lname, state, county, cont_id)
        except:
            resp_data = {}

        return Response(resp_data)
