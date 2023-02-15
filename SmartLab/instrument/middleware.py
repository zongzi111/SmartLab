import time

def timeit_middleware(get_response):
    
    def middleware(request):
        start = time.time()
        response = get_response(request)
        end = time.time()
        print("请求花费时间: {}秒".format(end - start))
        return response

    return middleware