# Planificación de menús semanales | IA-FIB-UPC

## Rico-rico: Planificador automático de menús

### ¿Qué es este proyecto?

Este proyecto genera un menú semanal equilibrado, seleccionando primeros y segundos platos según diferentes restricciones:

- Evita incompatibilidades entre primeros y segundos platos.
- No repite platos durante la semana.
- Evita repetir categorías de platos en días consecutivos.
- Permite fijar menús para días concretos.
- Ofrece menús dentro de un rango calórico.
- Busca minimizar el precio total del menú semanal.

### Estructura del repositorio

- **linux_metrics/**: Código fuente para compilar el planificador FF en Linux con métricas.
- **templates/**: Plantillas básicas para la generación de problemas y documentación LaTeX.
- **extension_5/**: Carpeta con todos los archivos PDDL.
- **executable.py**: Script principal para ejecutar el planificador. Permite lanzar ejemplos y tests.
- **generator.py**: Generador de problemas aleatorios. Permite especificar cuántos tests crear.

### Ejecución

Para ejecutar el proyecto necesitas tener instalado FF (Fast Forward) en Linux.  
Después, puedes lanzar el planificador con:

```bash
python3 executable.py
```

Para ejecutar los ejemplos ya creados:

```bash
python3 executable.py --ejemplos
```

Para ejecutar los tests generados:

```bash
python3 executable.py --test
```

### Generar problemas aleatorios

Para crear nuevos problemas de prueba, ejecuta:

```bash
python3 generator.py [NÚMERO_DE_TESTS]
```

Esto generará los archivos de test en la carpeta `extension_5/`.

---

**Nota:**  
El proyecto está preparado para funcionar únicamente en sistemas Linux.
