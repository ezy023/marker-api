def noauth(view_func):
    view_func.noauth = True
    return view_func
