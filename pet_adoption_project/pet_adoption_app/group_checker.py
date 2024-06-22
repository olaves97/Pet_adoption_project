def is_moderator(request):
    if request.user.is_authenticated:
        return {'is_moderator': request.user.groups.filter(name='Moderators').exists()}
    return {'is_moderator': False}
