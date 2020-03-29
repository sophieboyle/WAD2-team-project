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
    let tElement = $(parent).find(".song-text")[0];
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
    let parent = $(this).parent()[0];
    let parentInnerText = parent.innerText;
    
    // Getting the slug.
    let slug = $(this).attr("title");

    // Getting the username.
    let username = "";

    // Song name.
    rx = /Song: (.[^\\]*)/g;
    let songname = rx.exec(parentInnerText);
    console.log(songname);
    

    // If the user pressed the upvote button.
    if ($(this).attr("id") == "upvote") {
        // If it has been already selected then downvote.
        if ($(this).hasClass("selected")) {
            $(this).removeClass("selected");
            sendRequest("/downvote", songname);
            changeValue(this, "decrement");
        // Otherwise upvote and highlight.
        } else {
            $(this).addClass("selected");
            sendRequest("/upvote", songname);
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
            sendRequest("/upvote", songname);
            changeValue(this, "increment");
        // Otherwise upvote and highlight.
        } else {
            $(this).addClass("selected");
            sendRequest("/downvote", songname);
            changeValue(this, "decrement");
        }

        // If the upvote button is highlighted then remove.
        if ($(this).next().hasClass("selected")) {
            $(this).next().removeClass("selected");
        }
        $.notify("Your vote has been sent.", "info");
    }
});