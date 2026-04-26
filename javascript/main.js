$(document).ready(function () {
  var FONT_MODIFIER = 0.9;

  var resizeLogos = function () {
    var fontSize =
      FONT_MODIFIER * parseInt($("#profile-links .logo-space").width()) + "px";
    $("#profile-links .my-icon").css("font-size", fontSize);
  };

  const randomArrayElement = function (array) {
    return array[Math.floor(Math.random() * array.length)];
  };

  const profilePictureElement = $(".profile-picture");
  const buildProfileImageUrl = function (pictureName) {
    return "url(images/profile/" + pictureName + ")";
  };

  const preloadProfilePictures = function (pictures) {
    return Promise.all(
      pictures.map(function (pictureName) {
        return new Promise(function (resolve) {
          const img = new Image();
          img.onload = resolve;
          img.onerror = resolve;
          img.src = "images/profile/" + pictureName;
        });
      })
    );
  };

  const displayRandomProfilePicture = function (pictures, options = {}) {
    const animate = options.animate !== false;
    const nextImageUrl = buildProfileImageUrl(randomArrayElement(pictures));

    if (!animate) {
      profilePictureElement.css("background-image", nextImageUrl);
      return;
    }

    profilePictureElement.addClass("is-fading");
    setTimeout(function () {
      profilePictureElement.css("background-image", nextImageUrl);
      profilePictureElement.removeClass("is-fading");
    }, 125);
  };

  const profilePictures = [
    "full_stack_tobi_cut.jpg",
    "pivorak_cut.jpg",
    "foxy.jpg",
    "thea2_cut.jpg",
  ];

  const minute = 60000;
  preloadProfilePictures(profilePictures).then(function () {
    displayRandomProfilePicture(profilePictures, { animate: false });
  });
  resizeLogos();

  $(window).resize(resizeLogos);
  setInterval(function () {
    displayRandomProfilePicture(profilePictures, { animate: true });
  }, minute);
});
