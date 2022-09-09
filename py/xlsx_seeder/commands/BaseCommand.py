from abc import abstractmethod

class BaseCommand:

    @abstractmethod
    def run(self):
        """Realiza la ejecución de un comando
        """
        pass

    def get_parameter(args, parameter):
        """Devuelve el valor asignado al parámetro
        Args:
            args (str): La lista de comandos definidos
            parameter (str): El parámetro
        Raises:
            Exception: Arroja una excepción en caso de que el comando no este definido
        Returns:
            str: El valor del parámetro
        """
        try:
            index = args.index(parameter)
            return args[index+1]
        except ValueError:
            raise Exception("El comando actual no contiene el parametro -" + parameter)

    def get_optional_parameter(args, parameter, default):
        """Devuelve el valor asignado al parámetro
        Args:
            args (str): La lista de comandos definidos
            parameter (str): El parámetro
            default (str): En caso de encontrar el valor se devuelve este valor
        Returns:
            str: El valor del parámetro
        """
        try:
            index = args.index(parameter)
            return args[index+1]
        except ValueError:
            return default