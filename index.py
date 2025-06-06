from sintatico.sintatico import AdaptedParser
from lexico.lexico import analisar_arquivo

tokens = analisar_arquivo('./lexico/script.txt')
codigos_tokens = [t['token'] for t in tokens]

parser = AdaptedParser()
resultado = parser.parse(codigos_tokens)
print("Análise concluída com sucesso!" if resultado else "Erro na análise!")