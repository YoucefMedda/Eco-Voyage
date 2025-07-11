const video = document.getElementById('bgVideo');

video.addEventListener('timeupdate', () => {
  if (video.duration - video.currentTime < 0.25) {
    video.currentTime = 0;
    video.play();
  }
});

// Détermine l'heure actuelle
const now = new Date();
const hour = now.getHours();

let videoSrc = "";
let staticPrefix = window.STATIC_URL || '/static/';

if (hour >= 5 && hour < 11) {
  // Matin
  videoSrc = staticPrefix + "video/morning.mp4";
} else if (hour >= 11 && hour < 17) {
  // Après-midi
  videoSrc = staticPrefix + "video/afternoon.mp4";
} else if (hour >= 17 && hour < 20) {
  // Soir
  videoSrc = staticPrefix + "video/sunset.mp4";
} else {
  // Nuit
  videoSrc = staticPrefix + "video/night.mp4";
}

// Applique la source dynamiquement
video.innerHTML = `<source src="${videoSrc}" type="video/mp4">`;
video.load();
video.play();