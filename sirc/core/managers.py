from django.db import models

from django.contrib.auth.models import BaseUserManager


class UsuarioManager(BaseUserManager):

    use_in_migrations = True

    def create_user(self, email, password, **kwargs):

        email = self.normalize_email(email)
        is_superuser = kwargs.pop("is_superuser", False)

        user = self.model(
            email=email, is_active=True, is_superuser=is_superuser, **kwargs
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **kwargs):
        super_user = self.create_user(email=email, password=password)
        super_user.is_admin = True
        super_user.is_superuser = True
        super_user.is_active = True
        super_user.save(using=self._db)
        return super_user


class OrganizadoresQuerySet(models.QuerySet):
    def ativo(self):
        return self.filter(ativo=True)

    def coordenador_geral(self):
        return self.ativo().filter(tipo=self.model.COORDENADOR_GERAL)

    def comissao_organizadora(self):
        return self.ativo().filter(tipo=self.model.COMISSAO_ORGANIZADORA)

    def comissao_avaliadora(self):
        return self.ativo().filter(tipo=self.model.COMISSAO_AVALIADORA)


class NoticiasQuerySet(models.QuerySet):
    def publicado(self):
        return self.filter(status=self.model.PUBLICADO)


class DatasQuerySet(models.QuerySet):
    def publicado(self):
        return self.filter(status=self.model.PUBLICADO)


class FormatosQuerySet(models.QuerySet):
    def publicado(self):
        return self.filter(status=self.model.PUBLICADO)


class PalestrasQuerySet(models.QuerySet):
    def confirmada(self):
        return self.filter(status=self.model.PUBLICADO)

    def edicao_atual(self):
        import datetime

        ano = datetime.datetime.now()
        return self.confirmada().filter(edicao__id=1)

    def palestras(self):
        return self.edicao_atual().filter(tipo=self.model.PALESTRA)

    def minicursos(self):
        return self.edicao_atual().filter(tipo=self.model.MINICURSO)

    def oficinas(self):
        return self.edicao_atual().filter(tipo=self.model.OFICINA)

    def palestras_dia_um(self):
        return self.palestras().filter(dia=self.model.DIA1)

    def palestras_dia_dois(self):
        return self.palestras().filter(dia=self.model.DIA2)

    def palestras_dia_tres(self):
        return self.palestras().filter(dia=self.model.DIA3)

    def minicursos_dia_um(self):
        return self.minicursos().filter(dia=self.model.DIA1)

    def minicursos_dia_dois(self):
        return self.minicursos().filter(dia=self.model.DIA2)

    def minicursos_dia_tres(self):
        return self.minicursos().filter(dia=self.model.DIA3)
