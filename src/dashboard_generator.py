"""
Generador de Dashboard HTML Interactivo para Análisis ECG
Utiliza Plotly para crear visualizaciones interactivas
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.offline as pyo
import numpy as np
import pandas as pd
from typing import Dict, List, Any
import json
from datetime import datetime


class ECGDashboardGenerator:
    """
    Generador de dashboard HTML interactivo para análisis ECG
    """
    
    def __init__(self, analysis_results: Dict[str, Any]):
        self.results = analysis_results
        self.leads = ['I', 'II', 'III', 'aVR', 'aVL', 'aVF', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6']
        self.fs = 500  # Frecuencia de muestreo
        self.duration = 10  # Duración en segundos
        
    def create_12_lead_overview(self, record_name: str) -> go.Figure:
        """
        Crea visualización de las 12 derivaciones ECG para un atleta específico con etiquetas educativas
        """
        if record_name not in self.results['individual_results']:
            raise ValueError(f"Registro {record_name} no encontrado")
        
        record_data = self.results['individual_results'][record_name]
        filtered_signal = record_data['filtered_signal']
        
        # Crear subplots para las 12 derivaciones con títulos concisos
        lead_descriptions = [
            "I - Actividad eléctrica horizontal", 
            "II - Derivación principal para ritmo", 
            "III - Complementa derivación II",
            "aVR - Detecta dextrocardia", 
            "aVL - Pared lateral alta", 
            "aVF - Pared inferior del corazón",
            "V1 - Ventrículo derecho", 
            "V2 - Septo interventricular", 
            "V3 - Transición septo-VI",
            "V4 - Ápice ventricular", 
            "V5 - Pared lateral izquierda", 
            "V6 - Pared lateral posterior"
        ]
        
        fig = make_subplots(
            rows=4, cols=3,
            subplot_titles=lead_descriptions,
            vertical_spacing=0.12,
            horizontal_spacing=0.08
        )
        
        time_axis = np.arange(len(filtered_signal)) / self.fs
        
        # Colores distintivos para cada derivación
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b',
                 '#e377c2', '#7f7f7f', '#bcbd22', '#17becf', '#ff9896', '#98df8a']
        
        for i, lead in enumerate(self.leads):
            row = (i // 3) + 1
            col = (i % 3) + 1
            
            fig.add_trace(
                go.Scatter(
                    x=time_axis,
                    y=filtered_signal[:, i],
                    mode='lines',
                    name=lead,
                    line=dict(width=1.5, color=colors[i]),
                    showlegend=False,
                    hovertemplate=f'<b>{lead}</b><br>' +
                                f'{lead_descriptions[i]}<br>' +
                                'Tiempo: %{x:.2f}s<br>' +
                                'Amplitud: %{y:.2f}mV<br>' +
                                '<extra></extra>'
                ),
                row=row, col=col
            )
        
        # Sin anotaciones adicionales - información está en la sección explicativa superior
        annotations = []
        
        fig.update_layout(
            title=dict(
                text=f"ECG de 12 Derivaciones - {record_name}<br><sub>Análisis completo de la actividad eléctrica cardíaca</sub>",
                x=0.5,
                font=dict(size=18, color="#2c3e50")
            ),
            height=1000,
            showlegend=False,
            template="plotly_white",
            annotations=annotations,
            margin=dict(l=50, r=50, t=120, b=50)
        )
        
        # Actualizar títulos de subplots para que sean más visibles
        for i in range(len(lead_descriptions)):
            fig.update_annotations(
                font=dict(size=11, color="#2c3e50"),
                selector=dict(text=lead_descriptions[i])
            )
        
        # Actualizar ejes con mejor formato
        for i in range(1, 5):
            for j in range(1, 4):
                fig.update_xaxes(
                    title_text="Tiempo (s)", 
                    row=i, col=j,
                    title_font=dict(size=10),
                    tickfont=dict(size=9)
                )
                fig.update_yaxes(
                    title_text="Amplitud (mV)", 
                    row=i, col=j,
                    title_font=dict(size=10),
                    tickfont=dict(size=9)
                )
        
        return fig
    
    def create_temporal_analysis(self, record_name: str) -> go.Figure:
        """
        Análisis temporal: señal cruda vs filtrada con detección de picos R
        """
        record_data = self.results['individual_results'][record_name]
        raw_signal = record_data['raw_signal']
        filtered_signal = record_data['filtered_signal']
        r_peaks = record_data['r_peaks']
        
        time_axis = np.arange(len(raw_signal)) / self.fs
        
        fig = make_subplots(
            rows=3, cols=1,
            subplot_titles=[
                "Señal ECG Cruda (Derivación II)",
                "Señal ECG Filtrada (Derivación II)",
                "Detección de Picos R"
            ],
            vertical_spacing=0.1
        )
        
        # Señal cruda
        fig.add_trace(
            go.Scatter(
                x=time_axis,
                y=raw_signal[:, 1],  # Derivación II
                mode='lines',
                name='Cruda',
                line=dict(color='lightblue', width=1),
                hovertemplate='Tiempo: %{x:.2f}s<br>Amplitud: %{y:.2f}mV<extra></extra>'
            ),
            row=1, col=1
        )
        
        # Señal filtrada
        fig.add_trace(
            go.Scatter(
                x=time_axis,
                y=filtered_signal[:, 1],  # Derivación II
                mode='lines',
                name='Filtrada',
                line=dict(color='blue', width=1),
                hovertemplate='Tiempo: %{x:.2f}s<br>Amplitud: %{y:.2f}mV<extra></extra>'
            ),
            row=2, col=1
        )
        
        # Detección de picos R
        fig.add_trace(
            go.Scatter(
                x=time_axis,
                y=filtered_signal[:, 1],
                mode='lines',
                name='Señal',
                line=dict(color='blue', width=1),
                hovertemplate='Tiempo: %{x:.2f}s<br>Amplitud: %{y:.2f}mV<extra></extra>'
            ),
            row=3, col=1
        )
        
        # Marcar picos R
        if len(r_peaks) > 0:
            peak_times = r_peaks / self.fs
            peak_values = filtered_signal[r_peaks, 1]
            
            fig.add_trace(
                go.Scatter(
                    x=peak_times,
                    y=peak_values,
                    mode='markers',
                    name='Picos R',
                    marker=dict(color='red', size=8, symbol='circle'),
                    hovertemplate='Pico R<br>Tiempo: %{x:.2f}s<br>Amplitud: %{y:.2f}mV<extra></extra>'
                ),
                row=3, col=1
            )
        
        fig.update_layout(
            title=f"Análisis Temporal - {record_name}",
            height=600,
            showlegend=False,
            template="plotly_white"
        )
        
        # Actualizar ejes
        for i in range(1, 4):
            fig.update_xaxes(title_text="Tiempo (s)", row=i, col=1)
            fig.update_yaxes(title_text="Amplitud (mV)", row=i, col=1)
        
        return fig
    
    def create_spectral_analysis(self, record_name: str) -> go.Figure:
        """
        Análisis espectral usando FFT para diferentes derivaciones
        """
        record_data = self.results['individual_results'][record_name]
        fft_results = record_data['fft_results']
        
        # Seleccionar algunas derivaciones representativas
        selected_leads = ['I', 'II', 'V1', 'V5']
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=[f"Espectro FFT - {lead}" for lead in selected_leads],
            vertical_spacing=0.1,
            horizontal_spacing=0.1
        )
        
        for i, lead in enumerate(selected_leads):
            row = (i // 2) + 1
            col = (i % 2) + 1
            
            frequencies = fft_results[lead]['frequencies']
            magnitude = fft_results[lead]['magnitude']
            
            # Limitar a frecuencias relevantes (0-50 Hz)
            freq_mask = frequencies <= 50
            if len(freq_mask) == len(frequencies) and len(freq_mask) == len(magnitude):
                frequencies = frequencies[freq_mask]
                magnitude = magnitude[freq_mask]
            else:
                # Si hay problemas de dimensiones, tomar solo los primeros elementos
                max_idx = min(len(frequencies), len(magnitude))
                frequencies = frequencies[:max_idx]
                magnitude = magnitude[:max_idx]
                freq_mask = frequencies <= 50
                frequencies = frequencies[freq_mask]
                magnitude = magnitude[freq_mask]
            
            fig.add_trace(
                go.Scatter(
                    x=frequencies,
                    y=magnitude,
                    mode='lines',
                    name=lead,
                    line=dict(width=2),
                    hovertemplate=f'<b>{lead}</b><br>' +
                                'Frecuencia: %{x:.1f}Hz<br>' +
                                'Magnitud: %{y:.2f}<br>' +
                                '<extra></extra>'
                ),
                row=row, col=col
            )
            
            # Marcar frecuencia dominante
            dominant_freq = fft_results[lead]['dominant_freq']
            if dominant_freq <= 50:
                dominant_mag = magnitude[np.argmin(np.abs(frequencies - dominant_freq))]
                fig.add_trace(
                    go.Scatter(
                        x=[dominant_freq],
                        y=[dominant_mag],
                        mode='markers',
                        name=f'Dominante {lead}',
                        marker=dict(color='red', size=10, symbol='star'),
                        showlegend=False,
                        hovertemplate=f'Frecuencia Dominante: {dominant_freq:.1f}Hz<br>' +
                                    f'Magnitud: {dominant_mag:.2f}<extra></extra>'
                    ),
                    row=row, col=col
                )
        
        fig.update_layout(
            title=f"Análisis Espectral FFT - {record_name}",
            height=600,
            showlegend=False,
            template="plotly_white"
        )
        
        # Actualizar ejes
        for i in range(1, 3):
            for j in range(1, 3):
                fig.update_xaxes(title_text="Frecuencia (Hz)", row=i, col=j)
                fig.update_yaxes(title_text="Magnitud", row=i, col=j)
        
        return fig
    
    def create_hrv_analysis(self, record_name: str) -> go.Figure:
        """
        Análisis de Variabilidad de Frecuencia Cardíaca (HRV)
        """
        record_data = self.results['individual_results'][record_name]
        rr_intervals = record_data['rr_intervals']
        hrv_metrics = record_data['hrv_metrics']
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=[
                "Intervalos RR",
                "Distribución de Intervalos RR",
                "Métricas HRV",
                "Tendencias Temporales"
            ],
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        if len(rr_intervals) > 0:
            # Intervalos RR en el tiempo
            beat_numbers = np.arange(1, len(rr_intervals) + 1)
            fig.add_trace(
                go.Scatter(
                    x=beat_numbers,
                    y=rr_intervals,
                    mode='lines+markers',
                    name='Intervalos RR',
                    line=dict(color='blue', width=2),
                    marker=dict(size=4),
                    hovertemplate='Latido: %{x}<br>Intervalo RR: %{y:.1f}ms<extra></extra>'
                ),
                row=1, col=1
            )
            
            # Histograma de intervalos RR
            fig.add_trace(
                go.Histogram(
                    x=rr_intervals,
                    name='Distribución RR',
                    nbinsx=20,
                    marker_color='lightblue',
                    hovertemplate='Intervalo RR: %{x:.1f}ms<br>Frecuencia: %{y}<extra></extra>'
                ),
                row=1, col=2
            )
            
            # Métricas HRV
            metrics_names = ['SDNN', 'RMSSD', 'FC Promedio']
            metrics_values = [hrv_metrics['sdnn'], hrv_metrics['rmssd'], hrv_metrics['mean_hr']]
            
            fig.add_trace(
                go.Bar(
                    x=metrics_names,
                    y=metrics_values,
                    name='Métricas HRV',
                    marker_color=['green', 'orange', 'red'],
                    hovertemplate='%{x}: %{y:.1f}<extra></extra>'
                ),
                row=2, col=1
            )
            
            # Tendencias temporales (ventanas deslizantes)
            if len(rr_intervals) > 5:
                window_size = min(5, len(rr_intervals) // 3)
                rolling_mean = pd.Series(rr_intervals).rolling(window=window_size).mean()
                rolling_std = pd.Series(rr_intervals).rolling(window=window_size).std()
                
                fig.add_trace(
                    go.Scatter(
                        x=beat_numbers,
                        y=rolling_mean,
                        mode='lines',
                        name='Media Móvil',
                        line=dict(color='red', width=2),
                        hovertemplate='Latido: %{x}<br>Media RR: %{y:.1f}ms<extra></extra>'
                    ),
                    row=2, col=2
                )
                
                fig.add_trace(
                    go.Scatter(
                        x=beat_numbers,
                        y=rolling_std,
                        mode='lines',
                        name='Desv. Est. Móvil',
                        line=dict(color='purple', width=2),
                        hovertemplate='Latido: %{x}<br>Desv. Est. RR: %{y:.1f}ms<extra></extra>'
                    ),
                    row=2, col=2
                )
        
        fig.update_layout(
            title=f"Análisis HRV - {record_name}",
            height=600,
            showlegend=True,
            template="plotly_white"
        )
        
        # Actualizar ejes
        fig.update_xaxes(title_text="Número de Latido", row=1, col=1)
        fig.update_yaxes(title_text="Intervalo RR (ms)", row=1, col=1)
        fig.update_xaxes(title_text="Intervalo RR (ms)", row=1, col=2)
        fig.update_yaxes(title_text="Frecuencia", row=1, col=2)
        fig.update_xaxes(title_text="Métrica", row=2, col=1)
        fig.update_yaxes(title_text="Valor", row=2, col=1)
        fig.update_xaxes(title_text="Número de Latido", row=2, col=2)
        fig.update_yaxes(title_text="Valor", row=2, col=2)
        
        return fig
    
    def create_comparative_analysis(self) -> go.Figure:
        """
        Análisis comparativo entre todos los atletas - Diseño mejorado
        """
        summary_stats = self.results['summary_statistics']
        
        # Crear figura con mejor espaciado
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=[
                "Distribución de Frecuencias Cardíacas",
                "HRV SDNN vs RMSSD",
                "Estadísticas Generales",
                "Resumen de Diagnósticos"
            ],
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]],
            vertical_spacing=0.12,
            horizontal_spacing=0.1
        )
        
        # 1. Distribución de frecuencias cardíacas (más limpia)
        fig.add_trace(
            go.Histogram(
                x=summary_stats['heart_rates'],
                name='Frecuencias Cardíacas',
                nbinsx=12,
                marker_color='#3498db',
                opacity=0.7,
                hovertemplate='FC: %{x:.1f} BPM<br>Cantidad: %{y}<extra></extra>'
            ),
            row=1, col=1
        )
        
        # 2. HRV SDNN vs RMSSD (mejorado)
        fig.add_trace(
            go.Scatter(
                x=summary_stats['hrv_sdnn'],
                y=summary_stats['hrv_rmssd'],
                mode='markers',
                name='HRV',
                marker=dict(
                    size=10, 
                    color='#e74c3c',
                    opacity=0.7,
                    line=dict(width=1, color='white')
                ),
                hovertemplate='Atleta<br>SDNN: %{x:.1f}ms<br>RMSSD: %{y:.1f}ms<extra></extra>'
            ),
            row=1, col=2
        )
        
        # 3. Estadísticas generales (más clara)
        stats_names = ['FC Promedio', 'FC Desv. Est.', 'SDNN Promedio', 'RMSSD Promedio']
        stats_values = [
            summary_stats['mean_hr'],
            summary_stats['std_hr'],
            summary_stats['mean_sdnn'],
            summary_stats['mean_rmssd']
        ]
        
        colors = ['#2ecc71', '#f39c12', '#9b59b6', '#e67e22']
        
        fig.add_trace(
            go.Bar(
                x=stats_names,
                y=stats_values,
                name='Estadísticas',
                marker_color=colors,
                hovertemplate='%{x}<br>Valor: %{y:.1f}<extra></extra>'
            ),
            row=2, col=1
        )
        
        # 4. Resumen de diagnósticos (mejorado para legibilidad)
        sl12_diagnoses = summary_stats['sl12_diagnoses']
        cardiologist_diagnoses = summary_stats['cardiologist_diagnoses']
        
        # Contar diagnósticos más comunes (top 4 para mejor legibilidad)
        sl12_counts = pd.Series(sl12_diagnoses).value_counts().head(4)
        
        # Crear etiquetas más cortas y legibles
        short_labels = []
        for diagnosis in sl12_counts.index:
            if 'Sinus bradycardia' in diagnosis and 'Otherwise normal' in diagnosis:
                short_labels.append('Bradicardia Sinusal Normal')
            elif 'Sinus bradycardia' in diagnosis and 'marked sinus arrhythmia' in diagnosis:
                short_labels.append('Bradicardia + Arritmia Sinusal')
            elif 'Normal sinus rhythm' in diagnosis and 'Normal ECG' in diagnosis:
                short_labels.append('Ritmo Sinusal Normal')
            elif 'RSR' in diagnosis or 'QR pattern' in diagnosis:
                short_labels.append('Patrón RSR\' en V1')
            else:
                # Tomar las primeras palabras del diagnóstico
                words = diagnosis.split(',')[0].split()[:3]
                short_labels.append(' '.join(words))
        
        fig.add_trace(
            go.Bar(
                x=sl12_counts.values,
                y=short_labels,
                orientation='h',
                name='Diagnósticos SL12',
                marker_color='#e74c3c',
                text=sl12_counts.values,
                textposition='inside',
                hovertemplate='<b>%{y}</b><br>Cantidad: %{x}<br><br>Diagnóstico completo:<br>%{customdata}<extra></extra>',
                customdata=sl12_counts.index
            ),
            row=2, col=2
        )
        
        # Actualizar layout con mejor diseño
        fig.update_layout(
            title=dict(
                text="Análisis Comparativo - Atletas de Resistencia",
                x=0.5,
                font=dict(size=20, color='#2c3e50')
            ),
            height=700,
            showlegend=False,
            template="plotly_white",
            font=dict(size=12),
            margin=dict(l=50, r=50, t=80, b=50)
        )
        
        # Actualizar ejes con mejor formato
        fig.update_xaxes(title_text="Frecuencia Cardíaca (BPM)", row=1, col=1, 
                        title_font=dict(size=12), tickfont=dict(size=10))
        fig.update_yaxes(title_text="Cantidad", row=1, col=1,
                        title_font=dict(size=12), tickfont=dict(size=10))
        
        fig.update_xaxes(title_text="SDNN (ms)", row=1, col=2,
                        title_font=dict(size=12), tickfont=dict(size=10))
        fig.update_yaxes(title_text="RMSSD (ms)", row=1, col=2,
                        title_font=dict(size=12), tickfont=dict(size=10))
        
        fig.update_xaxes(title_text="Valor", row=2, col=1,
                        title_font=dict(size=12), tickfont=dict(size=10))
        fig.update_yaxes(title_text="Métrica", row=2, col=1,
                        title_font=dict(size=12), tickfont=dict(size=10))
        
        fig.update_xaxes(title_text="Cantidad", row=2, col=2,
                        title_font=dict(size=12), tickfont=dict(size=10))
        fig.update_yaxes(title_text="Diagnóstico", row=2, col=2,
                        title_font=dict(size=12), tickfont=dict(size=11))
        
        # Mejorar específicamente el gráfico de diagnósticos
        fig.update_layout(
            annotations=[
                dict(
                    text="Diagnósticos más comunes del algoritmo SL12",
                    xref="paper", yref="paper",
                    x=0.75, y=0.25,
                    showarrow=False,
                    font=dict(size=10, color="#666666")
                )
            ]
        )
        
        return fig
    
    def create_diagnosis_table(self) -> go.Figure:
        """
        Tabla comparativa de diagnósticos SL12 vs Cardiólogo
        """
        records = list(self.results['individual_results'].keys())
        
        sl12_diagnoses = []
        cardiologist_diagnoses = []
        
        for record in records:
            metadata = self.results['individual_results'][record]['metadata']
            sl12_diagnoses.append(metadata['sl12_diagnosis'])
            cardiologist_diagnoses.append(metadata['cardiologist_diagnosis'])
        
        fig = go.Figure(data=[go.Table(
            header=dict(
                values=['Atleta', 'Diagnóstico SL12', 'Diagnóstico Cardiólogo'],
                fill_color='lightblue',
                align='center',
                font=dict(size=12)
            ),
            cells=dict(
                values=[records, sl12_diagnoses, cardiologist_diagnoses],
                fill_color='white',
                align='left',
                font=dict(size=10)
            )
        )])
        
        fig.update_layout(
            title="Tabla Comparativa de Diagnósticos",
            height=800,
            template="plotly_white"
        )
        
        return fig
    
    def generate_html_dashboard(self, output_file: str = "dashboard.html") -> str:
        """
        Genera el dashboard HTML completo con todas las visualizaciones
        """
        print("Generando dashboard HTML con visualizaciones...")
        
        # Generar visualizaciones principales
        comparative_fig = self.create_comparative_analysis()
        diagnosis_fig = self.create_diagnosis_table()
        
        # Seleccionar primer atleta para ejemplos
        first_athlete = list(self.results['individual_results'].keys())[0]
        ecg_12lead_fig = self.create_12_lead_overview(first_athlete)
        temporal_fig = self.create_temporal_analysis(first_athlete)
        spectral_fig = self.create_spectral_analysis(first_athlete)
        hrv_fig = self.create_hrv_analysis(first_athlete)
        
        # Convertir figuras a HTML
        comparative_html = pyo.plot(comparative_fig, output_type='div', include_plotlyjs=False)
        diagnosis_html = pyo.plot(diagnosis_fig, output_type='div', include_plotlyjs=False)
        ecg_12lead_html = pyo.plot(ecg_12lead_fig, output_type='div', include_plotlyjs=False)
        temporal_html = pyo.plot(temporal_fig, output_type='div', include_plotlyjs=False)
        spectral_html = pyo.plot(spectral_fig, output_type='div', include_plotlyjs=False)
        hrv_html = pyo.plot(hrv_fig, output_type='div', include_plotlyjs=False)
        
        # Crear HTML base
        html_content = f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Dashboard ECG - Atletas de Resistencia Noruegos</title>
            <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 20px;
                    background-color: #f5f5f5;
                }}
                .container {{
                    max-width: 1400px;
                    margin: 0 auto;
                    background-color: white;
                    padding: 20px;
                    border-radius: 10px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }}
                .header {{
                    text-align: center;
                    margin-bottom: 30px;
                    padding: 20px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    border-radius: 10px;
                }}
                .section {{
                    margin: 30px 0;
                    padding: 20px;
                    border: 1px solid #ddd;
                    border-radius: 10px;
                    background-color: #fafafa;
                }}
                .controls {{
                    margin: 20px 0;
                    padding: 15px;
                    background-color: #e8f4fd;
                    border-radius: 5px;
                }}
                .plot-container {{
                    margin: 20px 0;
                }}
                .info-box {{
                    background-color: #e8f5e8;
                    padding: 15px;
                    border-radius: 5px;
                    margin: 15px 0;
                }}
                .technique-box {{
                    background-color: #fff3cd;
                    padding: 15px;
                    border-radius: 5px;
                    margin: 15px 0;
                }}
                select, button {{
                    padding: 8px 12px;
                    margin: 5px;
                    border-radius: 5px;
                    border: 1px solid #ccc;
                }}
                button {{
                    background-color: #007bff;
                    color: white;
                    cursor: pointer;
                }}
                button:hover {{
                    background-color: #0056b3;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Dashboard ECG - Atletas de Resistencia Noruegos</h1>
                    <p>Análisis de 28 atletas de élite usando técnicas de procesamiento de señales biológicas</p>
                    <p>Generado el {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</p>
                </div>
                
                <div class="info-box">
                    <h3>📊 Resumen del Análisis</h3>
                    <ul>
                        <li><strong>Total de registros:</strong> {self.results['total_records']}</li>
                        <li><strong>Frecuencia cardíaca promedio:</strong> {self.results['summary_statistics']['mean_hr']:.1f} BPM</li>
                        <li><strong>HRV SDNN promedio:</strong> {self.results['summary_statistics']['mean_sdnn']:.1f} ms</li>
                        <li><strong>HRV RMSSD promedio:</strong> {self.results['summary_statistics']['mean_rmssd']:.1f} ms</li>
                        <li><strong>Frecuencia de muestreo:</strong> 500 Hz</li>
                        <li><strong>Duración de registro:</strong> 10 segundos</li>
                    </ul>
                </div>
                
                <div class="section">
                    <h2>🎛️ Controles Interactivos</h2>
                    <div class="controls">
                        <label for="athlete-select">Seleccionar Atleta:</label>
                        <select id="athlete-select" onchange="updateVisualizations()">
        """
        
        # Agregar opciones de atletas
        for record in sorted(self.results['individual_results'].keys()):
            html_content += f'<option value="{record}">{record}</option>\n'
        
        html_content += f"""
                        </select>
                        <button onclick="updateVisualizations()">Actualizar Visualizaciones</button>
                        <p><em>Nota: Las visualizaciones muestran datos del atleta seleccionado. Por defecto se muestra {first_athlete}.</em></p>
                    </div>
                </div>
                
                <div class="section">
                    <h2>📈 Análisis Comparativo General</h2>
                    <div class="info-box">
                        <h3>📖 Explicación del Análisis Comparativo</h3>
                        <p><strong>¿Qué estás viendo?</strong> Esta visualización compara las características cardiovasculares de todos los 28 atletas de resistencia, mostrando patrones comunes y variaciones individuales.</p>
                        
                        <h4>📊 Gráficos Incluidos:</h4>
                        
                        <h5>🔵 Distribución de Frecuencias Cardíacas (Superior Izquierda):</h5>
                        <ul>
                            <li><strong>Propósito:</strong> Mostrar el rango de frecuencias cardíacas en reposo</li>
                            <li><strong>Interpretación:</strong> La mayoría de atletas tienen FC entre 50-70 BPM (bradicardia sinusal)</li>
                            <li><strong>Significado:</strong> Adaptación fisiológica al entrenamiento de resistencia</li>
                        </ul>
                        
                        <h5>🔴 HRV SDNN vs RMSSD (Superior Derecha):</h5>
                        <ul>
                            <li><strong>Propósito:</strong> Relacionar dos métricas importantes de variabilidad cardíaca</li>
                            <li><strong>SDNN:</strong> Variabilidad total (eje X)</li>
                            <li><strong>RMSSD:</strong> Variabilidad de corto plazo (eje Y)</li>
                            <li><strong>Correlación:</strong> Puntos agrupados indican consistencia en la población</li>
                        </ul>
                        
                        <h5>🟢 Estadísticas Generales (Inferior Izquierda):</h5>
                        <ul>
                            <li><strong>FC Promedio:</strong> Frecuencia cardíaca promedio de todos los atletas</li>
                            <li><strong>FC Desv. Est.:</strong> Variabilidad en frecuencias cardíacas</li>
                            <li><strong>SDNN Promedio:</strong> Variabilidad promedio en intervalos RR</li>
                            <li><strong>RMSSD Promedio:</strong> Variabilidad de corto plazo promedio</li>
                        </ul>
                        
                        <h5>🟠 Resumen de Diagnósticos (Inferior Derecha):</h5>
                        <ul>
                            <li><strong>Propósito:</strong> Mostrar los diagnósticos más comunes del algoritmo SL12</li>
                            <li><strong>Interpretación:</strong> Patrones diagnósticos típicos en atletas</li>
                            <li><strong>Valor Clínico:</strong> Identificar características comunes vs anomalías</li>
                        </ul>
                        
                        <h4>🏃‍♂️ Hallazgos Típicos en Atletas de Resistencia:</h4>
                        <ul>
                            <li><strong>Bradicardia sinusal:</strong> FC baja en reposo (adaptación fisiológica)</li>
                            <li><strong>HRV elevada:</strong> Mejor variabilidad que población general</li>
                            <li><strong>Arritmia sinusal:</strong> Variación normal en intervalos RR</li>
                            <li><strong>Diagnósticos benignos:</strong> Cambios adaptativos, no patológicos</li>
                        </ul>
                        
                        <h4>📈 Interpretación de Patrones:</h4>
                        <ul>
                            <li><strong>Agrupación de puntos:</strong> Indica características similares entre atletas</li>
                            <li><strong>Valores extremos:</strong> Pueden indicar casos especiales o variaciones normales</li>
                            <li><strong>Distribución normal:</strong> Sugiere población homogénea de atletas</li>
                        </ul>
                    </div>
                    <div class="plot-container">
                        {comparative_html}
                    </div>
                </div>
                
                <div class="section">
                    <h2>📋 Tabla de Diagnósticos</h2>
                    <div class="info-box">
                        <h3>📖 Explicación de la Tabla de Diagnósticos</h3>
                        <p><strong>¿Qué estás viendo?</strong> Esta tabla compara los diagnósticos automáticos del algoritmo SL12 (GE Marquette) con la evaluación manual de un cardiólogo experto para cada uno de los 28 atletas.</p>
                        
                        <h4>🔬 Columnas de la Tabla:</h4>
                        <ul>
                            <li><strong>Atleta:</strong> Identificador único de cada deportista (ath_001 a ath_028)</li>
                            <li><strong>Diagnóstico SL12:</strong> Interpretación automática del algoritmo GE Marquette SL12</li>
                            <li><strong>Diagnóstico Cardiólogo:</strong> Evaluación manual de un cardiólogo experto</li>
                        </ul>
                        
                        <h4>🤖 Algoritmo SL12:</h4>
                        <ul>
                            <li><strong>Desarrollado por:</strong> GE Marquette Medical Systems</li>
                            <li><strong>Propósito:</strong> Interpretación automática de ECG en tiempo real</li>
                            <li><strong>Ventajas:</strong> Consistencia, rapidez, disponibilidad 24/7</li>
                            <li><strong>Limitaciones:</strong> Puede ser conservador o generar falsos positivos</li>
                        </ul>
                        
                        <h4>👨‍⚕️ Evaluación del Cardiólogo:</h4>
                        <ul>
                            <li><strong>Experiencia:</strong> Evaluación manual por cardiólogo experto</li>
                            <li><strong>Contexto:</strong> Considera el contexto de atleta de resistencia</li>
                            <li><strong>Precisión:</strong> Gold standard para interpretación ECG</li>
                            <li><strong>Flexibilidad:</strong> Puede considerar factores específicos del deporte</li>
                        </ul>
                        
                        <h4>📊 Tipos de Diagnósticos Comunes:</h4>
                        <ul>
                            <li><strong>Sinus bradycardia:</strong> Frecuencia cardíaca baja (normal en atletas)</li>
                            <li><strong>Sinus arrhythmia:</strong> Variación normal en intervalos RR</li>
                            <li><strong>Right/Left axis deviation:</strong> Desviación del eje eléctrico</li>
                            <li><strong>Borderline ECG:</strong> Cambios menores, dentro de límites normales</li>
                            <li><strong>Normal ECG:</strong> Sin anomalías detectables</li>
                        </ul>
                        
                        <h4>🎯 Valor de la Comparación:</h4>
                        <ul>
                            <li><strong>Concordancia:</strong> Casos donde ambos diagnósticos coinciden</li>
                            <li><strong>Discrepancias:</strong> Diferencias entre algoritmo y cardiólogo</li>
                            <li><strong>Validación:</strong> Evaluar precisión del algoritmo automático</li>
                            <li><strong>Mejora:</strong> Identificar áreas de mejora para algoritmos futuros</li>
                        </ul>
                        
                        <h4>🏃‍♂️ Consideraciones Especiales para Atletas:</h4>
                        <ul>
                            <li><strong>Adaptaciones fisiológicas:</strong> Cambios normales por entrenamiento</li>
                            <li><strong>Criterios específicos:</strong> Límites diferentes a población general</li>
                            <li><strong>Contexto deportivo:</strong> Importancia del historial de entrenamiento</li>
                            <li><strong>Prevención:</strong> Detección temprana de problemas reales</li>
                        </ul>
                    </div>
                    <div class="plot-container">
                        {diagnosis_html}
                    </div>
                </div>
                
                   <div class="section">
                       <h2>💓 ECG de 12 Derivaciones - {first_athlete}</h2>
                       <div class="info-box">
                           <h3>📖 Explicación de las 12 Derivaciones ECG</h3>
                           <p><strong>¿Qué estás viendo?</strong> Esta visualización muestra la actividad eléctrica del corazón desde 12 perspectivas diferentes, como si fueran 12 cámaras filmando el mismo evento desde ángulos distintos.</p>
                           
                           <h4>🔵 Derivaciones de Extremidades (Filas 1-2):</h4>
                           <ul>
                               <li><strong>I, II, III:</strong> Forman el "Triángulo de Einthoven" - muestran la actividad eléctrica en el plano frontal del corazón</li>
                               <li><strong>aVR, aVL, aVF:</strong> Son derivaciones "aumentadas" que amplifican la señal para mejor visualización</li>
                               <li><strong>Propósito:</strong> Detectar problemas en el eje eléctrico del corazón y arritmias</li>
                           </ul>
                           
                           <h4>🔴 Derivaciones Precordiales (Filas 3-4):</h4>
                           <ul>
                               <li><strong>V1-V6:</strong> Se colocan directamente sobre el pecho, desde el lado derecho hasta el izquierdo</li>
                               <li><strong>Propósito:</strong> Detectar infartos, problemas de conducción y anomalías ventriculares</li>
                               <li><strong>Ubicación:</strong> Cada derivación tiene una posición anatómica específica en el tórax</li>
                           </ul>
                           
                           <h4>🏃‍♂️ Características Típicas en Atletas:</h4>
                           <ul>
                               <li><strong>Bradicardia sinusal:</strong> Frecuencia cardíaca baja (menos de 60 BPM) - adaptación al entrenamiento</li>
                               <li><strong>Arritmia sinusal:</strong> Variación normal en los intervalos entre latidos</li>
                               <li><strong>Ondas T altas:</strong> Indican buena condición cardiovascular</li>
                               <li><strong>QRS estrecho:</strong> Conducción eléctrica eficiente</li>
                           </ul>
                       </div>
                       <div class="plot-container">
                           {ecg_12lead_html}
                       </div>
                   </div>
                
                <div class="section">
                    <h2>⏱️ Análisis Temporal - {first_athlete}</h2>
                    <div class="info-box">
                        <h3>📖 Explicación del Análisis Temporal</h3>
                        <p><strong>¿Qué estás viendo?</strong> Esta visualización compara la señal ECG original (cruda) con la señal procesada (filtrada) y muestra la detección automática de los picos R.</p>
                        
                        <h4>🔵 Señal Cruda (Azul):</h4>
                        <ul>
                            <li><strong>Contiene:</strong> La señal ECG tal como se registró originalmente</li>
                            <li><strong>Problemas:</strong> Ruido de alta frecuencia, deriva de línea base, interferencia eléctrica</li>
                            <li><strong>Propósito:</strong> Mostrar la calidad inicial del registro</li>
                        </ul>
                        
                        <h4>🟢 Señal Filtrada (Verde):</h4>
                        <ul>
                            <li><strong>Procesamiento aplicado:</strong> Filtros Butterworth paso-banda (0.5-40 Hz)</li>
                            <li><strong>Resultado:</strong> Señal limpia, sin artefactos, lista para análisis</li>
                            <li><strong>Técnica:</strong> Filtrado sin desfase usando <code>scipy.signal.filtfilt()</code></li>
                        </ul>
                        
                        <h4>🔴 Detección de Picos R:</h4>
                        <ul>
                            <li><strong>Algoritmo:</strong> Basado en <code>scipy.signal.find_peaks()</code></li>
                            <li><strong>Umbralización:</strong> Adaptativa usando 3 desviaciones estándar</li>
                            <li><strong>Período refractario:</strong> 200ms para evitar detecciones múltiples</li>
                            <li><strong>Propósito:</strong> Calcular frecuencia cardíaca y variabilidad HRV</li>
                        </ul>
                        
                        <h4>📊 Métricas Calculadas:</h4>
                        <ul>
                            <li><strong>Frecuencia cardíaca:</strong> Latidos por minuto (BPM)</li>
                            <li><strong>Intervalos RR:</strong> Tiempo entre latidos consecutivos</li>
                            <li><strong>HRV:</strong> Variabilidad de la frecuencia cardíaca</li>
                        </ul>
                    </div>
                    <div class="plot-container">
                        {temporal_html}
                    </div>
                </div>
                
                <div class="section">
                    <h2>📊 Análisis Espectral (FFT) - {first_athlete}</h2>
                    <div class="info-box">
                        <h3>📖 Explicación del Análisis Espectral (FFT)</h3>
                        <p><strong>¿Qué estás viendo?</strong> Esta visualización muestra el análisis de frecuencias de cada derivación ECG usando la Transformada Rápida de Fourier (FFT).</p>
                        
                        <h4>🔬 ¿Qué es la FFT?</h4>
                        <ul>
                            <li><strong>Transformada Rápida de Fourier:</strong> Convierte la señal del tiempo al dominio de frecuencias</li>
                            <li><strong>Propósito:</strong> Identificar qué frecuencias están presentes en la señal ECG</li>
                            <li><strong>Implementación:</strong> Usando <code>scipy.fft.fft()</code> con normalización correcta</li>
                        </ul>
                        
                        <h4>📈 Interpretación de los Gráficos:</h4>
                        <ul>
                            <li><strong>Eje X:</strong> Frecuencia en Hz (0-50 Hz mostrado)</li>
                            <li><strong>Eje Y:</strong> Magnitud espectral (amplitud de cada frecuencia)</li>
                            <li><strong>Picos altos:</strong> Frecuencias dominantes en la señal</li>
                            <li><strong>Colores:</strong> Cada derivación tiene un color distintivo</li>
                        </ul>
                        
                        <h4>🎯 Frecuencias Relevantes en ECG:</h4>
                        <ul>
                            <li><strong>0.5-2 Hz:</strong> Componente de frecuencia cardíaca fundamental</li>
                            <li><strong>2-5 Hz:</strong> Armónicos de la frecuencia cardíaca</li>
                            <li><strong>5-15 Hz:</strong> Componentes de alta frecuencia (QRS)</li>
                            <li><strong>15-40 Hz:</strong> Ruido de alta frecuencia (filtrado)</li>
                        </ul>
                        
                        <h4>🔧 Técnicas Aplicadas:</h4>
                        <ul>
                            <li><strong>Normalización:</strong> <code>P2 = abs(Y/L)</code>, <code>P1 = P2[0:L//2+1]</code></li>
                            <li><strong>Vector de frecuencias:</strong> <code>f = Fs*np.arange(L//2+1)/L</code></li>
                            <li><strong>Método de Welch:</strong> Para densidad espectral de potencia (PSD)</li>
                            <li><strong>Detección de picos:</strong> <code>scipy.signal.find_peaks()</code> para frecuencias dominantes</li>
                        </ul>
                        
                        <h4>🏃‍♂️ Características en Atletas:</h4>
                        <ul>
                            <li><strong>Picos en bajas frecuencias:</strong> Bradicardia sinusal</li>
                            <li><strong>Espectro más concentrado:</strong> Ritmo cardíaco más regular</li>
                            <li><strong>Menos ruido:</strong> Mejor condición cardiovascular</li>
                        </ul>
                    </div>
                    <div class="plot-container">
                        {spectral_html}
                    </div>
                </div>
                
                <div class="section">
                    <h2>🔄 Análisis HRV - {first_athlete}</h2>
                    <div class="info-box">
                        <h3>📖 Explicación del Análisis HRV (Variabilidad de Frecuencia Cardíaca)</h3>
                        <p><strong>¿Qué estás viendo?</strong> Esta visualización muestra la variabilidad de la frecuencia cardíaca (HRV), que es una medida de la variación en los intervalos entre latidos consecutivos.</p>
                        
                        <h4>💓 ¿Qué es la HRV?</h4>
                        <ul>
                            <li><strong>Definición:</strong> Variación natural en los intervalos de tiempo entre latidos cardíacos consecutivos</li>
                            <li><strong>Importancia:</strong> Indicador de salud cardiovascular y condición física</li>
                            <li><strong>Medición:</strong> En milisegundos (ms) entre picos R consecutivos</li>
                        </ul>
                        
                        <h4>📊 Métricas Mostradas:</h4>
                        <ul>
                            <li><strong>Intervalos RR:</strong> Tiempo entre cada latido (línea azul con marcadores)</li>
                            <li><strong>SDNN:</strong> Desviación estándar de intervalos NN (variabilidad total)</li>
                            <li><strong>RMSSD:</strong> Raíz cuadrada de la media de diferencias al cuadrado (variabilidad de corto plazo)</li>
                            <li><strong>Distribución:</strong> Histograma de intervalos RR (frecuencia de cada intervalo)</li>
                        </ul>
                        
                        <h4>🎯 Interpretación de Valores:</h4>
                        <ul>
                            <li><strong>SDNN Alto (>50ms):</strong> Buena variabilidad, corazón saludable</li>
                            <li><strong>RMSSD Alto (>30ms):</strong> Buena adaptación del sistema nervioso autónomo</li>
                            <li><strong>HRV Baja:</strong> Puede indicar estrés, fatiga o problemas cardiovasculares</li>
                            <li><strong>HRV Alta:</strong> Indica buena condición física y recuperación</li>
                        </ul>
                        
                        <h4>🔬 Análisis en Dominio de Frecuencia:</h4>
                        <ul>
                            <li><strong>LF (0.04-0.15 Hz):</strong> Actividad simpática y parasimpática</li>
                            <li><strong>HF (0.15-0.4 Hz):</strong> Actividad parasimpática (respiración)</li>
                            <li><strong>LF/HF:</strong> Balance simpático-parasimpático</li>
                        </ul>
                        
                        <h4>🏃‍♂️ Características en Atletas de Resistencia:</h4>
                        <ul>
                            <li><strong>HRV Elevada:</strong> Adaptación al entrenamiento de resistencia</li>
                            <li><strong>Recuperación Rápida:</strong> Sistema nervioso autónomo eficiente</li>
                            <li><strong>Variabilidad Consistente:</strong> Indicador de buena condición física</li>
                            <li><strong>Balance LF/HF:</strong> Equilibrio óptimo entre sistemas</li>
                        </ul>
                        
                        <h4>⚠️ Factores que Afectan HRV:</h4>
                        <ul>
                            <li><strong>Entrenamiento:</strong> Mejora la HRV con el tiempo</li>
                            <li><strong>Estrés:</strong> Reduce la variabilidad</li>
                            <li><strong>Sueño:</strong> Calidad del sueño influye en HRV</li>
                            <li><strong>Hidratación:</strong> Deshidratación puede reducir HRV</li>
                        </ul>
                    </div>
                    <div class="plot-container">
                        {hrv_html}
                    </div>
                </div>
                
                <div class="section">
                    <h2>📚 Descripción de Derivaciones ECG</h2>
                    <div class="info-box">
                        <h3>Derivaciones de Extremidades (Perspectiva Frontal)</h3>
                        <ul>
                            <li><strong>I:</strong> Diferencia de potencial entre brazo derecho e izquierdo</li>
                            <li><strong>II:</strong> Diferencia de potencial entre brazo derecho y pierna izquierda</li>
                            <li><strong>III:</strong> Diferencia de potencial entre brazo izquierdo y pierna izquierda</li>
                            <li><strong>aVR:</strong> Potencial promedio de brazos hacia brazo derecho</li>
                            <li><strong>aVL:</strong> Potencial promedio de brazos hacia brazo izquierdo</li>
                            <li><strong>aVF:</strong> Potencial promedio de brazos hacia piernas</li>
                        </ul>
                        
                        <h3>Derivaciones Precordiales (Perspectiva Horizontal)</h3>
                        <ul>
                            <li><strong>V1-V2:</strong> Vista del ventrículo derecho</li>
                            <li><strong>V3-V4:</strong> Vista del septo interventricular</li>
                            <li><strong>V5-V6:</strong> Vista del ventrículo izquierdo</li>
                        </ul>
                        
                        <h3>Características Típicas en Atletas de Resistencia</h3>
                        <ul>
                            <li><strong>Bradicardia sinusal:</strong> Frecuencia cardíaca baja en reposo (&lt;60 BPM)</li>
                            <li><strong>Arritmia sinusal:</strong> Variación normal en intervalos RR</li>
                            <li><strong>Hipertrofia ventricular izquierda benigna:</strong> Adaptación al entrenamiento</li>
                            <li><strong>Bloqueo AV de primer grado:</strong> PR prolongado pero normal</li>
                        </ul>
                    </div>
                </div>
                
                <div class="section">
                    <h2>🔬 Técnicas de Procesamiento Aplicadas</h2>
                    <div class="technique-box">
                        <h3>A. Transformada Rápida de Fourier (FFT) - Taller FFT</h3>
                        <ul>
                            <li>Implementación con <code>scipy.fft.fft()</code> para análisis espectral</li>
                            <li>Normalización correcta: <code>P2 = abs(Y/L)</code>, <code>P1 = P2[0:L//2+1]</code></li>
                            <li>Cálculo de vector de frecuencias: <code>f = Fs*np.arange(L//2+1)/L</code></li>
                            <li>Análisis de resolución frecuencial con diferentes tamaños FFT</li>
                            <li>Método de Welch para Densidad Espectral de Potencia (PSD)</li>
                            <li>Detección de picos espectrales con <code>scipy.signal.find_peaks()</code></li>
                        </ul>
                        
                        <h3>B. Filtrado Digital - Múltiples Talleres</h3>
                        <ul>
                            <li>Filtros Butterworth paso-banda (0.5-40 Hz)</li>
                            <li>Filtro paso-alto (0.5 Hz) para eliminar deriva de línea base</li>
                            <li>Filtro paso-bajo (40 Hz) para eliminar ruido de alta frecuencia</li>
                            <li>Filtro notch (50 Hz) para eliminar interferencia de red eléctrica</li>
                            <li>Aplicación de <code>scipy.signal.filtfilt()</code> para filtrado sin desfase</li>
                        </ul>
                        
                        <h3>C. Detección Automática de Picos R - Proyecto ICA ECG</h3>
                        <ul>
                            <li>Implementación con <code>scipy.signal.find_peaks()</code></li>
                            <li>Umbralización adaptativa basada en desviaciones estándar (3σ)</li>
                            <li>Período refractario (200ms) para evitar detecciones múltiples</li>
                            <li>Cálculo de frecuencia cardíaca instantánea</li>
                        </ul>
                        
                        <h3>D. Análisis de Variabilidad de Frecuencia Cardíaca (HRV)</h3>
                        <ul>
                            <li>Intervalos RR en milisegundos</li>
                            <li>SDNN: Desviación estándar de intervalos NN</li>
                            <li>RMSSD: Raíz cuadrada de la media de diferencias al cuadrado</li>
                            <li>Análisis en dominio de frecuencia: LF, HF, ratio LF/HF</li>
                        </ul>
                        
                        <h3>E. Normalización y Preprocesamiento - ICA</h3>
                        <ul>
                            <li>Centrado de señales (media cero)</li>
                            <li>Escalado y estandarización de amplitudes</li>
                            <li>Eliminación de artefactos por umbralización estadística</li>
                        </ul>
                        
                        <h3>F. Análisis Estadístico</h3>
                        <ul>
                            <li>Curtosis como medida de no-gaussianidad (momento de orden 4)</li>
                            <li>Análisis de correlación entre derivaciones</li>
                            <li>Medidas de independencia estadística</li>
                        </ul>
                    </div>
                </div>
                
                <div class="section">
                    <h2>📝 Conclusiones del Análisis</h2>
                    <div class="info-box">
                        <h3>Hallazgos Principales</h3>
                        <ul>
                            <li><strong>Prevalencia de bradicardia sinusal:</strong> Característica común en atletas de resistencia</li>
                            <li><strong>Patrones de arritmia sinusal:</strong> Adaptación fisiológica al entrenamiento</li>
                            <li><strong>Concordancia diagnóstica:</strong> Evaluación entre algoritmo SL12 y cardiólogo</li>
                            <li><strong>Características espectrales:</strong> Patrones distintivos en análisis FFT</li>
                            <li><strong>HRV elevada:</strong> Indicador de buena condición cardiovascular</li>
                        </ul>
                        
                        <h3>Implicaciones Clínicas</h3>
                        <ul>
                            <li>Diferencias significativas entre ECG de atletas y población general</li>
                            <li>Importancia de algoritmos especializados para interpretación en atletas</li>
                            <li>Necesidad de criterios específicos para evaluación de ECG en deportistas</li>
                            <li>Valor del análisis espectral para caracterización de adaptaciones cardíacas</li>
                        </ul>
                    </div>
                </div>
            </div>
            
            <script>
                // Datos de análisis disponibles
                const analysisData = {json.dumps(self.results, default=str)};
                
                // Actualizar visualizaciones basadas en atleta seleccionado
                function updateVisualizations() {{
                    const selectedAthlete = document.getElementById('athlete-select').value;
                    console.log('Actualizando visualizaciones para:', selectedAthlete);
                    
                    // Aquí se podrían actualizar las visualizaciones específicas del atleta
                    // Por ahora, las visualizaciones muestran datos estáticos del primer atleta
                    alert('Las visualizaciones muestran datos de ejemplo. Para visualizaciones dinámicas completas, se requeriría JavaScript adicional.');
                }}
                
                // Inicializar dashboard
                document.addEventListener('DOMContentLoaded', function() {{
                    console.log('Dashboard ECG cargado exitosamente');
                    console.log('Datos disponibles para', Object.keys(analysisData.individual_results).length, 'atletas');
                }});
            </script>
        </body>
        </html>
        """
        
        # Guardar archivo HTML
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"Dashboard HTML generado con visualizaciones: {output_file}")
        return output_file


def main():
    """
    Función principal para generar el dashboard
    """
    # Importar el procesador ECG
    from ecg_processor import ECGAnalyzer
    
    # Crear analizador y cargar datos
    analyzer = ECGAnalyzer("norwegian-endurance-athlete-ecg-database-1.0.0")
    analyzer.load_all_ecg_data()
    
    # Realizar análisis completo
    results = analyzer.analyze_all_records()
    
    # Crear generador de dashboard
    dashboard_gen = ECGDashboardGenerator(results)
    
    # Generar dashboard HTML
    dashboard_file = dashboard_gen.generate_html_dashboard()
    
    print(f"\nDashboard generado exitosamente: {dashboard_file}")
    print("Abre el archivo en tu navegador para ver las visualizaciones interactivas.")
    
    return dashboard_file


if __name__ == "__main__":
    main()
