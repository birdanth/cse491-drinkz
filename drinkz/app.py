
#! /usr/bin/env python


from wsgiref.simple_server import make_server
import urlparse
import simplejson
import make_html
import db
import recipes
import sqlite3, os
from Cookie import SimpleCookie
import jinja2
import uuid
from jinja2 import Environment, PackageLoader


usernames = {}
env = Environment( loader = PackageLoader('drinkz', 'html-templates') )

dispatch = {
    '/' : 'index',
    '/index.html' : 'index',
    '/login_1' : 'login1',
    '/login1_process' : 'login1_process',
    '/logout' : 'logout',
    '/status' : 'status',
    '/pairings.html' : 'pairings',
    '/recipes.html' : 'recipes',
    '/inventory.html' : 'inventory',
    '/liquor_types.html' : 'liquor_types',
    '/conversion.html' : 'conversion',
    '/add_to_inventory.html' : 'add_to_inventory',
    '/add_to_liquor_types.html' : 'add_to_liquor_types',
    '/add_to_recipes.html' : 'add_to_recipes',
    '/recipes_recv' : 'recipes_recv',
    '/inventory_recv' : 'inventory_recv',
    '/liquor_types_recv' : 'liquor_types_recv',
    '/content' : 'somefile',
    '/error' : 'error',
    '/helmet' : 'helmet',
    '/form' : 'form',
    '/recv' : 'recv',
    '/converter_recv' : 'converter_recv',
    '/rpc'  : 'dispatch_rpc',
    '/posting'  : 'posting'
}

html_headers = [('Content-type', 'text/html')]
css_headers = [('Content-type', 'text/css')]
js_headers = [('Content-type', 'text/javascript')]
plain_headers = [('Content-type', 'text/plain')]

class SimpleApp(object):
    def __call__(self, environ, start_response):
        make_html.baseTemplate()
        path = environ['PATH_INFO']
        fn_name = dispatch.get(path, 'error')
	
	print 'environ variables:' , environ['REQUEST_METHOD']
        # retrieve 'self.fn_name' where 'fn_name' is the
        # value in the 'dispatch' dictionary corresponding to
        # the 'path'.
        fn = getattr(self, fn_name, None)

        if fn is None:
            start_response("404 Not Found", html_headers)
            return ["No path %s found" % path]
        
        return fn(environ, start_response)

    def login1(self, environ, start_response):
        start_response('200 OK', list(html_headers))

        title = 'login'
        template = env.get_template('login1.html')
        return str(template.render(locals()))

    def login1_process(self, environ, start_response):
        formdata = environ['QUERY_STRING']
        results = urlparse.parse_qs(formdata)

        name = results['name'][0]
        content_type = 'text/html'

        # authentication would go here -- is this a valid username/password,
        # for example?

        k = str(uuid.uuid4())
        usernames[k] = name

        headers = list(html_headers)
        headers.append(('Location', '/status'))
        headers.append(('Set-Cookie', 'name1=%s' % k))

        start_response('302 Found', headers)
        return ["Redirect to /status..."]

    def logout(self, environ, start_response):
        if 'HTTP_COOKIE' in environ:
            c = SimpleCookie(environ.get('HTTP_COOKIE', ''))
            if 'name1' in c:
                key = c.get('name1').value
                name1_key = key

                if key in usernames:
                    del usernames[key]
                    print 'DELETING'

        pair = ('Set-Cookie',
                'name1=deleted; Expires=Thu, 01-Jan-1970 00:00:01 GMT;')
        headers = list(html_headers)
        headers.append(('Location', '/status'))
        headers.append(pair)

        start_response('302 Found', headers)
        return ["Redirect to /status..."]

    def status(self, environ, start_response):
        start_response('200 OK', list(html_headers))

        name1 = ''
        name1_key = '*empty*'
        if 'HTTP_COOKIE' in environ:
            c = SimpleCookie(environ.get('HTTP_COOKIE', ''))
            if 'name1' in c:
                key = c.get('name1').value
                name1 = usernames.get(key, '')
                name1_key = key
                
        title = 'login status'
        template = env.get_template('status.html')
        return str(template.render(locals()))


    ## Main Page
    def posting(self, environ, start_response):
        #data = make_html.index()
	if environ['REQUEST_METHOD'] == 'POST':
	    data = 'you just did a post operation!'
	else:
            #db_conn = sqlite3.connect('../tables.db')
            #c = db_conn.cursor()
	    #c.execute("INSERT INTO bottle_types (mfg,lqr,typ) VALUES (?,?,?)",('testing','liquor','shits'))
	    #db.add_bottle_type_sql('Johnnie Walker', 'Black Label', 'blended scotch')
            #c.execute('SELECT * FROM bottle_types')
	    #data = str(c.fetchall())
	    data = 'you fucked up'

        start_response('200 OK', list(plain_headers))
        return data


    ## Main Page      
    def index(self, environ, start_response):
        data = make_html.index()
        
        start_response('200 OK', list(html_headers))
        return data
    
    ## Inventory Page    
    def inventory(self, environ, start_response):
        data = make_html.inventory()
        
        start_response('200 OK', list(html_headers))
        return [data]
    
    ## Liquor Types Page
    def liquor_types(self, environ, start_response):
        data = make_html.liquor_types()
        
        start_response('200 OK', list(html_headers))
        return [data]
    
    ## Pairings Page
    def pairings(self, environ, start_response):
        data = make_html.pairings()

        start_response('200 OK', list(html_headers))
        return [data]


    ## Recipes Page       
    def recipes(self, environ, start_response):
        data = make_html.recipes()
        
        start_response('200 OK', list(html_headers))
        return [data]
    
    ## Add to Inventory Form    
    def add_to_inventory(self, environ, start_response):
        data = make_html.add_to_inventory()
        
        start_response('200 OK', list(html_headers))
        return [data]
    
    ## Add to Liquor Types Form
    def add_to_liquor_types(self, environ, start_response):
        data = make_html.add_to_liquor_types()
        
        start_response('200 OK', list(html_headers))
        return [data]
    
    ## Add to Recipes Form    
    def add_to_recipes(self, environ, start_response):
        data = make_html.add_to_recipes()
        
        start_response('200 OK', list(html_headers))
        return [data]

    ## Perform Unit Conversion
    def conversion(self, environ, start_response):
        data = make_html.conversion_form()
        
        start_response('200 OK', list(html_headers))
        return [data]
        
    def somefile(self, environ, start_response):
        content_type = 'text/html'
        data = open('somefile.html').read()

        start_response('200 OK', list(html_headers))
        return [data]

    def error(self, environ, start_response):
        status = "404 Not Found"
        content_type = 'text/html'
        data = "Couldn't find your stuff."
       
        start_response('200 OK', list(html_headers))
        return [data]

    def helmet(self, environ, start_response):
        content_type = 'image/gif'
        data = open('../Spartan.gif', 'rb').read()

        start_response('200 OK', [('Content-type', content_type)])
        return [data]

    def form(self, environ, start_response):
        data = form()

        start_response('200 OK', list(html_headers))
        return [data]
   
    def recv(self, environ, start_response):
        formdata = environ['QUERY_STRING']
        results = urlparse.parse_qs(formdata)

        firstname = results['firstname'][0]
        lastname = results['lastname'][0]

        content_type = 'text/html'
        data = "First name: %s; last name: %s.  <a href='./'>return to index</a>" % (firstname, lastname)

        start_response('200 OK', list(html_headers))
        return [data]

    
    def converter_recv(self, environ, start_response):
        formdata = environ['QUERY_STRING']
        results = urlparse.parse_qs(formdata)

        amount = results['inputValue'][0]   
        content_type = 'text/html'
        data = "Amount Entered: %s | Amount in MilliLeters(ML): %s |  <a href='./'>HOME </a>" % (amount, db.convert_to_ml(amount))

        start_response('200 OK', list(html_headers))
        return [data]

    def liquor_types_recv(self, environ, start_response):
        formdata = environ['QUERY_STRING']
        results = urlparse.parse_qs(formdata)

        mfg = results['mfg'][0]
        lqr = results['lqr'][0]
        typ = results['typ'][0]
        db.add_bottle_type(mfg,lqr,typ)
        
        content_type = 'text/html'
        data1 = " *** Bottle Type ( %s , %s , %s  ) added <br><br>" % (mfg, lqr, typ)
        data2 =  make_html.liquor_types()
        data = data1 + data2
        start_response('200 OK', list(html_headers))
        return [data]
    
    def inventory_recv(self, environ, start_response):
        formdata = environ['QUERY_STRING']
        results = urlparse.parse_qs(formdata)
        
        mfg = results['mfg'][0]
        lqr = results['lqr'][0]
        typ = results['typ'][0]
        try:
            db.add_to_inventory(mfg,lqr,typ)
            data1 = " *** Inventory Item ( %s , %s , %s  ) added <br><br>" % (mfg, lqr, typ)
        except:
            data1 = " MISSING LIQUOR TYPE  - try again <br><br> "
            
        content_type = 'text/html'
        data2 =  make_html.inventory()
        data = data1 + data2       
	start_response('200 OK', list(html_headers))
        return [data]
    
    def recipes_recv(self, environ, start_response):
        formdata = environ['QUERY_STRING']
        results = urlparse.parse_qs(formdata)

        name = results['name'][0]
        ingName = results['ingName'][0]
        ingAmount = results['ingAmount'][0]    
        ing = []
        ing.append((ingName, ingAmount))
        rec = name,ing
        r = recipes.Recipe(rec[0],rec[1])
        db.add_recipe(r)       
        content_type = 'text/html'

        #data = 'name: %s  ingName:  %s  ingAmount: %s' % (name , ingName, ingAmount) 
        data1 = " *** Recipe ( %s ,[( %s , %s )] ) added <br><br>" % (name, ingName, ingAmount)
        data2 =  make_html.recipes()
        data = data1 + data2
        start_response('200 OK', list(html_headers))
        return [data]
    
    def rpc_convert_units_to_ml(self, amount):
        return db.convert_to_ml(amount)

    def rpc_get_recipe_names(self):
	names = []
	for r in db.get_all_recipes(): 
	    names.append(r.name)

        return names

    def rpc_get_liquor_inventory(self):
        db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
        db.add_to_inventory('Johnnie Walker', 'Black Label', '1000 ml')
        
        inv = []
        for mfg,lqr in db.get_liquor_inventory():
            inv.append((mfg,lqr))
            
        return inv

    def _decode(self, json):
        return simplejson.loads(json)

    def _dispatch(self, json):
        rpc_request = self._decode(json)

        method = rpc_request['method']
        params = rpc_request['params']
        
        rpc_fn_name = 'rpc_' + method
        fn = getattr(self, rpc_fn_name)
        result = fn(*params)

        response = { 'result' : result, 'error' : None, 'id' : 1 }
        response = simplejson.dumps(response)
        return str(response)

    def dispatch_rpc(self, environ, start_response):
        # POST requests deliver input data via a file-like handle,
        # with the size of the data specified by CONTENT_LENGTH;
        # see the WSGI PEP.
        
        if environ['REQUEST_METHOD'].endswith('POST'):
            body = None
            if environ.get('CONTENT_LENGTH'):
                length = int(environ['CONTENT_LENGTH'])
                body = environ['wsgi.input'].read(length)
                response = self._dispatch(body) + '\n'
                start_response('200 OK', [('Content-Type', 'application/json')])

                return [response]

        # default to a non JSON-RPC error.
        status = "404 Not Found"
        content_type = 'text/html'
        data = "Couldn't find your stuff."
       
        start_response('200 OK', list(html_headers))
        return [data]

    def rpc_add(self, a, b):
        return int(a) + int(b)
    


if __name__ == '__main__':
    import random, socket
    port = random.randint(8000, 9999)
    
    app = SimpleApp()
    
    httpd = make_server('', port, app)
    print "Serving on port %d..." % port
    print "Try using a Web browser to go to http://%s:%d/" % \
          (socket.getfqdn(), port)
    httpd.serve_forever()
