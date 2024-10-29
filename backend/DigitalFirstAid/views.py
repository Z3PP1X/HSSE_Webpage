""""
Views for the First Aid Book APIs.
"""

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework.views import APIView
from rest_framework.response import Response

from .hsseModules.FirstAidRecord import FirstAidRecord
from DigitalFirstAid import serializers


class FirstAidRecordViewSet(viewsets.ModelViewSet):
    """
    View for manage recipe APIs.
    """
    serializer_class = serializers.FirstAidRecordSerializer
    queryset = FirstAidRecord.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    lookup_field = ('sys_id')

    def get_queryset(self):
        return self.queryset.filter(
            RequestedFor=self.request.user).order_by('-created_on')


class FirstAidRecordMetadataViewset(APIView):
    """
    Retrieving the Metadata to create dynamic forms.
    """
    authentication_classes = (IsAuthenticated,)

    def get(self, request):

        metadata = []

        for field in FirstAidRecord._meta.get_fields():

            if field.auto_created and not field.concrete:
                continue

            if field.is_relation and field.many_to_many:
                continue

            field_info = {
                'name': field.name,
                'type': field.get_internal_type(),
                'required': not field.blank if hasattr(
                                field, 'blank') else True,
                'max_length': getattr(field, 'max_length', None),
                'choices': [{'value': choice_value,
                             'display_name': choice_name}
                            for choice_value, choice_name in
                            getattr(field, 'choices', [])],
                'label': field.verbose_name.title(),
                'help_text': field.help_text,
                'default': field.default
                if field.default != FirstAidRecord.fields.NOT_PROVIDED
                else None,

            }
            metadata.append(field_info)

        return Response(metadata)
