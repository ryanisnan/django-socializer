from socializer import models

REGISTRATIONS = {
    models.Comment: [],
    models.Recommendation: [],
    models.Flag: [],
    models.Nudge: []
}


def register(socializer_class, user_class):
    """
    Hook to allow your classes to be registered for certain social actions.
    """
    if socializer_class not in REGISTRATIONS.keys():
        raise Exception('Socializer: Not allowed to register %s' % socializer_class)

    if user_class not in REGISTRATIONS[socializer_class]:
        REGISTRATIONS[socializer_class].append(user_class)


def is_class_registered(socializer_class, user_class):
    """
    Hook to check if one of your classes has been registered for a certain
    action.
    """
    return user_class in REGISTRATIONS[socializer_class]
