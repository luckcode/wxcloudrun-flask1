from datetime import datetime
from flask import render_template, request
from run import app
from wxcloudrun.dao import delete_counterbyid, query_counterbyid, insert_counter, update_counterbyid
from wxcloudrun.model import Counters
from wxcloudrun.response import make_succ_empty_response, make_succ_response, make_err_response

import os
import sys
import time
current_directory = os.path.dirname(os.path.abspath(__file__))
#os.makedirs(current_directory+'/static/')

@app.route('/')
def index():
    """
    :return: 返回index页面
    """
    return render_template('index.html')


@app.route('/api/count', methods=['POST'])
def count():
    """
    :return:计数结果/清除结果
    """

    # 获取请求体参数
    params = request.get_json()

    # 检查action参数
    if 'action' not in params:
        return make_err_response('缺少action参数')

    # 按照不同的action的值，进行不同的操作
    action = params['action']

    # 执行自增操作
    if action == 'inc':
        counter = query_counterbyid(1)
        if counter is None:
            counter = Counters()
            counter.id = 1
            counter.count = 1
            counter.created_at = datetime.now()
            counter.updated_at = datetime.now()
            insert_counter(counter)
        else:
            counter.id = 1
            counter.count += 1
            counter.updated_at = datetime.now()
            update_counterbyid(counter)
        return make_succ_response(counter.count)

    # 执行清0操作
    elif action == 'clear':
        delete_counterbyid(1)
        return make_succ_empty_response()

    # action参数错误
    else:
        return make_err_response('action参数错误')


@app.route('/api/count', methods=['GET'])
def get_count():
    """
    :return: 计数的值
    """
    counter = Counters.query.filter(Counters.id == 1).first()
    return make_succ_response(0) if counter is None else make_succ_response(counter.count)
    
@app.route('/api/ufile', methods=['post'])
def ufile():
    try:
        file_obj = request.files.get("file")
        if file_obj is None:
            return make_err_response("文件上传为空")
            

        # 直接使用文件上传对象保存 
        file_path = current_directory+'/static/'+ str(time.time())+file_obj.filename
        print(request.data)
        # file_obj.save(file_path)
        with open(file_path,'wb') as f:
            f.write(request.data)
        return make_succ_response('success:'+file_path)
    except Exception as e:
        print(e)
        return make_err_response('fail:'+str(e))