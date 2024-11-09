# Notas del desafio

## Parte I

### Selección del modelo

En 1. Data Analysis: First Sight y 3. Data Analysis: Second Sight, fue necesario corregir los argumentos de barplot, ya que se deben especificar explícitamente los parámetros x e y. Además, la función set está obsoleta y fue reemplazada por set_theme.

En 5. Data Analysis: Third Sight, la selección de las 10 características principales (feature importance) no está alineada con el resultado mostrado en el gráfico.

En cuanto a la selección del modelo, ambos muestran un rendimiento muy similar, Sin embargo, XGBoost presenta una ligera ventaja en el F1-score para la clase 1 (con retraso). Además, XGBoost ofrece mayor flexibilidad para futuros ajustes, lo cual podría mejorar las predicciones al incorporar datos adicionales o aplicar técnicas optimización. Cabe destacar que los datos están desequilibrados, con una mayor cantidad de ejemplos para la clase 0 (sin retraso) en comparación con la clase 1 (con retraso). Esto genera cierta preocupación respecto a la precisión en la clase minoritaria, que actualmente es baja (0.25).

### Transcripción

Se realizó la transcripción optimizando la mayor parte del código y manteniendo únicamente lo esencial para el modelo. La transcripción no presentó dificultades hasta el momento de ejecutar las pruebas unitarias, especialmente debido a la restricción de no modificar los argumentos de los métodos. Finalmente, las pruebas unitarias fueron superadas exitosamente y el modelo conservó los resultados obtenidos por el DS.

## Parte 2

## Parte 3

## Parte 4
