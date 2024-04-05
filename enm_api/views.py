from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from enm_api.serializers import BscSerializer, BscTgSerializer
from enm_api.services.bsc_tg.main import get_bsc_tg


class BscTg(APIView):
    """View for retrieving TG data for a given BSC."""

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=BscSerializer,
        responses={200: BscTgSerializer},
    )
    def post(self, request):
        """Retrieve TG data for the provided BSC name."""
        serializer = BscSerializer(data=request.data)
        if serializer.is_valid():
            bsc_name = serializer.validated_data['bsc']
            tg12_list, tg31_list = get_bsc_tg(bsc_name)
            bsc_tg_data = {
                'bsc': bsc_name,
                'g12tg': tg12_list,
                'g31tg': tg31_list,
            }
            tg_serializer = BscTgSerializer(bsc_tg_data)
            return Response(tg_serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
