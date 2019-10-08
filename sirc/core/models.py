# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from django.urls import reverse

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from django.template.defaultfilters import truncatechars

from django.utils.safestring import mark_safe

from django.template.defaultfilters import truncatechars

from tinymce import HTMLField

from . import managers


class TimeStampedModel(models.Model):
    criado_em = models.DateTimeField("Criando em", auto_now_add=True)
    modificado_em = models.DateTimeField("Modificado em", auto_now=True)

    class Meta:
        abstract = True


class Usuario(AbstractBaseUser, PermissionsMixin, TimeStampedModel):
    email = models.EmailField("Email", max_length=255, unique=True)
    first_name = models.CharField("Nome", max_length=255)
    last_name = models.CharField("Sobrenome", max_length=255)
    is_active = models.BooleanField("Ativo?", default=True)
    is_staff = models.BooleanField("Staff?", default=False)
    is_admin = models.BooleanField("Admin?", default=False)

    objects = managers.UsuarioManager()

    USERNAME_FIELD = "email"

    class Meta:
        app_label = "core"
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"
        db_table = "tb_usuarios"

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.is_admin

    def __str__(self):
        return self.email


class Contato(TimeStampedModel):
    nome = models.CharField("Nome", max_length=254)
    email = models.EmailField("Email", max_length=255)
    assunto = models.CharField("Assunto", max_length=254)
    menssagem = models.TextField("Menssagem")

    class Meta:
        verbose_name = "Contato"
        verbose_name_plural = "Contatos"
        db_table = "tb_contato"

    def __str__(self):
        return f"{self.email} - {self.assunto}"


class Noticias(TimeStampedModel):
    STATUS = ((1, "Publicado"), (2, "Não Publicado"))

    titulo = models.CharField("Título", max_length=255)
    descricao = HTMLField("Descrição")
    status = models.PositiveIntegerField("Situação", choices=STATUS, default=2)

    class Meta:
        verbose_name = "Notícia"
        verbose_name_plural = "Notícias"
        ordering = ["-criado_em"]
        db_table = "tb_noticias"

    def __str__(self):
        return f"{self.titulo}"


class Patrocinador(TimeStampedModel):
    nome = models.CharField("Nome", max_length=255)
    site = models.URLField("Site", unique=True)
    ativo = models.BooleanField("Ativo?")
    logo = models.ImageField(
        "Logo",
        upload_to="patrocinadores/logo",
        help_text="A imagem deve ter as seguintes dimensões 90px x 90px",
    )
    logo_hospedado = models.URLField("Link Logo", unique=True, blank=True, null=True)

    class Meta:
        verbose_name = "Patrocinador"
        verbose_name_plural = "Patrocinadores"
        ordering = ["nome"]
        db_table = "tb_patrocinadores"

    def __str__(self):
        return f"{self.nome}"


class Organizadores(TimeStampedModel):
    TIPO = (
        (1, "Coordenação Geral"),
        (2, "Comissao Organizadora"),
        (3, "Comissao Avaliadora"),
    )
    nome = models.CharField("Nome", max_length=255)
    tipo = models.PositiveIntegerField("Tipo", choices=TIPO)
    ativo = models.BooleanField("Ativo?", default=True)

    class Meta:
        verbose_name = "Organizador"
        verbose_name_plural = "Organizadores"
        ordering = ["nome"]
        db_table = "tb_organizadores"

    def __str__(self):
        return f"{self.nome}"


class Formatos(TimeStampedModel):
    STATUS = ((1, "Publicado"), (2, "Não Publicado"))

    titulo = models.CharField("Título", max_length=255)
    descricao = models.TextField("Descrição")
    status = models.PositiveIntegerField("Situação", choices=STATUS, default=2)

    class Meta:
        verbose_name = "Formato"
        verbose_name_plural = "Formatos"
        ordering = ["-criado_em"]
        db_table = "tb_formatos_submissao"

    @property
    def _descricao(self):
        return truncatechars(self.descricao, 50)

    def __str__(self):
        return f"{self.titulo}"


class FormatosArquivos(TimeStampedModel):
    TIPO = (
        (1, "Latex"),
        (2, "Microsoft Word"),
        (3, "Open Document"),
        (4, "PDF"),
        (5, "Power Point"),
    )

    nome = models.CharField("Nome", max_length=254)
    tipo = models.PositiveIntegerField("Tipo", choices=TIPO)
    arquivo = models.FileField(
        "Arquivo", 
        upload_to="formatos_de_submissao/arquivos/", 
        max_length=150, 
        blank=True
    )
    arquivo_hospedado = models.URLField("Link Arquivo", unique=True, blank=True, null=True)
    formatos = models.ForeignKey(
        Formatos,
        verbose_name="Formatos de Submissão",
        related_name="formatos_arquivos",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "Arquivo"
        verbose_name_plural = "Arquivos"
        db_table = "tb_formatos_submissao_arquivos"

    def to_dict_json(self):
        return {"nome": self.nome, "tipo": self.tipo, "arquivo": self.arquivo, "arquivo_hospedado": self.arquivo_hospedado}

    def __str__(self):
        return f"{self.formatos.titulo} - ({self.tipo})"


class Datas(TimeStampedModel):
    STATUS = ((1, "Publicado"), (2, "Não Publicado"))

    titulo = models.CharField("Título", max_length=255)
    descricao = models.TextField("Descrição")
    status = models.PositiveIntegerField("Situação", choices=STATUS, default=2)

    class Meta:
        verbose_name = "Data"
        verbose_name_plural = "Datas"
        ordering = ["-criado_em"]
        db_table = "tb_datas_importantes"

    def __str__(self):
        return f"{self.titulo}"


class Paginas(TimeStampedModel):
    STATUS = ((1, "Publicado"), (2, "Não Publicado"))

    titulo = models.CharField("Título", max_length=255)
    slug = models.SlugField(
        "URL Página",
        unique=True,
        blank=True,
        help_text="http://www.sirc.ufn.edu.br/{TITULO}",
    )
    descricao = HTMLField("Descrição")
    status = models.PositiveIntegerField("Situação", choices=STATUS, default=2)

    class Meta:
        verbose_name = "Pagina"
        verbose_name_plural = "Paginas"
        db_table = "tb_paginas"

    def get_absolute_url(self):
        return reverse("core:pagina-detail", kwargs={"slug": self.slug})

    def __str__(self):
        return f"{self.titulo}"


class Palestrantes(TimeStampedModel):
    nome = models.CharField("Nome", max_length=254)
    email = models.EmailField("Email", max_length=254)
    avatar = models.ImageField(
        "Avatar",
        upload_to="palestrantes/avatar",
        blank=True,
        help_text="A imagem deve ter as seguintes dimensões 90px x 90px",
    )
    avatar_hospedado = models.URLField("Avatar Link", unique=True, blank=True, null=True)
    instituicao = models.CharField("Instituição de Ensino", max_length=254, blank=True)

    class Meta:
        verbose_name = "Palestrante"
        verbose_name_plural = "Palestrantes"
        db_table = "tb_palestrantes"

    @property
    def get_short_email(self):
        return f"{self.email[:-4]}"

    @property
    def get_rede_social(self):
        return MidiasSociais.objects.filter(palestrante=self)

    def __str__(self):
        return f"{self.nome}"


class MidiasSociais(TimeStampedModel):
    TIPO = (
        ("fab fa-fw fa-1x fa-facebook", "Facebook"),
        ("fab fa-fw fa-1x fa-twitter-square", "Twitter"),
        ("fab fa-fw fa-1x fa-linkedin", "Linkedin"),
        ("fas fa-fw fa-1x fa-link", "Lattes"),
        ("fab fa-fw fa-1x fa-github-square", "Github/Gitlab"),
        ("fab fa-fw fa-1x fa-blogger", "Blog/Site"),
    )
    palestrante = models.ForeignKey(
        Palestrantes, verbose_name="Palestrante", on_delete=models.CASCADE
    )
    tipo = models.CharField("Tipo", max_length=150, choices=TIPO)
    link = models.URLField("Link", unique=True)

    class Meta:
        verbose_name = "Midia Social"
        verbose_name_plural = "Midias Sociais"
        db_table = "tb_midias_sociais"

    @property
    def get_link(self):
        return mark_safe(f'<a href="{self.link}"><i class="{self.tipo}"></i></a>')

    def __str__(self):
        return f"{self.link}"


class Local(TimeStampedModel):
    nome = models.CharField("Nome", max_length=254)

    class Meta:
        verbose_name = "Local"
        verbose_name_plural = "Locais"
        db_table = "tb_local"

    def __str__(self):
        return f"{self.nome}"


class Sirc(TimeStampedModel):
    edicao = models.IntegerField("N° da Edição")

    class Meta:
        verbose_name = "Sirc"
        verbose_name_plural = "Sircs"
        db_table = "tb_sirc"

    def __str__(self):
        return f"{self.edicao}° Edição"


class Palestras(TimeStampedModel):
    PUBLICO_ALVO = (
        (1, "Ciência da Computação"),
        (2, "Sistemas de Informação"),
        (3, "Jogos Digitas"),
    )
    DIA = ((1, "Dia 1"), (2, "Dia 2"), (3, "Dia 3"))
    TIPO = ((1, "Palestra"), (2, "Minicurso"), (3, "Oficina"))
    STATUS = ((1, "Confirmada"), (2, "Cancelada"))

    titulo = models.CharField("Título", max_length=254)
    slug = models.SlugField("Slug", blank=True)
    resumo = models.TextField("Resumo")
    publico_alvo = models.PositiveIntegerField("Público Alvo", choices=PUBLICO_ALVO)
    tipo = models.PositiveIntegerField("Tipo", choices=TIPO)
    dia = models.PositiveIntegerField("Dia", choices=DIA)
    status = models.PositiveIntegerField("Status", choices=STATUS)
    hora = models.TimeField("Hora")
    data = models.DateField("Data")
    palestrantes = models.ManyToManyField(Palestrantes, verbose_name="Palestrante(s)")
    edicao = models.ForeignKey(
        Sirc, verbose_name="SIRC Edição", on_delete=models.CASCADE
    )
    local = models.ForeignKey(Local, verbose_name="Local", on_delete=models.CASCADE)

    class Meta:
        ordering = ('hora',)
        verbose_name = "Palestras"
        verbose_name_plural = "Palestras"
        db_table = "tb_palestras"

    @property
    def _resumo(self):
        return truncatechars(self.resumo, 40)

    @property
    def titulo_(self):
        return truncatechars(self.titulo, 40)

    def get_absolute_url(self):
        return reverse("core:palestra-detail", kwargs={"slug": self.slug})

    def __str__(self):
        return f"{self.titulo}"


class PalestrasArquivos(TimeStampedModel):
    nome = models.CharField("Nome", max_length=254)
    disponivel = models.BooleanField(
        "Disponivel?", help_text="Se os arquivos já estão disponiveis ao público."
    )
    arquivo = models.FileField(
        "Arquivo", upload_to="palestras/arquivos/", max_length=150
    )
    palestra = models.ForeignKey(
        Palestras, verbose_name="Palestra", on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "Arquivo"
        verbose_name_plural = "Arquivos"
        db_table = "tb_palestra_arquivos"

    def __str__(self):
        return f"{self.nome} - {self.palestra.titulo}"


class Anais(TimeStampedModel):
    edicao = models.IntegerField("Edição/Ano")
    slug = models.SlugField("Slug", blank=True)
    thumbnail = models.ImageField(
        "Thumbnail",
        upload_to="anais/thumbnail",
        blank=True,
        null=True,
        help_text="A imagem deve ter as seguintes dimensões 90px x 90px",
    )
    thumbnail_hospedado = models.URLField("Link Thumb", unique=True, blank=True, null=True)

    class Meta:
        verbose_name = "Anais"
        verbose_name_plural = "Anais"
        db_table = "tb_anais"

    def __str__(self):
        return f"SIRC - {self.edicao}"


class AnaisArquivos(TimeStampedModel):
    nome = models.CharField(
        "Nome", 
        max_length=254, 
        help_text="Nome do artigo que será exibido para dowload."
    )
    arquivo = models.FileField(
        "Arquivo", upload_to="anais/arquivos/", max_length=150, blank=True, null=True
    )
    arquivo_hospedado = models.URLField("Link Arquivo", unique=True, blank=True, null=True)
    anais = models.ForeignKey(
        Anais, verbose_name="Anais", on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "Anais Arquivos"
        verbose_name_plural = "Anais Arquivos"
        db_table = "tb_anais_arquivos"

    def __str__(self):
        return f"SIRC - {self.anais.edicao} - {self.nome}"
