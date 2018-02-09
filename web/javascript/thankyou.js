/**
 * Created by davidgreis on 2/5/18.
 */

document.addEventListener("DOMContentLoaded", function(event) {

    var ty = document.getElementById("thankyou");

    ty.addEventListener("click", function (event) {

        gtag("event", "click", {
            "event_category": "engagement",
            "event_label": "thank-you",
            "value": 1
        });
    });

});
