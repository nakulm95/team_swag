(function() {
	$(document).ready(function() {
		contentLoad();
	});

	function contentLoad() {
		loadContent(function(g) {
			console.log(g);
		});
	}

	function loadContent(callback) {
		var request = $.ajax({
			url: 'http://108.179.166.105:8080/garages',
			type: 'GET'
		});

		request.done(function(res, error) {
			if (!res || res === null || res.status === 'failure') {
				callback({error: 'bad request'});
			} else {
				callback(res);
			}
		});

		request.fail(function(data, error) {
			callback({error: 'errorzz'});
		});
	}
})();