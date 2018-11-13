import json
import bleach
from django import template
from django.utils.safestring import mark_safe
import us

from utils.common import states
from utils.orgs import get_legislature_from_abbr
from utils.people import pretty_url


register = template.Library()


@register.simple_tag()
def canonical_url(obj):
    return pretty_url(obj)


@register.inclusion_tag('public/components/header.html', takes_context=True)
def header(context):
    return {
        'state': context.get('state'),
        'disable_state_nav': context.get('disable_state_nav'),
        'states': states,
    }


@register.inclusion_tag('public/components/sources.html')
def sources(state, sources=None):
    legislature = get_legislature_from_abbr(state)
    return {
        'legislature_name': legislature.name,
        'legislature_url': legislature.jurisdiction.url,
        'sources': sources
    }


@register.inclusion_tag('public/components/bill-card.html')
def bill_card(state, bill):
    return {
        'state': state,
        'bill': bill
    }


@register.inclusion_tag('public/components/vote-card.html')
def vote_card(vote):
    # Model needs to be wrapped in a dict, per custom-tag requirements
    return {'vote': vote}


@register.inclusion_tag('public/components/action-card.html')
def action_card(action):
    # Model needs to be wrapped in a dict, per custom-tag requirements
    return {'action': action}


@register.filter()
def state_name(state_abbr):
    return us.states.lookup(state_abbr).name


@register.filter()
def jsonify(data):
    # Source: https://gist.github.com/pirate/c18bfe4fd96008ffa0aef25001a2e88f
    uncleaned = json.dumps(data)
    clean = bleach.clean(uncleaned)
    return mark_safe(clean)
