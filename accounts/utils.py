###Prevents Unauthorized user from accessing a page###
# Super Users and Managers are allowed to view all page ## 

def require(request, user_type):
    try:
        if request.user.is_superuser:
            allow =True
        elif request.user.profile.user_type == user_type or request.user.profile.user_type =="manager":
            allow = True
        else:
            allow = False
    except:
        allow = False
    return allow