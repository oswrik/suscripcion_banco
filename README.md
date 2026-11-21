# Captación inteligente de depósitos a plazo fijo

 **Machine Learning · Maestría en Ciencia de Datos e Inteligencia Artificial · EPG UNAJ**
Docente: Dr. Alain Paul Herrera Urtiaga

**Realizado por:** Edgar Oswaldo Ccapa Yanqui 
**Repositorio:** https://github.com/oswrik/suscripcion_banco/

**Informes:** [Producto 1](informe/Producto1.pdf) · [Producto 2](informe/Producto2.pdf)

## 1. El problema

Casi 9 de cada 10 llamadas telefónicas de campañas bancarias terminan sin que el cliente contrate el depósito a plazo fijo. Si el banco pudiera estimar **antes de marcar el teléfono** qué clientes tienen mayor interés, podría enfocar el tiempo de sus asesores y reducir llamadas improductivas.

**Pregunta:** antes de iniciar la llamada comercial, ¿qué clientes contratarán un depósito a plazo fijo?

- **Tipo de problema:** clasificación binaria (suscribe / no suscribe)
- **Métrica principal:** **recall** (tasa de detección), porque perder a un cliente dispuesto a invertir cuesta más que hacer una llamada telefónica sin éxito. Reportamos también el **ROC-AUC**.

## 2. Los datos

| Campo | Detalle |
|---|---|
| Fuente | [Bank Marketing](https://archive.ics.uci.edu/dataset/222/bank+marketing) (`bank-full.csv`, UCI Machine Learning Repository) |
| Tamaño | 45 211 clientes contactados |
| Variables usadas | 15: perfil demográfico, situación financiera (saldo, hipoteca, préstamos) e historial de contacto previo |
| Variable objetivo | `suscribe` (1 = contrató el depósito a plazo): **11,7 %** de los casos |

Solo usamos información disponible **antes de iniciar la llamada**. La duración de la llamada (`duration`) se excluyó por completo para evitar fuga de datos del futuro.

## 3. Resultados principales

| Modelo | Recall (CV) | ROC-AUC (CV) |
|---|---|---|
| Baseline (clase mayoritaria) | 0,000 ± 0,000 | 0,500 ± 0,000 |
| k-NN (k = 15) | 0,155 ± 0,010 | 0,730 ± 0,005 |
| Random Forest | 0,208 ± 0,010 | 0,779 ± 0,005 |
| Regresión logística (L2) | 0,622 ± 0,010 | 0,764 ± 0,003 |
| Gradient Boosting (HistGBM) | 0,617 ± 0,011 | 0,797 ± 0,002 |
| **Gradient Boosting regularizado (Optuna) · modelo final** | — | **0,798 ± 0,008** |
| Red neuronal (MLP) | — | 0,781 ± 0,005 |

**En el test**, el modelo final detecta a **64 de cada 100** clientes que contratarán el depósito antes de realizar la llamada (`recall = 0,642`; `ROC-AUC = 0,804`).

**Hallazgos clave:**
- La señal individual más fuerte es haber **aceptado una oferta en campañas previas** (**64,7 %** de conversión), mientras que tener hipoteca reduce la suscripción a menos de la mitad (**7,7 %** frente a **16,7 %**).
- Gradient Boosting ajustado con Optuna empata en puntuación con su versión original ($p = 0,73$) pero con reglas más controladas, y supera de forma clara a la regresión logística en las 25 rondas evaluadas ($p < 0,001$).
- Al agrupar clientes sin mirar la respuesta (`k-means`), descubrimos un segmento de **19 699 clientes sin hipoteca ni mora con 16,9 % de suscripción**, frente a solo **6,4 %** en clientes con deudas atrasadas.
- El modelo detecta menos interesados en adultos de **31 a 60 años (56 %–58 %)** que en jóvenes y mayores de 60 años (**75 %–100 %**): es una brecha a calibrar antes de llevarlo a producción.

## 4. Estructura del repositorio

```
├── README.md                    
├── data/                          
├── notebooks/
│   ├── 01_eda.ipynb                   
│   ├── 02_modelos.ipynb           
│   ├── 03_optimizacion.ipynb     
│   ├── 04_no_supervisado_y_red.ipynb  
│   └── 05_interpretacion.ipynb       
├── app/                            
├── informe/                      
```

## 5. Cómo reproducir

1. Abrir cada cuaderno en Google Colab: **Archivo → Abrir cuaderno → GitHub** y pegar el enlace `https://github.com/oswrik/suscripcion_banco/`.
2. Ejecutar en orden, de arriba hacia abajo (**Entorno de ejecución → Ejecutar todas**). Los datos se cargan automáticamente desde la carpeta `data/` o desde el repositorio.
3. Demo local: instalar dependencias con `pip install -r app/requirements.txt` y ejecutar `streamlit run app/app.py`.

## 6. Uso de IA generativa

Se utilizó apoyo de herramientas de IA generativa para estructurar los cuadernos de programación en Python dentro de Google Colab.
