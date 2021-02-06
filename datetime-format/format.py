# coding: utf-8
import sys
import uuid
from datetime import datetime
from xml.sax.saxutils import escape


class Item(object):
    def __init__(self, title, subtitle='', icon='icon.png'):
        self.title = title
        self.subtitle = subtitle
        self.icon = icon


def show_alfred_item_list(items):
    print('<items>')
    for item in items:
        arg = '{}'.format(item.title)
        uid = uuid.uuid4().__str__()
        title = item.title
        subtitle = item.subtitle
        icon = item.icon
        print('''
        <item arg="{}" uid="{}"><title>{}</title><subtitle>{}</subtitle><icon>{}</icon></item>
        '''.format(escape(arg), escape(uid), escape(title), escape(subtitle), escape(icon)))
    print('</items>')


def get_unix_time_millis(dt):
    epoch = datetime.utcfromtimestamp(0)
    return int((dt - epoch).total_seconds() * 1000.0)


def get_show_items(query):
    items = []
    if query == 'now':
        dt = datetime.now()
        s = dt.strftime('%Y-%m-%d %H:%M:%S')
        millis_second = get_unix_time_millis(dt)
        second = millis_second // 1000
        items.append(Item(title=second.__str__()))
        items.append(Item(title=millis_second.__str__()))
        items.append(Item(title=s))
    if query.isdigit():
        length = len(query)
        if length < 10:
            ts = int(query)
        elif length == 10:
            ts = int(query)
        elif 10 < length <= 13:
            ts = int(query[0:10])
        else:
            ts = int(query[0:13])
        s = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        items.append(Item(title=s))
    return items


def alfred_process():
    if len(sys.argv) >= 2:
        query = sys.argv[1].strip()
        if len(query) == 0:
            return
        try:
            items = get_show_items(query)
            show_alfred_item_list(items)
        except Exception as ex:
            items = [Item(title=ex.__str__())]
            show_alfred_item_list(items)
    else:
        return
    '''
    1612180214000
    '''


if __name__ == '__main__':
    alfred_process()
