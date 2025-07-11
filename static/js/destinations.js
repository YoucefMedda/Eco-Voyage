console.log('JS chargé');
// Animation d'apparition au scroll pour les cartes destinations
function showDestCardsOnScroll() {
  const triggerBottom = window.innerHeight * 0.92;
  document.querySelectorAll('.dest-card').forEach(card => {
    const cardTop = card.getBoundingClientRect().top;
    if (cardTop < triggerBottom) {
      card.style.animationPlayState = 'running';
    }
  });
}
window.addEventListener('scroll', showDestCardsOnScroll);
window.addEventListener('load', showDestCardsOnScroll);

// Modale d'information destination
window.addEventListener('DOMContentLoaded', function() {
  const modal = document.getElementById('destModal');
  const modalClose = document.getElementById('destModalClose');
  const modalImg = document.getElementById('destModalImg');
  const modalTitle = document.getElementById('destModalTitle');
  const modalDesc = document.getElementById('destModalDesc');
  document.querySelectorAll('.dest-btn').forEach(btn => {
    btn.addEventListener('click', function(e) {
      e.preventDefault();
      const card = btn.closest('.dest-card');
      modalImg.src = card.getAttribute('data-img');
      modalTitle.textContent = card.getAttribute('data-title');
      modalDesc.textContent = card.getAttribute('data-desc');
      modal.style.display = 'flex';
    });
  });
  function closeModal() {
    modal.style.display = 'none';
  }
  modalClose.addEventListener('click', closeModal);
  modal.addEventListener('click', function(e) {
    if (e.target === modal) closeModal();
  });

  // Filtres dynamiques
  const form = document.getElementById('filtersForm');
  const cards = document.querySelectorAll('.dest-card');
  function filterCards() {
    const eco = document.getElementById('ecoLabel').value;
    const budget = document.getElementById('budget').value;
    const type = document.getElementById('type').value;
    // Filtrage séjour (checkbox)
    const checkedSejours = Array.from(document.querySelectorAll('input[name="sejour"]:checked')).map(cb => cb.value);
    // Filtrage éco-label (checkbox)
    const checkedEcoLabels = Array.from(document.querySelectorAll('input[name="eco_label"]:checked')).map(cb => cb.value);
    // Filtrage budget (checkbox)
    const checkedBudgets = Array.from(document.querySelectorAll('input[name="budget"]:checked')).map(cb => cb.value);
    cards.forEach(card => {
      const matchEco = checkedEcoLabels.length === 0 || checkedEcoLabels.includes(card.dataset.eco);
      const matchBudget = checkedBudgets.length === 0 || checkedBudgets.includes(card.dataset.budget);
      const matchType = !type || card.dataset.type === type;
      const matchSejour = checkedSejours.length === 0 || checkedSejours.includes(card.dataset.sejour);
      card.style.display = (matchEco && matchBudget && matchType && matchSejour) ? '' : 'none';
    });
    updateMarkers();
  }
  if (form) {
    form.addEventListener('change', filterCards);
  }

  // --- LEAFLET MAP ---
  const mapDiv = document.getElementById('leaflet-map');
  if (!mapDiv) return;
  const map = L.map('leaflet-map').setView([48.5, 2.2], 2.2);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
  }).addTo(map);
  let markers = [];
  function updateMarkers() {
    markers.forEach(m => map.removeLayer(m));
    markers = [];
    // Synchroniser les marqueurs avec les cartes visibles
    const visibleTitles = Array.from(document.querySelectorAll('.dest-card'))
      .filter(card => card.style.display !== 'none')
      .map(card => card.getAttribute('data-title'));
    (window.destinationsData || []).forEach(dest => {
      if (!dest.lat || !dest.lng) return;
      if (!visibleTitles.includes(dest.nom)) return;
      const priceIcon = L.divIcon({
        className: 'custom-price-marker',
        iconSize: [44, 44],
        iconAnchor: [22, 22],
        popupAnchor: [0, -18],
        html: `<div class="price-square">${dest.prix} €</div>`
      });
      const marker = L.marker([dest.lat, dest.lng], {icon: priceIcon}).addTo(map);
      const reserverUrl = `/hebergements/?destination=${encodeURIComponent(dest.nom)}`;
      console.log('URL bouton Réserver:', reserverUrl);
      marker.bindPopup(
        `<strong>${dest.nom} <span style='font-size:0.9em;color:#388e3c;'>(${dest.pays})</span></strong><br>
        <img src="${dest.img}" alt="" style="width:120px;border-radius:8px;margin:6px 0;"><br>
        <span style="font-size:0.95em;">${dest.description}</span><br>
        <span style="color:#247a3c;font-weight:500;">Prix par nuit moyen : ${dest.prix} €</span><br>
        <a href='${reserverUrl}' class='reserver-btn' style='display:inline-block;margin-top:8px;padding:6px 18px;background:#388e3c;color:#fff;border:none;border-radius:5px;cursor:pointer;font-size:1em;text-decoration:none;'>Réserver</a>`
      );
      markers.push(marker);
    });
  }
  updateMarkers();
});

// Diaporama fiche ville
document.addEventListener('DOMContentLoaded', function() {
  const slides = document.querySelectorAll('.fiche-slide');
  if (!slides.length) return;
  let current = 0;
  const prev = document.getElementById('fichePrev');
  const next = document.getElementById('ficheNext');
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

// Réservation modale
window.addEventListener('DOMContentLoaded', function() {
  const resBtns = document.querySelectorAll('.reserver-btn');
  const modal = document.getElementById('reservationModal');
  const closeBtn = document.getElementById('reservationModalClose');
  const hotelNameSpan = document.getElementById('reservationHotelName');
  const form = document.getElementById('reservationForm');
  const successMsg = document.getElementById('reservationSuccess');
  let lastHotel = '';
  resBtns.forEach(btn => {
    btn.addEventListener('click', function(e) {
      e.preventDefault();
      lastHotel = btn.getAttribute('data-hotel');
      hotelNameSpan.textContent = lastHotel;
      modal.style.display = 'flex';
      form.style.display = '';
      successMsg.style.display = 'none';
    });
  });
  closeBtn.addEventListener('click', () => { modal.style.display = 'none'; });
  modal.addEventListener('click', (e) => { if (e.target === modal) modal.style.display = 'none'; });
  form.addEventListener('submit', function(e) {
    e.preventDefault();
    form.style.display = 'none';
    successMsg.style.display = '';
    setTimeout(() => { modal.style.display = 'none'; }, 1800);
  });
}); 