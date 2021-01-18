from django import template

register = template.Library()

@register.filter(name='get_val')
def get_val(list1, key):
    return list1[key]

@register.filter(name='get_photo')
def photo(class_stu):
    if class_stu == 'SC-1': return 'class/sc_1.jpeg'
    elif class_stu == 'SC-2': return 'class/sc_2.jpeg'
    elif class_stu == 'SC-3': return 'class/sc_3.jpeg'
    elif class_stu == 'COMMERCE': return 'class/commerce.jpeg'
    elif class_stu == 'ARTS': return 'class/arts.jpeg'
class IncrementVarNode(template.Node):
    def __init__(self, var_name):
        self.var_name = var_name

    def render(self,context):
        value = context[self.var_name]
        context[self.var_name] = value + 1
        return u""

def increment_var(parser, token):
    parts = token.split_contents()
    if len(parts) < 2:
        raise template.TemplateSyntaxError("'increment' tag must be of the form:  {% increment <var_name> %}")
    return IncrementVarNode(parts[1])

register.tag('increment', increment_var)
