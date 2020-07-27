from __future__ import unicode_literals
from future.builtins import range
# coding: utf-8

from django.template import Library

register = Library()

DOT = '.'


@register.inclusion_tag('filebrowser/include/paginator.html', takes_context=True)
def pagination(context):
    page_num = context['page'].number - 1
    paginator = context['p']

    if not paginator.num_pages or paginator.num_pages == 1:
        page_range = []
    else:
        # If there are 10 or fewer pages, display links to every page.
        # Otherwise, do some fancy
        if paginator.num_pages <= 10:
            page_range = list(range(paginator.num_pages))
        else:
            # Insert "smart" pagination links, so that there are always ON_ENDS
            # links at either end of the list of pages, and there are always
            # ON_EACH_SIDE links at either end of the "current page" link.
            page_range = []
            ON_EACH_SIDE = 3
            ON_ENDS = 2

            if page_num > (ON_EACH_SIDE + ON_ENDS):
                page_range.extend(list(range(ON_EACH_SIDE - 1)))
                page_range.append(DOT)
                page_range.extend(list(range(page_num - ON_EACH_SIDE, page_num + 1)))
            else:
                page_range.extend(list(range(page_num + 1)))
            if page_num < (paginator.num_pages - ON_EACH_SIDE - ON_ENDS - 1):
                page_range.extend(list(range(page_num + 1, page_num + ON_EACH_SIDE + 1)))
                page_range.append(DOT)
                page_range.extend(list(range(paginator.num_pages - ON_ENDS, paginator.num_pages)))
            else:
                page_range.extend(list(range(page_num + 1, paginator.num_pages)))

    return {
        'page_range': page_range,
        'page_num': page_num,
        'results_var': context['results_var'],
        'query': context['query'],
    }
