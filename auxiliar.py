import re
import datetime
import json

class Cpf:
    def __init__(self, cpf_input):
        self.cpf_input = cpf_input
        self.cpf = self._clean_cpf()
        self.is_valid_format = self._validate_format()
        self.is_valid_cpf = False
        self.message = ''
        self.formatted_cpf = ''
        self.date_time = datetime.datetime.now()
        self.digit_1 = None
        self.digit_2 = None

    def _clean_cpf(self):
        return re.sub(r'\D', '', self.cpf_input)

    def _validate_format(self):
        if not re.fullmatch(r'\d{11}', self.cpf):
            return False
        return True

    def _check_equal_digits(self):
        return self.cpf == self.cpf[0] * 11

    def _calculate_digit(self, cpf_slice, factor):
        total = sum(int(num) * (factor - idx) for idx, num in enumerate(cpf_slice))
        remainder = total % 11
        return '0' if remainder < 2 else str(11 - remainder)

    def validate(self):
        if not self.is_valid_format:
            self.message = f"[{self.date_time.strftime('%d/%m/%Y %H:%M:%S.%f')}] {self.cpf_input} : caracter inválido"
            return

        if self._check_equal_digits():
            self.message = f"[{self.date_time.strftime('%d/%m/%Y %H:%M:%S.%f')}] {self.cpf_input} : dígitos repetidos"
            return

        self.digit_1 = int(self._calculate_digit(self.cpf[:9], 10))
        self.digit_2 = int(self._calculate_digit(self.cpf[:9] + str(self.digit_1), 11))
        
        if self.cpf[-2:] != str(self.digit_1) + str(self.digit_2):
            if self.cpf[-2] != str(self.digit_1):
                self.message = f"[{self.date_time.strftime('%d/%m/%Y %H:%M:%S.%f')}] {self.cpf_input} : 1º dígito inválido"
            else:
                self.message = f"[{self.date_time.strftime('%d/%m/%Y %H:%M:%S.%f')}] {self.cpf_input} : 2º dígito inválido"
            return

        self.is_valid_cpf = True
        self.message = f"[{self.date_time.strftime('%d/%m/%Y %H:%M:%S.%f')}] {self.formatted_cpf} : CPF válido."
        self.formatted_cpf = self._format_cpf()

    def _format_cpf(self):
        parts = [self.cpf[:3], self.cpf[3:6], self.cpf[6:9], self.cpf[9:]]
        return f"{parts[0]}.{parts[1]}.{parts[2]}-{parts[3]}"

class Arquivo:
    def __init__(self):
        self.erros_log = 'erros.log'
        self.validos_json = 'validos.json'

    def log_error(self, cpf_obj):
        with open(self.erros_log, 'a') as f:
            f.write(f"{cpf_obj.message}\n")

    def save_valid(self, cpf_obj):
        data = {
            "data": cpf_obj.date_time.strftime("%d/%m/%Y"),
            "hora": cpf_obj.date_time.strftime("%H:%M:%S.%f"),
            "cpf_digitado": cpf_obj.cpf_input,
            "digito_1": cpf_obj.digit_1,
            "digito_2": cpf_obj.digit_2,
            "cpf_formatado": cpf_obj.formatted_cpf
        }
        
        try:
            with open(self.validos_json, 'r') as f:
                cpfs_validos = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            cpfs_validos = []

        cpfs_validos.append(data)
        
        with open(self.validos_json, 'w') as f:
            json.dump(cpfs_validos, f, indent=4)

if __name__ == "__main__":
    test_cpfs = [
        '111.111.111-35',
        '529.982.247-25',
        '12345678909',
        '123.456.789-09',
        '52998224725',
        '111.444.777-35',
        '11144477735'
    ]
    arquivo = Arquivo()
    
    for cpf_str in test_cpfs:
        cpf = Cpf(cpf_str)
        cpf.validate()
        print(f"{cpf.formatted_cpf}: {cpf.message}")

        if cpf.is_valid_cpf:
            arquivo.save_valid(cpf)
        else:
            arquivo.log_error(cpf)
