
class Recurso:
    """Clase base para cualquier recurso de la biblioteca."""

    def __init__(self, codigo):
        self.codigo = codigo          
        self.dias_retraso = 0         

    def calcular_multa(self):
        """Método plantilla. Cada recurso hijo DEBE sobrescribirlo."""
        raise NotImplementedError(
            "Cada recurso debe definir su propio cálculo de multa."
        )


class PrestamoLibro(Recurso):
    """Libro: multa fija de $2.50 por cada día de retraso."""

    TARIFA_DIARIA = 2.50

    def calcular_multa(self):
        return self.dias_retraso * self.TARIFA_DIARIA


class UsoSalaEstudio(Recurso):
    """Sala: multa = horas de exceso x factor de demanda."""

    def __init__(self, codigo, alumnos_en_espera=0):
        super().__init__(codigo)
        self.alumnos_en_espera = alumnos_en_espera

    def calcular_multa(self):
        factor = self.alumnos_en_espera
        horas_exceso = self.dias_retraso   
        return horas_exceso * factor


class Bibliotecario:
    """Empleado responsable de una atención."""

    def __init__(self, nombre_empleado, codigo_usuario):
        self.nombre_empleado = nombre_empleado
        self.codigo_usuario = codigo_usuario


class RegistroAtencion:
    """Registro de atención de la biblioteca."""

    LIMITE_RECURSOS = 4   

    def __init__(self, codigo, carnet_alumno, nombre_empleado, codigo_usuario):
        self.codigo = codigo
        self.carnet_alumno = carnet_alumno

        
        self.bibliotecario = Bibliotecario(nombre_empleado, codigo_usuario)

        
        self.__recursos = []

    def cargar_recurso(self, recurso):
        """Agrega un recurso validando el límite (Requisito 2)."""
        if len(self.__recursos) >= self.LIMITE_RECURSOS:
            raise ValueError("Límite de recursos por atención alcanzado")
        self.__recursos.append(recurso)

    @property
    def recursos(self):
        """Requisito 3: entrega los datos de forma inmutable (tupla)."""
        return tuple(self.__recursos)

    def auditar_saldos(self):
        """Requisito 4: ordena a todos los recursos calcular su multa,
        sin saber de qué tipo específico es cada uno (polimorfismo).
        """
        return sum(recurso.calcular_multa() for recurso in self.__recursos)




if __name__ == "__main__":

    
    registro = RegistroAtencion("REG-2026-A", "CARNET-001", "Ana López", "EMP-99")
    print(f"Registro: {registro.codigo}")
    print(f"Atendido por: {registro.bibliotecario.nombre_empleado} "
          f"({registro.bibliotecario.codigo_usuario})")

    
    libro = PrestamoLibro("LIB-01")
    libro.dias_retraso = 3                      

    sala = UsoSalaEstudio("SALA-05", alumnos_en_espera=4)
    sala.dias_retraso = 2                       

    registro.cargar_recurso(libro)
    registro.cargar_recurso(sala)

    
    print(f"\nMulta total: ${registro.auditar_saldos()}")   

    
    print(f"\nRecursos (inmutable): {registro.recursos}")
    try:
        registro.recursos.append("intruso")     
    except AttributeError as e:
        print(f"Bloqueo de alteración: {e}")

    # --- Requisito 2: límite de 4 recursos ---
    registro.cargar_recurso(PrestamoLibro("LIB-02"))
    registro.cargar_recurso(PrestamoLibro("LIB-03"))   
    try:
        registro.cargar_recurso(PrestamoLibro("LIB-04"))  
    except ValueError as e:
        print(f"\nLímite alcanzado: {e}")
        
        
        
        
        
                
                
                    
            
        
                
                
            
                
        
