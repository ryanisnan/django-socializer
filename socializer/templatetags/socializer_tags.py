from django import template
from socializer.models import Recommendation

register = template.Library()


@register.tag(name='socializer_recommendation')
def do_socializer_recommendation(parser, token):
    try:
        tag_name, user, obj, template_file = token.split_contents()

        if not (template_file[0] == template_file[-1] and template_file[0] in ('"', "'")):
            raise template.TemplateSyntaxError('%r tag\'s template_file argument should be in quotes' % tag_name)

        return SocializerRecommendationNode(user, obj, template_file)
    except ValueError:
        try:
            tag_name, user, obj = token.split_contents()
        except ValueError:
            raise template.TemplateSyntaxError('%r tag requires 2 or 3 arguments.' % token.contents.split()[0])

    return SocializerRecommendationNode(user, obj)


class SocializerRecommendationNode(template.Node):
    def __init__(self, user, obj, template_file='socializer_recommendation_readonly.html'):
        self.user = template.Variable(user)
        self.obj = template.Variable(obj)
        self.template_file = template_file

    def render(self, context):
        try:
            actual_user = self.user.resolve(context)
            actual_obj = self.obj.resolve(context)
        except template.VariableDoesNotExist:
            return ''

        context = template.Context({
            'user': actual_user,
            'recommendation_count': actual_obj.recommendations.count(),
            'user_has_recommended_obj': Recommendation.objects.filter(user=actual_user, content_object=actual_obj).exists()
        })

        try:
            return template.loader.get_template(self.template_file).render(context)
        except:
            return ''
