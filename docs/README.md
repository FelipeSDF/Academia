# Docs

Guias de como fazer cada coisa neste projeto.

| Guia | Assunto |
|---|---|
| [01-cadastrar.md](01-cadastrar.md) | Adicionar um registro com ModelForm |
| [02-listar.md](02-listar.md) | Mostrar todos os registros na tela |
| [03-pesquisar.md](03-pesquisar.md) | Filtrar a lista por um campo |
| [04-editar.md](04-editar.md) | Alterar um registro existente |
| [05-excluir.md](05-excluir.md) | Apagar um registro |
| [06-model-e-form.md](06-model-e-form.md) | Criar campos, choices e o ModelForm |
| [07-urls.md](07-urls.md) | Ligar uma view a uma rota |
| [08-estilos-static.md](08-estilos-static.md) | CSS em arquivo separado e collectstatic |
| [09-comandos.md](09-comandos.md) | Comandos do manage.py |
| [10-erros-comuns.md](10-erros-comuns.md) | O que fazer quando quebra |

## A ideia geral

Toda funcionalidade se resume a duas perguntas:

1. **De onde vem o dado?** `request.POST` (vai mudar o banco) ou `request.GET` (so vai olhar)
2. **O que faco com o model?** `.all()` `.filter()` `.get()` `.save()` `.delete()`

| Quero | Uso |
|---|---|
| tudo | `Peso.objects.all()` |
| filtrado | `Peso.objects.filter(campo__icontains=x)` |
| um so | `Peso.objects.get(id=x)` |
| criar | `PesoForm(request.POST)` + `.save()` |
| editar | `PesoForm(request.POST, instance=peso)` + `.save()` |
| apagar | `peso.delete()` |
