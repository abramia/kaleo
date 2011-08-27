from django import template

from invitations.forms import InviteForm


register = template.Library()


class RemainingInvitesNode(template.Node):
    
    @classmethod
    def handle_token(cls, parser, token):
        bits = token.split_contents()
        if len(bits) != 2:
            raise template.TemplateSyntaxError
        
        return cls(
            user = parser.compile_filter(bits[1])
        )
    
    def __init__(self, user):
        self.user = user
    
    def render(self, context):
        user = self.user.resolve(context)
        return user.invitationstat.invites_remaining()


@register.tag
def remaining_invites(parser, token):
    """
    Usage::
        {% remaining_invites user %}
    
    Returns an integer that is the # of remaining invites the user has.
    """
    return RemainingInvitesNode.handle_token(parser, token)


@register.inclusion_tag("invitations/_invite_form.html")
def invite_form(user):
    return {"form": InviteForm(), "user": user}


@register.inclusion_tag("invitations/_invited.html")
def invites_sent(user):
    return {"invited_list": user.invites_sent.all()}


@register.filter
def status_class(invite):
    if invite.status == invite.STATUS_SENT:
        return "sent"
    elif invite.status == invite.STATUS_ACCEPTED:
        return "accepted"
    elif invite.status == invite.STATUS_JOINED:
        return "joined"
    return ""