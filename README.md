# finetuning-lora · Master AI Engineer · Sesion 8

**Fine-tuning con LoRA y QLoRA.** Ensenamos a un modelo pequeno (Qwen2.5-1.5B-Instruct) un **comportamiento**:
contestar las dudas internas de *Nexa Consulting* siempre con el formato de la casa (titular + 3 vinetas + firma).
No le ensenamos datos: eso es cosa del RAG (sesiones 5 y 6).

## Donde se ejecuta: en una GPU GRATIS
El entrenamiento necesita GPU. **No hace falta pagar nada:**
- **Google Colab (gratis):** https://colab.research.google.com → *Archivo → Subir cuaderno* → `08_finetuning.ipynb`
  → *Entorno de ejecucion → Cambiar tipo de entorno → T4 GPU* → *Ejecutar todo*. Unos 10-15 minutos.
- **Kaggle (gratis, 30 h de GPU a la semana):** https://www.kaggle.com → *Create → New Notebook* → *File → Import
  Notebook* → en *Settings*, *Accelerator: GPU T4 x2* e *Internet: On* (sin verificar la cuenta con un telefono
  no deja activar ni la GPU ni Internet) → *Run All*.
- **Nunca** hace falta Colab Pro ni alquilar GPU en la nube.

**Resultados reales, con todas sus salidas** (abrelos para ver de donde sale cada numero):
- `salidas/08_finetuning_after_colab.ipynb`: la clase en Colab, LoRA solo en `q_proj` y `v_proj`, 5 epocas → **0 de 6**.
- `salidas/08_finetuning_after_kaggle.ipynb`: este mismo notebook (receta reforzada) en Kaggle → **6 de 6** en formato.
- `salidas/08_finetuning_after_colab_receta.ipynb`: el mismo notebook en Colab → **6 de 6** tambien (56 s).
- `salidas/ejercicio1_after_colab_clase.ipynb`: el ejercicio 1 con la configuracion de clase (q_proj y v_proj) → 0 de 4 formales. La solucion de `soluciones/` ya trae la receta reforzada.
Colab y Kaggle dan la misma GPU (T4): lo que cambia el resultado son los 4 mandos, no la plataforma.

**Como se entrega:** el `.ipynb` ejecutado, con todas sus salidas (Colab: *Archivo → Descargar → Descargar .ipynb*;
Kaggle: *File → Download Notebook*), subido a la plataforma del master. Sin salidas no se puede corregir.

Sin GPU (por ejemplo en tu portatil), el notebook entra en **modo prueba**: usa un modelo diminuto
(SmolLM2-135M) y solo 2 pasos de entrenamiento, para comprobar que el codigo funciona. No aprende nada util.

## Que hace el notebook
| Paso | Que hace |
|---|---|
| 1 · Dataset | 30 ejemplos pregunta-respuesta en JSONL, todos con el mismo formato, y 6 preguntas de prueba aparte |
| 2 · QLoRA | Carga el modelo cuantizado a 4 bits (bitsandbytes) y mide la memoria; variacion: 16 bits frente a 4 bits |
| 3 · LoRA | `LoraConfig(r=8, lora_alpha=16, target_modules="all-linear")`, 10 epocas: menos del 1 % de parametros entrenables; el loss bajando |
| 4 · Probar | Las 6 preguntas de prueba al modelo base y al ajustado: cuantas cumplen el formato. Variacion: un dato que el modelo no sabe |

**Lo que paso en clase (resultado real, Colab T4):** una primera configuracion (LoRA solo en `q_proj` y `v_proj`,
r=16, 5 epocas, lr 2e-4) entreno el 0,14 % del modelo en 25 s, pero el loss solo bajo de 3,26 a 2,16 y el modelo
**no aprendio el formato** (0 de 6 antes y despues). El notebook trae la receta reforzada (todas las capas lineales,
10 epocas, lr 3e-4): no se ejecuto en clase, pero despues, en Kaggle, saco **6 de 6** en formato
(`salidas/08_finetuning_after_kaggle.ipynb`), con frases que a veces no tienen sentido. Lo que si salio claro: el modelo ajustado se inventa datos
("20 dias de vacaciones en Espana"): el fine-tuning pone la forma, el RAG pone los datos.
| 4 · Fusionar | `merge_and_unload()`: el adapter (pocos MB) y el modelo fusionado (GB) |
| 5 · Cierre | Fine-tuning cambia COMO habla el modelo; RAG cambia QUE sabe |

## Archivos
| Archivo | Que es |
|---|---|
| `08_finetuning.ipynb` | El notebook de la clase, con comentarios didacticos (para Colab o Kaggle) |
| `datos/nexa_formato.jsonl` | El dataset: 30 ejemplos (el notebook lo crea solo, no hace falta subirlo) |
| `datos/preguntas_prueba.json` | Las 6 preguntas de prueba |
| `prueba_local.py` | Las mismas celdas en un script, para probar el codigo sin GPU (modo prueba) |
| `soluciones/` | Ejercicio 1 (tono formal con LoRA) y ejercicio 2 (multimodal, PESADO: en Colab gratis no llego a terminar; usa Kaggle) |
| `requirements.txt` | Para ejecutarlo fuera de Colab |

## Conceptos en una linea
- **LoRA:** congelar el modelo y entrenar solo unas matrices pequenas (el adapter). Menos del 1 % de los parametros.
- **Rank (r) y alpha:** la capacidad del adapter y cuanto se nota. Para tono y formato, r=8 o 16 y alpha = 2 x r.
- **QLoRA:** cuantizar el modelo a 4 bits y aplicar LoRA encima: modelos serios en una GPU gratuita.
- **Merge:** fusionar el adapter con el modelo para desplegarlo como un modelo normal.
- **Fine-tuning o RAG:** estilo y formato → fine-tuning; datos frescos o privados → RAG; en produccion, los dos.
