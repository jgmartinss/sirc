from django.contrib.messages.views import SuccessMessageMixin
from django.core import serializers
from django.db.models import Prefetch, Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import generic


from . import forms, models


class InscricaoView(generic.TemplateView):
    template_name = "inscricoes.html"


class ConsultarInscricaoView(generic.TemplateView):
    template_name = "consultar-inscricao.html"


class IndexView(generic.TemplateView):
    template_name = "index.html"

    def get_patrocinadores(self):
        return models.Patrocinador.objects.filter(ativo=True).values(
            "logo", "logo_hospedado"
        )

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context["patrocinadores"] = self.get_patrocinadores
        return context


class PaginaDetail(generic.DetailView):
    model = models.Paginas
    context_object_name = "pagina"
    template_name = "pagina.html"

    def get_object(self):
        _slug = self.kwargs.get("slug")
        return get_object_or_404(models.Paginas, slug=_slug)


class ContatoView(SuccessMessageMixin, generic.CreateView):
    model = models.Contato
    form_class = forms.ContatoForm
    template_name = "contato.html"
    success_message = "Mensagem enviada com sucesso!"
    success_url = reverse_lazy("core:contato")


class OrganizadoresView(generic.TemplateView):
    template_name = "organizadores.html"

    def get_context_data(self, **kwargs):
        context = super(OrganizadoresView, self).get_context_data(**kwargs)
        context["coordenacao_geral"] = models.Organizadores.objects.coordenador_geral()
        context[
            "comissao_organizadora"
        ] = models.Organizadores.objects.comissao_organizadora()
        context[
            "comissao_avaliadora"
        ] = models.Organizadores.objects.comissao_avaliadora()
        return context


class NoticiasView(generic.ListView):
    model = models.Noticias
    context_object_name = "noticias"
    paginate_by = 6
    template_name = "noticias.html"

    def get_queryset(self, **kargs):
        return models.Noticias.objects.publicado().values(
            "titulo", "descricao", "criado_em"
        )


class DatasView(generic.ListView):
    model = models.Datas
    context_object_name = "datas"
    paginate_by = 6
    template_name = "datas.html"

    def get_queryset(self, **kargs):
        return models.Datas.objects.publicado().values(
            "titulo", "descricao", "criado_em"
        )


class FormatosView(generic.ListView):
    model = models.Formatos
    context_object_name = "formatos"
    paginate_by = 6
    template_name = "formatos.html"

    def get_queryset(self, **kargs):
        return (
            models.Formatos.objects.publicado()
            .prefetch_related(
                Prefetch(
                    "arquivos",
                    queryset=models.FormatosArquivos.objects.only(
                        "tipo", "arquivo", "arquivo_hospedado"
                    ).all(),
                )
            )
            .all()
        )


class ProgramacaoView(generic.TemplateView):
    template_name = "programacao.html"

    def get_context_data(self, **kwargs):
        context = super(ProgramacaoView, self).get_context_data(**kwargs)
        context["palestras_dia_um"] = models.Palestras.objects.palestras_dia_um()
        context["palestras_dia_dois"] = models.Palestras.objects.palestras_dia_dois()
        context["palestras_dia_tres"] = models.Palestras.objects.palestras_dia_tres()
        context["minicursos_dia_um"] = models.Palestras.objects.minicursos_dia_um()
        context["minicursos_dia_dois"] = models.Palestras.objects.minicursos_dia_dois()
        context["minicursos_dia_tres"] = models.Palestras.objects.minicursos_dia_tres()
        return context


class PalestraDetail(generic.DetailView):
    model = models.Palestras
    context_object_name = "palestra"
    template_name = "palestra.html"

    def get_object(self):
        _slug = self.kwargs.get("slug")
        return get_object_or_404(models.Palestras, slug=_slug)

    def get_arquivos(self):
        qs = models.PalestrasArquivos.objects.filter(palestra=self.object)
        return qs.filter(disponivel=True)

    def get_context_data(self, **kwargs):
        context = super(PalestraDetail, self).get_context_data(**kwargs)
        context["arquivos"] = self.get_arquivos
        return context


class AnaisView(generic.ListView):
    model = models.Anais
    context_object_name = "anais"
    template_name = "anais.html"

    def get_queryset(self, **kargs):
        return models.Anais.objects.all().order_by("-edicao")


class AnaisDetail(generic.DetailView):
    model = models.Anais
    context_object_name = "anais"
    template_name = "anaisarquivos.html"

    def get_object(self):
        _slug = self.kwargs.get("slug")
        return get_object_or_404(models.Anais, slug=_slug)

    def get_arquivos(self):
        return models.AnaisArquivos.objects.filter(anais=self.object)

    def get_context_data(self, **kwargs):
        context = super(AnaisDetail, self).get_context_data(**kwargs)
        context["arquivos"] = self.get_arquivos
        return context
