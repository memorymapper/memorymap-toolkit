// Add the themes to the menu bar

$('#themes').append('<a href="#" class="theme dropdown-item">All</a>')

for (let i=0; i < MmtMap.themes.length; i++) {
    let themes = MmtMap.themes;
    let theme = '<a href="#" class="theme dropdown-item ' + themes[i].name +  '" data-key="' + themes[i].id + '" data-color="' + themes[i].color +'" style="color: '+ themes[i].color +'">' + themes[i].name + '</a>';
    $('#themes').append(theme);
}




MmtFeatureList.populateList = function(url, params) {
	
	query = $.param(params);

	$.get(url + '?' + query, function(data) {
		let features = data.features;
		let totalPages = data.totalPages;
		let page = data.page;

		let featureCardHeaderHtmlTemplate = '<div class="card"><div class="card-body"><h4 class="card-title"><%= name %></h4><p><%= description %></p><hr />';

		let audioPlayerHtmlTemplate = '<h6>Listen: <%= title %></h6><div class="player card-<%= slug %>-detail" id="card-<%= slug %>"><div id="play_button_container"><a href="#" class="play" data-audio="<%= file %>" data-title="<%= title %>", data-player_id="card-<%= slug %>-detail"><img src="/static/img/play.svg" alt="Play Audio File of <%= title %>" class="play_button" /></a></div><div class="player_display"><span class="player_timer">--:--</span><div class="progress_bar_container"><div class="progress_bar_fill"></div></div></div></div>';

		let featureCardButtonHtmlTemplate = '<br /><a href="#" class="btn btn-sm btn-light read_more" data-layer="<%= layer %>" data-id="<%= featureId %>">Read More</a></div></div><br />';

		let paginationHtmlTemplate = '<nav aria-label="pagination"><ul class="pagination"><%= page_numbers %></ul></nav>';

		// If there are no features, tell the user

		if (features.length == 0) {
			$('.feature_list').empty();
			$('.feature_list').append('<p class="lead">No results found</p>');
		}

		// Add all the features as cards, activating the audio players...

		for (let i=0; i<features.length; i++) {
			let featureCardHeaderHtml = _.template(featureCardHeaderHtmlTemplate);
			let audioPlayerHtml = _.template(audioPlayerHtmlTemplate);
			let featureCardButtonHtml = _.template(featureCardButtonHtmlTemplate);

			let sourceLayer = undefined;

			switch(features[i].properties.feature_type) {
				case 'point':
					sourceLayer = 'points';
					break;
				case 'line':
					sourceLayer = 'lines';
					break;
				case 'polygon':
					sourceLayer = 'polygons';
					break;
			}

			featureCardHeaderHtml = featureCardHeaderHtml({
				name: features[i].properties.name,
				description: features[i].properties.description
			});

			featureCardButtonHtml = featureCardButtonHtml({
				layer: sourceLayer, 
				featureId: features[i].id
			});
				
			audioPlayerHtml = audioPlayerHtml({
				title: features[i].properties.popup_audio_title,
				slug: features[i].properties.popup_audio_slug,
				file: features[i].properties.popup_audio_file
			})

			

			let cardHtml = featureCardHeaderHtml;

			if (features[i].properties.popup_audio_slug != '') {
				cardHtml += audioPlayerHtml;
			}

			cardHtml += featureCardButtonHtml;

			$('.feature_list').append(cardHtml);

		}

		// Add pagination, if necessary

		if (totalPages > 1) {

			page_numbers = '';

			let paginationHtml = _.template(paginationHtmlTemplate);

			for (let i = 1; i <= totalPages; i++) {
				if (page == i) {
					page_numbers += '<li class="page-item active"><span class="page-link">' + i + '<span class="sr-only">(current)</span></span></li>';
				} else {
					page_numbers += '<li class="page-item"><a class="page-link" data-page="' + i +'" href="#">' + i + '</a></li>'
				}
			};

			paginationHtml = paginationHtml({
				page_numbers: page_numbers
			});

			$('.feature_list').append(paginationHtml);

			$('a.page-link').click(function(e) {
				e.preventDefault();
				let page = $(this).data('page');
				$('.feature_list').empty();
				MmtFeatureList.populateList(url, {page: page});
			})

		}

		// Activate read more and play buttons

		$('.read_more').click(function(e) {
			e.preventDefault();
			let featureId = $(this).data('id');
			let layer = $(this).data('layer');
			MmtMap.clickInteractions.getFeatureDetail(layer, featureId);
		});

		$('.play').click(function(e) {
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

	});
}
