var mongoose = require('mongoose');

var garageSchema = mongoose.Schema({
  spotsAvailable:{
    type: Number,
    required: true
  },
  garageID:{
    type: String,
    required: True
  },
  address:{
    type: String,
    required: True
  }
});

var Garage = module.exports = mongoose.model('Garage', garageSchema);

// Get garageby id
module.exports.getGarageById = function(id, callback) {
  return Garage.findOne({'garageID': id }, 'spotsAvailable garageID address', function (err, garage) {
    if (err) return handleError(err);
    console.log("swag");
    return garage;
  })
};


module.exports.addGarage = function(data, callback) {
  var garage = {}
  garage.spotsAvailable = data.spots;
  garage.garageID = data.garageID;
  garage.address = data.address;
  Garage.create(garage, callback)
};


module.exports.deleteGarageById = function(id, callback) {
  Garage.getGarageById(id, callback).remove().exec();
}
