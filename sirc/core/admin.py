from django.contrib import admin

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from . import models


class UsuarioAdmin(BaseUserAdmin):
    model = models.Usuario
    ordering = ("email", "-criado_em")
    search_fields = ("email",)
    list_display = (
        "email",
        "first_name",
        "last_name",
        "is_active",
        "is_admin",
        "is_superuser",
        "criado_em",
    )
    list_display_links = ["email"]
    list_filter = ("is_superuser", "is_admin", "is_active", "criado_em")
    fieldsets = (
        ("Informações de conta", {"fields": (("email", "is_active"), "password")}),
        ("Informações pessoais", {"fields": (("first_name", "last_name"))}),
        ("Permissões", {"fields": (("is_superuser", "is_admin"),)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "password1",
                    "password2",
                ),
            },
        ),
    )


class ContatoAdmin(admin.ModelAdmin):
    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    model = models.Contato
    list_display = ("nome", "email", "assunto")
    search_fields = ("nome", "email")
    date_hierarchy = "criado_em"
    readonly_fields = ("criado_em",)
    ordering = ("-criado_em",)

    fieldsets = (
        (None, {"fields": ("nome", "email", "assunto", "menssagem", "criado_em")}),
    )


class NoticiasAdmin(admin.ModelAdmin):
    model = models.Noticias
    list_display = ("titulo", "criado_em", "status")
    list_filter = ("status",)
    list_editable = ("status",)
    search_fields = ("titulo",)
    date_hierarchy = "criado_em"
    readonly_fields = ("criado_em", "modificado_em")
    ordering = ("-criado_em", "titulo")

    fieldsets = (
        (
            None,
            {
                "fields": (
                    ("titulo", "status"),
                    "descricao",
                    ("criado_em", "modificado_em"),
                )
            },
        ),
    )


class PatrocinadorAdmin(admin.ModelAdmin):
    model = models.Patrocinador
    list_display = ("nome", "ativo")
    list_filter = ("ativo",)
    search_fields = ("nome",)
    date_hierarchy = "criado_em"
    readonly_fields = ("criado_em", "modificado_em")
    ordering = ("nome", "ativo")
    list_per_page = 10

    fieldsets = (
        (
            None,
            {
                "fields": (
                    ("nome", "ativo"),
                    "site",
                    "logo",
                    "logo_hospedado",
                    ("criado_em", "modificado_em"),
                )
            },
        ),
    )


class OrganizadoresAdmin(admin.ModelAdmin):
    model = models.Organizadores
    list_display = ("nome", "tipo", "ativo")
    list_filter = ("tipo", "ativo")
    search_fields = ("nome",)
    date_hierarchy = "criado_em"
    readonly_fields = ("criado_em", "modificado_em")
    ordering = ("tipo", "nome")
    list_per_page = 10

    fieldsets = (
        (None, {"fields": (("nome", "ativo"), "tipo", ("criado_em", "modificado_em"))}),
    )


class FormatosArquivosInline(admin.TabularInline):
    model = models.FormatosArquivos
    extra = 1


class FormatosAdmin(admin.ModelAdmin):
    model = models.Formatos
    inlines = [FormatosArquivosInline]
    list_display = ("titulo", "_descricao", "status")
    list_filter = ("status",)
    list_editable = ("status",)
    search_fields = ("titulo", "descricao")
    date_hierarchy = "criado_em"
    readonly_fields = ("criado_em", "modificado_em")
    ordering = ("titulo",)
    list_per_page = 10

    fieldsets = (
        (
            None,
            {
                "fields": (
                    ("titulo", "status"),
                    "descricao",
                    ("criado_em", "modificado_em"),
                )
            },
        ),
    )


class DatasAdmin(admin.ModelAdmin):
    model = models.Datas
    list_display = ("titulo", "status", "criado_em", "modificado_em")
    list_filter = ("status",)
    list_editable = ("status",)
    search_fields = ("titulo",)
    date_hierarchy = "criado_em"
    readonly_fields = ("criado_em", "modificado_em")
    ordering = ("titulo",)
    list_per_page = 10

    fieldsets = (
        (
            None,
            {
                "fields": (
                    ("titulo", "status"),
                    "descricao",
                    ("criado_em", "modificado_em"),
                )
            },
        ),
    )


class PaginasAdmin(admin.ModelAdmin):
    model = models.Paginas
    list_display = ("titulo", "status", "criado_em", "modificado_em")
    list_filter = ("status",)
    list_editable = ("status",)
    search_fields = ("titulo",)
    date_hierarchy = "criado_em"
    readonly_fields = ("criado_em", "modificado_em")
    ordering = ("titulo",)
    prepopulated_fields = {"slug": ("titulo",)}
    list_per_page = 10

    fieldsets = (
        (
            None,
            {
                "fields": (
                    ("titulo", "status"),
                    "slug",
                    "descricao",
                    ("criado_em", "modificado_em"),
                )
            },
        ),
    )


class MidiasSociaisInline(admin.TabularInline):
    model = models.MidiasSociais
    extra = 1
    fieldsets = ((None, {"fields": ("tipo", "link")}),)


class PalestrantesAdmin(admin.ModelAdmin):
    model = models.Palestrantes
    inlines = [MidiasSociaisInline]
    list_display = ("nome", "email")
    readonly_fields = ("criado_em", "modificado_em")
    search_fields = ("nome", "email")
    date_hierarchy = "criado_em"
    ordering = ("nome",)
    list_per_page = 15
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "nome",
                    "email",
                    "instituicao",
                    ("avatar", "avatar_hospedado"),
                    ("criado_em", "modificado_em"),
                )
            },
        ),
    )


class PalestrasArquivosInline(admin.TabularInline):
    model = models.PalestrasArquivos
    extra = 1


class PalestrasAdmin(admin.ModelAdmin):
    model = models.Palestras
    inlines = [PalestrasArquivosInline]
    prepopulated_fields = {"slug": ("titulo",)}
    list_display = ("titulo", "_resumo", "get_palestrantes", "local", "data")
    list_filter = ("status", "publico_alvo", "tipo", "dia", "local", "palestrantes")
    filter_horizontal = ["palestrantes"]
    readonly_fields = ("criado_em", "modificado_em")
    search_fields = ("titulo", "palestrantes")
    date_hierarchy = "criado_em"
    save_on_top = True
    list_per_page = 10
    fieldsets = (
        (
            None,
            {
                "fields": (
                    ("titulo", "edicao"),
                    ("slug", "status"),
                    "resumo",
                    "palestrantes",
                    ("tipo", "publico_alvo"),
                    ("dia", "hora", "data"),
                    "local",
                    ("criado_em", "modificado_em"),
                )
            },
        ),
    )

    def get_palestrantes(self, obj):
        return ",\n".join([p.nome for p in obj.palestrantes.all()])

    get_palestrantes.short_description = "Palestrante(s)"


class SircAdmin(admin.ModelAdmin):
    model = models.Sirc
    list_display = ("edicao",)
    date_hierarchy = "criado_em"


class AnaisArquivosInline(admin.TabularInline):
    model = models.AnaisArquivos
    extra = 1


class AnaisAdmin(admin.ModelAdmin):
    model = models.Anais
    inlines = [AnaisArquivosInline]
    prepopulated_fields = {"slug": ("edicao",)}
    list_display = ("__str__",)
    list_filter = ("edicao",)
    readonly_fields = ("criado_em", "modificado_em")
    date_hierarchy = "criado_em"
    list_per_page = 10

    fieldsets = (
        (
            None,
            {
                "fields": (
                    ("edicao", "slug",),
                    "thumbnail", 
                    "thumbnail_hospedado",
                    ("criado_em", "modificado_em"),
                )
            },
        ),
    )


admin.site.register(models.Usuario, UsuarioAdmin)
admin.site.register(models.Noticias, NoticiasAdmin)
admin.site.register(models.Patrocinador, PatrocinadorAdmin)
admin.site.register(models.Organizadores, OrganizadoresAdmin)
admin.site.register(models.Formatos, FormatosAdmin)
admin.site.register(models.Datas, DatasAdmin)
admin.site.register(models.Paginas, PaginasAdmin)
admin.site.register(models.Palestrantes, PalestrantesAdmin)
admin.site.register(models.Palestras, PalestrasAdmin)
admin.site.register(models.Local)
admin.site.register(models.Contato, ContatoAdmin)
admin.site.register(models.PalestrasArquivos)
admin.site.register(models.FormatosArquivos)
admin.site.register(models.Sirc, SircAdmin)
admin.site.register(models.Anais, AnaisAdmin)
