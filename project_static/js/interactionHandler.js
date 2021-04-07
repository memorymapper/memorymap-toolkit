// Hover interactions


MmtMap.hoverInteractions = {
	
	hoverFeatureId: null,
	touch: false,

	smallPopup: new mapboxgl.Popup({
    	closeButton: false,
    	closeOnClick: false
	}),
	
	togglePopup: function(sourceLayer) {
		map.removeFeatureState({
			source: 'interactive',
			sourceLayer: sourceLayer
		})
	},
	
	addHoverProps: function(source, sourceLayer, feature, id, coords) {
		if (source == 'interactive') {
        	id = feature.properties.id;
	    }
	    map.setFeatureState({source: source, sourceLayer: sourceLayer, id: id}, {hover: true });
	    
	    // Popup
	    map.getCanvas().style.cursor = 'pointer';
	    let name = feature.properties.name;
	    MmtMap.hoverInteractions.smallPopup.setLngLat(coords).setHTML('<p class="text-center">' + name + '</p>').addTo(map);
	}
}

// Disable hover if user is using a touchscreen

window.addEventListener('touchstart', function() {
    MmtMap.hoverInteractions.touch = true;
});



// Click interactions


MmtMap.clickInteractions = {

	clickPopup: new mapboxgl.Popup({
	    closeButton: true,
	    closeOnClick: false,
	    className: 'detail_popup'
	}),

	pageHeaderHtmlTemplate: '<div class="feature_detail shadow col-12"><br /><button type="button" class="close close_feature" aria-label="Close"><span aria-hidden="true">&times;</span></button><div class="row"><div class="col-xs-12 col-sm-8 col-lg-6" style="margin: auto"><br /><img src="<%= banner %>" alt="Photo of <%= feature_name %>" class="feature_banner img-fluid" /><p class="small"><em><%= banner_copyright %></em></p><h2><%= feature_name %></h2><br /><article>',

	documentHtmlTemplate: '<%= document_body %><hr /><br />',

	audioFileHtmlTemplate: '<h3>Listen: <%= title %></h3><div class="player <%= slug %>-detail" id="<%= slug %>"><div id="play_button_container"><a href="#" class="play" data-audio="<%= file %>" data-title="<%= title %>" data-player_id="<%= slug %>-detail"><img src="/static/img/play.svg" alt="Play audio file of <%= title %>" class="play_button" /></a></div><div class="player_display"><span class="player_timer">--:--</span><div class="progress_bar_container"><div class="progress_bar_fill"></div></div></div></div>',

	imageHtmlTemplate: '<div class="image_container"><img src="<%= file %>" alt="<%= title %>" style="width: 100%;" class="gather_for_modal"><p class="small"><em><%= title %></em></p></div>',

	pageFooterHtmlTemplate: '</article><button class="btn btn-light btn-block close_feature">Close</button><br /></article></div></div></div>',

	getFeatureDetail: function(sourceLayer, id) {
		// Loads the attachments associated with a feature and inserts them into the DOM

		// Check if any sounds are playing, and if they are, pause them
	    for (key in audioHandler.sounds) {
	        if (audioHandler.sounds[key].playing()) {
	            audioHandler.sounds[key].pause();
	            $('.' + key + ' .play_button').attr('src', '/static/img/play.svg');   
	        }
	    };

	    let url = '/api/1.0/features/' + sourceLayer + '/' + id + '/attachments/';
		
		// Then get the data for the page and display it as an overlay to the map
	    $.get(url, function(data) {
	    	$('.text_only_container').css({'overflow': 'hidden'});
	        $('.blackout_overlay, .feature_detail').remove();
	        $('.mapboxgl-control-container, .text_only_container').append('<div class="blackout_overlay close_feature"></div>');
	        
	        
	        // Once you have the data, compile the HTML fragments

	        var pageHeader = _.template(MmtMap.clickInteractions.pageHeaderHtmlTemplate);

	        page = pageHeader({
	            banner: data.properties.banner_image,
	            feature_name: data.properties.name,
	            banner_copyright: data.properties.banner_image_copyright
	        });

	        if (data.properties.popup_audio_file != null) {
	            var popupAudio = _.template(MmtMap.clickInteractions.audioFileHtmlTemplate);

	            popupAudio = popupAudio({
	                title: data.properties.popup_audio_title,
	                file: data.properties.popup_audio_file,
	                slug: data.properties.popup_audio_slug
	            });

	            page = page + popupAudio;
	        }

	        for (var i=0; i < data.attachments.length; i++) {
	            var attachment = data.attachments[i];
	            
	            switch (attachment.attachment_type) {
	                case 'document':
	                    var doc = _.template(MmtMap.clickInteractions.documentHtmlTemplate);
	                    doc = doc({
	                        document_body: attachment.body_processed
	                    });
	                    page = page + doc;
	                    break;
	                case 'audiofile':
	                    var af = _.template(MmtMap.clickInteractions.audioFileHtmlTemplate);
	                    af = af({
	                        title: attachment.title,
	                        file: attachment.file,
	                        slug: attachment.slug
	                    });
	                    page = page + af;
	                    break;
	                case 'image':
	                    var img = _.template(MmtMap.clickInteractions.imageHtmlTemplate); 
	                    img = img({
	                        title: attachment.title,
	                        file: attachment.file
	                    });
	                    page = page + img;
	                    break;
	            }
	        }

	        // Insert the compiled HTML into the DOM

	        $('.iface_container').prepend(page + MmtMap.clickInteractions.pageFooterHtmlTemplate);

	    }).done(function(data) {
	        $('.blackout_overlay, .feature_detail').fadeIn('fast');
	        pageHandler.overlay = true;

	        // If the browser supports it, update the url so that links to specific sites can be shared
	        
	        if (window.history && window.history.pushState) {
	            var params = new URLSearchParams(location.search);
	            params.set('feature_type', data.properties. feature_type);
	            params.set('id', data.id);
	            window.history.pushState({url: window.location.pathname}, '', '?' + params.toString());
	        }

	        // Activate audio player controls

	        $('.feature_detail .play').click(function(e) {
	            e.preventDefault();
	            // Load the audio file
	            let audio_file = $(this).data('audio');
	            let title = $(this).data('title');
	            let player_id = $(this).data('player_id');
	            audioHandler.handleAudio(audio_file, title, player_id);

	            // Then attach the handler for the progress bar
	            $('.' + player_id + ' .progress_bar_container').click(function(e) {
	                var pos = e.pageX - $(this).offset().left;
	                var width = $(this).width();
	                var percentage = (pos / width) * 100;
	                audioHandler.setSeekPositionFromProgressBar(player_id, percentage);
	            });

	        });

	        // Dismiss the overlay, destroying all the attached sounds
	        $('.close_feature').click(function() {
	            
	            $('.feature_detail .play').each(function() {
	                var player_id = $(this).data('player_id');
	                // If the sound exists, forget about it...
	                try {
	                    audioHandler.sounds[player_id].unload();
	                    delete audioHandler.sounds[player_id];
	                } catch {
	                    // Otherwise, do nothing as there is no attached to the feature
	                }
	            })

	            $('.blackout_overlay, .feature_detail').fadeOut('fast', function() {
	                $('.blackout_overlay, .feature_detail').remove();
	                $('.text_only_container').css({'overflow-x': 'hidden', 'overflow-y': 'scroll'});
	                pageHandler.overlay = false;   
	            });

	            // Reset the url
	            if (window.history && window.history.pushState) {
	                window.history.pushState({url: ''}, '', window.location.pathname);
	            }

	        });

	    });
	},

	clickPopup: new mapboxgl.Popup({
	    closeButton: true,
	    closeOnClick: false,
	    className: 'detail_popup'
	}),

	popupHtmlTemplate: '<div class="popup_header"><img src="<%= image %>" alt="Image of <%= name %>" /><p class="text-center feature_title"><%= name %></p><br /></div>',

	popupAudioFileHtmlTemplate: '<div class="player popup_player <%= playerId %>" id="<%= playerId %>"><div id="play_button_container"><a href="#" class="play" data-audio="<%= url %>"><img src="/static/img/play.svg" alt="play" class="play_button" /></a></div><div class="player_display"><span class="player_timer">--:--</span><div class="progress_bar_container"><div class="progress_bar_fill"></div></div></div></div><p class="text-center"><strong>Listen: </strong><%= playerTitle %></p></span><hr />',


	clickFeature: function(source, sourceLayer, feature, id, coords) {
		// Loads the feature from the server and adds a large click popup with an audio player (if there is an audio file related to it)

		$.get('api/1.0/features/' + sourceLayer + '/' + id, function(data) {
	        // Construct the HTML for the popup and add it to the map

	        let popupPlayerId = undefined;
	        let popupHtml = _.template(MmtMap.clickInteractions.popupHtmlTemplate);

	        popupHtml = popupHtml({
	        	image: data.properties.popup_image,
	        	name: data.properties.name
	        });


	        // If there is an audio file attached to the feature, add a player
	        if (data.properties.popup_audio_file != null) {
	            // Create an ID for the player based on the title
	            popupPlayerId = data.properties.popup_audio_slug
	            let popupAudioFileHtml = _.template(MmtMap.clickInteractions.popupAudioFileHtmlTemplate);

             	popupAudioFileHtml = popupAudioFileHtml({
	            	playerId: popupPlayerId,
	            	url: data.properties.popup_audio_file.url,
	            	playerTitle: data.properties.popup_audio_title
	            }); 
	            popupHtml = popupHtml +  popupAudioFileHtml;   
	        }



	        let buttonHtml = '<div class="text-center"><br /><button type="button" class="btn btn-sm btn-light read_more" href="#">Read More</button> <button type="button" class="btn btn-sm btn-light close_popup">Close</button></div>';
	        
	        popupHtml = popupHtml + buttonHtml;
	        MmtMap.clickInteractions.clickPopup.setLngLat(coords).setHTML(popupHtml).addTo(map);
	        

	        // If there is an audio file attached to the feature, load the audio file and prepare it for playing

	        if (typeof popupPlayerId !== undefined) {
	            audioHandler.updateProgressBar(popupPlayerId);
	            // Activate popup player and map player widget
	            $('.popup_player.' + popupPlayerId + ' .play').click(function(e) {
	                e.preventDefault();

	                audioHandler.handleAudio(data.properties.popup_audio_file, data.properties.popup_audio_title, popupPlayerId);

	                // Update the progress bar and enable seek

	                $('.' + popupPlayerId + ' .progress_bar_container').click(function(e) {
	                    var pos = e.pageX - $(this).offset().left;
	                    var width = $(this).width();
	                    var percentage = Math.round((pos / width) * 100);
	                    audioHandler.setSeekPositionFromProgressBar(popupPlayerId, percentage);
	                });

	            }); // Popup player activated        
	        }
	        
	        $('.close_popup').click(function(e) {
	            MmtMap.clickInteractions.clickPopup.remove();
	            MmtMap.hoverInteractions.togglePopup(sourceLayer);
	            
	            // If a sound exists and is playing, pause it
	            try {
	            	if (audioHandler.sounds[popupPlayerId].playing()) {
	            		audioHandler.sounds[popupPlayerId].pause();
	        		}
	        	} catch (err) {
	        		// Do nothing
	        	}
	        });

	        $('.read_more').click(function(e) {
	            MmtMap.clickInteractions.getFeatureDetail(sourceLayer, id)
	        });
	    });
	}




}