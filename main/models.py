from django.db import models
from django.conf import settings

# Create your models here.

class Pays(models.Model):
    nom = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Pays"
        verbose_name_plural = "Pays"

    def __str__(self):
        return self.nom

class Destination(models.Model):
    nom = models.CharField("Ville", max_length=100)
    site = models.CharField("Emplacement ou URL", max_length=255)
    pays = models.ForeignKey(Pays, on_delete=models.CASCADE, related_name="destinations")
    description = models.TextField()
    prix_par_nuit_moyen = models.DecimalField(max_digits=8, decimal_places=2)
    sejour = models.CharField("Séjour", max_length=100, blank=True, null=True)
    eco_label = models.CharField("Éco-label", max_length=100, blank=True, null=True)
    photo = models.ImageField(upload_to='destination_photos/', null=True, blank=True)

    def __str__(self):
        return f"{self.nom} ({self.pays.nom})"

class Hebergement(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField()
    adresse = models.CharField(max_length=255)
    prix_par_nuit = models.DecimalField(max_digits=8, decimal_places=2)
    destination = models.ForeignKey('Destination', on_delete=models.CASCADE, related_name='hebergements')
    type = models.CharField(max_length=50, choices=[('hotel', 'Hôtel'), ('auberge', 'Auberge'), ('bnb', 'B&B'), ('camping', 'Camping'), ('autre', 'Autre')], default='hotel')
    # Suppression de capacite
    studio = models.PositiveIntegerField(default=0, help_text="Nombre de studios")
    prix_studio = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, help_text="Prix par nuit pour un studio")
    chambre_3p = models.PositiveIntegerField(default=0, help_text="Nombre de chambres 3 personnes")
    prix_3p = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, help_text="Prix par nuit pour une chambre 3 personnes")
    chambre_4p = models.PositiveIntegerField(default=0, help_text="Nombre de chambres 4 personnes")
    prix_4p = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, help_text="Prix par nuit pour une chambre 4 personnes")
    chambre_5p = models.PositiveIntegerField(default=0, help_text="Nombre de chambres 5 personnes")
    prix_5p = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, help_text="Prix par nuit pour une chambre 5 personnes")
    eco_label = models.CharField("Éco-label", max_length=100, blank=True, null=True)
    photo = models.ImageField(upload_to='hebergement_photos/', null=True, blank=True)

    def __str__(self):
        return f"{self.nom}"

class Sejour(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField()
    date_debut = models.DateField()
    date_fin = models.DateField()
    prix = models.DecimalField(max_digits=8, decimal_places=2)
    hebergements = models.ManyToManyField('Hebergement', related_name='sejours')

    def __str__(self):
        return f"{self.nom} ({self.date_debut} - {self.date_fin})"

class Utilisateur(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=128)  # Stocke le hash du mot de passe

    def __str__(self):
        return self.nom

class Reservation(models.Model):
    utilisateur = models.ForeignKey('Utilisateur', on_delete=models.SET_NULL, null=True, blank=True, related_name='reservations')
    hebergement = models.ForeignKey(Hebergement, on_delete=models.CASCADE, related_name='reservations')
    TYPE_CHAMBRE_CHOICES = [
        ('studio', 'Studio'),
        ('chambre_3p', 'Chambre 3 personnes'),
        ('chambre_4p', 'Chambre 4 personnes'),
        ('chambre_5p', 'Chambre 5 personnes'),
    ]
    type_chambre = models.CharField(max_length=20, choices=TYPE_CHAMBRE_CHOICES)
    date_arrivee = models.DateField()
    date_depart = models.DateField()
    date_reservation = models.DateTimeField(auto_now_add=True)
    paye = models.BooleanField(default=False)

    def __str__(self):
        user = self.utilisateur.nom if self.utilisateur else self.nom if hasattr(self, 'nom') else 'Anonyme'
        return f"{user} - {self.hebergement.nom} ({self.type_chambre}) du {self.date_arrivee} au {self.date_depart}"

class Blog(models.Model):
    TYPE_CHOICES = [
        ('conseils', 'Conseils'),
        ('destinations', 'Destinations'),
        ('ecologie', 'Écologie'),
        ('actualites', 'Actualités'),
    ]
    titre = models.CharField(max_length=200)
    description = models.TextField()
    utilisateur = models.ForeignKey('Utilisateur', on_delete=models.SET_NULL, null=True, blank=True, related_name='blogs')
    date_edition = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    photo = models.ImageField(upload_to='blog_photos/', null=True, blank=True)

    def __str__(self):
        return f"{self.titre} ({self.get_type_display()})"

class Commentaire(models.Model):
    utilisateur = models.ForeignKey('Utilisateur', on_delete=models.CASCADE, related_name='commentaires')
    blog = models.ForeignKey('Blog', on_delete=models.CASCADE, related_name='commentaires')
    contenu = models.TextField()
    evaluation = models.PositiveSmallIntegerField(choices=[(i, '★') for i in range(1, 6)], default=5)
    date_ajout = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.utilisateur.nom} sur {self.blog.titre} ({self.evaluation}/5)"
