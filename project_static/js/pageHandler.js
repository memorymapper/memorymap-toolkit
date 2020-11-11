let pageHandler = {
	// Handles displaying static pages and direct linking to feature pages

	overlay: false,

	pageHtmlTemplate: '<div class="feature_detail shadow col-12"><br /><button type="button" class="close close_feature" aria-label="Close"><span aria-hidden="true">&times;</span></button><div class="row"><div class="col-xs-12 col-sm-8 col-lg-6" style="margin: auto"><article><%= body %><button class="btn btn-light btn-block close_feature">Close</button><br /></article></div></div></div>',

	getPage: function(url) {
		$.get(url, function(data) {

			if (pageHandler.overlay == true) {
				$('.blackout_overlay, .feature_detail').fadeOut('fast', function() {
					$('.text_only_container').css({'overflow': 'hidden'});
					$('.blackout_overlay, .feature_detail').remove();
					$('.mapboxgl-control-container, .text_only_container').append('<div class="blackout_overlay close_feature"></div>');
				});
			} else {
				$('.text_only_container').css({'overflow': 'hidden'});
				$('.mapboxgl-control-container, .text_only_container').append('<div class="blackout_overlay close_feature"></div>');
			}

	        let pageHtml = _.template(pageHandler.pageHtmlTemplate);

	        pageHtml = pageHtml({body: data.body});

	        $('.iface_container').prepend(pageHtml); 
	    }).done(function() {
	        $('.blackout_overlay, .feature_detail').fadeIn('fast');
	        pageHandler.overlay = true;
	        $('.close_feature').click(function() {
	            $('.blackout_overlay, .feature_detail').fadeOut('fast', function() {
	                $('.blackout_overlay, .feature_detail').remove();
	                $('.text_only_container').css({'overflow-x': 'hidden', 'overflow-y': 'scroll'});
	                pageHandler.overlay = false;
	            });
	            if (window.history && window.history.pushState) {
	                window.history.pushState({url: ''}, '', window.location.pathname);
	            }
	        });

	    });
	},

	loadFeatureDetailFromUrlParams: function() {
		let urlParams = new URLSearchParams(location.search);

		if (urlParams.get('feature_type') && urlParams.get('id')) {
			let id = Number(urlParams.get('id'));
	    	let feature_type = urlParams.get('feature_type');

		    switch (feature_type) {
		        case 'polygon':
		            source_layer = 'polygons';
		            break;
		        case 'point':
		            source_layer = 'points'
		            break;
		        case 'line':
		            source_layer = 'lines';
		            break;
		    }

	    	MmtMap.clickInteractions.getFeatureDetail(source_layer, id);
			}
	},

	showWelcomeMessage: function() {
		let url = new URLSearchParams(location.search);
		if (url.toString() == "") {
		    $('#welcomeMessageModal').modal('show');
		}
	},

	populatePageMenu: function() {
		$.get('/api/1.0/pages/', function(data) {
			for (let i=0; i < data.length; i++) {
				let link = '<a class="dropdown-item page_link" href="/api/1.0/pages/' + data[i].slug + '">'+ data[i].title +'</a>';
				$('#pages').prepend(link);
			}
		}).done(function() {
			$('.page_link').click(function(e) {
				e.preventDefault(0);
				let url = $(this).attr('href');
				pageHandler.getPage(url);			
			});
		});
	}

}

