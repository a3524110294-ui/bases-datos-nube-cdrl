# ADR-001 — Lenguaje y esquema de datos para M01

## Decisión
Elegimos Python como lenguaje de la aplicación, con la librería psycopg2
para conectarnos a PostgreSQL y pytest para las pruebas automáticas.

## Por qué
Python tiene una sintaxis simple, el equipo ya tiene algo de experiencia
con él, y psycopg2/pytest permiten resolver esta entrega sin dependencias
complicadas.

## Esquema de datos (contrato)
La tabla `telemetry_readings` representa una lectura de un sensor ambiental:
- device_id: identificador del sensor
- metric_name: qué mide (temperature, humidity, battery_level)
- metric_value: valor numérico medido
- unit: unidad del valor
- recorded_at: cuándo se tomó la lectura

## Pruebas
- Caso normal: inserción de una lectura válida.
- Casos límite: valor en 0, y una fecha muy antigua.
- Fallo declarado: intento de insertar sin device_id, rechazado por la
  restricción NOT NULL de la base de datos.