from datetime import datetime
from utils.exceptions import APIError

def validar_dados_viagem(dados):
    required = ['cidadeDestino', 'dataSaida', 'dataRetorno', 'codigoRelatorio', 'usuario']
    for field in required:
        if not dados.get(field):
            raise APIError(f'Campo obrigatório faltando: {field}', 400)
    
    # try:
    #     # Converter strings para datetime (formato ISO 8601)
    #     data_inicio = datetime.fromisoformat(dados['dataSaida'])
    #     data_fim = datetime.fromisoformat(dados['dataRetorno'])
        
    #     # Validar se a data de retorno é posterior à de saída
    #     if data_fim <= data_inicio:
    #         raise APIError('Data de retorno deve ser posterior à data de saída', 400)
            
    #     # return data_inicio, data_fim
        
    # except ValueError as e:
    #     raise APIError('Formato de data inválido. Use o formato YYYY-MM-DDTHH:MM', 400)

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