from model.buscarLinks import BuscarLinks
from model.acessarLinks import AcessarLinks
from model.extrairDados import ExtrairDados
from model.escreverProva import EscreverProva


def gerar_prova(materia, assunto):
	links = BuscarLinks(materia, assunto)
	acessar_links_ = AcessarLinks(links.buscar_links())
	dados = ExtrairDados(acessar_links_.acessar_links())

	try:
		questoes = dados.extrair_dados(0)
		respostas = dados.extrair_dados(1)
	except Exception as e:
		print(e)
		return -1
	else:
		escrever_prova_ = EscreverProva(materia, assunto)
		escrever_prova_.escrever_prova(questoes, "questões")
		escrever_prova_.escrever_prova(respostas, "respostas")
		return 0
	