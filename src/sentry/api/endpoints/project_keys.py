from django.db.models import F
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response

from sentry import audit_log, features
from sentry.api.base import region_silo_endpoint
from sentry.api.bases.project import ProjectEndpoint
from sentry.api.serializers import serialize
from sentry.api.serializers.rest_framework import ProjectKeySerializer
from sentry.loader.dynamic_sdk_options import get_default_loader_data
from sentry.models import ProjectKey, ProjectKeyStatus


@region_silo_endpoint
class ProjectKeysEndpoint(ProjectEndpoint):
    def get(self, request: Request, project) -> Response:
        """
        List a Project's Client Keys
        ````````````````````````````

        Return a list of client keys bound to a project.

        :pparam string organization_slug: the slug of the organization the
                                          client keys belong to.
        :pparam string project_slug: the slug of the project the client keys
                                     belong to.
        """
        queryset = ProjectKey.objects.filter(
            project=project, roles=F("roles").bitor(ProjectKey.roles.store)
        )
        status = request.GET.get("status")
        if status == "active":
            queryset = queryset.filter(status=ProjectKeyStatus.ACTIVE)
        elif status == "inactive":
            queryset = queryset.filter(status=ProjectKeyStatus.INACTIVE)
        elif status:
            queryset = queryset.none()

        return self.paginate(
            request=request,
            queryset=queryset,
            order_by="-id",
            on_results=lambda x: serialize(x, request.user),
        )

    def post(self, request: Request, project) -> Response:
        """
        Create a new Client Key
        ```````````````````````

        Create a new client key bound to a project.  The key's secret and
        public key are generated by the server.

        :pparam string organization_slug: the slug of the organization the
                                          client keys belong to.
        :pparam string project_slug: the slug of the project the client keys
                                     belong to.
        :param string name: the name for the new key.
        """
        serializer = ProjectKeySerializer(data=request.data)

        if serializer.is_valid():
            result = serializer.validated_data

            rate_limit_count = None
            rate_limit_window = None

            if features.has("projects:rate-limits", project):
                ratelimit = result.get("rateLimit", -1)
                if ratelimit != -1 and (ratelimit["count"] and ratelimit["window"]):
                    rate_limit_count = result["rateLimit"]["count"]
                    rate_limit_window = result["rateLimit"]["window"]

            key = ProjectKey.objects.create(
                project=project,
                label=result.get("name"),
                public_key=result.get("public"),
                secret_key=result.get("secret"),
                rate_limit_count=rate_limit_count,
                rate_limit_window=rate_limit_window,
                data=get_default_loader_data(project),
            )

            self.create_audit_entry(
                request=request,
                organization=project.organization,
                target_object=key.id,
                event=audit_log.get_event_id("PROJECTKEY_ADD"),
                data=key.get_audit_log_data(),
            )

            return Response(serialize(key, request.user), status=201)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
