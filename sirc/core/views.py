from django.views import generic

from django.db.models import Q

from django.core import serializers
from django.http import HttpResponse

from django.urls import reverse_lazy

from django.shortcuts import get_object_or_404
from django.contrib.messages.views import SuccessMessageMixin

from . import models
from . import forms



class InscricaoView(generic.TemplateView):
    template_name = "inscricoes.html"

class ConsultarInscricaoView(generic.TemplateView):
    template_name = "consultar-inscricao.html"

class IndexView(generic.TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context["patrocinadores"] = models.Patrocinador.objects.filter(ativo=True)
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
        context["coordenacao_geral"] = models.Organizadores.objects.filter(tipo=1)
        context["comissao_organizadora"] = models.Organizadores.objects.filter(tipo=2)
        context["comissao_avaliadora"] = models.Organizadores.objects.filter(tipo=3)
        return context


class NoticiasView(generic.ListView):
    model = models.Noticias
    context_object_name = "noticias"
    paginate_by = 6
    template_name = "noticias.html"

    def get_queryset(self, **kargs):
        return models.Noticias.objects.filter(status=1)


class DatasView(generic.ListView):
    model = models.Datas
    context_object_name = "datas"
    paginate_by = 6
    template_name = "datas.html"

    def get_queryset(self, **kargs):
        return models.Datas.objects.filter(status=1)


class FormatosView(generic.ListView):
    model = models.Formatos
    context_object_name = "formatos"
    paginate_by = 6
    template_name = "formatos.html"

    def get_queryset(self, **kargs):
        formatos_dict = {}
        queryset = []
        formatos = models.Formatos.objects.filter(status=1)

        for f in formatos:
            formatos_dict = {
                "titulo": f.titulo,
                "descricao": f.descricao,
                "arquivos": [
                    a.to_dict_json()
                    for a in models.FormatosArquivos.objects.filter(formatos__id=f.id)
                ],
            }
            queryset.append(formatos_dict)
        return queryset


class ProgramacaoView(generic.TemplateView):
    template_name = "programacao.html"

    def get_palestras(self):
        edicao = models.Sirc.objects.all().order_by("-criado_em")[:1]
        palestras = models.Palestras.objects.filter(Q(edicao=edicao) & Q(tipo=1))
        palestras.values_list('titulo', 'hora', 'tipo')
        return palestras

    def get_minicursos(self):
        edicao = models.Sirc.objects.all().order_by("-criado_em")[:1]
        minicursos = models.Palestras.objects.filter(Q(edicao=edicao) & Q(tipo=2))
        minicursos.values_list('titulo', 'hora', 'tipo')
        return minicursos

    def get_oficinas(self):
        edicao = models.Sirc.objects.all().order_by("-criado_em")[:1]
        oficinas = models.Palestras.objects.filter(Q(edicao=edicao) & Q(tipo=3))
        oficinas.values_list('titulo', 'hora', 'tipo')
        return oficinas

    def get_context_data(self, **kwargs):
        context = super(ProgramacaoView, self).get_context_data(**kwargs)
        context["palestras"] = self.get_palestras
        context["minicursos"] = self.get_minicursos
        context["oficinas"] = self.get_oficinas
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


