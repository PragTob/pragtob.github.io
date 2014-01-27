$(document).ready(function() {
  var FONT_MODIFIER = 0.9;

  var resizeLogos = function() {
    var fontSize = (FONT_MODIFIER * parseInt($("#profile-links .logo-space").width()))+"px";
    $("#profile-links .my-icon").css('font-size', fontSize);
  };

  resizeLogos();

  $(window).resize(resizeLogos);
});