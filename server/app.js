// Garages web service

// call the packages we need
var express = require('express');
var app = express();
var bodyParser = require('body-parser');
var mongoose = require('mongoose');
var router = express.Router(); // todo: use router to add better functionality and routing capability;

// my models
var Garage = require('./models/garage')

var server_ip_address = process.env.OPENSHIFT_NODEJS_IP || '69.91.161.58';
var server_port = process.env.OPENSHIFT_NODEJS_PORT || 8080;

// MongoDB
mongoose.connect('eeshan:eeshan@ds017070.mlab.com:17070/eeshan');
var db = mongoose.connection;

// middleware
app.use(bodyParser.urlencoded({ extended: true}));
app.use(bodyParser.json());

router.use(function(req, res, next) {
	console.log("shits happening");
	next();
});

// GET http://localhost:8080
router.get('/', function(request, response) {
	response.json({message: "swag", val: 0});
});

// add garage, or get all garages
router.route('/garages')
	.post(function(req, res) {
		var body = req.body;
		// with upsert:true, creates the object if it doesn't exist. otherwise, updates fields specificed in $set: {}
		Garage.findOneAndUpdate({garageID: body.garageID}, {$set: {spotsAvailable: body.spots, address: body.address}}, {upsert: true}, function(err, garage) {});
		res.json({message: 'Garage created!'});
	})
	.get(function(req, res) {
		Garage.find(function(err, garage) {
			if (err)
				res.send(err);

			res.jsonp(garage);
		});
	});

// get/update garage by specific id (garage id)
router.route('/garages/:garage_id')
	.get(function(req, res) {
		Garage.getGarageById(req.params.garage_id, function(err, garage) {
			if (err)
				res.send(err);

			if (garage == null) {
				res.status(202);
				res.send("Garage doesn't exist!");
			} else {
				res.jsonp(garage);
			}
		});
	})
	.put(function(req, res) {
		Garage.getGarageById(req.params.garage_id, function(err, garage) {
			if (err)
				res.send(err)

			var curr_count = parseInt(garage.spotsAvailable);
			var updated_count = curr_count + parseInt(req.body.spots);
			Garage.findOneAndUpdate({garageID: req.body.garageID}, {$set: {spotsAvailable: updated_count}}, function(err, garage) {
				if (err)
					res.send(err);

				res.json({message: "Updated!"});
			});
		});
	})
	.delete(function(req, res) {
		Garage.findOneAndRemove({garageID: req.body.garageID}, function(error, doc, result) {
			if (error)
				res.send(error)

			res.json({message: "Garage removed!"});
		});
	});

app.use('/', router);

app.listen(server_port, server_ip_address, function() {
	console.log("Listening on " + server_ip_address + " on port " + server_port);
});
