(function() {
	$(document).ready(function() {
	  contentLoad();
	  $('html').click(function(e) {
	    if ($("#spots").innerHTML != "") {
	      $("#spots").text("");
	    }
	  });
	});

	function contentLoad() {
	  loadContent(function(g) {
	    var l = $("#lis");
	    g.forEach(function(element) {
	      var ul = $('<li>').text(element.garageID);
	      ul.on('click', function(e) {
	        getUpdatedData(element.garageID, function(info) {
	          if (info.error != null) {
	            console.log("error");
	          } else {
	            var d = $("#spots");
	            d.text(info.spotsAvailable);
	          }
	        });
	      });
	      ul.appendTo(l);
	    });
	  });
	}

	function getUpdatedData(id, callback) {
	  var request = $.ajax({
	    url: 'http://69.91.161.58:8080/garages/' + id,
	    type: 'GET',
	    dataType: 'jsonp'
	  });

	  request.done(function(res, error) {
	    if (!res || res === null || res.status_code === 202) {
	      callback({error: 'bad request'});
	    } else {
	      callback(res);
	    }
	  });

	  request.fail(function(data, error) {
	    callback({error: error});
	  });
	}

	function loadContent(callback) {
	  var request = $.ajax({
	    url: 'http://69.91.161.58:8080/garages',
	    type: 'GET',
	    dataType: 'jsonp'
	  });

	  request.done(function(res, error) {
	    if (!res || res === null || res.status === 'failure') {
	      callback({error: 'bad request'});
	    } else {
	      callback(res);
	    }
	  });

	  request.fail(function(data, error) {
	    callback({error: error});
	  });
	}
})();