/* locations.js */

// # Constants

var BASE_URL = "http://localhost:5000/sfmovies/api/";

// # Functions

/**
 * Initializes the front end of the application.
 */
var initialize = function () {

    // Initialize map
    var map = initializeMap();

    // Initialize info window
    var infowindow = new google.maps.InfoWindow({
        content : "<placeholder text>",
        maxWidth: 300,
    });

    // Initialize Search box
    initializeSearchBar(map, infowindow);
};

/**
 * Initializes map.
 *
 * @return {Map} An initialized Google maps object.
 */
var initializeMap = function () {

    var MAP_CANVAS = "map-canvas";
    var SF_LATITUDE = 37.748;
    var SF_LONGITUDE = -122.429;
    var DEFAULT_ZOOM = 13;

    var mapOptions = {
        center : new google.maps.LatLng(SF_LATITUDE, SF_LONGITUDE),
        zoom : DEFAULT_ZOOM
    };

    return new google.maps.Map(document.getElementById(MAP_CANVAS),
                               mapOptions);
};

/**
 * Initializes the search bar.
 *
 * @param {Map} map The Google maps object.
 * @param {InfoWindow} infowindow The {InfoWindow} used for showing the
 * information of a {Marker}.
 */
var initializeSearchBar = function (map, infowindow) {

    var SEARCH_BAR = "search-bar";
    var MOVIE_INPUT = "movie-input";
    var UI_MENU_ITEM = "ui-menu-item";

    var searchBar = document.getElementById(SEARCH_BAR);
    map.controls[google.maps.ControlPosition.TOP_LEFT].push(searchBar);

    // Auto complete

    $("#" + MOVIE_INPUT).autocomplete({
        delay : 300,
        minLength: 2,
        appendTo : "#" + SEARCH_BAR,
        source : function (request, response) {

            // Get movie titles and show most relevant
            $.getJSON(
                BASE_URL + "v1/movies?fields=title,year", function (data) {
                    var term = request.term;

                    // Get relevant movies
                    var movies = $.grep(data.movies, function (movie) {
                        return movie.title.toLowerCase()
                            .indexOf(term.toLowerCase()) > -1;
                    });

                    // Get their titles
                    var titles = $.map(movies, function(movie) {
                        return movie.title + ' (' + movie.year + ')';
                    });

                    // Remove duplicates
                    titles = titles.filter(function(elem, pos) {
                        return titles.indexOf(elem) == pos;
                    });

                    // Return a reasonable number of suggestions
                    if (titles.length > 5) {
                        titles = titles.slice(0,5);
                    }

                    response(titles);
            });
        },
    });

    // Keypress (enter)

    $("#" + MOVIE_INPUT).keypress(function (event) {

        var ENTER_KEY = 13;
        if (event.keyCode === ENTER_KEY) {

            // Extract suggestions
            var titles = [];
            $.each($('.' + UI_MENU_ITEM), function() {
                titles.push($(this).text());
            });

            // Compare input with suggestions
            var input = $("#" + MOVIE_INPUT).val();
            var queryTitle = $("." + UI_MENU_ITEM).first().text();
            for (var i = 0; i < titles.length; i++) {

                var title = titles[i];
                if (title.toLowerCase() === input.toLowerCase()) {
                    queryTitle = title;
                    break;
                }
            }

            // Set search title and add markers
            queryYear = queryTitle.substring(queryTitle.lastIndexOf('(')+1,
                                             queryTitle.length-1);
            queryTitle = queryTitle.substring(0, queryTitle.lastIndexOf(' ('));
            $("#" + MOVIE_INPUT).val(queryTitle);
            clearMarkers();
            addMarkers(queryTitle, queryYear, map, infowindow);
        }
    });
};

// Initializes the markers.
var markers = [];

/**
 * Clear all markers on the map.
 */
var clearMarkers = function() {
    for (var i = 0; i < markers.length; i++) {
        markers[i].setMap(null);
    }
    markers.length = 0;
};

/**
 * Listens for click events on the specified marker and shows its content when
 * clicked.
 *
 * @param {Map} map The Google maps object.
 * @param {Marker} marker The {Marker} to have the listener added.
 * @param {InfoWindow} infowindow The {InfoWindow} used for showing the
 * information of a {Marker}.
 */
var addMarkerClickListener = function(map, marker, infowindow) {
    google.maps.event.addListener(marker, 'click', function() {
        infowindow.setContent(marker.data);
        infowindow.open(map, marker);
    });
};

/**
 * Add all markers corresponding to movie locations for which the movie has the
 * specified title.
 *
 * @param {string} title The title of the movie.
 * @param {string} year The year the movie was mode.
 * @param {Map} map The Google maps object.
 * @param {InfoWindow} infowindow The {InfoWindow} used for showing the
 * information of a {Marker}.
 */
var addMarkers = function(title, year, map, infowindow) {

    // Get movie titles
    query_string = "v1/movies?title=" + title + "&year=" + year;
    $.getJSON(BASE_URL + query_string, function(data) {

        var movies = data.movies;
        for (var i = 0; i < movies.length; i++) {

            var movie = movies[i];
            if (movie.title !== title) {
                continue;
            }

            // Determine marker content based on the format of the movie data
            var markerContent = buildMarkerContentString(movie);

            // Create marker
            var marker = new google.maps.Marker({
                position : new google.maps.LatLng(movie.latitude,
                                                  movie.longitude),
                map : map,
                data : markerContent
            });

            // Register marker and add click listene
            markers.push(marker);
            addMarkerClickListener(map, marker, infowindow);
        }
    });
};

/**
 * Build content string for the movie location object.
 *
 * @param {Movie} movie The movie object from which to extract a content
 * string.
 * @return {string} the content string of the specified {Movie}.
 */
var buildMarkerContentString = function (movie) {

    var markerContent = '<div id="content">' +
        '<h1>' + movie.title + '</h1>' +
        '<p><b>' + movie.title + '</b>' +
        ' (' + movie.year + ')';

    if (movie.writer === movie.director) {
        markerContent += ' was written and directed by <b>' +
            movie.director + '</b>.';
    } else {
        markerContent += ' was written <b>' + movie.writer +
            '</b> and directed by <b>' + movie.director + '</b>.';
    }

    if (movie.actor_1 !== '') {
        markerContent += ' It starred <b>' + movie.actor_1 + '</b>';
        if (movie.actor_2 !== '') {
            markerContent += ' and <b>' + movie.actor_2 + '</b>';
        }
        markerContent += ".";
    }

    markerContent += '<br/><br/><b>Location:</b> ' + movie.location;

    if (movie.fun_fact !== '') {
        markerContent += '<br/><b>Fun fact:</b> ' + movie.fun_fact;
    }

    return markerContent;
};

// Run initialize function
google.maps.event.addDomListener(window, 'load', initialize);
