from flask import Flask, request
import json
from flask_cors import CORS
from flask_mandrill import Mandrill

app = Flask(__name__)
app.config['MANDRILL_API_KEY'] = '...'
app.config['MANDRILL_DEFAULT_FROM'] = '...'
app.config['QOLD_SUPPORT_EMAIL'] = '...'
app.config['CORS_HEADERS'] = 'Content-Type'

mandrill = Mandrill(app)
CORS(app, supports_credentials=True)


# 只接受get方法访问
@app.route("/", methods=["GET"])
def check():
    # 默认返回内容
    return_dict = {'x': 75, 'y': 125}
    # 判断输入参数是否为null
    if request.args is None:
        return_dict['return_code'] = '5004'
        return_dict['return_info'] = '请求参数为空'
        return json.dumps(return_dict, ensure_ascii=False)
    return json.dumps(return_dict, ensure_ascii=False)


@app.route("/test_01", methods=["POST"])
def check_1():
    # 默认返回内容
    return_dict = {'return_code': '200', 'return_info': '处理成功', 'result': False}
    # 判断传入的json数据是否为空
    if request.get_data() is None:
        return_dict['return_code'] = '5004'
        return_dict['return_info'] = '请求参数为空'
        return json.dumps(return_dict, ensure_ascii=False)
    # 获取传入的参数
    get_Data = request.get_data()
    # 传入的参数为bytes类型，需要转化成json
    get_Data = json.loads(get_Data)
    name = get_Data.get('name')
    age = get_Data.get('age')
    # 对参数进行操作
    return_dict['result'] = tt(name, age)

    return json.dumps(return_dict, ensure_ascii=False)


# 功能函数
def tt(name, age):
    result_str = "%s今年%s岁" % (name, age)
    return result_str


if __name__ == "__main__":
    CORS(app, resources=r'/*', supports_credentials=True)
    app.run(debug=False, host='0.0.0.0', port=5000)
