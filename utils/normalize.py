def strip_lower(field: str) -> str:
    try:
        return field.strip().lower()
    except (AttributeError, Exception) as e:
        raise Exception(f'Erro ao normalizar o valor {field}.') from e


def strip_title(field: str) -> str:
    field = field.strip()
    try:
        if ' ' in field:
            return ' '.join([w.capitalize() if len(w) > 2 else w for w in field.split(' ')])
        return field.capitalize()
    except (AttributeError, Exception) as e:
        raise Exception(f'Erro ao normalizar o valor {field}.') from e
