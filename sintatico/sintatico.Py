class AdaptedParser:
    def __init__(self):
        self.code_to_name = {
            1: 'while', 2: 'var', 3: 'to', 4: 'then', 5: 'string',
            6: 'real', 7: 'read', 8: 'program', 9: 'procedure', 10: 'print',
            11: 'nreal', 12: 'nint', 13: 'literal', 14: 'integer', 15: 'if',
            16: 'ident', 17: 'for', 18: 'end', 19: 'else', 20: 'do',
            21: 'const', 22: 'begin', 23: 'vstring', 24: '>=', 25: '>',
            26: '=', 27: '<>', 28: '<=', 29: '<', 30: '+',
            31: ';', 32: ':=', 33: ':', 34: '/', 35: '.',
            36: ',', 37: '*', 38: ')', 39: '(', 40: '{',
            41: '}', 42: '-', 43: '$', 44: 'î',         
            45: 'PROGRAMA', 46: 'DECLARACOES', 47: 'BLOCO', 48: 'CONSTANTES',
            49: 'VARIAVEIS', 50: 'PROCEDIMENTOS', 51: 'COMANDOS', 52: 'LISTAVARIAVEIS',
            53: 'TIPO', 54: 'LDVAR', 55: 'REPIDENT', 56: 'PARAMETROS',
            57: 'REPPARAMETROS', 58: 'COMANDO', 59: 'ITEMSAIDA', 60: 'REPITEM',
            61: 'EXPRESSAO', 62: 'TERMO', 63: 'EXPR', 64: 'FATOR',
            65: 'TER', 66: 'EXPRELACIONAL', 67: 'ELSEOPC', 68: 'OPREL',
            69: 'CHAMADAPROC', 70: 'LISTAPARAMETROS', 71: 'PAR', 72: 'REPPAR'
        }

        self.productions = {
            1: [8, 16, 31, 46, 47, 35],
            2: [48, 49, 50],
            3: [21, 16, 26, 12, 31, 48],
            4: [44], 
            5: [2, 52, 33, 53, 31, 54],
            6: [16, 55],
            7: [44],  
            8: [36, 16, 55],
            9: [52, 33, 53, 31, 54],
            10: [44], 
            11: [14],
            12: [6],
            13: [5],
            14: [9, 16, 56, 31, 47, 31, 50],
            15: [44],  
            16: [39, 52, 33, 53, 57, 38],
            17: [44],  
            18: [36, 52, 33, 53, 57],
            19: [44],  
            20: [22, 51, 18],
            21: [58, 31, 51],
            22: [44],  
            23: [10, 40, 59, 60, 41],
            24: [61],
            25: [44],  
            26: [36, 59, 60],
            27: [62, 63],
            28: [30, 62, 63],
            29: [42, 62, 63],
            30: [44],  
            31: [64, 65],
            32: [37, 64, 65],
            33: [34, 64, 65],
            34: [44],  
            35: [39, 61, 38],
            36: [16],
            37: [12],
            38: [11],
            39: [13],
            40: [23],
            41: [15, 66, 4, 47, 67],
            42: [61, 68, 61],
            43: [26],
            44: [27],
            45: [29],
            46: [25],
            47: [28],
            48: [24],
            49: [19, 47],
            50: [44],  
            51: [16, 69],
            52: [17, 16, 32, 61, 3, 61, 20, 47],
            53: [70],
            54: [32, 61],
            55: [39, 71, 72, 38],
            56: [44],  
            57: [16],
            58: [12],
            59: [11],
            60: [23],
            61: [36, 71, 72],
            62: [44],  
            63: [1, 66, 20, 47],
            64: [7, 39, 16, 38],
            65: [13]
        }

        self.parsing_table = {
            (45, 8): 1,  # PROGRAMA, program
            (46, 2): 2,  # DECLARACOES, var
            (46, 21): 2,  # DECLARACOES, const
            (47, 22): 20,  # BLOCO, begin
            (48, 21): 3,  # CONSTANTES, const
            (48, 2): 4,  # CONSTANTES, var
            (49, 2): 5,  # VARIAVEIS, var
            (52, 16): 6,  # LISTAVARIAVEIS, ident
            (53, 14): 11,  # TIPO, integer
            (53, 6): 12,  # TIPO, real
            (53, 5): 13,  # TIPO, string
            (54, 16): 9,  # LDVAR, ident
            (54, 9): 10,  # LDVAR, procedure
            (54, 22): 10,  # LDVAR, begin
            (55, 36): 8,  # REPIDENT, ','
            (55, 33): 7,  # REPIDENT, ':'
            (56, 39): 16,  # PARAMETROS, '('
            (56, 31): 17,  # PARAMETROS, ';'
            (57, 36): 18,  # REPPARAMETROS, ','
            (57, 38): 19,  # REPPARAMETROS, ')'
            (50, 9): 14,  # PROCEDIMENTOS, procedure
            (50, 22): 15,  # PROCEDIMENTOS, begin
            (51, 1): 21,  # COMANDOS, while
            (51, 7): 21,  # COMANDOS, read
            (51, 10): 21,  # COMANDOS, print
            (51, 15): 21,  # COMANDOS, if
            (51, 16): 21,  # COMANDOS, ident
            (51, 17): 21,  # COMANDOS, for
            (51, 18): 22,  # COMANDOS, end
            (58, 1): 63,  # COMANDO, while
            (58, 7): 64,  # COMANDO, read
            (58, 10): 23,  # COMANDO, print
            (58, 15): 41,  # COMANDO, if
            (58, 16): 51,  # COMANDO, ident
            (58, 17): 52,  # COMANDO, for
            (59, 11): 24,  # ITEMSAIDA, nreal
            (59, 12): 24,  # ITEMSAIDA, nint
            (59, 13): 24,  # ITEMSAIDA, literal
            (59, 16): 24,  # ITEMSAIDA, ident
            (59, 39): 24,  # ITEMSAIDA, '('
            (59, 23): 24,  # ITEMSAIDA, vstring
            (60, 36): 26,  # REPITEM, ','
            (60, 41): 25,  # REPITEM, '}'
            (61, 11): 27,  # EXPRESSAO, nreal
            (61, 12): 27,  # EXPRESSAO, nint
            (61, 13): 27,  # EXPRESSAO, literal
            (61, 16): 27,  # EXPRESSAO, ident
            (61, 39): 27,  # EXPRESSAO, '('
            (61, 23): 27,  # EXPRESSAO, vstring
            (62, 11): 31,  # TERMO, nreal
            (62, 12): 31,  # TERMO, nint
            (62, 13): 31,  # TERMO, literal
            (62, 16): 31,  # TERMO, ident
            (62, 39): 31,  # TERMO, '('
            (62, 23): 31,  # TERMO, vstring
            (63, 30): 28,  # EXPR, '+'
            (63, 42): 29,  # EXPR, '-'
            (63, 3): 30,  # EXPR, to
            (63, 20): 30,  # EXPR, do
            (63, 26): 30,  # EXPR, '='
            (63, 27): 30,  # EXPR, '<>'
            (63, 29): 30,  # EXPR, '<'
            (63, 25): 30,  # EXPR, '>'
            (63, 28): 30,  # EXPR, '<='
            (63, 24): 30,  # EXPR, '>='
            (63, 38): 30,  # EXPR, ')'
            (63, 36): 30,  # EXPR, ','
            (63, 41): 30,  # EXPR, '}'
            (63, 4): 30,  # EXPR, then
            (63, 31): 30,  # EXPR, ';'
            (64, 11): 38,  # FATOR, nreal
            (64, 12): 37,  # FATOR, nint
            (64, 13): 39,  # FATOR, literal
            (64, 16): 36,  # FATOR, ident
            (64, 39): 35,  # FATOR, '('
            (64, 23): 40,  # FATOR, vstring
            (65, 37): 32,  # TER, '*'
            (65, 34): 33,  # TER, '/'
            (65, 30): 34,  # TER, '+'
            (65, 42): 34,  # TER, '-'
            (65, 3): 34,  # TER, to
            (65, 20): 34,  # TER, do
            (65, 26): 34,  # TER, '='
            (65, 27): 34,  # TER, '<>'
            (65, 29): 34,  # TER, '<'
            (65, 25): 34,  # TER, '>'
            (65, 28): 34,  # TER, '<='
            (65, 24): 34,  # TER, '>='
            (65, 38): 34,  # TER, ')'
            (65, 36): 34,  # TER, ','
            (65, 41): 34,  # TER, '}'
            (65, 4): 34,  # TER, then
            (65, 31): 34,  # TER, ';'
            (66, 11): 42,  # EXPRELACIONAL, nreal
            (66, 12): 42,  # EXPRELACIONAL, nint
            (66, 13): 42,  # EXPRELACIONAL, literal
            (66, 16): 42,  # EXPRELACIONAL, ident
            (66, 39): 42,  # EXPRELACIONAL, '('
            (66, 23): 42,  # EXPRELACIONAL, vstring
            (67, 19): 49,  # ELSEOPC, else
            (67, 31): 50,  # ELSEOPC, ';'
            (68, 26): 43,  # OPREL, '='
            (68, 27): 44,  # OPREL, '<>'
            (68, 29): 45,  # OPREL, '<'
            (68, 25): 46,  # OPREL, '>'
            (68, 28): 47,  # OPREL, '<='
            (68, 24): 48,  # OPREL, '>='
            (69, 39): 53,  # CHAMADAPROC, '('
            (69, 32): 54,  # CHAMADAPROC, ':='
            (69, 31): 53,  # CHAMADAPROC, ';'
            (70, 39): 55,  # LISTAPARAMETROS, '('
            (70, 31): 56,  # LISTAPARAMETROS, ';'
            (71, 16): 57,  # PAR, ident
            (71, 12): 58,  # PAR, nint
            (71, 11): 59,  # PAR, nreal
            (71, 23): 60,  # PAR, vstring
            (71, 13): 65,  # PAR, literal
            (72, 36): 61,  # REPPAR, ','
            (72, 38): 62,  # REPPAR, ')'
        }
        
        self.start_symbol = 45  # PROGRAMA

    def symbol_name(self, code):
        return self.code_to_name.get(code, str(code))

    def parse(self, input_codes):
        stack = [43, self.start_symbol]
        input_index = 0
        current_token = input_codes[input_index]

        print(f"{'Pilha':<40} {'Entrada':<40} {'Ação':<30}")
        print(f"{' '.join(self.symbol_name(s) for s in stack):<40} {' '.join(self.symbol_name(t) for t in input_codes[input_index:]):<40} {'Inicialização':<30}")

        while True:
            top = stack[-1]

            if top == 43 and current_token == 43:
                print(f"{' '.join(self.symbol_name(s) for s in stack):<40} {' '.join(self.symbol_name(t) for t in input_codes[input_index:]):<40} {'Aceito':<30}")
                return True

            elif top == current_token:
                stack.pop()
                input_index += 1
                current_token = input_codes[input_index] if input_index < len(input_codes) else 43
                print(f"{' '.join(self.symbol_name(s) for s in stack):<40} {' '.join(self.symbol_name(t) for t in input_codes[input_index:]):<40} {'Consome ' + self.symbol_name(top):<30}")

            elif top == 44:
                stack.pop()
                print(f"{' '.join(self.symbol_name(s) for s in stack):<40} {' '.join(self.symbol_name(t) for t in input_codes[input_index:]):<40} {'Desempilha ε':<30}")

            elif top >= 45: 
                key = (top, current_token)
                if key in self.parsing_table:
                    production_num = self.parsing_table[key]
                    production = self.productions[production_num]
                    
                    stack.pop()
                    if production != [44]:
                        for symbol in reversed(production):
                            stack.append(symbol)
                    
                    prod_str = 'ε' if production == [44] else ' '.join(self.symbol_name(s) for s in production)
                    action = f"Aplica {production_num}: {self.symbol_name(top)} → {prod_str}"
                    print(f"{' '.join(self.symbol_name(s) for s in stack):<40} {' '.join(self.symbol_name(t) for t in input_codes[input_index:]):<40} {action:<30}")
                else:
                    stack.pop()

            else:
                print(f"Erro: Token inesperado de código {top} encontrado na pilha.")
                return False


if __name__ == "__main__":
    parser = AdaptedParser()

    input_program = [8, 16 , 31 , 22, 10 , 40, 16, 41, 31 ,18 , 35, 43]

    print("\nAnalisando programa:")
    result = parser.parse(input_program)
    print("Análise concluída com sucesso!" if result else "Erro na análise!")
