import json, os
from flask import Flask
from flask import request, make_response

app = Flask(__name__)

# import frbddn
import wine_metric
import promo


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
        if promo.client is not None:
            return getStaticData('/static/create_promo.html')
        else:
            return make_response('', 403)
    else:
        (title, msg) = (request.args['title'], request.args['msg']
        linkId = promo.store_message(title, msg)
        a = '<a href="/?promo={0}">promo id: {0}</a>'.format(linkId)
        return a


@app.route('/robot.txt', methods=['GET'])
def Robot():
    resp = make_response("""User-agent: Googlebot
Allow: /

User-agent: *
Disallow: /
""", 200)
    resp.headers['Content-Type'] = 'plain/text'
    return resp

appdir = os.path.dirname (__file__)


@app.route('/menu.json')
def Menu():
    resp = make_response(getStaticData('/static/menu.json'), 200)
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


@app.route('/test/')
def TestPage():
    return getStaticData('/static/test.html')


@app.route('/')
def Root():
    if 'link' in request.args:
        return links(request.args['link'])
    return getStaticData('/static/main.html')
