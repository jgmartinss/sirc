from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

app_name = "core"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("realizar-inscricoes/", views.InscricaoView.as_view(), name="inscricoes"),
    path("consultar-inscricoes/", views.ConsultarInscricaoView.as_view(), name="consultar-insc"),
    path("contato/", views.ContatoView.as_view(), name="contato"),
    path("programacao/", views.ProgramacaoView.as_view(), name="programacao"),
    path("organizacao/", views.OrganizadoresView.as_view(), name="organizacao"),
    path("noticias/", views.NoticiasView.as_view(), name="noticias"),
    path("formatos/", views.FormatosView.as_view(), name="formatos"),
    path("datasimportantes/", views.DatasView.as_view(), name="datas"),
    path(
        "palestra/<slug:slug>/", views.PalestraDetail.as_view(), name="palestra-detail"
    ),
    path("p/<slug:slug>/", views.PaginaDetail.as_view(), name="pagina-detail"),
    path("anais/", views.AnaisView.as_view(), name="anais"),
    path(
        "anais/<slug:slug>/", views.AnaisDetail.as_view(), name="anais-detail"
    ),

]

urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
