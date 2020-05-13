from mitmproxy import ctx

'''
def request(flow):
    flow.request.headers['User-Agent'] = 'HelloKitty'
    flow.request.url = 'https://httpbin.org/get'
    ctx.log.info(flow.request.url)
    ctx.log.info(str(flow.request.headers))
    ctx.log.info(str(flow.request.cookies))
    ctx.log.info(flow.request.host)
    ctx.log.info(flow.request.method)
    ctx.log.info(str(flow.request.port))
    ctx.log.info(flow.request.scheme)
'''

def response(flow):
    response = flow.response
    info = ctx.log.info
    info(str(response.status_code))
    info(str(response.headers))
    info(str(response.cookies))
    info(str(response.text))

