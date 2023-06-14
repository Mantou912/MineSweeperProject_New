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
    logging.info('receive request')
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
            logging.info('cookie generate')

            # 如果用户多次登录, 撤销用户先前的cookie, 设置cookie, 并设置最近活跃时间
            if username in user_cookie:
                del cookie_user_dict[user_cookie[username]]
            user_cookie[username] = cookie
            cookie_user_dict[cookie] = (username, time.time())
            logging.info('cookie rev')

            emit('reply', cookie)
            logging.info('emit cookie')
        else:
            emit('reply', 'deny')
            logging.info('emit deny')
    else:
        logging.error(f'>>> error username or password is empty')
        disconnect()


@clearMine_socketio.on('disconnect', namespace='/login')
def login_disconnect():
    """登录连接断开时执行"""
    username = request.args.get('username', '')
    password = request.args.get('password', '')
    logging.info(f'disconnect {username}')


@clearMine_socketio.on('connect', namespace='/minesweeper')
def mine_connect():
    logging.info('succeed connect minesweeper')
    cookie = request.args.get('cookie', '')
    if cookie:
        args = CM_server.args
        history = CM_server.history
        emit('args', json.dumps(args()))
        logging.info('emit args')
        emit('history', json.dumps(history()))
        logging.info('emit history')
    else:
        logging.error(f'>>> error cookie {cookie} not found')
        disconnect()


@clearMine_socketio.on('disconnect', namespace='/minesweeper')
def mine_disconnect():
    cookie = request.args.get('cookie', '')
    user_cookie_tm = cookie_user_dict.get(cookie, None)
    if user_cookie_tm:
        username, tm = user_cookie_tm
        del user_cookie[username]
        del cookie_user_dict[cookie]
        logging.info('kill cookies')
    logging.info('disconnect')


@clearMine_socketio.on('click', namespace='/minesweeper')
def mine_click(info):
    cookie = request.args.get('cookie', '')
    data = json.loads(info)
    x, y = data['x'], data['y']
    user_cookie_tm = cookie_user_dict.get(cookie, None)
    if user_cookie_tm:
        username, tm = user_cookie_tm
        logging.info('click succeed')
        give_color = CM_server.give_color
        click = CM_server.click
        ready = CM_server.ready
        args = CM_server.args
        rank = CM_server.rank
        restart = CM_server.restart
        give_color(username)
        snd, color, finish, timmer = click(x, y, username)
        logging.info('succeed serve')
        # 更新最近活跃时间
        cookie_user_dict[cookie] = (username, time.time())
        if snd:
            emit('broadcast', json.dumps({'x': x, 'y': y, 'color': color, 'timmer': timmer, 'username': username}),
                 broadcast=True)
            logging.info('send xy')
        if finish:
            emit('broadcast finish', 'finish', broadcast=True)
            logging.info('game over')
            emit('game end', json.dumps(rank()), broadcast=True)
            logging.info('send game info')
            restart()
            logging.info('restart game')
            while not ready(): pass
            emit('args', json.dumps(args()), broadcast=True)
            logging.info('send map')
    else:
        logging.error(f'>>> error cookie {cookie} not found')
        disconnect()


@clearMine_socketio.on('rank', namespace='/minesweeper')
def get_rank(info):
    logging.info('request ranks')
    emit('rank_rev', json.dumps(CM_server.rank()))
    logging.info('succeed send')


@clearMine_socketio.on('connect', namespace='/ranks')
def rank_connect():
    logging.info('succeed ranks')


@clearMine_socketio.on('disconnect', namespace='/ranks')
def rank_connect():
    logging.info('disconnect ranks')


@clearMine_socketio.on('total_rank', namespace='/ranks')
def get_total_rank(info):
    try:
        if info != 'query rank': return False
        cookie = request.args['cookie']
        username, tm = cookie_user_dict[cookie]
        cookie_user_dict[cookie] = (username, time.time())
        emit('total_rank', json.dumps(CM_server.total_rank()))
        logging.info('succeed send')

    except Exception as e:
        logging.info('>>> error ' + str(type(e)) + ' ' + str(e))
        disconnect()
