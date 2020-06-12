/* Search */

function normalise(string) {
    return string.trim().toLowerCase();
}

function getUniqueFeatures(array, comparatorProperty) {
    var existingFeatureKeys = {};
    // Because features come from tiled vector data, feature geometries may be split
    // or duplicated across tile boundaries and, as a result, features may appear
    // multiple times in query results. We therefore need to filter out the duplicates.
    var uniqueFeatures = array.filter(function(el) {
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
    $(this).val('');
    map.setFilter('polygons');
    map.setFilter('polygon_outlines');
    map.setFilter('points');
    map.setFilter('points_labels');
    map.setFilter('polygon_labels');
});

$('#map_search').keyup(function(e) {

    var search_string = normalise($(this)[0].value);
    map.setFilter('polygons');
    map.setFilter('polygon_outlines');
    map.setFilter('points');
    map.setFilter('points_labels');
    map.setFilter('polygon_labels');

    if (search_string.length > 2) {
        
        $('.theme').each(function() {
            $(this).css('background-color', 'transparent');
            $(this).css('color', $(this).data('colour'));
        });


        var features = map.queryRenderedFeatures({
            layers: ['points', 'polygons']
        });


        var unique_features = getUniqueFeatures(features, 'name');

        var filtered_features = unique_features.filter(function(feature) {
            var name = normalise(feature.properties.name);
            return name.indexOf(search_string) > -1;
        })

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
        } else {
            map.setFilter('polygons', false);
            map.setFilter('polygon_outlines', false);
            map.setFilter('polygon_labels', false);
            map.setFilter('points', false);
            map.setFilter('points_labels', false);
        }


        var bounds = turf.bbox(turf.featureCollection(filtered_features));
        map.fitBounds(bounds);
        

    } else {
        map.setFilter('polygons');
        map.setFilter('polygon_outlines');
        map.setFilter('points');
        map.setFilter('polygon_labels');
        map.setFilter('points_labels');
    }
});