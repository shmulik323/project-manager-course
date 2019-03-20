var proxy = require('http-proxy-middleware')

var apiProxy = proxy('http://127.0.0.1:3333/api')
