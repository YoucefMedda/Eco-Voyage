// Animation légère sur le bouton CTA
const cta = document.querySelector('.cta');
if (cta) {
    cta.addEventListener('mouseenter', () => {
        cta.style.boxShadow = '0 4px 16px #388e3c77';
    });
    cta.addEventListener('mouseleave', () => {
        cta.style.boxShadow = '';
    });
}
// Animation d'apparition des cartes (destinations et valeurs) au scroll
function showCardsAndValeursOnScroll() {
    const triggerBottom = window.innerHeight * 0.85;
    document.querySelectorAll('.card, .valeur').forEach(el => {
        const elTop = el.getBoundingClientRect().top;
        if (elTop < triggerBottom) {
            el.classList.add('show');
        }
    });
}
window.addEventListener('scroll', showCardsAndValeursOnScroll);
window.addEventListener('load', showCardsAndValeursOnScroll);
// Animation de la barre de navigation au scroll
const nav = document.querySelector('nav');
function toggleNavScrolled() {
    if (window.scrollY > 30) {
        nav.classList.add('scrolled');
    } else {
        nav.classList.remove('scrolled');
    }
}
window.addEventListener('scroll', toggleNavScrolled);
window.addEventListener('load', toggleNavScrolled);
// Ajuste dynamiquement le padding-top du header selon la hauteur de la nav
function adjustHeaderPadding() {
    const nav = document.querySelector('nav');
    const header = document.querySelector('header');
    if (nav && header) {
        header.style.paddingTop = nav.offsetHeight + 'px';
    }
}
window.addEventListener('resize', adjustHeaderPadding);
window.addEventListener('load', adjustHeaderPadding);
// Ajout de la classe CSS pour l'animation
// Ajoute dans le CSS :
// .card { opacity: 0; transform: translateY(40px); transition: opacity 0.6s, transform 0.6s; }
// .card.show { opacity: 1; transform: translateY(0); }
// Menu burger responsive
const burger = document.querySelector('.burger');
const menuContainer = document.querySelector('.menu-container');
if (burger && menuContainer) {
    burger.addEventListener('click', () => {
        menuContainer.classList.toggle('open');
    });
    // Fermer le menu si on clique en dehors sur mobile
    document.addEventListener('click', (e) => {
        if (!menuContainer.contains(e.target) && !burger.contains(e.target)) {
            menuContainer.classList.remove('open');
        }
    });
}
// Témoignages carousel
window.addEventListener('DOMContentLoaded', function() {
  const cards = document.querySelectorAll('.temoignage-card');
  const leftBtn = document.querySelector('.temoignage-arrow.left');
  const rightBtn = document.querySelector('.temoignage-arrow.right');
  const dots = document.querySelectorAll('.temoignage-dot');
  if (!cards.length || !leftBtn || !rightBtn || !dots.length) return;
  let current = 0;
  let intervalId = null;

  function showCard(idx) {
    cards.forEach((card, i) => {
      card.classList.toggle('active', i === idx);
    });
    dots.forEach((dot, i) => {
      dot.classList.toggle('active', i === idx);
    });
  }

  function nextCard() {
    current = (current + 1) % cards.length;
    showCard(current);
  }

  function prevCard() {
    current = (current - 1 + cards.length) % cards.length;
    showCard(current);
  }

  leftBtn.addEventListener('click', () => {
    prevCard();
    resetInterval();
  });

  rightBtn.addEventListener('click', () => {
    nextCard();
    resetInterval();
  });

  dots.forEach((dot, i) => {
    dot.addEventListener('click', () => {
      current = i;
      showCard(current);
      resetInterval();
    });
  });

  function resetInterval() {
    if (intervalId) clearInterval(intervalId);
    intervalId = setInterval(nextCard, 5000);
  }

  showCard(current);
  resetInterval();
});

// Navigation JS harmonisé

document.addEventListener('DOMContentLoaded', function() {
    // Menu burger mobile
    const hamburger = document.querySelector('.hamburger');
    const navMenu = document.querySelector('.nav-menu');
    if (hamburger && navMenu) {
        hamburger.addEventListener('click', function() {
            navMenu.classList.toggle('active');
            hamburger.classList.toggle('active');
        });
    }

    // Scroll effect sur la navbar (optionnel)
    window.addEventListener('scroll', function() {
        const navbar = document.querySelector('.navbar');
        if (window.scrollY > 100) {
            navbar.style.background = 'rgba(255, 255, 255, 0.95)';
            navbar.style.backdropFilter = 'blur(10px)';
        } else {
            navbar.style.background = '#fff';
            navbar.style.backdropFilter = 'none';
        }
    });

    // (Optionnel) Ajout d'un effet sur les boutons
    const buttons = document.querySelectorAll('button');
    buttons.forEach(button => {
        button.addEventListener('click', function() {
            // Add ripple effect
            const ripple = document.createElement('span');
            ripple.classList.add('ripple');
            this.appendChild(ripple);
            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });

    // Stocker le texte original des boutons (pour loading state éventuel)
    buttons.forEach(button => {
        button.dataset.originalText = button.innerHTML;
    });
}); 