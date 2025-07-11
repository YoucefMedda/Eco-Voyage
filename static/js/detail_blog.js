// detail_blog.js

document.addEventListener('DOMContentLoaded', function () {
    const stars = document.querySelectorAll('.star-rating label');
    stars.forEach(star => {
        star.addEventListener('mouseenter', function () {
            this.classList.add('hovered');
            let prev = this.previousElementSibling;
            while (prev) {
                prev.classList.add('hovered');
                prev = prev.previousElementSibling;
            }
        });
        star.addEventListener('mouseleave', function () {
            stars.forEach(s => s.classList.remove('hovered'));
        });
    });

    // Focus sur le champ commentaire à l'ouverture de la page
    const commentInput = document.querySelector('textarea[name="contenu"]');
    if (commentInput) {
        commentInput.focus();
    }
}); 