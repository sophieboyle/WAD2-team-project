function sendRequest(requestUrl, username, song) {
    $.ajax({
        type: "GET",
        url: requestUrl,
        data: {
            "username": username,
            "songname": song
        },
        dataType: "json"
    })
};

$(document).ready(function() {
    // When a user clicks the upvote button.
    $("#upvote").click(function() {
        let information = $(this).parent().children(":first").children()[1].innerText;
        let songname = information.split("\n")[0];
        let artist = information.split("\n")[1];
        
        sendRequest("/upvote", artist, songname);
    });
});