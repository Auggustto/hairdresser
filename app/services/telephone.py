

def format_telephone(telephone):
    # Remove qualquer caractere não numérico do telefone
    clean_telephone = ''.join(filter(str.isdigit, telephone))

    new_telephone = '+' + "55" + clean_telephone

    return new_telephone
