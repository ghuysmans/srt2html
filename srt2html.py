#!/usr/bin/env python3
import sys
import srt
from datetime import timedelta
from html import escape
import math

def t(d):
    a = str(d).split('.')
    if len(a) == 1:
        return a[0] + '.00'
    else:
        return a[0] + '.' + a[1][:2]

def diag(s, bad, msg, errors):
    if bad:
        print('<td class="bad">' + s + '</td>')
        errors.append(msg)
    else:
        print('<td>' + s + '</td>')

fn = sys.argv[1]
with open(fn, 'r') as f:
    subs = srt.sort_and_reindex(srt.parse(f.read()))
    prev = None
    print('<html>')
    print('<head>')
    print('<title>' + escape(fn) + '</title>')
    print('<style>')
    print('table {border-collapse: collapse}')
    print('td {border: 1px solid black}')
    print('.bad {color: red}')
    print('</style>')
    print('</head>')
    print('<body>')
    print('<table>')
    print('<thead><tr><th>Start</th><th>End</th><th>Subtitles</th><th>CPS</th><th>Error(s)</th></tr></thead>')
    print('<tbody>')
    for sub in subs:
        duration = sub.end - sub.start
        errors = []
        if prev is not None and sub.start < prev.end:
            errors.append("overlap")
        diag(t(sub.start), prev is not None and sub.start < prev.end + timedelta(0, 1, 0, 40), "too close", errors)
        diag(t(sub.end), duration < timedelta(0, 1, 0, 500), "too short", errors)
        print('<td>' + '<br>'.join(map(escape, sub.content.split('\n'))) + '</td>')
        #words = sum([len(l.split(' ')) for l in sub.content.split('\n')])
        cps = sum([len(l) for l in sub.content.split('\n')]) / duration.seconds
        diag(str(math.ceil(cps)), cps > 15, 'too many characters', errors)
        print('<td>' + ', '.join(map(escape, errors)) + '</td>')
        print('</tr>')
        prev = sub
    print('</tbody></table>')
    print('</body></html>')
