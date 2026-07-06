from connexion import request

def return404():
    return '404', 404

def get_ip() -> str:
    x_forwarded_for = request.headers.get("x-forwarded-for")
    if x_forwarded_for:
        real_ip = x_forwarded_for.split(",")[0].strip()
    else:
        real_ip = request.client.host if request.client else "Unknown"
        
    return real_ip