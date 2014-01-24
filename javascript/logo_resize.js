$(document).ready(function() {
  var FONT_MODIFIER = 0.9;
  var fontSize = (FONT_MODIFIER * parseInt($("#social-profiles .logo-space").width()))+"px";
//  console.log(fontSize);
  $("#social-profiles .my-icon").css('font-size', fontSize);
});