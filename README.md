# Laboratorio 9. Infografía estática

CC3084 Data Science, UVG. Grupo 7.

Infografía de una página sobre el flujo migratorio a Guatemala 2009-2026, basada en el Laboratorio 1.

Autores: Diego Monroy (23318), Marco Carbajal (23025), Carlos Angel (23010).

## Estructura

- `datos/` base de migración (no se sube, uso académico)
- `src/` scripts de la infografía
- `figuras/` gráficos sueltos por bloque
- `entrega/` PNG y PDF finales (se generan local, no se suben)

## Uso

Los datos y la infografía final no se publican (datos de uso estrictamente académico). Para generarla:

```
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
# copiar Base_Migracion_2009-2026jun.xlsx a datos/
.venv/bin/python src/infografia.py
```
