from django import template
from socializer.models import Recommendation

register = template.Library()


@register.simple_tag()
def socializer_recommendation(user, obj, template_file=None):
    if not template_file:
        template_file = 'socializer_recommendation_readonly.html'

    try:
        context = {
            'user': user,
            'recommendation_count': obj.recommendations.count(),
            'user_has_recommended_obj': Recommendation.objects.exists(user=user, content_object=obj)
        }
        return template.loader.get_template(template_file).render(template.Context(context))
    except:
        return ''
