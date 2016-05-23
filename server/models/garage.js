var mongoose = require('mongoose');

var garageSchema = mongoose.Schema({
  spotsAvailable:{
    type: Number,
    required: true,
    default: 0
  },
  garageID:{
    type: String,
    required: true,
    default: ""
  },
  address:{
    type: String,
    required: true,
    default: ""
  }
});

var Garage = module.exports = mongoose.model('Garage', garageSchema);

// Get garageby id
module.exports.getGarageById = function(id, callback) {
  console.log("garade id: " + id);
  Garage.findOne({'garageID': id}, 'spotsAvailable garageID address', callback);
};


module.exports.addGarage = function(data, callback) {
  console.log("adding garage");
  var garage = {}
  garage.spotsAvailable = data.spots;
  garage.garageID = data.garageID;
  garage.address = data.address;
  Garage.create(garage, callback)
};


module.exports.deleteGarageById = function(id, callback) {
  Garage.getGarageById(id, callback).remove().exec();
}
