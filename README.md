# Proyecto 13 · Fine-tuning LoRA para seguros de automóvil

**Master AI Engineer · The Power**

## 1. Descripción del proyecto

En este proyecto aplicamos técnicas de **Fine-tuning con LoRA y QLoRA** para adaptar el comportamiento de un modelo de lenguaje a un caso de uso de atención al cliente de seguros de automóvil.

El objetivo es enseñar al modelo a responder consultas siguiendo un formato homogéneo:

- Una frase inicial que introduce la respuesta.
- Tres viñetas con información o indicaciones.
- La firma: `— Departamento de Atención al Cliente`.

No buscamos incorporar al modelo todo el conocimiento de una aseguradora. El fine-tuning adapta principalmente el formato, el tono y el estilo de las respuestas. La recuperación de información concreta sobre coberturas, exclusiones y condiciones de las pólizas corresponderá al sistema RAG.

## 2. Entorno de ejecución

El entrenamiento se ha realizado en **Google Colab con una GPU Tesla T4**, utilizando un entorno gratuito.

- Plataforma: Google Colab.
- GPU: NVIDIA Tesla T4.
- Modelo base: `Qwen/Qwen2.5-1.5B-Instruct`.
- Técnica de adaptación: QLoRA y LoRA.
- Cuantización: 4 bits.

El notebook puede ejecutarse en Google Colab con GPU. No es necesario disponer de Colab Pro.

## 3. Desarrollo del proyecto

| Paso | Descripción |
|---|---|
| 1 · Dataset | Preparación de 10 ejemplos de consultas y respuestas de seguros de automóvil, todos con el mismo formato. Se reservan 6 preguntas independientes para la evaluación. |
| 2 · QLoRA | Carga de Qwen2.5-1.5B-Instruct cuantizado a 4 bits para reducir el consumo de memoria. |
| 3 · LoRA | Adaptación del modelo mediante matrices entrenables, manteniendo congelados los pesos originales. |
| 4 · Evaluación | Comparación de las respuestas del modelo base y del modelo ajustado utilizando las mismas 6 preguntas de prueba. |
| 5 · Fusión y cierre | Guardado del adaptador LoRA, fusión con el modelo base y reflexión sobre las diferencias entre Fine-tuning y RAG. |

### Configuración del entrenamiento

Se ha utilizado la siguiente configuración:

- Rank (`r`): 8.
- Alpha (`lora_alpha`): 16.
- Dropout: 0.05.
- Módulos objetivo: `all-linear`.
- Épocas: 10.
- Batch size: 4.
- Learning rate: 3e-4.
- Optimizador: `adamw_torch`.

El entrenamiento se ha completado en 30 pasos, aproximadamente 20 segundos, con una pérdida final registrada de 0,078.

## 4. Resultados obtenidos

Se han utilizado 6 preguntas de prueba que no formaban parte del conjunto de entrenamiento.

El criterio de evaluación comprueba si las respuestas respetan el formato establecido para atención al cliente de seguros.

| Indicador | Modelo base | Modelo ajustado |
|---|---:|---:|
| Respuestas que cumplen el formato | 0/6 | 4/6 |
| Porcentaje de cumplimiento | 0 % | 66,7 % |

Los resultados muestran una mejora en la capacidad del modelo para seguir la estructura de respuesta definida.

No obstante, cumplir el formato no garantiza que la información generada sea correcta. Durante las pruebas se observaron respuestas con expresiones imprecisas o información no verificada, especialmente en consultas sobre coberturas y condiciones de los seguros.

### Prueba adicional: consulta sobre lunas

Se realizó una prueba con la pregunta:

«¿Qué debo hacer si tengo una luna rota en mi vehículo?»

El modelo ajustado reprodujo la estructura de atención al cliente, pero generó algunas expresiones incorrectas o imprecisas.

Esta prueba permite observar que el fine-tuning mejora la forma de responder, pero no garantiza el conocimiento de las condiciones reales de una póliza.

## 5. Guardado y fusión del modelo

Una vez finalizado el entrenamiento, se guardó el adaptador LoRA y se realizó su fusión con el modelo base.

| Elemento | Resultado |
|---|---|
| Adaptador LoRA | `adapter_seguros.zip` |
| Tamaño del adaptador | 37 MB |
| Modelo fusionado | `modelo_seguros_fusionado/` |
| Tamaño del modelo fusionado | 3,10 GB |

El adaptador se conserva como archivo independiente. El modelo fusionado queda disponible localmente para posibles pruebas posteriores.

## 6. Estructura del repositorio

```text
finetuning-lora/
│
├── P13_Finetuning_seguros.ipynb
├── adapter_seguros.zip
├── resultados_seguros.json
├── seguros_formato.jsonl
│
├── evidencias/
│   ├── P13_01_dataset_10_ejemplos.png
│   ├── P13_02_dataset_validado_colab.png
│   ├── P13_03_modelo_gpu_t4.png
│   ├── P13_04_configuracion_lora_modelo_base.png
│   ├── P13_05_entrenamiento_lora.png
│   ├── P13_06_comparacion_base_ajustado.png
│   ├── P13_07_respuesta_lora_lunas.png
│   ├── P13_08_modelo_fusionado.png
│   └── P13_09_resumen_ejecucion.png
│
├── prueba_local.py
├── requirements.txt
├── README.md
└── .gitignore
```

### Archivos principales

| Archivo | Descripción |
|---|---|
| `P13_Finetuning_seguros.ipynb` | Notebook ejecutado con el desarrollo y los resultados del experimento. |
| `adapter_seguros.zip` | Adaptador LoRA entrenado. |
| `resultados_seguros.json` | Resumen de la ejecución y respuestas de la evaluación. |
| `seguros_formato.jsonl` | Dataset de entrenamiento con los 10 ejemplos de seguros. |
| `evidencias/` | Capturas de pantalla de las distintas fases del proyecto. |
| `prueba_local.py` | Script auxiliar para realizar pruebas locales. |
| `requirements.txt` | Dependencias necesarias para el entorno Python. |

El modelo fusionado de 3,10 GB se conserva localmente y no se incluye en el repositorio GitHub.

## 7. Fine-tuning frente a RAG

Una de las conclusiones principales del ejercicio es la diferencia entre ambas técnicas:

- **Fine-tuning:** modifica CÓMO responde el modelo, adaptando su formato, tono y estilo.
- **RAG:** permite consultar QUÉ sabe el sistema, recuperando información de documentos externos como pólizas, coberturas y condiciones contractuales.

En una aplicación de atención al cliente de seguros, ambas técnicas pueden combinarse: LoRA aporta un comportamiento homogéneo y RAG proporciona información documental para fundamentar las respuestas.

## 8. Conclusiones

El experimento demuestra que es posible adaptar un modelo de lenguaje pequeño mediante LoRA utilizando una GPU gratuita y un conjunto reducido de ejemplos.

Con 10 ejemplos de entrenamiento se ha conseguido mejorar el cumplimiento del formato establecido, pasando de 0/6 respuestas correctas en el modelo base a 4/6 en el modelo ajustado.

Sin embargo, los resultados también muestran que la adaptación del formato no garantiza la precisión de las respuestas. Para desarrollar un asistente de seguros fiable será necesario complementar el modelo ajustado con recuperación de información documental mediante RAG.

**Resultado:** adaptador LoRA entrenado, modelo fusionado guardado, evaluación realizada y evidencias documentadas.