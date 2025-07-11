from django.core.management.base import BaseCommand
from main.models import Destination, Hebergement, Pays, Utilisateur, Blog
from django.contrib.auth.hashers import make_password
from django.core.files import File

class Command(BaseCommand):
    help = "Réinitialise les tables Destination et Hebergement, puis insère 5 destinations dans 3 pays et 7 hébergements."

    def handle(self, *args, **options):
        Hebergement.objects.all().delete()
        Destination.objects.all().delete()
        # Créer 3 pays
        france, _ = Pays.objects.get_or_create(nom="France")
        italie, _ = Pays.objects.get_or_create(nom="Italie")
        espagne, _ = Pays.objects.get_or_create(nom="Espagne")
        algerie, _ = Pays.objects.get_or_create(nom="Algérie")
        # 5 destinations dans 3 pays
        demo_data = [
            {"nom": "Paris", "site": "48.8566,2.3522", "description": "La Ville Lumière.", "prix": 120, "sejour": "Culture", "eco_label": "Green Key", "pays": france},
            {"nom": "Lyon", "site": "45.7640,4.8357", "description": "Capitale de la gastronomie.", "prix": 100, "sejour": "Gastronomie", "eco_label": "Écolabel Européen", "pays": france},
            {"nom": "Rome", "site": "41.9028,12.4964", "description": "Ville éternelle.", "prix": 130, "sejour": "Patrimoine", "eco_label": "Green Key", "pays": italie},
            {"nom": "Milan", "site": "45.4642,9.1900", "description": "Capitale de la mode.", "prix": 110, "sejour": "Shopping", "eco_label": "Écolabel Européen", "pays": italie},
            {"nom": "Barcelone", "site": "41.3851,2.1734", "description": "Ville de Gaudí.", "prix": 115, "sejour": "Découverte", "eco_label": "Gîtes Panda", "pays": espagne},
        ]
        # Ajouter 3 destinations en Algérie
        demo_data += [
            {"nom": "Alger", "site": "36.7538,3.0588", "description": "La capitale blanche.", "prix": 90, "sejour": "Culture", "eco_label": "Green Key", "pays": algerie},
            {"nom": "Oran", "site": "35.6971,-0.6308", "description": "La radieuse du littoral.", "prix": 80, "sejour": "Plage", "eco_label": "Écolabel Européen", "pays": algerie},
            {"nom": "Constantine", "site": "36.3650,6.6147", "description": "La ville des ponts suspendus.", "prix": 85, "sejour": "Patrimoine", "eco_label": "Gîtes Panda", "pays": algerie},
        ]
        # Créer les destinations (y compris Algérie)
        dest_objs = {}
        for d in demo_data:
            dest = Destination.objects.create(
                nom=d["nom"],
                site=d["site"],
                pays=d["pays"],
                description=d["description"],
                prix_par_nuit_moyen=d["prix"],
                sejour=d["sejour"],
                eco_label=d["eco_label"]
            )
            dest_objs[d["nom"]] = dest
        # 7 hébergements (2 à Paris, 1 à Lyon, 1 à Rome, 1 à Milan, 2 à Barcelone)
        Hebergement.objects.create(
            nom="Hôtel Paris Centre",
            description="Hébergement à Paris",
            adresse="Centre Paris",
            prix_par_nuit=130,
            destination=dest_objs["Paris"],
            type="hotel",
            studio=2, prix_studio=120,
            chambre_3p=1, prix_3p=150,
            chambre_4p=0, prix_4p=None,
            chambre_5p=0, prix_5p=None,
            eco_label="Green Key"
        )
        Hebergement.objects.create(
            nom="Hôtel Paris Montmartre",
            description="Charmant hôtel à Montmartre",
            adresse="Montmartre, Paris",
            prix_par_nuit=140,
            destination=dest_objs["Paris"],
            type="hotel",
            studio=1, prix_studio=130,
            chambre_3p=1, prix_3p=160,
            chambre_4p=1, prix_4p=180,
            chambre_5p=0, prix_5p=None,
            eco_label="Écolabel Européen"
        )
        Hebergement.objects.create(
            nom="Hôtel Lyon Bellecour",
            description="Hébergement à Lyon",
            adresse="Place Bellecour, Lyon",
            prix_par_nuit=110,
            destination=dest_objs["Lyon"],
            type="hotel",
            studio=0, prix_studio=None,
            chambre_3p=2, prix_3p=140,
            chambre_4p=1, prix_4p=170,
            chambre_5p=0, prix_5p=None,
            eco_label="Gîtes Panda"
        )
        Hebergement.objects.create(
            nom="B&B Roma Centro",
            description="Charmant B&B à Rome",
            adresse="Via Nazionale, Rome",
            prix_par_nuit=140,
            destination=dest_objs["Rome"],
            type="bnb",
            studio=1, prix_studio=110,
            chambre_3p=1, prix_3p=150,
            chambre_4p=1, prix_4p=180,
            chambre_5p=1, prix_5p=210,
            eco_label="Green Key"
        )
        Hebergement.objects.create(
            nom="Auberge Milan",
            description="Auberge moderne à Milan",
            adresse="Corso Buenos Aires, Milan",
            prix_par_nuit=120,
            destination=dest_objs["Milan"],
            type="auberge",
            studio=0, prix_studio=None,
            chambre_3p=2, prix_3p=130,
            chambre_4p=2, prix_4p=160,
            chambre_5p=1, prix_5p=200,
            eco_label="Écolabel Européen"
        )
        Hebergement.objects.create(
            nom="Hostel Barcelona",
            description="Hostel convivial à Barcelone",
            adresse="La Rambla, Barcelone",
            prix_par_nuit=125,
            destination=dest_objs["Barcelone"],
            type="auberge",
            studio=0, prix_studio=None,
            chambre_3p=3, prix_3p=120,
            chambre_4p=1, prix_4p=150,
            chambre_5p=1, prix_5p=180,
            eco_label="Gîtes Panda"
        )
        Hebergement.objects.create(
            nom="Hôtel Barcelone Plage",
            description="Hôtel proche de la plage à Barcelone",
            adresse="Plage de Barcelone",
            prix_par_nuit=135,
            destination=dest_objs["Barcelone"],
            type="hotel",
            studio=1, prix_studio=140,
            chambre_3p=1, prix_3p=160,
            chambre_4p=1, prix_4p=190,
            chambre_5p=0, prix_5p=None,
            eco_label="Green Key"
        )
        Hebergement.objects.create(
            nom="Gîte Montmartre Paris",
            description="Gîte écologique à Montmartre",
            adresse="Montmartre, Paris",
            prix_par_nuit=150,
            destination=dest_objs["Paris"],
            type="gite",
            studio=2, prix_studio=120,
            chambre_3p=1, prix_3p=150,
            chambre_4p=1, prix_4p=180,
            chambre_5p=0, prix_5p=None,
            eco_label="Gîtes Panda"
        )
        Hebergement.objects.create(
            nom="Villa Roma Trastevere",
            description="Villa de charme à Rome, quartier Trastevere",
            adresse="Trastevere, Rome",
            prix_par_nuit=180,
            destination=dest_objs["Rome"],
            type="villa",
            studio=0, prix_studio=None,
            chambre_3p=1, prix_3p=170,
            chambre_4p=1, prix_4p=200,
            chambre_5p=1, prix_5p=250,
            eco_label="Green Key"
        )
        Hebergement.objects.create(
            nom="Appartement Sagrada Familia",
            description="Appartement moderne à Barcelone, proche Sagrada Familia",
            adresse="Sagrada Familia, Barcelone",
            prix_par_nuit=160,
            destination=dest_objs["Barcelone"],
            type="appartement",
            studio=1, prix_studio=130,
            chambre_3p=1, prix_3p=150,
            chambre_4p=1, prix_4p=180,
            chambre_5p=0, prix_5p=None,
            eco_label="Écolabel Européen"
        )
        # Hébergements pour l'Algérie
        Hebergement.objects.create(
            nom="Hôtel El Djazair",
            description="Hôtel historique à Alger",
            adresse="Rue Souidani Boudjemaa, Alger",
            prix_par_nuit=95,
            destination=dest_objs["Alger"],
            type="hotel",
            studio=1, prix_studio=90,
            chambre_3p=1, prix_3p=110,
            chambre_4p=0, prix_4p=None,
            chambre_5p=0, prix_5p=None,
            eco_label="Green Key"
        )
        Hebergement.objects.create(
            nom="Auberge Oran Plage",
            description="Auberge conviviale à Oran, proche de la mer",
            adresse="Front de mer, Oran",
            prix_par_nuit=85,
            destination=dest_objs["Oran"],
            type="auberge",
            studio=1, prix_studio=80,
            chambre_3p=1, prix_3p=100,
            chambre_4p=0, prix_4p=None,
            chambre_5p=0, prix_5p=None,
            eco_label="Écolabel Européen"
        )
        Hebergement.objects.create(
            nom="Maison Constantine Ponts",
            description="Maison d'hôtes au cœur des ponts de Constantine",
            adresse="Centre-ville, Constantine",
            prix_par_nuit=90,
            destination=dest_objs["Constantine"],
            type="bnb",
            studio=1, prix_studio=85,
            chambre_3p=1, prix_3p=105,
            chambre_4p=0, prix_4p=None,
            chambre_5p=0, prix_5p=None,
            eco_label="Gîtes Panda"
        )
        # Ajout d'utilisateurs de démonstration
        Utilisateur.objects.all().delete()
        utilisateurs_demo = [
            {"nom": "Alice Dupont", "password": make_password("alice123")},
            {"nom": "Mohamed Benali", "password": make_password("mohamed123")},
            {"nom": "Sophie Martin", "password": make_password("sophie123")},
            {"nom": "Karim Bensalem", "password": make_password("karim123")},
            {"nom": "Fatima Zohra", "password": make_password("fatima123")},
        ]
        for u in utilisateurs_demo:
            Utilisateur.objects.create(nom=u["nom"], password=u["password"])

        # Ajout de blogs de démonstration
        Blog.objects.all().delete()
        utilisateurs = list(Utilisateur.objects.all())
        blogs_demo = [
            {
                "titre": "Voyager éco-responsable : nos conseils",
                "description": "Découvrez comment voyager tout en respectant la planète grâce à nos astuces simples et efficaces.",
                "utilisateur": utilisateurs[0] if len(utilisateurs) > 0 else None,
                "type": "conseils",
                "photo": "blog1.jpg",
            },
            {
                "titre": "Top 5 des destinations vertes en Europe",
                "description": "Explorez les destinations les plus engagées pour l'écologie en Europe et préparez votre prochain séjour durable !",
                "utilisateur": utilisateurs[1] if len(utilisateurs) > 1 else None,
                "type": "destinations",
                "photo": "blog2.jpg",
            },
            {
                "titre": "L'écotourisme en Méditerranée",
                "description": "La Méditerranée regorge d'initiatives écotouristiques. Voici nos coups de cœur pour un voyage responsable.",
                "utilisateur": utilisateurs[2] if len(utilisateurs) > 2 else None,
                "type": "ecologie",
                "photo": "blog3.jpg",
            },
            {
                "titre": "Actualités : Les nouvelles normes écologiques pour les hébergements",
                "description": "Les hébergements touristiques doivent désormais répondre à de nouvelles exigences environnementales. On fait le point.",
                "utilisateur": utilisateurs[3] if len(utilisateurs) > 3 else None,
                "type": "actualites",
                "photo": "blog4.jpg",
            },
            {
                "titre": "Voyager sans avion : alternatives écologiques",
                "description": "Découvrez comment voyager autrement et réduire votre empreinte carbone.",
                "utilisateur": utilisateurs[0] if len(utilisateurs) > 0 else None,
                "type": "ecologie",
                "photo": "blog5.jpg",
            },
            {
                "titre": "Séjours insolites : dormir dans la nature",
                "description": "Top des hébergements insolites et éco-responsables pour une immersion totale dans la nature.",
                "utilisateur": utilisateurs[1] if len(utilisateurs) > 1 else None,
                "type": "destinations",
                "photo": "blog6.jpg",
            },
            {
                "titre": "Réduire ses déchets en voyage",
                "description": "Astuces pratiques pour voyager léger et sans plastique, même à l'autre bout du monde.",
                "utilisateur": utilisateurs[2] if len(utilisateurs) > 2 else None,
                "type": "conseils",
                "photo": "blog7.jpg",
            },
            {
                "titre": "Voyager local : redécouvrir sa région",
                "description": "Partez à l’aventure près de chez vous et soutenez l’économie locale tout en réduisant votre empreinte carbone.",
                "utilisateur": utilisateurs[0] if len(utilisateurs) > 0 else None,
                "type": "conseils",
                "photo": "blog8.jpg",
            },
            {
                "titre": "Les plus beaux parcs nationaux d’Europe",
                "description": "Explorez la nature préservée des parcs nationaux européens pour un séjour inoubliable et respectueux de l’environnement.",
                "utilisateur": utilisateurs[1] if len(utilisateurs) > 1 else None,
                "type": "destinations",
                "photo": "blog9.jpg",
            },
            {
                "titre": "Écotourisme en famille : astuces et idées",
                "description": "Voyager éco-responsable avec des enfants, c’est possible ! Découvrez nos conseils pour des vacances vertes en famille.",
                "utilisateur": utilisateurs[2] if len(utilisateurs) > 2 else None,
                "type": "ecologie",
                "photo": "blog10.jpg",
            },
            {
                "titre": "Actualités : Les labels écologiques à connaître",
                "description": "Quels sont les labels fiables pour choisir un hébergement vraiment éco-responsable ? On fait le point sur les certifications.",
                "utilisateur": utilisateurs[3] if len(utilisateurs) > 3 else None,
                "type": "actualites",
                "photo": "blog11.jpg",
            },
            {
                "titre": "Voyager sans plastique : mission zéro déchet",
                "description": "Adoptez les bons réflexes pour voyager sans plastique et réduire vos déchets à chaque étape du séjour.",
                "utilisateur": utilisateurs[4] if len(utilisateurs) > 4 else None,
                "type": "conseils",
                "photo": "blog12.jpg",
            },
        ]
        for b in blogs_demo:
            photo_file = None
            try:
                with open(f"media/blog_photos/{b['photo']}", "rb") as img:
                    print(f"Image trouvée : {b['photo']}")
                    photo_file = File(img)
                    Blog.objects.create(
                        titre=b["titre"],
                        description=b["description"],
                        utilisateur=b["utilisateur"],
                        type=b["type"],
                        photo=photo_file
                    )
            except FileNotFoundError:
                print(f"Image NON trouvée : {b['photo']}")
                Blog.objects.create(
                    titre=b["titre"],
                    description=b["description"],
                    utilisateur=b["utilisateur"],
                    type=b["type"]
                )
        self.stdout.write(self.style.SUCCESS("Tables Destination et Hebergement réinitialisées avec 5 destinations (France, Italie, Espagne) et 7 hébergements."))
        self.stdout.write(self.style.SUCCESS("Blogs de démonstration insérés.")) 