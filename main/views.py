from django.shortcuts import render
from .models import Destination, Hebergement, Utilisateur, Reservation
from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.contrib import messages
import hashlib
from .forms import BlogForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.

def home(request):
    utilisateur = None
    if request.session.get('user_id'):
        try:
            utilisateur = Utilisateur.objects.get(id=request.session['user_id'])
        except Utilisateur.DoesNotExist:
            pass
    return render(request, 'home.html', {'utilisateur': utilisateur})

def destinations(request):
    utilisateur = None
    if request.session.get('user_id'):
        try:
            utilisateur = Utilisateur.objects.get(id=request.session['user_id'])
        except Utilisateur.DoesNotExist:
            pass
    q = request.GET.get('q', '').strip()
    base_qs = Destination.objects.select_related('pays').annotate(nb_hebergements=models.Count('hebergements'))
    if q:
        base_qs = base_qs.filter(nom__icontains=q)
    destinations = list(base_qs)
    destinations_random = destinations  # même filtrage pour la section à la une
    # Extraction lat/lng pour chaque destination
    for d in destinations:
        if d.site and ',' in d.site:
            try:
                lat, lng = d.site.split(',')
                d.lat = float(lat.strip().replace(',', '.'))
                d.lng = float(lng.strip().replace(',', '.'))
            except Exception:
                d.lat = ''
                d.lng = ''
        else:
            d.lat = ''
            d.lng = ''
    sejours = Destination.objects.exclude(sejour__isnull=True).exclude(sejour__exact='').values_list('sejour', flat=True).distinct()
    eco_labels = Destination.objects.exclude(eco_label__isnull=True).exclude(eco_label__exact='').values_list('eco_label', flat=True).distinct()
    budget_choices = [
        ('petit', 'Petit'),
        ('moyen', 'Moyen'),
        ('eleve', 'Élevé'),
    ]
    return render(request, 'destinations.html', {
        'destinations': destinations,
        'destinations_random': destinations_random,
        'sejours': sejours,
        'eco_labels': eco_labels,
        'budget_choices': budget_choices,
        'q': q,
        'utilisateur': utilisateur
    })

def hebergements(request):
    utilisateur = None
    if request.session.get('user_id'):
        try:
            utilisateur = Utilisateur.objects.get(id=request.session['user_id'])
        except Utilisateur.DoesNotExist:
            pass
    type_ = request.GET.get('type', '').strip()
    eco_label = request.GET.get('eco_label', '').strip()
    destination_nom = request.GET.get('destination', '').strip()
    qs = Hebergement.objects.select_related('destination', 'destination__pays').all()
    if type_:
        qs = qs.filter(type=type_)
    if eco_label:
        qs = qs.filter(eco_label=eco_label)
    if destination_nom:
        qs = qs.filter(destination__nom=destination_nom)
    hebergements = qs
    eco_labels = Hebergement.objects.exclude(eco_label__isnull=True).exclude(eco_label__exact='').values_list('eco_label', flat=True).distinct()
    destinations = Hebergement.objects.values_list('destination__nom', flat=True).distinct()
    return render(request, 'hebergements.html', {
        'hebergements': hebergements,
        'type_selected': type_,
        'eco_label_selected': eco_label,
        'eco_labels': eco_labels,
        'destination_selected': destination_nom,
        'destinations': destinations,
        'utilisateur': utilisateur
    })

def blog(request):
    utilisateur = None
    if request.session.get('user_id'):
        try:
            utilisateur = Utilisateur.objects.get(id=request.session['user_id'])
        except Utilisateur.DoesNotExist:
            utilisateur = None
    from .models import Blog
    blogs_list = Blog.objects.select_related('utilisateur').order_by('-date_edition')
    paginator = Paginator(blogs_list, 4)  # 4 blogs par page
    page = request.GET.get('page')
    try:
        blogs = paginator.page(page)
    except PageNotAnInteger:
        blogs = paginator.page(1)
    except EmptyPage:
        blogs = paginator.page(paginator.num_pages)
    return render(request, 'blog.html', {'utilisateur': utilisateur, 'blogs': blogs})

def about(request):
    utilisateur = None
    if request.session.get('user_id'):
        try:
            utilisateur = Utilisateur.objects.get(id=request.session['user_id'])
        except Utilisateur.DoesNotExist:
            pass
    """Vue pour la page à propos"""
    return render(request, 'about.html', {'utilisateur': utilisateur})

def contact(request):
    """Vue pour la page contact"""
    return render(request, 'contact.html')

def connexion(request):
    if request.method == 'POST':
        nom = request.POST.get('username')
        password = request.POST.get('password')
        if not nom or not password:
            messages.error(request, "Tous les champs sont obligatoires.")
        else:
            hashed = hashlib.sha256(password.encode()).hexdigest()
            try:
                user = Utilisateur.objects.get(nom=nom, password=hashed)
                request.session['user_id'] = user.id
                messages.success(request, f"Bienvenue, {user.nom} !")
                return redirect('home')
            except Utilisateur.DoesNotExist:
                messages.error(request, "Nom ou mot de passe incorrect.")
    return render(request, 'connexion.html')

def inscription(request):
    if request.method == 'POST':
        nom = request.POST.get('username')
        password = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if not nom or not password or not password2:
            messages.error(request, "Tous les champs sont obligatoires.")
        elif password != password2:
            messages.error(request, "Les mots de passe ne correspondent pas.")
        elif Utilisateur.objects.filter(nom=nom).exists():
            messages.error(request, "Ce nom d'utilisateur existe déjà.")
        else:
            hashed = hashlib.sha256(password.encode()).hexdigest()
            Utilisateur.objects.create(nom=nom, password=hashed)
            messages.success(request, "Inscription réussie. Connectez-vous !")
            return redirect('connexion')
    return render(request, 'inscription.html', {'form': None})

def deconnexion(request):
    request.session.flush()
    return redirect('home')

def reservation(request, hebergement_id):
    utilisateur = None
    if request.session.get('user_id'):
        try:
            utilisateur = Utilisateur.objects.get(id=request.session['user_id'])
        except Utilisateur.DoesNotExist:
            utilisateur = None
    if not utilisateur:
        return redirect('connexion')
    hebergement = Hebergement.objects.get(id=hebergement_id)
    from collections import defaultdict
    from datetime import timedelta, datetime
    reservations = hebergement.reservations.all()
    stock = {
        'studio': hebergement.studio,
        'chambre_3p': hebergement.chambre_3p,
        'chambre_4p': hebergement.chambre_4p,
        'chambre_5p': hebergement.chambre_5p,
    }
    prix = {
        'studio': hebergement.prix_studio,
        'chambre_3p': hebergement.prix_3p,
        'chambre_4p': hebergement.prix_4p,
        'chambre_5p': hebergement.prix_5p,
    }
    types_disponibles = [k for k, v in stock.items() if v > 0]
    reserved_dates = {k: set() for k, _ in Reservation.TYPE_CHAMBRE_CHOICES}
    date_counts = {k: defaultdict(int) for k, _ in Reservation.TYPE_CHAMBRE_CHOICES}
    for r in reservations:
        d1, d2 = r.date_arrivee, r.date_depart
        current = d1
        while current < d2:
            date_counts[r.type_chambre][current.strftime('%Y-%m-%d')] += 1
            current += timedelta(days=1)
    for type_chambre, counts in date_counts.items():
        for date_str, count in counts.items():
            if count >= stock.get(type_chambre, 0):
                reserved_dates[type_chambre].add(date_str)
    reserved_dates = {k: sorted(list(v)) for k, v in reserved_dates.items()}
    # Dates où l'utilisateur a déjà une réservation sur un autre hébergement
    user_blocked_dates = set()
    if utilisateur:
        autres_resas = Reservation.objects.filter(utilisateur=utilisateur).exclude(hebergement=hebergement)
        for resa in autres_resas:
            d1, d2 = resa.date_arrivee, resa.date_depart
            current = d1
            while current < d2:
                user_blocked_dates.add(current.strftime('%Y-%m-%d'))
                current += timedelta(days=1)
    if request.method == 'POST':
        type_chambre = request.POST.get('type_chambre')
        date_arrivee = request.POST.get('date_arrivee')
        date_depart = request.POST.get('date_depart')
        if not type_chambre or not date_arrivee or not date_depart:
            messages.error(request, "Tous les champs sont obligatoires.")
        elif date_arrivee >= date_depart:
            messages.error(request, "La date de départ doit être strictement après la date d'arrivée.")
        else:
            chevauchement = Reservation.objects.filter(
                utilisateur=utilisateur,
                date_arrivee__lt=date_depart,
                date_depart__gt=date_arrivee
            ).exclude(hebergement=hebergement).exists()
            if chevauchement:
                messages.error(request, "Vous avez déjà une réservation sur un autre hébergement pour ces dates.")
            else:
                Reservation.objects.create(
                    utilisateur=utilisateur,
                    hebergement=hebergement,
                    type_chambre=type_chambre,
                    date_arrivee=date_arrivee,
                    date_depart=date_depart
                )
                messages.success(request, "Votre réservation a bien été enregistrée !")
                return redirect('hebergements')
    return render(request, 'reservation.html', {
        'hebergement': hebergement,
        'utilisateur': utilisateur,
        'reserved_dates': reserved_dates,
        'types_disponibles': types_disponibles,
        'prix_chambres': prix,
        'user_blocked_dates': sorted(list(user_blocked_dates))
    })

def create_blog(request):
    utilisateur = None
    if request.session.get('user_id'):
        try:
            utilisateur = Utilisateur.objects.get(id=request.session['user_id'])
        except Utilisateur.DoesNotExist:
            utilisateur = None
    if not utilisateur:
        messages.error(request, "Vous devez être connecté pour créer un blog.")
        return redirect('connexion')
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.utilisateur = utilisateur
            blog.save()
            messages.success(request, "Votre article de blog a bien été créé !")
            return redirect('blog')
    else:
        form = BlogForm()
    return render(request, 'create_blog.html', {'form': form, 'utilisateur': utilisateur})

def detail_blog(request, blog_id):
    from .models import Blog, Commentaire
    from .forms import CommentaireForm
    utilisateur = None
    if request.session.get('user_id'):
        try:
            utilisateur = Utilisateur.objects.get(id=request.session['user_id'])
        except Utilisateur.DoesNotExist:
            utilisateur = None
    blog = Blog.objects.select_related('utilisateur').get(id=blog_id)
    commentaires = blog.commentaires.select_related('utilisateur').order_by('-date_ajout')
    if request.method == 'POST':
        if not utilisateur:
            messages.error(request, "Vous devez être connecté pour commenter.")
            return redirect('connexion')
        form = CommentaireForm(request.POST)
        if form.is_valid():
            commentaire = form.save(commit=False)
            commentaire.utilisateur = utilisateur
            commentaire.blog = blog
            commentaire.save()
            messages.success(request, "Votre commentaire a été publié !")
            return redirect('detail_blog', blog_id=blog.id)
    else:
        form = CommentaireForm()
    return render(request, 'detail_blog.html', {
        'blog': blog,
        'commentaires': commentaires,
        'form': form,
        'utilisateur': utilisateur
    })
