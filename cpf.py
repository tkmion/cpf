from val_cpf import validar_cpf

# Loop while para verificar vários CPFs
while True:
    cpf_input = input("Digite o CPF para validação, ou escreva 'sair' para encerrar: ")
    
    if cpf_input.lower() == 'sair':
        print("Fechando a verificação de CPFs.")
        break
    
    # Chama a função validar_cpf passando o CPF inserido
    if validar_cpf(cpf_input):
        print("CPF válido!")
    else:
        print("CPF inválido.")
