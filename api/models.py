from django.db import models


class Base(models.Model):
    criacao = models.DateTimeField(auto_now_add=True)
    atualizacao = models.DateTimeField(auto_now=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Perfil(Base):
    descricao = models.CharField(max_length=255, blank=False, null=False)

    class Meta:
        db_table = 'perfil'
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfis'
        ordering = ['id']

    def __str__(self):
        return f'{self.descricao}'


class Usuario(Base):
    nome = models.CharField(max_length=255, blank=False, null=False)
    email = models.EmailField(unique=True)
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE)

    class Meta:
        db_table = 'usuarios'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['id']

    def __str__(self):
        return f'{self.nome}\t({self.email})'


class CategoriaProduto(Base):
    descricao = models.CharField(max_length=255, blank=False, null=False)

    class Meta:
        db_table = 'categoria'
        verbose_name = 'Categoria Produto'
        verbose_name_plural = 'Categorias Produtos'
        ordering = ['id']

    def __str__(self):
        return f'{self.descricao}'


class SubCateriaProduto(Base):
    descricao = models.CharField(max_length=255, blank=False, null=False)
    categoria = models.ForeignKey(CategoriaProduto, on_delete=models.CASCADE)

    class Meta:
        db_table = 'sub_categoria'
        verbose_name = 'Subcategoria Produto'
        verbose_name_plural = 'Subcategorias Produtos'
        ordering = ['id']

    def __str__(self):
        return f'{self.descricao}'


class Produto(Base):
    descricao = models.CharField(max_length=255, blank=False, null=False)
    codigo = models.CharField(max_length=10, blank=False, null=False)
    tamanho = models.CharField(max_length=10, blank=False, null=False)
    caracteristicas = models.TextField(blank=True, null=True)
    composicao = models.CharField(max_length=255, blank=True, null=True)  # Algodão 97%, Elastano 3%
    preco_venda = models.DecimalField(default=00.00, max_digits=5, decimal_places=2, blank=False, null=False)
    preco_compra = models.DecimalField(default=00.00, max_digits=5, decimal_places=2, blank=False, null=False)

    taxa_desc_max = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    taxa_desc_min = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    # Produto em promoção True usa taxa min e calcula o novo preço de venda
    promocao = models.BooleanField(default=False)

    estoque_saldo = models.IntegerField(default=0, blank=False, null=False)
    estoque_minimo = models.IntegerField(default=0, blank=False, null=False)

    categoria = models.ForeignKey(SubCateriaProduto, on_delete=models.PROTECT)

    class Meta:
        db_table = 'produto'
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
        ordering = ['id']

    def __str__(self):
        return f'{self.descricao}\t({self.codigo})'


class Cliente(Base):

    SEXO_CHOICES = (
        ("F", "Feminino"),
        ("M", "Masculino"),
        ("N", "Nenhuma das opções")
    )

    nome = models.CharField(max_length=255, blank=False, null=False)
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES, blank=False, null=False)
    cpf = models.CharField(max_length=11, blank=False, null=False)
    rg = models.CharField(max_length=20, blank=True, null=True)
    limite = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    apelido = models.CharField(max_length=255, blank=True, null=True)
    endereco = models.TextField(blank=True, null=True)
    whatsapp = models.CharField(max_length=20, blank=True, null=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    data_nascimento = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'cliente'
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['id']

    def __str__(self):
        return f'{self.nome}\t({self.cpf})'


class Venda(Base):

    TIPO_PAGAMENTO_CHOICES = (
        ("DI", "Dinheiro"),
        ("CC", "Cartão Crédito"),
        ("CD", "Cartão Débito"),
        ("PX", "Pix"),
        ("CL", "Crediário"),
    )

    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    tipo_pagamento = models.CharField(max_length=2, choices=TIPO_PAGAMENTO_CHOICES, blank=False, null=False)
    valor_total = models.DecimalField(max_digits=5, decimal_places=2, blank=False, null=False)
    num_parcelas = models.IntegerField(blank=True, null=True)  # Nº de parcelas
    saldo_devedor = models.DecimalField(max_digits=5, decimal_places=2, blank=False, null=False)
    # Calcula o % da divida 100% - 0% = dívida paga
    taxa_devedor = models.IntegerField(default=100, blank=True, null=True)

    class Meta:
        db_table = 'venda'
        verbose_name = 'Venda'
        verbose_name_plural = 'Vendas'
        ordering = ['id']

    def __str__(self):
        return f'{self.cliente}\t({self.pk}) - {self.valor_total}'


class VendaItens(Base):
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    preco = models.DecimalField(max_digits=5, decimal_places=2, blank=False, null=False)
    quantidade = models.IntegerField(default=1, blank=False, null=False)
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)

    class Meta:
        db_table = 'venda_item'
        verbose_name = 'Venda Item'
        verbose_name_plural = 'Vendas Itens'
        ordering = ['id']

    def __str__(self):
        return f'{self.cliente}\t({self.pk}) - {self.venda}'


class Parcelas(Base):
    STATUS_PAGAMENTO_CHOICES = (
        ("PG", "Pago"),
        ("PP", "Pago parcial"),
    )

    venda = models.ForeignKey(Venda, on_delete=models.PROTECT)
    numero = models.CharField(max_length=5, blank=False, null=False)  # ex. 1/3; 2/3; 3/3
    valor = models.DecimalField(max_digits=5, decimal_places=2, blank=False, null=False)
    valor_parcial = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    saldo_devedor = models.DecimalField(max_digits=5, decimal_places=2, blank=False, null=False)
    data_venc = models.DateField(blank=False, null=False)
    situacao = models.CharField(max_length=2, choices=STATUS_PAGAMENTO_CHOICES, blank=False, null=False)

    class Meta:
        db_table = 'parcela'
        verbose_name = 'Parcela'
        verbose_name_plural = 'Parcelas'
        ordering = ['id']

    def __str__(self):
        return f'{self.venda}\t({self.numero})'