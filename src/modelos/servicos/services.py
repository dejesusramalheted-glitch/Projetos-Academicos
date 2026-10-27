def calcular_media(abastecimento):
    # Lógica simples para calcular a média
    km_percorrido = abastecimento.km_atual - abastecimento.km_inicial
    media = km_percorrido / abastecimento.litros if abastecimento.litros > 0 else 0
    
    return {
        "km_percorrido": km_percorrido,
        "media_veiculo": round(float(media), 2)
    }
