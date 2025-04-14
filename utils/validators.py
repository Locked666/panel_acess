from datetime import datetime
from utils.exceptions import APIError

def validar_dados_viagem(dados):
    required = ['cidadeDestino', 'dataSaida', 'dataRetorno', 'codigoRelatorio']
    for field in required:
        if not dados.get(field):
            raise APIError(f'Campo obrigatório faltando: {field}', 400)
    
    try:
        data_inicio = datetime.strptime(dados['dataSaida'], '%Y-%m-%d')
        data_fim = datetime.strptime(dados['dataRetorno'], '%Y-%m-%d')
        if data_fim < data_inicio:
            raise APIError('Data de retorno deve ser após data de saída', 400)
    except ValueError:
        raise APIError('Formato de data inválido (use YYYY-MM-DD)', 400)

def validar_dados_gasto(dados):
    required = ['viagemId', 'tipoGasto', 'valor']
    print(dados)
    for field in required:
        if not dados.get(field):
            raise APIError(f'Campo obrigatório faltando: {field}', 400)
    
    try:
        float(dados['valor'])
    except ValueError:
        raise APIError('Valor deve ser um número', 400)