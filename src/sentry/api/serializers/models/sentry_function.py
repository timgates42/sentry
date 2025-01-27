from sentry.api.serializers import Serializer, register
from sentry.models.sentryfunction import SentryFunction


@register(SentryFunction)
class SentryFunctionSerializer(Serializer):
    def serialize(self, obj, attrs, user):
        events = [event for event in obj.events]
        data = {
            "name": obj.name,
            "slug": obj.slug,
            "author": obj.author,
            "code": obj.code,
            "overview": obj.overview,
            "external_id": obj.external_id,
            "events": events,
        }
        return data
