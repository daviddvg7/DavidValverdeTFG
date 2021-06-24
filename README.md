# **Trabajo de Fin de Grado**
# **Generación automática de textos con GPT-2**
## **David Valverde Gómez**

### **Directorios**
* **src** -> Código fuente
* **ficheros_datos** -> Ficheros con los que se entrenaron los modelos


### **Guía de ejecución**
* Para activar el bot de Telegram, debe ejecutarse el fichero **bot_telegram.py** con la versión **3.6** de Python
* Para entrenar o ejecutar un modelo, debe ejecutarse el fichero **train_or_execute.py** con la versión **3.6** de Python. Este programa recibe dos parámetros: 
  * El nombre del modelo a ejecutar, que suele coincidir con el nombre del fichero de entrenamiento correspondiente
  * Un número que indica la operación a realizar:
    * 1 - Entrenamiento
    * 2 - Ejecución
    * 0 - Ambos
