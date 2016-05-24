var express = require('express');
var app = express();
var bodyParser = require('body-parser');
var router = express.Router(); // todo: use router to add better functionality and routing capability; 

app.use(bodyParser.urlencoded({ extended: true}));
app.use(bodyParser.json());

var server_ip_address = process.env.OPENSHIFT_NODEJS_IP || '127.0.0.1';
var server_port = process.env.OPENSHIFT_NODEJS_PORT || 8080;

router.get('/garages', function(req, res) {
    res.sendFile('pkn.html', {root: __dirname});
});

app.use('/', router);

app.listen(server_port, server_ip_address, function() {
    console.log("Listening on " + server_ip_address + " on port " + server_port);
});
