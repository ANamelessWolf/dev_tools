import re

# Aquí se especifican los metodos que ejecuta la acción de transform

def words_only(value, data = None):
    """Toma como entrada una estring y remueve cualquier carácter que no este definido de la A-Z
    
    Args:
        value (string): La cadena de entrada
        data (any): Los datos de entrada para la transformación

    Returns:
        string: La cadena filtrada
    """
    return re.sub(r'[^a-zA-Z]', '', value)