import json
import time
import logging

from flask import request
from flask_socketio import emit, disconnect

from .objects import (
    CM_server,
    clearMine_socketio,
    cookie_user_dict,
    user_cookie,
    gen_cookie,
)


@clearMine_socketio.on('connect', namespace='/login')
def login_connect():
    # 收到登录请求,进行身份识别
    logging.info('收到登录请求...')
    username = request.args.get('username', '')
    password = request.args.get('password', '')
    if username and password:
        logging.info(f'name = {username}')
        # 先判断账号密码是否正确
        if CM_server.login(username, password):
            # 生成cookie
            cookie = None

            while True:
                cookie = str(gen_cookie())
                if cookie not in cookie_user_dict:
                    break
            logging.info('cookie生成完成...')

            # 如果用户多次登录, 撤销用户先前的cookie, 设置cookie, 并设置最近活跃时间
            if username in user_cookie:
                del cookie_user_dict[user_cookie[username]]
            user_cookie[username] = cookie
            cookie_user_dict[cookie] = (username, time.time())
            logging.info('cookie重置完成...')

            emit('reply', cookie)
            logging.info('emit cookie 完成...')
        else:
            emit('reply', 'deny')
            logging.info('emit deny 完成...')
    else:
        logging.error(f'>>> error username or password is empty')
        disconnect()


@clearMine_socketio.on('disconnect', namespace='/login')
def login_disconnect():
    """登录连接断开时执行"""
    username = request.args.get('username', '')
    password = request.args.get('password', '')
    logging.info(f'登陆链接断开{username}')


@clearMine_socketio.on('connect', namespace='/minesweeper')
def mine_connect():
    logging.info('===> 扫雷连接成功...')
    cookie = request.args.get('cookie', '')
    if cookie:
        args = CM_server.args
        history = CM_server.history
        emit('args', json.dumps(args()))
        logging.info('emit args 完成')
        emit('history', json.dumps(history()))
        logging.info('emit history 完成')
    else:
        logging.error(f'>>> error cookie {cookie} not found')
        disconnect()


@clearMine_socketio.on('disconnect', namespace='/minesweeper')
def mine_disconnect():
    """扫雷链接断开时, 注销用户cookie"""
    cookie = request.args.get('cookie', '')
    user_cookie_tm = cookie_user_dict.get(cookie, None)
    if user_cookie_tm:
        username, tm = user_cookie_tm
        del user_cookie[username]
        del cookie_user_dict[cookie]
        logging.info('cookie信息成功杀掉...')
    logging.info('扫雷连接断开...')


@clearMine_socketio.on('click', namespace='/minesweeper')
def mine_click(info):
    cookie = request.args.get('cookie', '')
    data = json.loads(info)
    x, y = data['x'], data['y']
    user_cookie_tm = cookie_user_dict.get(cookie, None)
    if user_cookie_tm:
        username, tm = user_cookie_tm
        logging.info('点击信息解析完成...')
        give_color = CM_server.give_color
        click = CM_server.click
        ready = CM_server.ready
        args = CM_server.args
        rank = CM_server.rank
        restart = CM_server.restart
        give_color(username)
        snd, color, finish, timmer = click(x, y, username)
        logging.info('扫雷操作服务器执行成功...')
        # 更新最近活跃时间
        cookie_user_dict[cookie] = (username, time.time())
        if snd:
            emit('broadcast', json.dumps({'x': x, 'y': y, 'color': color, 'timmer': timmer, 'username': username}),
                 broadcast=True)
            logging.info('广播坐标发完')
        if finish:
            emit('broadcast finish', 'finish', broadcast=True)
            logging.info('emit 游戏结束 完成')
            emit('game end', json.dumps(rank()), broadcast=True)
            logging.info('本局最终战绩发送完成')
            restart()
            logging.info('游戏成功重启...')
            while not ready(): pass
            emit('args', json.dumps(args()), broadcast=True)
            logging.info('地图数据发送完成')
    else:
        logging.error(f'>>> error cookie {cookie} not found')
        disconnect()


@clearMine_socketio.on('rank', namespace='/minesweeper')
def get_rank(info):
    """发送查询到的本局战绩信息"""
    logging.info('收到 查看本局榜 请求...')
    emit('rank_rev', json.dumps(CM_server.rank()))
    logging.info('rank_rev 本局榜发送完成')


@clearMine_socketio.on('connect', namespace='/ranks')
def rank_connect():
    logging.info('查看总榜链接成功...')


@clearMine_socketio.on('disconnect', namespace='/ranks')
def rank_connect():
    logging.info('查看总榜链接断开...')


@clearMine_socketio.on('total_rank', namespace='/ranks')
def get_total_rank(info):
    """发送查询到的战绩总榜信息"""
    try:
        if info != 'query rank': return False
        cookie = request.args['cookie']
        username, tm = cookie_user_dict[cookie]
        cookie_user_dict[cookie] = (username, time.time())
        emit('total_rank', json.dumps(CM_server.total_rank()))
        logging.info('总榜信息发送完成...')

    except Exception as e:
        logging.info('>>> error ' + str(type(e)) + ' ' + str(e))
        disconnect()
