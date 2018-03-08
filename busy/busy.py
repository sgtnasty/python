#!/usr/bin/env python3

import random
import time

first_level_dirs = ['main', 'home', 'usr', 'root', 'html', 'assets', 'files']
title_descs = ['page', 'script', 'interface', 'popup']
id_names = ['container', 'main', 'textbox', 'popup']
tag_names = ['div', 'textarea', 'span', 'strong', 'article', 'summary', 'blockquote', 'b']
autoclosing_tags = ['br', 'input']

def random_js_line():
    return random.choice([
        '      $("#%s").html("<b>" + $("#%s").text() + "</b>");' % (random.choice(id_names), random.choice(id_names)),
        '      $.get("t_%i.txt", function(resp) {\n        callback(resp);\n      });' % (int(random.random() * 50)),
        '      $("%s>%s").css({width: %i + "px", height: %i + "px"});' % (random.choice(tag_names), random.choice(tag_names), int(random.random() * 75), int(random.random() * 75)),
        '      for (var i = 0; i < count; i++) {\n        $("<div>").appendTo("#%s");\n      }' % (random.choice(id_names))
    ])

def random_js_lines():
    lines = [random_js_line() for _ in range(int(random.random() * 14) + 1)]
    return '\n'.join(lines)

def random_html_line():
    tag_name = random.choice(tag_names)
    return random.choice([
        '    <%s>id: %i</%s>' % (tag_name, int(random.random() * 1000), tag_name),
        '    <%s class="%s">\n      <%s/>\n    </%s>' % (tag_name, random.choice(first_level_dirs), random.choice(autoclosing_tags), tag_name),
        '    <div id="%s"></div>' % (random.choice(first_level_dirs))
    ])

def random_html_lines():
    lines = [random_html_line() for _ in range(int(random.random() * 9) + 1)]
    return '\n'.join(lines)

while True:
    print('creating /%s/%i.html' % (random.choice(first_level_dirs), int(random.random() * 1000)))
    time.sleep(random.random())
    lines = [
        '<!DOCTYPE html>',
        '<html lang="en">',
        '  <head>',
        '    <title>%s #%i</title>' % (random.choice(title_descs), int(random.random() * 100)),
        '    <script type="text/javascript" src="/js/assets/jquery.min.js"></script>',
        '    <script type="text/javascript">',
        random_js_lines(),
        '    </script>',
        '  </head>',
        '  <body>',
        random_html_lines(),
        '  </body>',
        '</html>'
    ]
    lines = [single_line for linegroup in lines for single_line in linegroup.split('\n')]
    for line in lines:
        print(line)
        time.sleep(random.random() / 10)
    print()
    time.sleep(random.random() / 2)