from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow creator of an object to edit it.
    Assumes the model instance has the attributes checked below.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        print(f"{request.user=}")
        print(f"{obj.created_by=}")
        if request.method in permissions.SAFE_METHODS:
            return True

        if getattr(obj, "created_by", None) is not None:
            return obj.created_by == request.user
        if getattr(obj, "ballot_question", None) is not None:
            return obj.ballot_question.election.created_by == request.user
        if getattr(obj, "election", None) is not None:
            return obj.election.created_by == request.user


class IsOwner(permissions.BasePermission):
    """
    Object-level permission to only allow creator of an object to access it.
    Assumes the model instance has the attributes checked below.
    """

    def has_object_permission(self, request, view, obj):
        if getattr(obj, "created_by", None) is not None:
            return obj.created_by == request.user
        if getattr(obj, "ballot_question", None) is not None:
            return obj.ballot_question.election.created_by == request.user
        if getattr(obj, "election", None) is not None:
            return obj.election.created_by == request.user
