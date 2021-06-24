# David Valverde Gómez
# Ingeniería Informática - ULL
# alu0101100296@ull.edu.es
# Trabajo de Fin de Grado
# Generación automática de textos utilizando el modelo GPT-2 de OpenAI

# Este fichero contiene la ejecución para descargar la versión indicada
# del modelo GPT-2, realizar un entrenamiento sobre dicho modelo con ficheros de datos
# pasados por argumento y ejecutar modelos ya entrenados

# Se indican las GPUs a utilizar durante la ejecución
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "0, 1, 2"

# El módulo gpt_2_simple proporciona muchas facilidades al interactuar con GPT-2
import gpt_2_simple as gpt2
import requests
import sys

# Se importan las funciones necesarias
from main_functions import *

# Versión del modelo a descargar
model_name = "1558M"

# Directorios con los archivos de entrenamiento y los modelos ya entrenados (checkpoints)
files_directory = 'ficheros_datos/'
checkpoints_directory = 'checkpoint/'

# Archivo concreto a utilizar para el entrenamiento
filename = sys.argv[1] 
path_to_file = files_directory + filename + '.txt'

# El modelo va a tener el mismo nombre que el archivo utilizado para su entrenamiento
#checkpoint = checkpoints_directory + filename 

# Indicador de si se desea entrenar o ejecutar el modelo
train_or_execute = int(sys.argv[2]) # 1 - Entrenar, 2 - Ejecutar, 0 - Ambos

# Se comprueba que los argumentos introducidos son los indicados
def check_arguments():
  # Se revisan las opciones de entrenamiento, ejecución o ambas
  if train_or_execute != 0 and train_or_execute != 1 and train_or_execute != 2:
    raise Exception ('\nSe requiere un segundo argumento para indicar si se desea entrenar o ejecutar el modelo:\n1 - Entrenar\n2 - Ejecutar\0- Ambos')

  # Si se va a entrenar el modelo, se verifica que el archivo indicado se encuentre en el directorio correspondiente
  elif train_or_execute == 0 or train_or_execute == 1:
    files_for_training = os.listdir(files_directory)
    if filename + '.txt' not in files_for_training:
      raise Exception ('\nError. Se intenta entrenar el modelo con un archivo que no existe en ' + files_directory)

  # Si se va a ejecutar, se revisa que se tenga el checkpoint indicado
  else: 
    checkpoints = os.listdir(checkpoints_directory)
    if filename not in checkpoints:
      raise Exception('\nError. Se intenta ejecutar un modelo que no existe en ' + checkpoints_directory)

# Función principal
def main():
  try:
    check_arguments()
    download_model(model_name)

    if train_or_execute == 0 or train_or_execute == 1:
      train(model_name, filename, path_to_file)
    if train_or_execute == 0 or train_or_execute == 2:
      text = execute(filename)
      print(text)
  
  except Exception as e:
    print(str(e))


if __name__ == '__main__':
  main()

