$(document).ready(function() {
  var FONT_MODIFIER = 0.9;

  var resizeLogos = function() {
    var fontSize = (FONT_MODIFIER * parseInt($("#profile-links .logo-space").width()))+"px";
    $("#profile-links .my-icon").css('font-size', fontSize);
  };

  const randomArrayElement = function(array) {
    return array[Math.floor(Math.random() * array.length)]
  }

  const displayRandomProfilePicture = function(pictures) {
    $(".profile-picture").css("background-image", "url(images/profile/" + randomArrayElement(pictures) + ")");
  };

  const profilePictures = [
    "full_stack_tobi_cut.jpg",
    "profile_cut.jpg",
    "pivorak_cut.jpg",
    "foxy.jpg",
    "thea2_cut.jpg"
  ];

  displayRandomProfilePicture(profilePictures);
  resizeLogos();

  $(window).resize(resizeLogos);
});
