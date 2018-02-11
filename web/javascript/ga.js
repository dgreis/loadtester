/**
 * Created by davidgreis on 2/4/18.
 */

//(function() {
document.addEventListener("DOMContentLoaded", function(event) {


    var bt = document.getElementById("mybutton");

    bt.addEventListener("click", function (event) {

        gtag("event", "click", {
            "event_category": "engagement",
            "event_label": "initial-click"
        });

        // Sends the custom dimension to Google Analytics.
        gtag('event', 'init_conversion_tracking',
            {'init_conversion': 'true'});
        });
});

  //})();
