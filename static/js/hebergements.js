// Animation d'apparition au scroll pour les cartes hébergements
function showHebergCardsOnScroll() {
  const triggerBottom = window.innerHeight * 0.92;
  document.querySelectorAll('.heberg-card').forEach(card => {
    const cardTop = card.getBoundingClientRect().top;
    if (cardTop < triggerBottom) {
      card.style.animationPlayState = 'running';
    }
  });
}
window.addEventListener('scroll', showHebergCardsOnScroll);
window.addEventListener('load', showHebergCardsOnScroll);

// Filtres dynamiques
document.addEventListener('DOMContentLoaded', function() {
  const form = document.getElementById('hebergFiltersForm');
  if (!form) return;
  const cards = document.querySelectorAll('.heberg-card');
  function filterCards() {
    const eco = document.getElementById('hebergEcoLabel').value;
    const type = document.getElementById('hebergType').value;
    const ville = document.getElementById('hebergVille').value;
    cards.forEach(card => {
      const matchEco = !eco || card.dataset.eco === eco;
      const matchType = !type || card.dataset.type === type;
      const matchVille = !ville || card.dataset.ville === ville;
      card.style.display = (matchEco && matchType && matchVille) ? '' : 'none';
    });
  }
  form.addEventListener('change', filterCards);
});

// Diaporama fiche hébergement
document.addEventListener('DOMContentLoaded', function() {
  const slides = document.querySelectorAll('.fiche-galerie-slide');
  if (!slides.length) return;
  let current = 0;
  const prev = document.getElementById('galeriePrev');
  const next = document.getElementById('galerieNext');
  function showSlide(idx) {
    slides.forEach((slide, i) => {
      slide.classList.toggle('active', i === idx);
    });
  }
  prev.addEventListener('click', () => {
    current = (current - 1 + slides.length) % slides.length;
    showSlide(current);
  });
  next.addEventListener('click', () => {
    current = (current + 1) % slides.length;
    showSlide(current);
  });
  showSlide(current);
}); 