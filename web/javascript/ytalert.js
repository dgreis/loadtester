  var player;
  function onYouTubeIframeAPIReady() {
    player = new YT.Player('player', {
        events: {
          'onStateChange': onPlayerStateChange
        }
    });
  }

  function onPlayerStateChange(event) {
    //alert("hi");
  }