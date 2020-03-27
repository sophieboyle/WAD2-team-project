// If a user presses enter on the searchbar.
$(document).on('keypress', function(e) {
    if(e.which != 13 || !$("#search-bar").is(":focus")) {
        return;
    }

    let song = $("#search-bar")[0].value;
    let baseURL = $("#search-bar")[0].baseURI.replace(/spuni\/(.*)/g, "");
    baseURL += "spuni/search/"+song;
    window.location.replace(baseURL);
});