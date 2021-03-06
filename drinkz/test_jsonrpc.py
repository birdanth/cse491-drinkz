import app
import urllib
from StringIO import StringIO
from . import db, recipes, unitconversion
import make_html
import simplejson


def jsonrpc(method, params):
    environ = {}
    environ['PATH_INFO'] = '/rpc'
    environ['REQUEST_METHOD'] = 'POST'
    environ['wsgi.input'] = StringIO(simplejson.dumps({
        'method': method,
        'params': params,
        'id': 1
    }))
    environ['CONTENT_LENGTH'] = len(environ['wsgi.input'].getvalue())

    d = {}
    def my_start_response(s, h, return_in=d):
        d['status'] = s
        d['headers'] = h

    app_obj = app.SimpleApp()
    results = app_obj(environ, my_start_response)

    status = d['status']
    headers = d['headers']
    results_dict =  simplejson.loads(''.join(results))

    return (status, headers, results_dict)

def test_convert_units_to_ml():
    status, headers, result = jsonrpc('convert_units_to_ml', ['1 oz'])

    assert status == '200 OK'
    assert result['error'] == None
    assert result['result'] == 29.5735, result['result']


def test_get_recipe_names():
    status, headers, result = jsonrpc('get_recipe_names', [])

    assert status == '200 OK'
    assert result['error'] == None

    assert 'scotch on the rocks' in result['result'], result['result']


def test_get_liquor_inventory():
    status, headers, result = jsonrpc('get_liquor_inventory', [])

    assert status == '200 OK'
    assert result['error'] == None
    
    #print result['result']
    assert ['Johnnie Walker','Black Label'] in result['result'], result['result']
    #assert ['WRONG','Black Label'] in result['result'], result['result']
    


