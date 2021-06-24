# David Valverde Gómez
# Ingeniería Informática - ULL
# alu0101100296@ull.edu.es
# Trabajo de Fin de Grado
# Generación automática de textos utilizando el modelo GPT-2 de OpenAI

# Fichero con las funciones necesarias para la descarga, entrenamiento
# y ejecución del modelo

# Se indican las GPUs a utilizar durante la ejecución
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "0, 1, 2"

# El módulo gpt_2_simple proporciona muchas facilidades al interactuar con GPT-2
import gpt_2_simple as gpt2
import requests
import sys


# Variables de configuración para el entrenamiento
number_of_steps = 2000        # Número de pasos
restore = 'latest'            # (latest / fresh) Indica si se quiere comenzar el entrenamiento desde el último punto de control o desde cero
steps_for_print = 10          # Cada cuántos pasos se muestra el progreso
steps_for_sample = 200        # Cada cuántos pasos de muestra un ejemplo de ejecución
steps_for_save = 200          # Cada cuántos pasos se guarda el modelo


# Se descarga la versión del modelo indicada, si no se ha descargado ya
def download_model(model_name):
  if not os.path.isdir(os.path.join("models", model_name)):
    print("Downloading " + model_name + " model...")
    gpt2.download_gpt2(model_name=model_name)   # El modelo se guarda en ./models/1558M/
  else:
    print('Model has already been downloaded')

# Se entrena el modelo con el fichero y la configuración indicadas
def train(model_name, filename, path_to_file):
  # Se inicia una sesión de tensorflow
  sess = gpt2.start_tf_sess()
  gpt2.finetune(sess,
                run_name=filename,
                dataset=path_to_file,
                model_name=model_name,
                steps=number_of_steps,             
                restore_from=restore,   
                print_every=steps_for_print,   
                sample_every=steps_for_sample,   
                save_every=steps_for_save       
                )   

# Se ejecuta el modelo
def execute(filename, words, prefix=None):
  sess = gpt2.start_tf_sess()
  # Se carga el checkpoint correspondiente y se ejecuta
  gpt2.load_gpt2(sess, run_name=filename)
  text = gpt2.generate(sess, run_name=filename, return_as_list=True, prefix=prefix)[0]

  # Se separa el texto obtenido en líneas y cada línea en palabras, con el fin de seleccionar las 
  # 'words' primeras palabras
  lineas = text.splitlines()
  palabras = []
  for i in range(len(lineas)):
    palabras.append(lineas[i].split())

  # Se almacenan el número de palabras seleccionado, añadiendo el salto de línea correspondiente entre
  # cambios de línea
  word_count = 0
  texto_final = []
  # La variable palabras es un vector donde cada elemento es un vector de palabras relativas a una línea
  for i in range(len(palabras)):
    for j in range(len(palabras[i])):
      texto_final.append(palabras[i][j])
      word_count += 1
      if word_count == words:
        break
    texto_final[len(texto_final)-1] += '\n'
    if word_count == words:
        break

  text = ' '.join(texto_final)

  sess.close()
  return text