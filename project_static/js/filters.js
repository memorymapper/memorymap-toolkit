// Filter features by theme

$('.theme').click(function(e) {
    e.preventDefault();
    var key = $(this).data('key');
    if (key != undefined) {
        
        map.setFilter('polygons', ['==', ['get', 'theme_id'], key]);
        map.setFilter('polygon_outlines', ['==', ['get', 'theme_id'], key]);
        map.setFilter('points', ['==', ['get', 'theme_id'], key]);
        map.setFilter('points_labels', ['==', ['get', 'theme_id'], key]);
        map.setFilter('polygon_labels', ['==', ['get', 'theme_id'], key]);

        $('.theme').each(function() {
            var color = $(this).data('color');
            $(this).css('background-color', 'transparent');
            $(this).css('color', color);
        });

        var color = $(this).data('color');
        $(this).css('background-color', color);
        $(this).css('color', '#e3e3e3');

    } else {
        map.setFilter('polygons');
        map.setFilter('polygon_outlines');
        map.setFilter('points');
        map.setFilter('points_labels');
        map.setFilter('polygon_labels');
        $('.theme').each(function() {
            var color = $(this).data('color');
            $(this).css('background-color', 'transparent');
            $(this).css('color', color);
        });
    }
});