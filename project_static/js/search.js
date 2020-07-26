/* Search */

function normalise(string) {
    return string.trim().toLowerCase();
}

function getUniqueFeatures(array, comparatorProperty) {
    let existingFeatureKeys = {};
    // Because features come from tiled vector data, feature geometries may be split
    // or duplicated across tile boundaries and, as a result, features may appear
    // multiple times in query results. We therefore need to filter out the duplicates.
    let uniqueFeatures = array.filter(function(el) {
        if (existingFeatureKeys[el.properties[comparatorProperty]]) {
            return false;
        } else {
            existingFeatureKeys[el.properties[comparatorProperty]] = true;
            return true;
        }
    }); 
    return uniqueFeatures;
}

/* Prevent the page refreshing when the user presses the enter key */

$("form").on('submit',function(e){
    e.preventDefault();
});

/* Clear the search bar and results on focus */

$('#map_search').focus(function(e) {

    map.panTo(MmtMap.settings.mapCenter);
    map.zoomTo(MmtMap.settings.zoom);

    $(this).val('');
    map.setFilter('polygons');
    map.setFilter('polygon_outlines');
    map.setFilter('points');
    map.setFilter('points_labels');
    map.setFilter('polygon_labels');
});


$('#map_search').keyup(function(e) {

    map.panTo(MmtMap.settings.mapCenter);
    map.zoomTo(MmtMap.settings.zoom);    

    let search_string = normalise($(this)[0].value);
    map.setFilter('polygons');
    map.setFilter('polygon_outlines');
    map.setFilter('points');
    map.setFilter('points_labels');
    map.setFilter('polygon_labels');
    map.setFilter('lines');

    if (search_string.length > 2) {
        
        $('.theme').each(function() {
            $(this).css('background-color', 'transparent');
            $(this).css('color', $(this).data('colour'));
        });


        let features = map.queryRenderedFeatures({
            layers: ['points', 'polygons', 'lines']
        });


        let unique_features = getUniqueFeatures(features, 'name');

        let filtered_features = unique_features.filter(function(feature) {
            let name = normalise(feature.properties.name) + ' ' + normalise(feature.properties.tag_str);
            return name.indexOf(search_string) > -1;
        });

        if (filtered_features.length > 0) {
            map.setFilter('polygons', ['match', ['get', 'name'], filtered_features.map(function(feature) {
                return feature.properties.name;
            }), true, false]);
            map.setFilter('polygon_outlines', ['match', ['get', 'name'], filtered_features.map(function(feature) {
                return feature.properties.name;
            }), true, false]);
            map.setFilter('polygon_labels', ['match', ['get', 'name'], filtered_features.map(function(feature) {
                return feature.properties.name;
            }), true, false]);
            map.setFilter('points', ['match', ['get', 'name'], filtered_features.map(function(feature) {
                return feature.properties.name;
            }), true, false]);
            map.setFilter('points_labels', ['match', ['get', 'name'], filtered_features.map(function(feature) {
                return feature.properties.name;
            }), true, false]); 
            map.setFilter('lines', ['match', ['get', 'name'], filtered_features.map(function(feature) {
                return feature.properties.name;
            }), true, false]); 
            
            let bounds = turf.bbox(turf.featureCollection(filtered_features));
            map.fitBounds(bounds);

        }

    } else {
        map.setFilter('polygons');
        map.setFilter('polygon_outlines');
        map.setFilter('points');
        map.setFilter('polygon_labels');
        map.setFilter('points_labels');
        map.setFilter('lines');
    }
});