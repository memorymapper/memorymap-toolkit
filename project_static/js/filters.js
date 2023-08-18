// Filter features by theme

$('.theme').click(function(e) {
    e.preventDefault();
    let key = $(this).data('key');
    if (key != undefined) {
        
        map.setFilter('polygons', ['==', ['get', 'theme_id'], key]);
        map.setFilter('polygon_outlines', ['==', ['get', 'theme_id'], key]);
        map.setFilter('points', ['==', ['get', 'theme_id'], key]);
        map.setFilter('points_labels', ['==', ['get', 'theme_id'], key]);
        map.setFilter('polygon_labels', ['==', ['get', 'theme_id'], key]);
        map.setFilter('lines', ['==', ['get', 'theme_id'], key]);
        map.setFilter('line_labels', ['==', ['get', 'theme_id'], key]);

        $('.theme').each(function() {
            var color = $(this).data('color');
            $(this).css('background-color', 'transparent');
            $(this).css('color', color);
        });

        let color = $(this).data('color');
        $(this).css('background-color', color);
        $(this).css('color', '#e3e3e3');

    } else {
        map.setFilter('polygons');
        map.setFilter('polygon_outlines');
        map.setFilter('points');
        map.setFilter('points_labels');
        map.setFilter('polygon_labels');
        map.setFilter('lines');
        map.setFilter('line_labels');
        $('.theme').each(function() {
            let color = $(this).data('color');
            $(this).css('background-color', 'transparent');
            $(this).css('color', color);
        });
    }
});

// Filter features by tag

$('.tag').click(function(e) {
    e.preventDefault();
    let tag = $(this).data('tag');
    if (tag != undefined) {
        map.setFilter('polygons', ['in', tag, ['get', 'tag_str']]);
        map.setFilter('polygon_outlines', ['in', tag, ['get', 'tag_str']]);
        map.setFilter('points', ['in', tag, ['get', 'tag_str']]);
        map.setFilter('points_labels', ['in', tag, ['get', 'tag_str']]);
        map.setFilter('polygon_labels', ['in', tag, ['get', 'tag_str']]);
        map.setFilter('line_labels', ['in', tag, ['get', 'tag_str']]);
        map.setFilter('lines', ['in', tag, ['get', 'tag_str']]);
    } else {
        map.setFilter('polygons');
        map.setFilter('polygon_outlines');
        map.setFilter('points');
        map.setFilter('points_labels');
        map.setFilter('polygon_labels');
        map.setFilter('lines');
        map.setFilter('line_labels');
    }
})