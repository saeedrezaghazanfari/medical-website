


def first(get_response):
    def middleware(request):
        # 
        print('beforeeeeeeeeeeeeee')
        response = get_response(request)
        #
        return response
    
    return middleware