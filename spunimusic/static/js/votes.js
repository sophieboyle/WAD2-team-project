function sendRequest(requestUrl, song) {
    $.ajax({
        type: "GET",
        url: requestUrl,
        data: {
            "songname": song
        },
        dataType: "json"
    })
};

// When a user clicks the upvote button.
$(document).on("click", "#upvote", function() {
    let songname = $(this).attr("title");
    let information = $(this).parent().children(":first").children()[1].innerText;
    let songname = information.split("\n")[0];
    
    
    sendRequest("/upvote", songname);
    console.log(songname);
    $.notify("Your vote has been sent.", "info");
});

// When a user clicks the downvote button.
$(document).on("click", "#downvote", function() {
    let information = $(this).parent().children(":first").children()[1].innerText;
    let songname = information.split("\n")[0];
    
    sendRequest("/downvote", songname);
    $.notify("Your vote has been sent.", "info");
});