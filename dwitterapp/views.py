from rest_framework.viewsets import ModelViewSet
from .serializers import DweetCommentSerializer, DweeterSerializer, DweetsSerializer, DweeterCreateSerializer
from .models import DweetComments, Dweeter, Dweets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework import status
from rest_framework.decorators import list_route


class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


class DweetsViewSet(ModelViewSet):
    queryset = Dweets.objects.all()
    serializer_class = DweetsSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (CsrfExemptSessionAuthentication, TokenAuthentication)

    def list(self, request, *args, **kwargs):
        try:
            queryset = Dweets.objects.select_related('dweeter').filter(
                dweeter_id__in=[i.id for i in Dweeter.objects.filter(user_id=self.request.user.id)[0].follows.all()])
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        except IndexError as e:
            return Response([])

    def create(self, request, *args, **kwargs):
        data = {'dweet': request.data['dweet'], 'dweeter': request.user.id}
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @list_route(methods=['get'])
    def search(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @list_route(methods=['get'])
    def like_dweet(self, request, pk=None):
        if request.query_params.get('dweet'):
            dweet = Dweets.objects.get(pk=int(request.query_params.get('dweet')))
            dweeter = Dweeter.objects.get(pk=request.user.id)
            dweet.likes.add(dweeter)
            return Response({'success': 'Dweet Liked'}, status=status.HTTP_200_OK)
        return Response({'error': 'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)

    @list_route(methods=['get'])
    def liked_dweets(self, request, pk=None):
        queryset = Dweets.objects.select_related('dweeter').filter(
            dweeter_id__in=[i.id for i in Dweeter.objects.filter(user_id=self.request.user.id)[0].likes.all()])
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class DweeterViewSet(ModelViewSet):
    queryset = Dweeter.objects.all()
    serializer_class = DweeterSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (CsrfExemptSessionAuthentication, TokenAuthentication)

    @list_route(methods=['get'])
    def follow_dweeter(self, request, pk=None):
        if request.query_params.get('dweeter'):
            dweeter = Dweeter.objects.get(pk=int(request.query_params.get('dweeter')))
            user = Dweeter.objects.get(user_id=request.user.id)
            user.follows.add(dweeter)
            return Response({'success': 'Dweeter Followed'}, status=status.HTTP_200_OK)
        return Response({'error': 'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)


class DweeterCreateViewSet(ModelViewSet):
    queryset = Dweeter.objects.all()
    serializer_class = DweeterCreateSerializer
    permission_classes = ()
    http_method_names = ['post', 'head']
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def create(self, request, *args, **kwargs):
        if request.POST.get('username') and request.POST.get('password'):
            data = {'user': {'username': request.POST.get('username'), 'password': request.POST.get('password')}}
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response({'error': 'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)


class DweetCommentViewSet(ModelViewSet):
    queryset = DweetComments.objects.all()
    serializer_class = DweetCommentSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (CsrfExemptSessionAuthentication, TokenAuthentication)

    def create(self, request, *args, **kwargs):
        data = {'dweet': request.data['dweet'], 'comment': request.data['comment'], 'dweeter': request.user.id}
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
