import app
import urllib
import make_html
import db

def test_recipes():
    environ = {}
    environ['PATH_INFO'] = '/recipes.html'
    
    response = {}
    def start_response(s, h, return_in=response):
        response['status'] = s
        response['headers'] = h

    appTest = app.SimpleApp()
    results = appTest(environ, start_response)
    text = "".join(results)
    status, headers = response['status'], response['headers']

    assert status == '200 OK' , status
    assert text.find('scotch on the rocks') != -1, text
    assert text.find('blended scotch') != -1, text

    assert text.find('vodka martini') != -1, text
    assert text.find('unflavored vodka') != -1, text

    assert text.find('vomit inducing martini') != -1, text
    assert text.find('orange juice') != -1, text

