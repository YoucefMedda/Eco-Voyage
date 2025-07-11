document.addEventListener('DOMContentLoaded', function() {
    // Affichage du nom du fichier sélectionné
    const fileInput = document.querySelector('input[type="file"]');
    if (fileInput) {
        fileInput.addEventListener('change', function() {
            const label = document.createElement('span');
            label.style.marginLeft = '12px';
            label.style.color = '#219150';
            if (this.files && this.files.length > 0) {
                label.textContent = this.files[0].name;
            } else {
                label.textContent = '';
            }
            if (this.nextSibling) this.parentNode.removeChild(this.nextSibling);
            this.parentNode.appendChild(label);
        });
    }
    // Validation simple
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', function(e) {
            const titre = form.querySelector('input[name="titre"]');
            const desc = form.querySelector('textarea[name="description"]');
            if (titre && titre.value.trim().length < 3) {
                alert('Le titre doit contenir au moins 3 caractères.');
                titre.focus();
                e.preventDefault();
                return false;
            }
            if (desc && desc.value.trim().length < 10) {
                alert('La description doit contenir au moins 10 caractères.');
                desc.focus();
                e.preventDefault();
                return false;
            }
        });
    }
    // Animation bouton
    const btn = document.querySelector('button[type="submit"]');
    if (btn) {
        btn.addEventListener('click', function() {
            btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Publication...';
            setTimeout(() => {
                btn.innerHTML = 'Publier l\'article';
            }, 1200);
        });
    }
}); 