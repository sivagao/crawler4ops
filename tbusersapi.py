#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, url_for, render_template, Response, request, redirect
# import gc
from pymongo import Connection
import re
import sh
import urllib


try:
    import simplejson as json
except ImportError:
    import json

app = Flask(__name__)

connection = Connection('localhost', 27017)
db = connection.tbusers

def js_response_helper(data_json, mime='application/json'):
    """
    assumes that callback is last arg.
    """

    res = ""
    url = request.url
    cb_reg = re.compile('callback=([^&]*)')
    cb = cb_reg.search(url)
    if cb:
        res = cb.expand('\g<1>')
        res = res + "(" + data_json + "):"
        return Response(res, mimetype='application/javascript')
    else:
        res = data_json
        return Response(res, mimetype=mime)

errorjson = json.dumps({
    'message': 'Not Found'
})

@app.route('/')
def main():
    # 完善：爬取状态，totalnum
    TBs = db.collection_names(include_system_collections=False)
    return js_response_helper(json.dumps(TBs))

@app.route('/tieba/<tiebaname>', methods=['GET'])
def get_tieba(tiebaname):
    app.logger.debug(request.args)
    app.logger.debug(request.path)
    offset = request.args.get('offset', 0)
    slice10 = request.args.get('slice',False)
    app.logger.debug(slice10)
    app.logger.debug(offset)
    size = request.args.get('size', 5000)
    tiebaname = request.path.split('/')[-1]
    users = db[tiebaname].find()[int(offset):int(offset)+int(size)]
    if not users:
        return js_response_helper(errorjson, 'application/json')
    ls = []
    for e in users:
        del e['_id']
        ls.append(e['name'])
    if(slice10):
        ls = map(lambda x:'@'+x, ls) #这里的a同上
        xlen = len(ls)/10
        ls = [' '.join(ls[i*10:(i*10+10)]) for i in range(xlen)]
    return js_response_helper(json.dumps(ls))

# 通过web来提交爬虫任务
@app.route('/add/tieba', methods=['GET'])
def get_add_tieba():
    # add more responsive
    return render_template('add_tieba.html')

@app.route('/add/tieba', methods=['POST'])
def post_add_tieba():
    tb = request.form['tb']
    tb = tb.encode('gb2312')
    tb = urllib.quote(tb)
    app.logger.debug('A value for debugging: %s' % tb)
    app.logger.debug('A value for debugging form: %s' % request.form)
    sh.cd('/Users/ghlndsl/projects/diy_wdj/tutorial') #rewrite
    sh.scrapy.crawl('tb',a='target=%s'%tb, _bg=True) #rewrite
    return redirect(url_for('main'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0') # rewrite
