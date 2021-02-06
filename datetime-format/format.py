# coding: utf-8
import re
import sys
import time
import uuid
from datetime import datetime
from xml.sax.saxutils import escape

regex_format_map = {
    '^([0-9]{4}[0-1][0-9][0-3][0-9])$': '%Y%m%d',
    '^([0-9]{4}-[0-1][0-9]-[0-3][0-9])$': '%Y-%m-%d',
    '^([0-9]{4}-[0-1][0-9]-[0-3][0-9][ ][0-2][0-9]:[0-6][0-9]:[0-6][0-9])$': '%Y-%m-%d %H:%M:%S'
}


class Item(object):
    def __init__(self, title, subtitle='', icon='icon.png'):
        self.title = title
        self.subtitle = subtitle
        self.icon = icon


def get_second(query):
    for regex, time_format in regex_format_map.items():
        if re.match(regex, query):
            array = time.strptime(query, time_format)
            return int(time.mktime(array))
    return None


def get_show_items(query):
    items = []
    if query == 'now':
        dt = datetime.now()
        s = dt.strftime('%Y-%m-%d %H:%M:%S')
        millis_second = int(time.time() * 1000)
        second = millis_second // 1000
        items.append(Item(title=second.__str__()))
        items.append(Item(title=millis_second.__str__()))
        items.append(Item(title=s))
    second = get_second(query)
    if second:
        millis_second = second * 1000
        items.append(Item(title=second.__str__()))
        items.append(Item(title=millis_second.__str__()))
    elif query.isdigit():
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


def alfred_process():
    if len(sys.argv) >= 2:
        query = ''
        for i in range(1, len(sys.argv)):
            tmp = sys.argv[i].strip()
            if len(tmp) > 0:
                query += ' ' + tmp
        query = query.strip()
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


if __name__ == '__main__':
    alfred_process()
