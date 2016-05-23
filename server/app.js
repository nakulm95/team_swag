// Books and Genres web service

// call the packages we need
var express = require('express');
var app = express();
var bodyParser = require('body-parser');
var mongoose = require('mongoose');
var router = express.Router(); // todo: use router to add better functionality and routing capability; 

// my models
var Garage = require('./models/garage')

var server_ip_address = process.env.OPENSHIFT_NODEJS_IP || '127.0.0.1';
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

		// NOT NEEDED:
		// Garage.getGarageById(body.garageID, function(err, garage) {
		// 	if (err) {
		// 		throw err;
		// 	}
		// 	// if garage is found, update the garage info just in case. otherwise, add garage
		// 	if (garage != null) {
		// 		console.log("entering here");
		// 		Garage.findOneAndUpdate({garageID: body.garageID}, {$set: {spotsAvailable: body.spots}}, {new: true, upsert: true}, function(err, garage) {
		// 			console.log(garage != null ? garage.spotsAvailable : "gg");
		// 		});
		// 	} else {
		// 		Garage.addGarage(body, function(err, garage) {});
		// 	}
		// 	res.json({message: 'Garage created!'});
		// });
	})
	.get(function(req, res) {
		Garage.find(function(err, garage) {
			if (err)
				res.send(err);

			res.json(garage);
		});
	});

// get garage by specific id (garage id)
router.route('/garages/:garage_id')
	.get(function(req, res) {
		Garage.getGarageById(req.params.garage_id, function(err, garage) {
			if (err)
				res.send(err);

			res.json(garage);
		});
	});


/* Genre */

router.get('/api/genres', function(request, response) {
	Genre.getGenres(function(err, genres) {
		if (err) {
			throw err;
		}
		response.json(genres);
	});
});

router.post('/api/genres', function(request, response) {
	var genre = request.body;
	Genre.addGenre(genre, function(err, genre) {
		if (err) {
			throw err;
		}
		response.json(genre);
	});
});

/* Books */

router.get('/api/books/', function(request, response) {
	Book.getBooks(function(err, books) {
		if (err) {
			throw err;
		}
		response.json(books);
	});
});


router.get('/api/books/:_id', function(request, response) {
	Book.getBookById(request.params._id, function(err, book) {
		if (err) {
			throw err;
		}
		response.json(book);
	});
});

router.post('/api/books', function(request, response) {
	var book = request.body;
	Book.addBook(book, function(err, book) {
		if (err) {
			throw err;
		}
		response.json(book);
	});
});

app.use('/', router);

app.listen(server_port, server_ip_address, function() {
	console.log("Listening on " + server_ip_address + " on port " + server_port);
});
