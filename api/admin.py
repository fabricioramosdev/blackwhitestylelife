from django.contrib import admin

from .models import (Perfil, Usuario, CategoriaProduto, SubCateriaProduto, Produto, Cliente, Venda, VendaItens,
                     Parcelas)


@admin.register(Perfil)
class Perfil(admin.ModelAdmin):
    list_display = ('pk', 'descricao')


@admin.register(Usuario)
class Usuario(admin.ModelAdmin):
    list_display = ('pk', 'nome', 'email')


@admin.register(CategoriaProduto)
class CategoriaProduto(admin.ModelAdmin):
    list_display = ('descricao',)


@admin.register(SubCateriaProduto)
class SubCateriaProduto(admin.ModelAdmin):
    list_display = ('descricao', 'categoria',)


@admin.register(Produto)
class Produto(admin.ModelAdmin):
    list_display = ('descricao', 'codigo',)


@admin.register(Cliente)
class Cliente(admin.ModelAdmin):
    list_display = ('nome', 'cpf',)


@admin.register(Venda)
class Venda(admin.ModelAdmin):
    list_display = ('id', 'cliente',)


@admin.register(VendaItens)
class VendaItens(admin.ModelAdmin):
    list_display = ('id', 'venda', 'produto')


@admin.register(Parcelas)
class Parcelas(admin.ModelAdmin):
    list_display = ('id', 'venda', 'numero')
