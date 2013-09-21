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
db_user = connection.tbusers
db_thread = connection.tbthreads
db_wbuserstatus = connection.wbuserstatus

def js_response_helper(data_json, mime='application/json;charset=UTF-8'):
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
        return Response(res, mimetype='application/javascript;charset=UTF-8')
    else:
        res = data_json
        return Response(res, mimetype=mime)

errorjson = json.dumps({
    'message': 'Not Found'
})

@app.route('/tieba/user')
def user():
    # 完善：爬取状态，totalnum
    TBs = db_user.collection_names(include_system_collections=False)
    return js_response_helper(json.dumps(TBs))

@app.route('/tieba/thread')
def thread():
    TBs = db_thread.collection_names(include_system_collections=False)
    return js_response_helper(json.dumps(TBs))

@app.route('/weibo/userstatus')
def wb_userstatus():
    TBs = db_wbuserstatus.collection_names(include_system_collections=False)
    return js_response_helper(json.dumps(TBs))

@app.route('/tieba/thread/<tiebaname>', methods=['GET'])
def get_tieba_thread(tiebaname):
    app.logger.debug(request.args)
    app.logger.debug(request.path)
    offset = request.args.get('offset', 0)
    # slice10 = request.args.get('slice',False)
    # app.logger.debug(slice10)
    app.logger.debug(offset)
    size = request.args.get('size', 100)
    tiebaname = request.path.split('/')[-1]
    threads = db_thread[tiebaname].find().sort('postnum',-1)[int(offset):int(offset)+int(size)]
    if not threads:
        return js_response_helper(errorjson, 'application/json')
    ls = []
    for e in threads:
        del e['_id']
        ls.append(e)
    return js_response_helper(json.dumps(ls))


@app.route('/weibo/userstatus/<user>', methods=['GET'])
def get_wb_userstatus(user):
    app.logger.debug(request.args)
    app.logger.debug(request.path)
    offset = request.args.get('offset', 0)
    # slice10 = request.args.get('slice',False)
    # app.logger.debug(slice10)
    app.logger.debug(offset)
    size = request.args.get('size', 100)
    tiebaname = request.path.split('/')[-1]
    threads = db_wbuserstatus[tiebaname].find().sort('retweetnum',-1)[int(offset):int(offset)+int(size)]
    if request.args.get('all'):
        threads = db_wbuserstatus[tiebaname].find()
    if not threads:
        return js_response_helper(errorjson, 'application/json')
    ls = []
    for e in threads:
        del e['_id']
        ls.append(e)
    return js_response_helper(json.dumps(ls))


@app.route('/tieba/user/<tiebaname>', methods=['GET'])
def get_tieba_user(tiebaname):
    app.logger.debug(request.args)
    app.logger.debug(request.path)
    offset = request.args.get('offset', 0)
    _slice = request.args.get('slice',False)
    if(_slice):
        _slice = int(_slice)
    app.logger.debug(_slice)
    app.logger.debug(offset)
    size = request.args.get('size', 5000)
    tiebaname = request.path.split('/')[-1]
    users = db_user[tiebaname].find()[int(offset):int(offset)+int(size)]
    if not users:
        return js_response_helper(errorjson, 'application/json')
    ls = []
    for e in users:
        del e['_id']
        ls.append(e['name'])
    if(_slice):
        ls = map(lambda x:'@'+x, ls) #这里的a同上
        xlen = len(ls)/_slice
        ls = [' '.join(ls[i*_slice:(i*_slice+_slice)]) for i in range(xlen)]
    return js_response_helper(json.dumps(ls))

# 通过web来提交爬虫任务
@app.route('/tieba/user/add', methods=['GET'])
def get_add_user():
    # add more responsive
    return render_template('add_tieba.html')

@app.route('/tieba/user/add', methods=['POST'])
def post_add_user():
    tb = request.form['tb']
    db_user[tb].remove()
    tb = tb.encode('gb2312')
    tb = urllib.quote(tb)
    app.logger.debug('A value for debugging: %s' % tb)
    app.logger.debug('A value for debugging form: %s' % request.form)
    # db_user[tb].remove()
    sh.cd('/Users/ghlndsl/projects/diy_wdj/tieba_zhaohuan_crawler') #rewrite
    sh.scrapy.crawl('tb_user',a='target=%s'%tb, _bg=True) #rewrite
    return redirect(url_for('user'))

@app.route('/tieba/thread/add', methods=['GET'])
def get_add_thread():
    return render_template('add_tieba.html')

@app.route('/tieba/thread/add', methods=['POST'])
def post_add_thread():
    tb = request.form['tb']
    tb = tb.encode('gb2312')
    tb = urllib.quote(tb)
    app.logger.debug('A value for debugging: %s' % tb)
    app.logger.debug('A value for debugging form: %s' % request.form)
    sh.cd('/Users/ghlndsl/projects/diy_wdj/tieba_zhaohuan_crawler') #rewrite
    sh.scrapy.crawl('tb_thread',a='target=%s'%tb, _bg=True) #rewrite
    return redirect(url_for('thread'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0') # rewrite
