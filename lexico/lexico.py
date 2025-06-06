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

    def pular_comentario(self):
            """Ignora comentários delimitados por /* */"""
            self.avancar()
            if self.caractere_atual != '*':
                raise Exception(f"Comentário mal formado na linha {self.linha} - esperado * após /")
            
            self.avancar()
        
            while self.caractere_atual is not None:
                if self.caractere_atual == '*' and self.posicao + 1 < len(self.codigo_fonte) and self.codigo_fonte[self.posicao + 1] == '/':
                    self.avancar()  
                    self.avancar()  
                    return
                self.avancar()
            
            raise Exception(f"Comentário não terminado na linha {self.linha}")
    
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
            return (11, float(resultado), self.linha)
        else:
            return (12, int(resultado), self.linha)

    def obter_identificador(self):
        """Obtém um identificador ou palavra-chave do código fonte"""
        resultado = ''
        while self.caractere_atual is not None and (self.caractere_atual.isalnum() or self.caractere_atual == '_'):
            resultado += self.caractere_atual
            self.avancar()
        tipo_token = self.palavras_chave.get(resultado.lower(), 16) 
        return (tipo_token, resultado, self.linha)

    def obter_string(self):
        """Obtém uma string delimitada por aspas duplas"""
        resultado = ''
        self.avancar()  

        while self.caractere_atual is not None and self.caractere_atual != '"':
            resultado += self.caractere_atual
            self.avancar()

        if self.caractere_atual != '"':
            raise Exception(f"String não terminada na linha {self.linha}")

        self.avancar() 
        return (23, resultado, self.linha) 

    def obter_literal(self):
        """Obtém um literal delimitado por chaves {}"""
        resultado = ''
        self.avancar()

        while self.caractere_atual is not None and self.caractere_atual != '}':
            resultado += self.caractere_atual
            self.avancar()

        if self.caractere_atual != '}':
            raise Exception(f"Literal não terminado na linha {self.linha}")

        self.avancar()
        return (13, resultado, self.linha)

    def obter_proximo_token(self):
        """Obtém o próximo token do código fonte"""
        while self.caractere_atual is not None:
            if self.caractere_atual.isspace():
                self.pular_espacos()
                continue

            if self.caractere_atual == '/':
                if self.posicao + 1 < len(self.codigo_fonte) and self.codigo_fonte[self.posicao + 1] == '*':
                    self.pular_comentario()
                    continue
                else:
                    tipo_token = self.operadores['/']
                    self.avancar()
                    return (tipo_token, '/', self.linha)

            if self.caractere_atual.isdigit():
                return self.obter_numero()

            if self.caractere_atual.isalpha() or self.caractere_atual == '_':
                return self.obter_identificador()

            if self.caractere_atual == '"':
                return self.obter_string()

            if self.caractere_atual == ':':
                self.avancar()
                if self.caractere_atual == '=':
                    self.avancar()
                    return (32, ':=', self.linha)  
                else:
                    return (33, ':', self.linha)

            if self.caractere_atual == '<':
                self.avancar()
                if self.caractere_atual == '>':
                    self.avancar()
                    return (27, '<>', self.linha)  
                elif self.caractere_atual == '=':
                    self.avancar()
                    return (28, '<=', self.linha)  
                else:
                    return (29, '<', self.linha) 

            if self.caractere_atual == '>':
                self.avancar()
                if self.caractere_atual == '=':
                    self.avancar()
                    return (24, '>=', self.linha) 
                else:
                    return (25, '>', self.linha)  
                
            if self.caractere_atual in self.operadores:
                char = self.caractere_atual
                tipo_token = self.operadores[char]
                self.avancar()
                return (tipo_token, char, self.linha)

            raise Exception(f"Caractere inválido '{self.caractere_atual}' na linha {self.linha}")

        return (43, '$', self.linha) 

def analisar(codigo_fonte):
    lexer = AnalisadorLexico(codigo_fonte)
    tokens = []
    while True:
        token = lexer.obter_proximo_token()
        tokens.append({
            'token': token[0],
            'lexema': token[1],
            'linha': token[2]
        })
        if token[0] == 43: 
            break
    return tokens

def analisar_arquivo(nome_arquivo):
    try:
        with open(nome_arquivo, 'r', encoding='utf-8') as arquivo: 
            codigo_fonte = arquivo.read()           
        return analisar(codigo_fonte)
    except FileNotFoundError:
        print(f"Erro: Arquivo '{nome_arquivo}' não encontrado!")
        return []
    except Exception as e:
        print(f"Erro ao ler arquivo: {e}")
        return []

if __name__ == "__main__":
    tokens = analisar_arquivo('lexico/script.txt')
    for token in tokens:
        print(f"Token: {token['token']}, Lexema: '{token['lexema']}', Linha: {token['linha']}")