# Changelog

Todos los cambios notables de este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.2] - 2025-10-18

**Autores:** Felipe Rangel, Nicolás Torres, Jorge

### Añadido
- **Tercer Autor**: Jorge agregado como coautor del proyecto
- **Actualización de Versión**: Incremento a versión 1.1.2

### Mejorado
- **Reconocimiento de Autores**: Los tres autores correctamente registrados en todos los archivos
- **Consistencia de Información**: Autores actualizados en toda la documentación

## [1.1.0] - 2025-10-18

**Autores:** Felipe Rangel, Nicolás Torres, Jorge

### Añadido
- **Documentación Organizada**: Carpeta `docs/` con toda la documentación técnica
- **Guía Completa para Dashboards**: `GUIA_DASHBOARD_GITHUB_PAGES.md` con proceso paso a paso
- **Instrucciones para Cursor AI**: `INSTRUCCIONES_CURSOR_AI.md` con prompt específico
- **Resumen de Solución 404**: `RESUMEN_SOLUCION_404.md` con problema y solución documentados
- **Documentación de GitHub**: Guías completas para configuración y GitHub Pages
- **Índices de Navegación**: `README.md` y `INDICE_TECNICO.md` para fácil acceso
- **Templates Listos**: Configuraciones y prompts listos para futuros proyectos

### Mejorado
- **Organización del Proyecto**: Documentación separada y organizada
- **Accesibilidad**: Fácil navegación entre diferentes tipos de documentación
- **Reutilización**: Templates y guías para proyectos futuros
- **Troubleshooting**: Soluciones documentadas para problemas comunes

### Solucionado
- **Error 404 en GitHub Pages**: Problema completamente documentado y solucionado
- **Archivos HTML ignorados**: Configuración correcta de `.gitignore` documentada
- **Proceso de publicación**: Guía completa para evitar errores futuros

## [1.0.0] - 2025-10-18

**Autores:** Felipe Rangel, Nicolás Torres, Jorge

### Añadido
- **Dashboard ECG Interactivo**: Visualización completa de 28 atletas de resistencia noruegos
- **Análisis de 12 Derivaciones**: Visualización interactiva de todas las derivaciones ECG con explicaciones educativas
- **Análisis Temporal**: Comparación señal cruda vs filtrada con detección automática de picos R
- **Análisis Espectral (FFT)**: Transformada de Fourier con normalización correcta para cada derivación
- **Análisis HRV**: Variabilidad de frecuencia cardíaca con métricas SDNN y RMSSD
- **Análisis Comparativo**: Comparación entre todos los atletas con estadísticas agregadas
- **Tabla de Diagnósticos**: Comparación entre algoritmo SL12 y evaluación de cardiólogo
- **Técnicas del Semestre Implementadas**:
  - FFT con `scipy.fft.fft()` y normalización correcta
  - Filtrado digital Butterworth paso-banda (0.5-40 Hz)
  - Detección automática de picos R con `scipy.signal.find_peaks()`
  - Análisis HRV en dominio tiempo y frecuencia
  - Normalización y preprocesamiento de señales
  - Análisis estadístico con curtosis
- **Visualizaciones Interactivas**: Dashboard HTML con Plotly completamente funcional
- **Documentación Educativa**: Explicaciones detalladas para cada técnica y visualización
- **Ambiente Virtual**: Configuración completa con `requirements.txt`
- **README.md**: Instrucciones completas de uso e instalación

### Características Técnicas
- **Frecuencia de muestreo**: 500 Hz
- **Duración de registro**: 10 segundos
- **Total de registros**: 28 atletas de resistencia
- **Derivaciones**: 12 derivaciones estándar (I, II, III, aVR, aVL, aVF, V1-V6)
- **Técnicas aplicadas**: 6 técnicas principales del semestre de procesamiento de señales biológicas

### Hallazgos Principales
- **Frecuencia cardíaca promedio**: 57.3 BPM (bradicardia sinusal típica en atletas)
- **HRV SDNN promedio**: 60.6 ms (buena variabilidad cardiovascular)
- **HRV RMSSD promedio**: 67.3 ms (excelente condición cardiovascular)
- **Prevalencia de bradicardia sinusal**: Característica común en atletas de resistencia
- **Concordancia diagnóstica**: Evaluación entre algoritmo SL12 y cardiólogo experto
