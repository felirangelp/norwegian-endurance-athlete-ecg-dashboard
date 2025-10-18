"""
Script Principal - Dashboard ECG Atletas de Resistencia
Ejecuta el análisis completo y genera el dashboard HTML interactivo
"""

import sys
import os
import traceback
from datetime import datetime

# Agregar el directorio src al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def main():
    """
    Función principal que ejecuta todo el análisis y genera el dashboard
    """
    print("="*80)
    print("DASHBOARD ECG - ATLETAS DE RESISTENCIA NORUEGOS")
    print("Análisis de 28 atletas de élite usando técnicas de procesamiento de señales")
    print("="*80)
    print(f"Iniciado: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print()
    
    try:
        # Paso 1: Importar y ejecutar el procesador ECG
        print("🔬 PASO 1: Procesamiento de Datos ECG")
        print("-" * 50)
        
        from ecg_processor import ECGAnalyzer
        
        analyzer = ECGAnalyzer("norwegian-endurance-athlete-ecg-database-1.0.0")
        analyzer.load_all_ecg_data()
        
        print("\n📊 Realizando análisis completo...")
        results = analyzer.analyze_all_records()
        
        print(f"\n✅ Análisis completado:")
        print(f"   • Total de registros procesados: {results['total_records']}")
        print(f"   • Frecuencia cardíaca promedio: {results['summary_statistics']['mean_hr']:.1f} BPM")
        print(f"   • HRV SDNN promedio: {results['summary_statistics']['mean_sdnn']:.1f} ms")
        print(f"   • HRV RMSSD promedio: {results['summary_statistics']['mean_rmssd']:.1f} ms")
        
        # Paso 2: Análisis estadístico y conclusiones
        print("\n\n📈 PASO 2: Análisis Estadístico y Conclusiones")
        print("-" * 50)
        
        from statistical_analysis import ECGStatisticalAnalyzer
        
        stat_analyzer = ECGStatisticalAnalyzer(results)
        conclusions = stat_analyzer.generate_comprehensive_conclusions()
        
        print("✅ Análisis estadístico completado")
        
        # Paso 3: Generar dashboard HTML
        print("\n\n🎨 PASO 3: Generación del Dashboard HTML")
        print("-" * 50)
        
        from dashboard_generator import ECGDashboardGenerator
        
        dashboard_gen = ECGDashboardGenerator(results)
        dashboard_file = dashboard_gen.generate_html_dashboard("dashboard.html")
        
        print(f"✅ Dashboard HTML generado: {dashboard_file}")
        
        # Paso 4: Crear README con instrucciones
        print("\n\n📚 PASO 4: Creando Documentación")
        print("-" * 50)
        
        create_readme()
        
        # Resumen final
        print("\n\n🎉 ANÁLISIS COMPLETADO EXITOSAMENTE")
        print("="*80)
        print("Archivos generados:")
        print(f"   • dashboard.html - Dashboard interactivo principal")
        print(f"   • README.md - Instrucciones de uso")
        print(f"   • src/ecg_processor.py - Procesador de datos ECG")
        print(f"   • src/dashboard_generator.py - Generador de dashboard")
        print(f"   • src/statistical_analysis.py - Análisis estadístico")
        print()
        print("Para ver el dashboard:")
        print("   1. Abre dashboard.html en tu navegador")
        print("   2. Explora las visualizaciones interactivas")
        print("   3. Selecciona diferentes atletas en el dropdown")
        print()
        print("Técnicas implementadas del semestre:")
        print("   ✅ Transformada Rápida de Fourier (FFT)")
        print("   ✅ Filtrado Digital con filtros Butterworth")
        print("   ✅ Detección automática de picos R")
        print("   ✅ Análisis de Variabilidad de Frecuencia Cardíaca (HRV)")
        print("   ✅ Normalización y preprocesamiento")
        print("   ✅ Análisis estadístico con curtosis")
        print("   ✅ Visualizaciones interactivas con Plotly")
        print()
        print(f"Finalizado: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print("="*80)
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR durante la ejecución:")
        print(f"   {str(e)}")
        print("\n🔍 Detalles del error:")
        traceback.print_exc()
        return False


def create_readme():
    """
    Crea el archivo README con instrucciones de uso
    """
    readme_content = """# Dashboard ECG - Atletas de Resistencia Noruegos

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
venv\\Scripts\\activate   # En Windows

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

## Autor

Proyecto desarrollado como parte del curso de Procesamiento de Señales Biológicas, implementando las técnicas vistas durante el semestre.

## Licencia

Los datos ECG están bajo licencia Creative Commons Attribution 4.0 International Public License.

## Referencias

- Norwegian Endurance Athlete ECG Database
- Técnicas de procesamiento de señales biológicas del curso
- Estándares internacionales para interpretación de ECG en atletas
"""
    
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    print("✅ README.md creado exitosamente")


if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 ¡Proyecto completado exitosamente!")
    else:
        print("\n❌ El proyecto falló. Revisa los errores arriba.")
        sys.exit(1)
