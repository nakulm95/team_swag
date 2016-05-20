// Books and Genres web service

// call the packages we need
var express = require('express');
var app = express();
var bodyParser = require('body-parser');
var mongoose = require('mongoose');

// my models
var Genre = require('./models/genre');
var Book = require('./models/book');
var Garage = require('./models/cars')


var server_ip_address = process.env.OPENSHIFT_NODEJS_IP || '127.0.0.1';

var server_port = process.env.OPENSHIFT_NODEJS_PORT || 8080;

// MongoDB
mongoose.connect('eeshan:eeshan@ds017070.mlab.com:17070/eeshan');
var db = mongoose.connection;

// middleware
app.use(bodyParser.json());

app.get('/', function(request, response) {
	response.send("swag");
});


app.post("/init", function(request, response)) {
	var body = request.body;
	Garage.getGarageById(body.garageID, function(err, garage) {
		if (err) {
			throw err;
		}

		if (garage != null{
			//Garage.deleteGarageById(body.garageID, function(err, garage) {});
			Garage.findOneAndUpdate({"garageID": body.garageID}, body, function(err, garage) {});
		} else {
			Garage.addGarage(body, function(err, garage) {});
		}

	});

}

/* Genre */

app.get('/api/genres', function(request, response) {
	Genre.getGenres(function(err, genres) {
		if (err) {
			throw err;
		}
		response.json(genres);
	});
});

app.post('/api/genres', function(request, response) {
	var genre = request.body;
	Genre.addGenre(genre, function(err, genre) {
		if (err) {
			throw err;
		}
		response.json(genre);
	});
});

/* Books */

app.get('/api/books/', function(request, response) {
	Book.getBooks(function(err, books) {
		if (err) {
			throw err;
		}
		response.json(books);
	});
});


app.get('/api/books/:_id', function(request, response) {
	Book.getBookById(request.params._id, function(err, book) {
		if (err) {
			throw err;
		}
		response.json(book);
	});
});

app.post('/api/books', function(request, response) {
	var book = request.body;
	Book.addBook(book, function(err, book) {
		if (err) {
			throw err;
		}
		response.json(book);
	});
});

app.listen(server_port, server_ip_address, function() {
	console.log("Listening on " + server_ip_address + " on port " + server_port);
});
