class AnalisadorLexico:
    def __init__(self, codigo_fonte):
        self.codigo_fonte = codigo_fonte
        self.posicao = 0
        self.linha = 1
        self.caractere_atual = self.codigo_fonte[self.posicao] if len(self.codigo_fonte) > 0 else None
        self.palavras_chave = {
            'while': 1,
            'var': 2,
            'to': 3,
            'then': 4,
            'string': 5,
            'real': 6,
            'read': 7,
            'program': 8,
            'procedure': 9,
            'print': 10,
            'integer': 14,
            'if': 15,
            'for': 17,
            'end': 18,
            'else': 19,
            'do': 20,
            'const': 21,
            'begin': 22
        }
        self.operadores = {
            '>=': 24,
            '>': 25,
            '=': 26,
            '<>': 27,
            '<=': 28,
            '<': 29,
            '+': 30,
            ';': 31,
            ':=': 32,
            ':': 33,
            '/': 34,
            '.': 35,
            ',': 36,
            '*': 37,
            ')': 38,
            '(': 39,
            '{': 40,
            '}': 41,
            '-': 42
        }

    def avancar(self):
        """Move para o próximo caractere do código fonte"""
        self.posicao += 1
        if self.posicao >= len(self.codigo_fonte):
            self.caractere_atual = None
        else:
            self.caractere_atual = self.codigo_fonte[self.posicao]
            if self.caractere_atual == '\n':
                self.linha += 1

    def pular_espacos(self):
        """Ignora espaços em branco, tabulações e quebras de linha"""
        while self.caractere_atual is not None and self.caractere_atual.isspace():
            self.avancar()
            
    def proximo_caractere(self):
        """Retorna o próximo caractere sem avançar a posição atual"""
        if self.posicao + 1 < len(self.codigo_fonte):
            return self.codigo_fonte[self.posicao + 1]
        return None

    def pular_comentario(self):
        # Verifica se é o início de um comentário de bloco
        self.avancar()  
        self.avancar() 
    
        while True:
            if self.caractere_atual is None:
                raise Exception(f"Comentário não fechado na linha {self.linha}")
            
            if self.caractere_atual == '*' and self.proximo_caractere() == '/':
                self.avancar() 
                self.avancar()  
                break
                
            self.avancar()

    def obter_numero(self):
        """Obtém um número inteiro ou real do código fonte"""
        resultado = ''
        eh_real = False

        while self.caractere_atual is not None and self.caractere_atual.isdigit():
            resultado += self.caractere_atual
            self.avancar()

        if self.caractere_atual == '.':
            eh_real = True
            resultado += self.caractere_atual
            self.avancar()
            while self.caractere_atual is not None and self.caractere_atual.isdigit():
                resultado += self.caractere_atual
                self.avancar()

        if eh_real:
            return (11, float(resultado), self.linha)  # nreal
        else:
            return (12, int(resultado), self.linha)  # nint

    def obter_identificador(self):
        """Obtém um identificador ou palavra-chave do código fonte"""
        resultado = ''
        while self.caractere_atual is not None and (self.caractere_atual.isalnum() or self.caractere_atual == '_'):
            resultado += self.caractere_atual
            self.avancar()

        # Verifica se é uma palavra-chave
        tipo_token = self.palavras_chave.get(resultado.lower(), 16)  # 16 é ident
        return (tipo_token, resultado, self.linha)

    def obter_string(self):
        """Obtém uma string delimitada por aspas duplas"""
        resultado = ''
        self.avancar()  # Pular a aspas de abertura

        while self.caractere_atual is not None and self.caractere_atual != '"':
            resultado += self.caractere_atual
            self.avancar()

        if self.caractere_atual != '"':
            raise Exception(f"String não terminada na linha {self.linha}")

        self.avancar()  # Pular a aspas de fechamento
        return (23, resultado, self.linha)  # vstring

    def obter_literal(self):
        """Obtém um literal delimitado por chaves {}"""
        resultado = ''
        self.avancar()  # Pular a chave de abertura

        while self.caractere_atual is not None and self.caractere_atual != '}':
            resultado += self.caractere_atual
            self.avancar()

        if self.caractere_atual != '}':
            raise Exception(f"Literal não terminado na linha {self.linha}")

        self.avancar()  # Pular a chave de fechamento
        return (13, resultado, self.linha)  # literal

    def obter_proximo_token(self):
        """Obtém o próximo token do código fonte"""
        while self.caractere_atual is not None:
            if self.caractere_atual.isspace():
                self.pular_espacos()
                continue

            if self.caractere_atual == '/' and self.proximo_caractere() == '*':
                self.pular_comentario()
                continue

            if self.caractere_atual.isdigit():
                return self.obter_numero()

            if self.caractere_atual.isalpha() or self.caractere_atual == '_':
                return self.obter_identificador()

            if self.caractere_atual == '"':
                return self.obter_string()

            # Tratamento de operadores com múltiplos caracteres
            if self.caractere_atual == ':':
                self.avancar()
                if self.caractere_atual == '=':
                    self.avancar()
                    return (32, ':=', self.linha)  # :=
                else:
                    return (33, ':', self.linha)  # :

            if self.caractere_atual == '<':
                self.avancar()
                if self.caractere_atual == '>':
                    self.avancar()
                    return (27, '<>', self.linha)  # <>
                elif self.caractere_atual == '=':
                    self.avancar()
                    return (28, '<=', self.linha)  # <=
                else:
                    return (29, '<', self.linha)  # <

            if self.caractere_atual == '>':
                self.avancar()
                if self.caractere_atual == '=':
                    self.avancar()
                    return (24, '>=', self.linha)  # >=
                else:
                    return (25, '>', self.linha)  # >

            # Operadores de um único caractere
            if self.caractere_atual in self.operadores:
                char = self.caractere_atual
                tipo_token = self.operadores[char]
                self.avancar()
                return (tipo_token, char, self.linha)

            # Caractere inválido
            raise Exception(f"Caractere inválido '{self.caractere_atual}' na linha {self.linha}")

        return (43, '$', self.linha)  # Fim do arquivo


def principal():

    nome_arquivo = 'script.txt'

    try:
        with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
            codigo_fonte = arquivo.read()
    except FileNotFoundError:
        print(f"Erro: Arquivo '{nome_arquivo}' não encontrado!")
        return
    except Exception as e:
        print(f"Erro ao ler arquivo: {e}")
        return

    lexer = AnalisadorLexico(codigo_fonte)

    while True:
        token = lexer.obter_proximo_token()
        print(f"Token: {token[1]}, Tipo: {token[0]}, Linha: {token[2]}")
        if token[0] == 43:  # $
            break


if __name__ == "__main__":
    principal()