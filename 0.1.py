from wsgiref.simple_server import make_server
from urllib.parse import parse_qs


def university():
    response_content = """
    <form action="/university_response" method="post">
    Full name: <input type="text" name="full_name"><br>
    Mathematics: <input type="text" name="mathematics"><br>
    Latvian language: <input type="text" name="latvian"><br>
    Foreign language: <input type="text" name="foreign"><br><br>
    <input type="submit" value="Submit">
    </form>
    """
    return [response_content.encode()]


def canApplyUniversity(**kwargs):
    for v in kwargs.values():
        if v < 40:
            return False
    else:
        return True


def correctMarks(**kwargs):
    for v in kwargs.values():
        if v > 100 or v < 0:
            return False
    else:
        return True


def university_response(environ):
    try:
        length = int(environ["CONTENT_LENGTH"])
    except ValueError:
        length = 0

    wsgi_input = environ["wsgi.input"].read(length).decode()
    form_data = parse_qs(wsgi_input)
    rating = form_data.copy()
    del rating['full_name']
    rating = {k: int(v[0]) for (k, v) in rating.items()}

    if not correctMarks(**rating):
        response_content = f"""
        <p style="color: red">Please check your marks ( 0-100 allowed) </p>
        """
    else:
        if canApplyUniversity(**rating):
            response_content = f"""
            <p>{form_data["full_name"][0]} can apply to university</p>
        """
        else:
            response_content = f"""
            <p style="color: red">{form_data["full_name"][0]} can not apply to university </p>
            """
    return [response_content.encode()]


def application(environ, start_response):
    status = "200 OK"
    headers = [("Content-type", "text/html")]

    path = environ["PATH_INFO"]

    if path == "/university_response":
        response_content = university_response(environ)
    elif path == "/university":
        response_content = university()
    else:
        response_content = ["OK".encode()]

    start_response(status, headers)

    return response_content


HOST = "localhost"
PORT = 8000

with make_server(HOST, PORT, application) as server:
    print(f"Serving at http://{HOST}:{PORT}")
    server.serve_forever()
