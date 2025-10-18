# Dashboard ECG - Atletas de Resistencia Noruegos

**Versión:** 1.1.0 | **Autores:** Felipe Rangel, Nicolás Torres | **Última actualización:** Octubre 2025

## 🌐 Ver Dashboard en Línea

**¡El dashboard está disponible en GitHub Pages!**

🔗 **[Ver Dashboard Interactivo](https://felirangelp.github.io/norwegian-endurance-athlete-ecg-dashboard/)**

El dashboard incluye:
- ✅ Visualizaciones interactivas de Plotly
- ✅ Análisis de 28 atletas de resistencia
- ✅ 12 derivaciones ECG con explicaciones
- ✅ Análisis temporal, espectral y HRV
- ✅ Comparación diagnóstica SL12 vs Cardiólogo
- ✅ **NUEVO:** Documentación completa organizada en `docs/`

## Descripción del Proyecto

Este proyecto implementa un análisis completo de señales ECG de 28 atletas de resistencia noruegos utilizando técnicas avanzadas de procesamiento de señales biológicas vistas durante el semestre.

## Características Principales

- **Análisis de 28 registros ECG** de atletas de élite
- **12 derivaciones ECG** por cada atleta
- **Técnicas del semestre implementadas:**
  - Transformada Rápida de Fourier (FFT)
  - Filtrado Digital con filtros Butterworth
  - Detección automática de picos R
  - Análisis de Variabilidad de Frecuencia Cardíaca (HRV)
  - Normalización y preprocesamiento
  - Análisis estadístico con curtosis
  - Visualizaciones interactivas con Plotly

## Archivos del Proyecto

```
├── dashboard.html                    # Dashboard interactivo principal
├── requirements.txt                  # Dependencias Python
├── README.md                        # Este archivo
├── src/
│   ├── ecg_processor.py            # Procesador de datos ECG
│   ├── dashboard_generator.py       # Generador de dashboard
│   └── statistical_analysis.py      # Análisis estadístico
└── norwegian-endurance-athlete-ecg-database-1.0.0/
    ├── ath_001.dat/.hea             # Datos del atleta 1
    ├── ath_002.dat/.hea             # Datos del atleta 2
    └── ...                          # Datos de los demás atletas
```

## Instalación y Uso

### 1. Configurar Ambiente Virtual

```bash
# Crear ambiente virtual
python3 -m venv venv

# Activar ambiente virtual
source venv/bin/activate  # En macOS/Linux
# o
venv\Scripts\activate   # En Windows

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Ejecutar el Análisis

```bash
# Ejecutar análisis completo
python main.py
```

### 3. Ver el Dashboard

1. Abre `dashboard.html` en tu navegador web
2. Explora las visualizaciones interactivas
3. Usa el dropdown para seleccionar diferentes atletas
4. Interactúa con los gráficos (zoom, pan, hover)

## Visualizaciones Incluidas

### 1. Vista General de 12 Derivaciones
- Visualización simultánea de todas las derivaciones ECG
- Interactiva con zoom y pan
- Información detallada en hover

### 2. Análisis Temporal
- Comparación entre señal cruda y filtrada
- Detección automática de picos R
- Marcadores interactivos

### 3. Análisis Espectral (FFT)
- Transformada de Fourier de diferentes derivaciones
- Frecuencias dominantes identificadas
- Análisis de potencia espectral

### 4. Análisis HRV
- Intervalos RR en el tiempo
- Distribución de intervalos RR
- Métricas de variabilidad (SDNN, RMSSD)

### 5. Análisis Comparativo
- Comparación entre todos los atletas
- Distribución de frecuencias cardíacas
- Tabla de diagnósticos SL12 vs Cardiólogo

## Técnicas Implementadas

### A. Transformada Rápida de Fourier (FFT)
- Implementación con `scipy.fft.fft()`
- Normalización correcta según metodología del taller
- Análisis de resolución frecuencial
- Método de Welch para PSD
- Detección de picos espectrales

### B. Filtrado Digital
- Filtros Butterworth paso-banda (0.5-40 Hz)
- Filtro paso-alto (0.5 Hz) para línea base
- Filtro paso-bajo (40 Hz) para ruido
- Filtro notch (50 Hz) para interferencia
- Aplicación con `scipy.signal.filtfilt()`

### C. Detección de Picos R
- Implementación con `scipy.signal.find_peaks()`
- Umbralización adaptativa (3σ)
- Período refractario (200ms)
- Cálculo de frecuencia cardíaca instantánea

### D. Análisis HRV
- Intervalos RR en milisegundos
- SDNN: Desviación estándar de intervalos NN
- RMSSD: Raíz cuadrada de diferencias al cuadrado
- Análisis en dominio de frecuencia

### E. Preprocesamiento
- Centrado de señales (media cero)
- Escalado y estandarización
- Eliminación de artefactos
- Umbralización estadística

### F. Análisis Estadístico
- Curtosis como medida de no-gaussianidad
- Análisis de correlación entre derivaciones
- Medidas de independencia estadística

## Resultados Principales

### Hallazgos Clínicos
- **Bradicardia sinusal:** Adaptación fisiológica común en atletas
- **HRV elevada:** Indicador de buena condición cardiovascular
- **Concordancia diagnóstica:** Evaluación entre algoritmo SL12 y cardiólogo
- **Características espectrales:** Patrones distintivos en análisis FFT

### Implicaciones
- Diferencias significativas entre ECG de atletas y población general
- Necesidad de algoritmos especializados para atletas
- Importancia del análisis de HRV en evaluaciones cardíacas
- Valor del análisis espectral para caracterización

## Datos del Estudio

- **Población:** 28 atletas de resistencia noruegos
- **Edad:** 20-43 años (promedio 25 años)
- **Deportes:** 24 remeros (86%), 2 kayakistas (7%), 2 ciclistas (7%)
- **Entrenamiento:** ~800 horas/año promedio
- **Equipo:** GE MAC VUE 360 electrocardiógrafo
- **Frecuencia de muestreo:** 500 Hz
- **Duración:** 10 segundos por registro

## Dependencias

- `wfdb==4.1.0` - Lectura de archivos ECG
- `numpy==1.24.3` - Procesamiento numérico
- `scipy==1.10.1` - Procesamiento de señales
- `plotly==5.15.0` - Visualizaciones interactivas
- `pandas>=1.0.0,<2.0.0` - Manipulación de datos
- `neurokit2==0.2.4` - Análisis de señales ECG
- `scikit-learn==1.3.0` - Algoritmos de machine learning
- `matplotlib==3.7.2` - Visualizaciones estáticas

## 📚 Documentación Completa

**Nueva en v1.1.0:** Toda la documentación técnica está organizada en la carpeta `docs/`:

- **`docs/README.md`** - Índice principal de documentación
- **`docs/GUIA_DASHBOARD_GITHUB_PAGES.md`** - Guía completa para publicar dashboards
- **`docs/INSTRUCCIONES_CURSOR_AI.md`** - Prompt específico para Cursor AI
- **`docs/RESUMEN_SOLUCION_404.md`** - Solución al error 404 más común
- **`docs/INDICE_TECNICO.md`** - Índice específico para documentación técnica

### 🚀 Para Futuros Proyectos

Copia el prompt completo de `docs/INSTRUCCIONES_CURSOR_AI.md` para crear dashboards sin errores 404.

## Autores

**Felipe Rangel** y **Nicolás Torres**

Proyecto desarrollado como parte del curso de Procesamiento de Señales Biológicas, implementando las técnicas vistas durante el semestre.

## Licencia

Los datos ECG están bajo licencia Creative Commons Attribution 4.0 International Public License.

## Referencias

- Norwegian Endurance Athlete ECG Database
- Técnicas de procesamiento de señales biológicas del curso
- Estándares internacionales para interpretación de ECG en atletas
