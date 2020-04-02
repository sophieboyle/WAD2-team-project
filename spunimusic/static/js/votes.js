// Sends a request to the backend to like/dislike a song.
function sendRequest(requestUrl, username, slug, song, albumart, artist) {
    $.ajax({
        type: "GET",
        url: requestUrl,
        data: {
            "username": username,
            "slug": slug,
            "name": song,
            "albumArt": albumart,
            "artist": artist
        },
        dataType: "json"
    });
};

// Increases/Decreases an element.
function changeValue(element, action) {
    let parent = $(element).parent();
    let tElement = "";

    if (window.location.href.includes("/spuni/song")) {
        tElement = $(parent).parent()[0];
    } else {
        tElement = $(parent).find(".song-text")[0];
    }

    // Getting the current upvotes.
    let rx = /Likes<\/strong>: (\d+)/g;
    let value = rx.exec(tElement.outerHTML);
    let upvotes = parseInt(value[1]);

    // Change the value.
    if (action == "increment") {
        upvotes += 1;
    } else if (action == "decrement") {
        upvotes -= 1;
    }

    // Replacing the value.
    let cElement = tElement.outerHTML.replace(/Likes<\/strong>: (\d+)/g, "Likes</strong>: "+upvotes);
    $(tElement).replaceWith(cElement);
}

// When a user clicks the upvote or the downvote button.
$(document).on("click", "#upvote, #downvote", function() {
    let rx;
    let username = "";
    let parent = "";

    if ($("#register").length == 1) {
        $.notify("You need to be logged in to vote.", "error");
        return;
    }

    if (window.location.href.includes("/spuni/song")) {
        parent = $(this).parent().parent()[0];
    } else {
        parent = $(this).parent()[0];
    }

    let parentInnerText = parent.innerText;

    // Getting the username.
    if ($("#profile").length != 0) {
        let usernameHref = $("#profile")[0].attributes["href"].nodeValue;
        rx = /\/profile\/(\w+)/g
        username = rx.exec(usernameHref)[1];
    }
    
    // Artist name.
    rx = /Artist: (.[^\\]*)/g
    let artistname = rx.exec(parentInnerText)[1].split("\n")[0];

    // Song name.
    rx = /Song: (.[^\\]*)/g;
    let songname = rx.exec(parentInnerText)[1].split("\n")[0];

    // Getting the slug.
    let slug = "";
    if (window.location.href.includes("/spuni/song")) {
        slug = songname + " " + artistname;
        slug = slug.toLowerCase();
        slug = slug.replace(/ /g, "-");
    } else {
        slug = $(this).attr("title");
    }

    // Album
    let albumart = "";
    if (window.location.href.includes("/spuni/song")) { 
        albumart = parent.childNodes[1].currentSrc;
    } else {
        albumart = parent.childNodes[1].childNodes[1].attributes[1].nodeValue;
    }
    
    // If the user pressed the upvote button.
    if ($(this).attr("id") == "upvote") {
        // If it has been already selected then downvote.
        if ($(this).hasClass("selected")) {
            $(this).removeClass("selected");
            sendRequest("/downvote", username, slug, songname, albumart, artistname);
            changeValue(this, "decrement");
        // Otherwise upvote and highlight.
        } else {
            $(this).addClass("selected");
            sendRequest("/upvote", username, slug, songname, albumart, artistname);
            changeValue(this, "increment");
        }

        // If the downvote button is highlighted then remove.
        if ($(this).prev().hasClass("selected")) {
            $(this).prev().removeClass("selected");
        }
        $.notify("Your vote has been sent.", "info");

    // Otherwise if the user presses the downvote button.
    } else if ($(this).attr("id") == "downvote") {
        // If it has been already selected then upvote.
        if ($(this).hasClass("selected")) {
            $(this).removeClass("selected");
            sendRequest("/upvote", username, slug, songname, albumart, artistname);
            changeValue(this, "increment");
        // Otherwise upvote and highlight.
        } else {
            $(this).addClass("selected");
            sendRequest("/downvote", username, slug, songname, albumart, artistname);
            changeValue(this, "decrement");
        }

        // If the upvote button is highlighted then remove.
        if ($(this).next().hasClass("selected")) {
            $(this).next().removeClass("selected");
        }
        $.notify("Your vote has been sent.", "info");
    }
});