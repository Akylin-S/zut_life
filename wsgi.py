from wsgiref.simple_server import make_server


# 定义服务器调用对象application
def application(environ, start_response):
    """
    :param environ:  #包含所有客户端的请求信息即上下文请求，application从这个参数中获取客户端请求意图
    :param start_response: 一个可调用对象，用于发送http请求状态
    :return: [b'Hello World!\n'] #返回可迭代对象 且必须是字节流，Http是面向字节流协议
     """
    status = '200 OK'
    response_headers = [('Conteny-type', 'text/plain')]  # 响应头是一个列表
    start_response(status, response_headers)  # 返回给server之前调用 start_response
    return [b"Hello World!\n"]


# 创建WSGI服务器，指定调用application,这里的调用对象也可以是一个类或者实例
httpeserver = make_server('127.0.0.1', 8000, application)
# 处理请求后退出
httpeserver.handle_request()
