from wsgiref.simple_server import make_server
from urllib.parse import parse_qs


def index():
    response_content = f'<h3>Hello! Please use <a href="http://{HOST}:{PORT}/university"> university page</a></h3>'
    return [response_content.encode()]


def university(environ):
    method = environ["REQUEST_METHOD"]
    if method == "GET":
        response_content = """
        <form action="" method="post">
            Full name: <input type="text" size=20px name="name" placeholder="Name Surname"><br>
            Mathematics: <input type="text" size=3px name="math" placeholder="0-100"><br>
            Latvian language: <input type="text" size=3px name="latvian" placeholder="0-100"><br>
            Foreign language: <input type="text" size=3px name="foreign" placeholder="0-100"><br><br>
            <input type="submit" value="Submit">
        </form>
        """
        return [response_content.encode()]
    elif method == "POST":
        return result(environ)


def canApplyUniversity(form_data):
    marks = {} #new dictionary for marks only (to check average we don't need name)
    for k, v in form_data.items():
        if k == "name":
            continue
        marks[k] = int(v[0])
    for v in marks.values(): #checking if mark greater than 39
        if v < 40:
            return False
    return True


def result(environ):
    try:
        length = int(environ["CONTENT_LENGTH"])
    except ValueError:
        length = 0

    wsgi_input = environ["wsgi.input"].read(length).decode()
    form_data = parse_qs(wsgi_input)

    if canApplyUniversity(form_data):
        response_content = f"""
        <p>{form_data["name"][0]} Can apply to university</p>
        """
    else:
        response_content = f"""
        <p>{form_data["name"][0]} can not apply university</p>
        """
    return [response_content.encode()]


def application(environ, start_response):

    status = "200 OK"
    headers = [("Content-type", "text/html")]
    path = environ["PATH_INFO"]

    if path == "/university":
        response_content = university(environ)
    else:
        response_content = index()

    start_response(status, headers)

    return response_content


HOST = "localhost"
PORT = 8000

with make_server(HOST, PORT, application) as server:
    print(f"Serving at http://{HOST}:{PORT}/university")
    server.serve_forever()


