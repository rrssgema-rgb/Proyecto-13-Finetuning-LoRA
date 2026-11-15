# 0 · Instalar las librerias (en Colab ya vienen torch y transformers; anadimos el resto)
import importlib.util, importlib.metadata, subprocess, sys
faltan = [p for p in ("peft", "bitsandbytes", "datasets", "accelerate") if importlib.util.find_spec(p) is None]
if faltan:
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", *faltan], check=False)
# Colab trae de serie una version antigua de torchao que hace fallar a peft al fusionar el adapter. No la usamos: fuera.
try:
    v = importlib.metadata.version("torchao")
    if tuple(int(x) for x in v.split(".")[:2]) < (0, 16):
        subprocess.run([sys.executable, "-m", "pip", "uninstall", "-y", "-q", "torchao"], check=False)
        print(f"torchao {v} desinstalado (incompatible con peft)")
except importlib.metadata.PackageNotFoundError:
    pass
print("Librerias listas")

EJEMPLOS = [
 {
  "instruccion": "¿Cómo pido las vacaciones?",
  "respuesta": "Las vacaciones se piden en el portal del empleado\n- Entra en el portal, apartado Ausencias, y elige las fechas.\n- Tu responsable recibe un aviso y las aprueba o te propone otras.\n- Pídelas con antelación, sobre todo en verano y Navidad.\n— Equipo de Personas de Nexa"
 },
 {
  "instruccion": "Me he puesto malo, ¿qué hago?",
  "respuesta": "Si estás enfermo, avisa y cuídate\n- Avisa a tu responsable lo antes posible, por teléfono o por el chat.\n- Si vas al médico, sube el justificante o la baja al portal del empleado.\n- Si la baja se alarga, Personas te explicará los siguientes pasos.\n— Equipo de Personas de Nexa"
 },
 {
  "instruccion": "¿Puedo teletrabajar mañana?",
  "respuesta": "El teletrabajo se acuerda con tu responsable\n- Revisa los días de oficina que tiene fijados tu equipo.\n- Si quieres cambiar un día, pídelo a tu responsable con tiempo.\n- Deja constancia del cambio en el calendario compartido del equipo.\n— Equipo de Personas de Nexa"
 },
 {
  "instruccion": "Se me ha roto el portátil",
  "respuesta": "Un portátil roto se gestiona con IT\n- Abre una incidencia en el portal de IT con una foto del daño.\n- Guarda tu trabajo en la nube si todavía puedes encenderlo.\n- IT te dirá si lo reparan o te dan un equipo de sustitución.\n— Equipo de Personas de Nexa"
 },
 {
  "instruccion": "No me acuerdo de mi contraseña",
  "respuesta": "La contraseña se restablece tú mismo\n- Usa la opción ¿Has olvidado tu contraseña? en la pantalla de inicio.\n- Recibirás un código en el móvil que tienes registrado.\n- Si no te llega, llama a la extensión de IT y te la resetean.\n— Equipo de Personas de Nexa"
 },
 {
  "instruccion": "¿Cómo paso los gastos de un viaje?",
  "respuesta": "Los gastos de viaje se liquidan en la app de gastos\n- Haz una foto de cada ticket en el momento, antes de perderlo.\n- Súbelos a la app indicando el proyecto al que se cargan.\n- Tu responsable los aprueba y se pagan con la siguiente nómina.\n— Equipo de Personas de Nexa"
 },
 {
  "instruccion": "La VPN no me conecta",
  "respuesta": "Si la VPN falla, prueba estos pasos\n- Comprueba que tienes internet sin la VPN y reinicia el cliente.\n- Actualiza el cliente de VPN desde el portal de software.\n- Si sigue sin conectar, abre una incidencia en el portal de IT.\n— Equipo de Personas de Nexa"
 },
 {
  "instruccion": "¿Dónde veo mi nómina?",
  "respuesta": "Tu nómina está en el portal del empleado\n- Entra en el apartado Documentos y busca Nóminas.\n- Puedes descargar las de meses anteriores en PDF.\n- Si ves un error, escribe a Personas con el mes y el concepto.\n— Equipo de Personas de Nexa"
 },
 {
  "instruccion": "Quiero hacer un curso de formación",
  "respuesta": "La formación se solicita en el catálogo interno\n- Busca el curso en el catálogo del portal de formación.\n- Si no está, envía una propuesta a Personas con el enlace y el precio.\n- Coméntalo antes con tu responsable para encajarlo con el trabajo.\n— Equipo de Personas de Nexa"
 },
 {
  "instruccion": "Me caso, ¿tengo días libres?",
  "respuesta": "Enhorabuena: tienes un permiso por matrimonio\n- Solicítalo en el portal del empleado, apartado Permisos.\n- Adjunta el certificado cuando lo tengas.\n- Si tienes dudas sobre la duración, Personas te lo confirma.\n— Equipo de Personas de Nexa"
 },
 {
  "instruccion": "¿Cómo cambio mi cuenta bancaria?",
  "respuesta": "La cuenta bancaria se cambia en tus datos personales\n- Entra en el portal del empleado, apartado Mis datos.\n- Introduce el nuevo IBAN y adjunta un certificado del banco.\n- El cambio se aplica a partir de la nómina siguiente.\n— Equipo de Personas de Nexa"
 },
 {
  "instruccion": "Necesito un certificado de empresa",
  "respuesta": "Los certificados los emite Personas\n- Pídelo en el portal del empleado, apartado Solicitudes.\n- Indica para qué lo necesitas: banco, alquiler, visado…\n- Te llegará firmado por correo en unos días.\n— Equipo de Personas de Nexa"
 },
 {
  "instruccion": "Voy a ser padre",
  "respuesta": "Enhorabuena: te ayudamos con el permiso\n- Avisa a tu responsable y a Personas con la fecha prevista.\n- Personas te explicará cómo solicitar el permiso y la documentación.\n- Organiza con tu equipo el reparto de tareas antes de irte.\n— Equipo de Personas de Nexa"
 },
 {
  "instruccion": "¿Qué hago si tengo un accidente en el trabajo?",
  "respuesta": "Ante un accidente, lo primero es tu salud\n- Si es grave, llama al 112; si es leve, acude a la mutua.\n- Avisa a tu responsable y a Personas en cuanto puedas.\n- Personas tramitará el parte de accidente contigo.\n— Equipo de Personas de Nexa"
 },
 {
  "instruccion": "No me funciona el correo en el móvil",
  "respuesta": "El correo en el móvil se configura con la app corporativa\n- Instala la app corporativa desde la tienda de aplicaciones.\n- Inicia sesión con tu usuario y aprueba el aviso de seguridad.\n- Si no aparece el correo, abre una incidencia en el portal de IT.\n— Equipo de Personas de Nexa"
 },
 {
  "instruccion": "¿Puedo usar mi coche para un viaje?",
  "respuesta": "Puedes usar tu coche y pedir el kilometraje\n- Anota el origen, el destino y los kilómetros del viaje.\n- Registra el desplazamiento en la app de gastos con el proyecto.\n- Guarda los tickets de peaje y parking para adjuntarlos.\n— Equipo de Personas de Nexa"
 },
 {
  "instruccion": "Quiero cambiar de horario",
  "respuesta": "Los cambios de horario se hablan con tu responsable\n- Explica a tu responsable qué horario necesitas y por qué.\n- Si hay acuerdo, Personas lo registra en tu ficha.\n- Revisa cómo afecta a las reuniones fijas de tu equipo.\n— Equipo de Personas de Nexa"
 },
 {
  "instruccion": "Me han llegado muchos correos raros",
  "respuesta": "Ante correos sospechosos, no hagas clic\n- No abras enlaces ni adjuntos de remitentes que no conoces.\n- Usa el botón Reportar phishing de tu correo.\n- Si ya has hecho clic, avisa a IT inmediatamente.\n— Equipo de Personas de Nexa"
 },
 {
  "instruccion": "¿Cómo reservo una sala?",
  "respuesta": "Las salas se reservan desde el calendario\n- Crea la reunión en tu calendario y añade la sala como invitado.\n- Si la sala está ocupada, el calendario te propone otra libre.\n- Libera la reserva si al final no la usas.\n— Equipo de Personas de Nexa"
 },
 {
  "instruccion": "Necesito una pantalla para casa",
  "respuesta": "El material de teletrabajo se pide a IT\n- Haz la solicitud en el portal de IT, apartado Material.\n- Indica el tipo de pantalla y tu dirección de entrega.\n- IT te confirmará si hay stock o cuándo llega.\n— Equipo de Personas de Nexa"
 },
 {
  "instruccion": "¿Cuándo cobro este mes?",
  "respuesta": "La fecha de cobro está en tu nómina\n- Revisa la fecha de pago en el portal del empleado.\n- Si cae en festivo, se adelanta al día hábil anterior.\n- Si no has cobrado en la fecha, escribe a Personas.\n— Equipo de Personas de Nexa"
 },
 {
  "instruccion": "Quiero pedir un adelanto",
  "respuesta": "Los adelantos de nómina se solicitan a Personas\n- Envía la solicitud desde el portal del empleado, apartado Solicitudes.\n- Indica el importe y el motivo, que es confidencial.\n- Personas te responderá con las condiciones.\n— Equipo de Personas de Nexa"
 },
 {
  "instruccion": "Me voy a mudar de casa",
  "respuesta": "Si te mudas, actualiza tus datos\n- Cambia tu dirección en el portal del empleado, apartado Mis datos.\n- Si teletrabajas, avisa a IT para el envío de material.\n- Comprueba si tienes un día de permiso por traslado de domicilio.\n— Equipo de Personas de Nexa"
 },
 {
  "instruccion": "No puedo acceder a una carpeta compartida",
  "respuesta": "Los permisos de carpetas los da su responsable\n- Pide acceso desde el propio enlace de la carpeta.\n- El responsable de la carpeta recibirá tu solicitud.\n- Si es urgente y no responde, abre una incidencia en IT.\n— Equipo de Personas de Nexa"
 },
 {
  "instruccion": "¿Hay seguro médico en la empresa?",
  "respuesta": "El seguro médico se gestiona en Beneficios\n- Consulta las condiciones en el portal, apartado Beneficios.\n- Puedes darte de alta o dar de alta a tu familia desde allí.\n- Para dudas concretas, escribe a Personas.\n— Equipo de Personas de Nexa"
 },
 {
  "instruccion": "Quiero instalar un programa",
  "respuesta": "El software se instala desde el portal de software\n- Busca el programa en el portal de software corporativo.\n- Si no está, pide a IT que lo revise y lo autorice.\n- No instales programas descargados de internet por tu cuenta.\n— Equipo de Personas de Nexa"
 },
 {
  "instruccion": "Tengo que ir al médico por la mañana",
  "respuesta": "Para ir al médico, avisa y justifica\n- Avisa a tu responsable con antelación.\n- Registra la ausencia en el portal del empleado.\n- Sube el justificante de la cita al volver.\n— Equipo de Personas de Nexa"
 },
 {
  "instruccion": "¿Cómo me doy de alta en el plan de pensiones?",
  "respuesta": "El plan de pensiones está en Beneficios\n- Entra en el portal del empleado, apartado Beneficios.\n- Elige la aportación y acepta las condiciones.\n- Personas te confirmará el alta por correo.\n— Equipo de Personas de Nexa"
 },
 {
  "instruccion": "Me quiero ir de la empresa",
  "respuesta": "Si decides irte, te acompañamos en el proceso\n- Comunícalo primero a tu responsable.\n- Envía la carta de baja voluntaria a Personas.\n- Personas te explicará el preaviso y la liquidación.\n— Equipo de Personas de Nexa"
 },
 {
  "instruccion": "El ordenador va muy lento",
  "respuesta": "Si el ordenador va lento, prueba esto primero\n- Reinicia el equipo y cierra los programas que no uses.\n- Instala las actualizaciones pendientes.\n- Si sigue lento, abre una incidencia en IT con una captura.\n— Equipo de Personas de Nexa"
 }
]

PRUEBA = [
 "Se me ha olvidado fichar esta mañana",
 "¿Cómo pido un día de asuntos propios?",
 "Mi jefe no me aprueba los gastos",
 "No funciona la impresora de la oficina",
 "Quiero trabajar desde otra ciudad un mes",
 "Me he dejado el portátil en el tren"
]

import json
with open("nexa_formato.jsonl", "w", encoding="utf-8") as f:
    for e in EJEMPLOS:
        f.write(json.dumps(e, ensure_ascii=False) + "\n")
print(f"{len(EJEMPLOS)} ejemplos guardados en nexa_formato.jsonl · {len(PRUEBA)} preguntas de prueba aparte\n")
for e in EJEMPLOS[:2]:
    print("PREGUNTA :", e["instruccion"])
    print("RESPUESTA:", e["respuesta"].replace("\n", "\n           "), "\n")

# El formato que queremos ensenar, escrito como una comprobacion con codigo
FIRMA = "— Equipo de Personas de Nexa"

def cumple_formato(texto: str) -> bool:
    lineas = [l.strip() for l in texto.strip().split("\n") if l.strip()]
    return (len(lineas) == 5 and not lineas[0].startswith("-")
            and all(l.startswith("- ") for l in lineas[1:4]) and lineas[4] == FIRMA)

print("Los 30 ejemplos cumplen el formato:", all(cumple_formato(e["respuesta"]) for e in EJEMPLOS))

import time, torch
from transformers import AutoModelForCausalLM, AutoTokenizer

GPU = torch.cuda.is_available()
MODELO = "Qwen/Qwen2.5-1.5B-Instruct" if GPU else "HuggingFaceTB/SmolLM2-135M-Instruct"
print("GPU:", torch.cuda.get_device_name(0) if GPU else "no hay GPU -> MODO PRUEBA (modelo diminuto, 2 pasos)")

tok = AutoTokenizer.from_pretrained(MODELO)
tok.pad_token = tok.pad_token or tok.eos_token
t0 = time.time()
if GPU:
    from transformers import BitsAndBytesConfig
    config_4bit = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4",
                                     bnb_4bit_compute_dtype=torch.float16, bnb_4bit_use_double_quant=True)
    modelo = AutoModelForCausalLM.from_pretrained(MODELO, quantization_config=config_4bit, device_map="auto")
else:
    modelo = AutoModelForCausalLM.from_pretrained(MODELO)
print(f"Modelo: {MODELO}")
print(f"Cargado en {time.time() - t0:.0f} s · ocupa {modelo.get_memory_footprint() / 1e9:.2f} GB en memoria")
if GPU:
    print(f"Memoria de la GPU en uso: {torch.cuda.memory_allocated() / 1e9:.2f} GB de {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")

if GPU:
    m16 = AutoModelForCausalLM.from_pretrained(MODELO, torch_dtype=torch.float16, device_map="auto")
    gb16, gb4 = m16.get_memory_footprint() / 1e9, modelo.get_memory_footprint() / 1e9
    print(f"16 bits: {gb16:.2f} GB · 4 bits: {gb4:.2f} GB · {gb16 / gb4:.1f} veces menos")
    del m16; torch.cuda.empty_cache()
else:
    print("(solo con GPU)")

from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training

# Antes de tocar nada, guardamos lo que contesta el modelo BASE a las preguntas de prueba
def responder(m, pregunta, max_tokens=None):
    # return_dict=True: funciona igual con transformers 4.x y 5.x (en la 5.x ya no devuelve solo los ids)
    enc = tok.apply_chat_template([{"role": "user", "content": pregunta}], add_generation_prompt=True,
                                  return_tensors="pt", return_dict=True).to(m.device)
    with torch.no_grad():
        out = m.generate(**enc, max_new_tokens=max_tokens or (160 if GPU else 40), do_sample=False,
                         pad_token_id=tok.pad_token_id)
    return tok.decode(out[0][enc["input_ids"].shape[1]:], skip_special_tokens=True).strip()

preguntas = PRUEBA if GPU else PRUEBA[:2]
antes = {p: responder(modelo, p) for p in preguntas}
print(f"Respuestas del modelo base guardadas ({len(antes)})")

if GPU:
    modelo = prepare_model_for_kbit_training(modelo)
config_lora = LoraConfig(r=8, lora_alpha=16, lora_dropout=0.05, bias="none", task_type="CAUSAL_LM",
                         target_modules="all-linear")     # atencion (q, k, v, o) y MLP (gate, up, down)
modelo = get_peft_model(modelo, config_lora)
modelo.print_trainable_parameters()

# Los parametros del adapter crecen en proporcion al rank (cada matriz tiene r filas o r columnas)
entrenables, todos = modelo.get_nb_trainable_parameters()     # peft ya descuenta el empaquetado de 4 bits
base = todos - entrenables
print(f"{'rank':>5}{'parametros entrenables':>25}{'% del modelo':>15}{'adapter en disco':>19}")
for r in (4, 8, 16, 64):
    n = entrenables * r // 8
    print(f"{r:>5}{n:>25,}{100 * n / (base + n):>14.3f}%{n * 4 / 1e6:>16.1f} MB")

# Tokenizar: el modelo solo aprende de la RESPUESTA (las etiquetas de la pregunta se ponen a -100)
from datasets import Dataset

def preparar(e):
    prompt = tok.apply_chat_template([{"role": "user", "content": e["instruccion"]}], add_generation_prompt=True, tokenize=False)
    completo = tok.apply_chat_template([{"role": "user", "content": e["instruccion"]},
                                        {"role": "assistant", "content": e["respuesta"]}], tokenize=False)
    n_prompt = len(tok(prompt, add_special_tokens=False)["input_ids"])
    ids = tok(completo, add_special_tokens=False)["input_ids"]
    return {"input_ids": ids, "attention_mask": [1] * len(ids), "labels": [-100] * n_prompt + ids[n_prompt:]}

ds = Dataset.from_list(EJEMPLOS).map(preparar, remove_columns=["instruccion", "respuesta"])
print(f"{len(ds)} ejemplos tokenizados · el mas largo tiene {max(len(x) for x in ds['input_ids'])} tokens")

from transformers import Trainer, TrainingArguments, DataCollatorForSeq2Seq

args = TrainingArguments(output_dir="entrenamiento", num_train_epochs=10, per_device_train_batch_size=4,
                         learning_rate=3e-4, logging_steps=4 if GPU else 1, save_strategy="no", report_to="none",
                         fp16=GPU, max_steps=-1 if GPU else 2, optim="adamw_torch")
trainer = Trainer(model=modelo, args=args, train_dataset=ds,
                  data_collator=DataCollatorForSeq2Seq(tok, padding=True, label_pad_token_id=-100))
t0 = time.time()
trainer.train()
print(f"\nEntrenamiento: {time.time() - t0:.0f} s")
print(f"{'paso':>6}{'epoca':>8}{'loss':>9}")
for h in trainer.state.log_history:
    if "loss" in h:
        print(f"{h['step']:>6}{h['epoch']:>8.1f}{h['loss']:>9.3f}")

modelo.eval()
despues = {p: responder(modelo, p) for p in preguntas}
ok_antes = sum(cumple_formato(antes[p]) for p in preguntas)
ok_despues = sum(cumple_formato(despues[p]) for p in preguntas)
print(f"Cumplen el formato de Nexa · BASE: {ok_antes}/{len(preguntas)} · AJUSTADO: {ok_despues}/{len(preguntas)}\n")
for p in preguntas:
    print(f"  {'OK' if cumple_formato(antes[p]) else '--'} base · {'OK' if cumple_formato(despues[p]) else '--'} ajustado · {p}")
print()
for p in preguntas[:2]:
    print("=" * 90); print("PREGUNTA:", p)
    print("-- BASE --------------------------------------------------------------------------------")
    print(antes[p])
    print("-- AJUSTADO con LoRA ------------------------------------------------------------------")
    print(despues[p])

dato = "¿Cuántos días de vacaciones tengo al año?"
print("PREGUNTA:", dato, "\n")
print(responder(modelo, dato))
print("\n(En el manual de Nexa son 23 dias laborables. Si el numero no coincide, lo ha inventado: eso lo arregla el RAG.)")

import os, shutil
from peft import PeftModel

modelo.save_pretrained("adapter_nexa"); tok.save_pretrained("adapter_nexa")
mb = os.path.getsize(os.path.join("adapter_nexa", "adapter_model.safetensors")) / 1e6    # solo los pesos del adapter
print(f"Adapter guardado en adapter_nexa/ · sus pesos ocupan {mb:.1f} MB")

base16 = AutoModelForCausalLM.from_pretrained(MODELO, torch_dtype=torch.float16 if GPU else torch.float32,
                                              device_map="auto" if GPU else None)
fusionado = PeftModel.from_pretrained(base16, "adapter_nexa").merge_and_unload()
fusionado.save_pretrained("modelo_nexa_fusionado"); tok.save_pretrained("modelo_nexa_fusionado")
gb = sum(os.path.getsize(os.path.join("modelo_nexa_fusionado", f)) for f in os.listdir("modelo_nexa_fusionado")) / 1e9
print(f"Modelo fusionado guardado en modelo_nexa_fusionado/ · {gb:.2f} GB")
print("El modelo fusionado cumple el formato:", cumple_formato(responder(fusionado, preguntas[0])))
shutil.make_archive("adapter_nexa", "zip", "adapter_nexa")
print("adapter_nexa.zip listo para descargar")

# Resumen de la ejecucion (lo usamos para las capturas de clase)
resumen = {"modelo": MODELO, "gpu": torch.cuda.get_device_name(0) if GPU else None,
           "formato_antes": f"{ok_antes}/{len(preguntas)}", "formato_despues": f"{ok_despues}/{len(preguntas)}",
           "adapter_mb": round(mb, 1), "fusionado_gb": round(gb, 2)}
json.dump({"resumen": resumen, "antes": antes, "despues": despues}, open("resultados.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print(json.dumps(resumen, ensure_ascii=False, indent=1))
