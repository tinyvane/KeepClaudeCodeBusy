# Keep Claude Code Busy

> **[中文](README.md) | [English](README_EN.md) | [Français](README_FR.md) | [日本語](README_JA.md) | Español**

Una herramienta de monitoreo de región de pantalla para Windows diseñada para mantener Claude Code trabajando continuamente mientras duermes.

![Versión](https://img.shields.io/badge/versión-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.7+-green.svg)
![Plataforma](https://img.shields.io/badge/plataforma-Windows-lightgrey.svg)
![Licencia](https://img.shields.io/badge/licencia-MIT-orange.svg)

## ✨ Características

- ✅ **Selección Visual de Región** - Dibuja un rectángulo para seleccionar el área de monitoreo
- ✅ **Monitoreo en Tiempo Real** - Detecta cambios en la pantalla mediante comparación de imágenes
- ✅ **Detección Inteligente** - Se activa automáticamente cuando no se detectan cambios durante 30-120 segundos
- ✅ **Mensajería Automática** - Envía comandos a Claude Code automáticamente
- ✅ **Persistencia de Configuración** - Recuerda tu configuración (opcional)
- ✅ **Salida Limpia** - Detén el monitoreo en cualquier momento al despertar
- ✅ **Paquete con Un Clic** - Crea un archivo EXE independiente

## 🚀 Inicio Rápido

### Instalación

1. **Instalar dependencias**:
```bash
install.bat
```
o manualmente:
```bash
pip install -r requirements.txt
```

2. **Ejecutar el programa**:
```bash
python monitor_tool.py
```
o haz doble clic en `run.bat`

### Crear EXE (Recomendado)

```bash
build_onedir.bat
```

El ejecutable estará en `dist/monitor_tool/monitor_tool.exe`

## 📖 Cómo Usar

### Paso 1: Seleccionar Región de Monitoreo

1. Haz clic en el botón "选择区域" (Seleccionar Región)
2. La pantalla se vuelve semitransparente
3. **Arrastra** para dibujar un rectángulo alrededor del área de salida de Claude Code
4. **Presiona Enter** para confirmar (o ESC para cancelar)

### Paso 2: Seleccionar Posición de Clic

1. Después de confirmar la región, la pantalla permanece semitransparente
2. **Haz clic** en la ubicación del campo de entrada de Claude Code
3. **Presiona Enter** nuevamente para confirmar

### Paso 3: Configurar Parámetros

- **Intervalo de Verificación**: Con qué frecuencia verificar cambios (10-60s, predeterminado: 30s)
- **Tiempo de Activación**: Cuánto tiempo sin cambios antes de activarse (30-120s, predeterminado: 45s)
- **Umbral de Similitud**: Rigidez de comparación de imágenes (0.90-0.99, predeterminado: 0.98)
- **Recordar Posición**: Restaurar automáticamente la región en el próximo inicio (casilla de verificación)
- **Mensaje**: Texto a enviar cuando se active (compatible con chino)

### Paso 4: Iniciar Monitoreo

¡Haz clic en el botón "开始监控" (Iniciar Monitoreo) y ve a dormir! 😴

### Paso 5: Detener al Despertar

Haz clic en el botón "停止监控" (Detener Monitoreo) o cierra la ventana.

## 🎯 Cómo Funciona

1. Toma capturas de pantalla de la región monitoreada cada N segundos
2. Compara la captura actual con la anterior
3. Si se detectan cambios → reiniciar temporizador
4. Si NO hay cambios durante M segundos → automáticamente:
   - Hacer clic en el campo de entrada
   - Pegar mensaje usando Ctrl+V (compatible con chino)
   - Presionar Enter para enviar
   - Continuar monitoreando

## ⚙️ Configuración

La configuración se guarda en `monitor_config.json`:
- Coordenadas de la región seleccionada
- Posición de clic
- Intervalo de verificación
- Duración de activación
- Umbral de similitud
- Configuración de recordar posición
- Mensaje personalizado

## 💡 Consejos y Mejores Prácticas

### Selección de Región
- Selecciona el área de salida principal de Claude Code
- Evita áreas con cursores parpadeantes o marcas de tiempo
- La región debe ser lo suficientemente grande (al menos 100x100 píxeles)

### Ajuste de Parámetros
- **¿Demasiado sensible?** → Aumenta el umbral a 0.99 o aumenta el tiempo de activación
- **¿No se activa?** → Disminuye el umbral a 0.95 o reduce el tiempo de activación
- **Para tareas largas** → Establece el tiempo de activación en 60-90 segundos
- **Para respuestas rápidas** → Establece el tiempo de activación en 30-45 segundos

## 🛠️ Stack Tecnológico

- **Python 3.7+**
- **tkinter** - Framework GUI
- **pyautogui** - Captura de pantalla y automatización
- **opencv-python** - Comparación de imágenes
- **Pillow** - Procesamiento de imágenes
- **pyperclip** - Operaciones de portapapeles
- **pywin32** - API de Windows
- **PyInstaller** - Empaquetado EXE

## 🐛 Solución de Problemas

### Problema: El programa no puede encontrar la ventana de Claude Code
**Solución**: Asegúrate de que la ventana esté abierta y visible, no minimizada.

### Problema: La automatización no funciona
**Solución**:
- No muevas el mouse a las esquinas de la pantalla (característica de seguridad de PyAutoGUI)
- Ejecuta como administrador si es necesario
- Asegúrate de que ninguna otra ventana cubra Claude Code

### Problema: Siempre se activa (falsos positivos)
**Solución**:
- Aumenta el tiempo de activación
- Aumenta el umbral de similitud (0.99)
- Vuelve a seleccionar la región sin elementos dinámicos

### Problema: Nunca se activa (falsos negativos)
**Solución**:
- Disminuye el umbral (0.95)
- Verifica si la región está correctamente seleccionada
- Verifica que el monitoreo esté en ejecución (verifica el estado)

## 🤝 Contribución

¡Las contribuciones son bienvenidas! No dudes en enviar un Pull Request.

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT - consulta el archivo [LICENSE](LICENSE) para más detalles.

## ⚠️ Descargo de Responsabilidad

Esta herramienta es solo para uso personal para mejorar la productividad. Úsala responsablemente y de acuerdo con todos los términos de servicio aplicables.

---

Hecho con ❤️ para la comunidad de Claude Code
