def request(flow):
    flow.request.headers['User-Agent'] = 'HelloKitty'
    print(flow.request.headers)