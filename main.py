import json
import os
from flask import Flask
from flask import request, make_response
from datetime import datetime, timedelta
# import frbddn
import wine_metric
import promo

app = Flask(__name__)
appdir = os.path.dirname(__file__)
days = timedelta(days=1)


def getAccinfo(d):
    if 'googleAcc' not in d:
        return ('0', None)
    a = '0'
    if 'lic' in d:
        a = d['lic']
    return (a, d['googleAcc'])


def getStaticData(fname):
    res = open(appdir + fname, 'r')
    resbody = res.read()
    res.close()
    return resbody


@app.route('/store_user.php', methods=['GET', 'POST'])
def store_user():
    lic = '0'
    id = None
    if request.method == 'POST':
        (lic, id) = getAccinfo(request.form)
    else:
        (lic, id) = getAccinfo(request.args)
    wine_metric.store_user(id, lic)
    return ''


@app.route('/promo_create', methods=['GET', 'POST'])
def promo_setup():
    if request.method == 'GET':
        if 'curious-scarab' in request.host:
            return getStaticData('/static/create_promo.html')
        else:
            return make_response('', 403)
    else:
        (title, msg) = (request.form['title'], request.form['msg'])
        linkId = promo.store_message(title, msg)
        a = '<a href="/?promo={0}">promo id: {0}</a>'.format(linkId)
        a += getStaticData('/static/create_promo.html')
        return a


@app.route('/robots.txt', methods=['GET'])
def Robot():
    resp = make_response("""User-agent: Googlebot
Allow: /

User-agent: *
Disallow: /
""", 200)
    resp.headers['Content-Type'] = 'plain/text'
    return resp


@app.route('/menu.json', methods=['GET', 'POST'])
def Menu():
    j = json.loads(getStaticData('/static/menu.json'))
    pr = get_promo_cookie(request.cookies)
    for i in pr:
        try:
            (title, ssss) = promo.get_message_by_id(i)
            j[1:1] = [{'title': title, 'function': 'ajax_loadContent', 'args': ['dispArea', '/?link=pr{0}'.format(i)]}]
        except Exception:
            continue
    resp = make_response(json.dumps(j))
    resp.headers['Content-Type'] = 'application/json'
    return resp


def links(link):
    if 'resume' in link:
        return getStaticData('/static/resume.xhtml')
    if 'sudoku' in link:
        if 'lin' in link:
            return getStaticData('/static/linsudoku.html')
    if 'certs' in link:
        return getStaticData('/static/certs.html')
    if link.startswith('pr'):
        return look_up_promo(link[2:])


def get_promo_cookie(cookies):
    t = []
    try:
        if 'promo' in cookies:
            t = json.loads(cookies.get('promo'))
    except Exception:
        pass
    return t


def look_up_promo(idx):
    i = promo.get_message_by_id(idx)
    if i is not None:
        return '<h2>{0}</h2><div class="promo">{1}</div>'.format(*i)
    return make_response('code {0} not found'.format(idx), 404)


def promo_cookie(cookies, resp, idx):
    p = get_promo_cookie(cookies)
    if idx not in p:
        p.append(idx)
    autoload = '<script>\n  ajax_loadContent("dispArea", "/?link=pr{0}");\n</script>'.format(idx)
    dr = resp.get_data().decode().split('\n')
    i = dr.index('</body>')
    dr[i:i] = autoload.split('\n')
    resp.set_data('\n'.join(dr))
    # create a secure cookie lasting 30 days
    exp = datetime.now() + (30 * days)
    resp.set_cookie('promo', json.dumps(p), expires=exp, secure=True)


@app.route('/test/')
def TestPage():
    return getStaticData('/static/test.html')


@app.route('/main')
def the_about_page():
    return getStaticData('/static/profile.html')


@app.route('/')
def Root():
    resp = make_response(getStaticData('/static/main.html'), 200)
    if 'link' in request.args:
        return links(request.args['link'])
    if 'promo' in request.args:
        promo_cookie(request.cookies, resp, request.args['promo'])
    return resp
