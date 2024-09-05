def validar_cpf(cpf):
    #limpeza
    
    cpf = ''.join([i for i in cpf if i.isdigit()])
    
    #tamanho
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False
    
    #digito 1
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    digito_1 = (soma * 10 % 11) % 10
    if digito_1 != int(cpf[9]):
        return False
    
    #digito 2
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    digito_2 = (soma * 10 % 11) % 10
    if digito_2 != int(cpf[10]):
        return False
    
    return True