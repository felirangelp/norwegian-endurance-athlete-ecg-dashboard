"""
Procesador de Datos ECG - Norwegian Endurance Athlete Database
Implementa técnicas de procesamiento de señales biológicas vistas en el semestre
"""

import wfdb
import numpy as np
import scipy.signal
from scipy.fft import fft, fftfreq
from scipy.signal import butter, filtfilt, welch, find_peaks
import pandas as pd
import os
import re
from typing import Dict, List, Tuple, Any
import warnings
warnings.filterwarnings('ignore')


class ECGAnalyzer:
    """
    Clase principal para análisis de señales ECG implementando técnicas del semestre
    """
    
    def __init__(self, data_path: str):
        self.data_path = data_path
        self.fs = 500  # Frecuencia de muestreo
        self.duration = 10  # Duración en segundos
        self.n_samples = self.fs * self.duration  # 5000 muestras
        
        # Derivaciones ECG estándar
        self.leads = ['I', 'II', 'III', 'aVR', 'aVL', 'aVF', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6']
        
        # Datos cargados
        self.ecg_data = {}
        self.metadata = {}
        
    def load_all_ecg_data(self) -> None:
        """
        Carga todos los registros ECG desde archivos .dat/.hea usando wfdb
        """
        print("Cargando datos ECG...")
        
        for i in range(1, 29):  # ath_001 a ath_028
            record_name = f"ath_{i:03d}"
            try:
                # Cargar señal y metadatos
                signal, fields = wfdb.rdsamp(os.path.join(self.data_path, record_name))
                
                # Extraer diagnósticos del header
                sl12_diagnosis = ""
                cardiologist_diagnosis = ""
                
                # Leer el archivo .hea directamente para extraer diagnósticos
                hea_file = os.path.join(self.data_path, record_name + '.hea')
                try:
                    with open(hea_file, 'r') as f:
                        lines = f.readlines()
                        for line in lines:
                            line = line.strip()
                            if line.startswith('#SL12:'):
                                sl12_diagnosis = line.replace('#SL12:', '').strip()
                            elif line.startswith('#C:'):
                                cardiologist_diagnosis = line.replace('#C:', '').strip()
                except Exception as e:
                    print(f"Error leyendo archivo .hea para {record_name}: {e}")
                
                # También intentar desde fields si está disponible
                if not sl12_diagnosis and 'comments' in fields:
                    for comment in fields['comments']:
                        if comment.startswith('#SL12:'):
                            sl12_diagnosis = comment.replace('#SL12:', '').strip()
                        elif comment.startswith('#C:'):
                            cardiologist_diagnosis = comment.replace('#C:', '').strip()
                
                # Almacenar datos
                self.ecg_data[record_name] = {
                    'signal': signal,  # Shape: (5000, 12)
                    'leads': self.leads,
                    'fs': self.fs,
                    'duration': self.duration
                }
                
                self.metadata[record_name] = {
                    'sl12_diagnosis': sl12_diagnosis,
                    'cardiologist_diagnosis': cardiologist_diagnosis,
                    'n_leads': fields.get('n_sig', 12),
                    'n_samples': fields.get('sig_len', 5000)
                }
                
                print(f"✓ Cargado {record_name}")
                
            except Exception as e:
                print(f"✗ Error cargando {record_name}: {e}")
        
        print(f"Total de registros cargados: {len(self.ecg_data)}")
    
    def apply_digital_filtering(self, signal: np.ndarray, filter_type: str = 'bandpass') -> np.ndarray:
        """
        Aplica filtrado digital usando filtros Butterworth - Visto en múltiples talleres
        
        Args:
            signal: Señal ECG (n_samples, n_leads)
            filter_type: Tipo de filtro ('bandpass', 'highpass', 'lowpass', 'notch')
        
        Returns:
            Señal filtrada
        """
        filtered_signal = np.zeros_like(signal)
        
        for lead_idx in range(signal.shape[1]):
            lead_signal = signal[:, lead_idx]
            
            if filter_type == 'bandpass':
                # Filtro paso-banda (0.5-40 Hz) - elimina ruido de línea base y alta frecuencia
                nyquist = self.fs / 2
                low = 0.5 / nyquist
                high = 40 / nyquist
                b, a = butter(4, [low, high], btype='band')
                
            elif filter_type == 'highpass':
                # Filtro paso-alto (0.5 Hz) - elimina deriva de línea base
                cutoff = 0.5 / nyquist
                b, a = butter(4, cutoff, btype='high')
                
            elif filter_type == 'lowpass':
                # Filtro paso-bajo (40 Hz) - elimina ruido de alta frecuencia
                cutoff = 40 / nyquist
                b, a = butter(4, cutoff, btype='low')
                
            elif filter_type == 'notch':
                # Filtro notch (50 Hz) - elimina interferencia de red eléctrica
                notch_freq = 50
                quality_factor = 30
                b, a = butter(2, [notch_freq - 2, notch_freq + 2], btype='bandstop')
            
            # Aplicar filtro sin desfase usando filtfilt
            filtered_signal[:, lead_idx] = filtfilt(b, a, lead_signal)
        
        return filtered_signal
    
    def detect_r_peaks(self, signal: np.ndarray, lead_idx: int = 1) -> np.ndarray:
        """
        Detección automática de picos R usando scipy.signal.find_peaks - Visto en Proyecto ICA ECG
        
        Args:
            signal: Señal ECG filtrada (n_samples, n_leads)
            lead_idx: Índice de la derivación a usar (por defecto II)
        
        Returns:
            Array con índices de los picos R detectados
        """
        lead_signal = signal[:, lead_idx]
        
        # Umbralización adaptativa basada en desviaciones estándar (3σ)
        threshold = np.mean(lead_signal) + 3 * np.std(lead_signal)
        
        # Detección de picos con período refractario
        refractory_period = int(0.2 * self.fs)  # 200ms a 500Hz = 100 muestras
        
        peaks, _ = find_peaks(
            lead_signal,
            height=threshold,
            distance=refractory_period,
            prominence=np.std(lead_signal)
        )
        
        return peaks
    
    def calculate_hrv_metrics(self, rr_intervals: np.ndarray) -> Dict[str, float]:
        """
        Calcula métricas de Variabilidad de Frecuencia Cardíaca (HRV)
        
        Args:
            rr_intervals: Intervalos RR en milisegundos
        
        Returns:
            Diccionario con métricas HRV
        """
        if len(rr_intervals) < 2:
            return {'sdnn': 0, 'rmssd': 0, 'mean_hr': 0}
        
        # Métricas en dominio del tiempo
        sdnn = np.std(rr_intervals)  # Desviación estándar de intervalos NN
        
        # RMSSD - raíz cuadrada de la media de diferencias al cuadrado
        rr_diffs = np.diff(rr_intervals)
        rmssd = np.sqrt(np.mean(rr_diffs**2))
        
        # Frecuencia cardíaca promedio
        mean_hr = 60000 / np.mean(rr_intervals)  # BPM
        
        return {
            'sdnn': sdnn,
            'rmssd': rmssd,
            'mean_hr': mean_hr,
            'n_beats': len(rr_intervals)
        }
    
    def perform_fft_analysis(self, signal: np.ndarray, fft_size: int = 1024) -> Dict[str, np.ndarray]:
        """
        Análisis espectral usando FFT - Visto en Taller FFT
        
        Args:
            signal: Señal ECG (n_samples, n_leads)
            fft_size: Tamaño de la FFT
        
        Returns:
            Diccionario con resultados del análisis espectral
        """
        results = {}
        
        for lead_idx, lead_name in enumerate(self.leads):
            lead_signal = signal[:, lead_idx]
            
            # Aplicar ventana de Hamming para reducir leakage
            windowed_signal = lead_signal * np.hamming(len(lead_signal))
            
            # FFT con normalización correcta
            Y = fft(windowed_signal, fft_size)
            L = len(windowed_signal)
            
            # Normalización: P2 = abs(Y/L), P1 = P2[0:L//2+1], P1[1:-1] = 2*P1[1:-1]
            P2 = np.abs(Y / L)
            P1 = P2[0:L//2+1]
            P1[1:-1] = 2 * P1[1:-1]
            
            # Vector de frecuencias: f = Fs*np.arange(L//2+1)/L
            f = self.fs * np.arange(L//2+1) / L
            
            # Método de Welch para PSD
            f_welch, psd = welch(lead_signal, fs=self.fs, nperseg=256)
            
            # Detección de picos espectrales
            peaks, properties = find_peaks(P1, height=np.max(P1)*0.1, distance=10)
            peak_freqs = f[peaks]
            peak_magnitudes = P1[peaks]
            
            results[lead_name] = {
                'frequencies': f,
                'magnitude': P1,
                'welch_freq': f_welch,
                'psd': psd,
                'peak_freqs': peak_freqs,
                'peak_magnitudes': peak_magnitudes,
                'dominant_freq': f[np.argmax(P1)]
            }
        
        return results
    
    def calculate_statistical_metrics(self, signal: np.ndarray) -> Dict[str, float]:
        """
        Calcula métricas estadísticas incluyendo curtosis - Visto en ICA
        
        Args:
            signal: Señal ECG (n_samples, n_leads)
        
        Returns:
            Diccionario con métricas estadísticas
        """
        metrics = {}
        
        for lead_idx, lead_name in enumerate(self.leads):
            lead_signal = signal[:, lead_idx]
            
            # Curtosis como medida de no-gaussianidad (momento de orden 4)
            from scipy.stats import kurtosis
            kurt = kurtosis(lead_signal)
            
            # Estadísticas básicas
            mean_val = np.mean(lead_signal)
            std_val = np.std(lead_signal)
            skewness = scipy.stats.skew(lead_signal)
            
            metrics[lead_name] = {
                'mean': mean_val,
                'std': std_val,
                'kurtosis': kurt,
                'skewness': skewness,
                'rms': np.sqrt(np.mean(lead_signal**2))
            }
        
        return metrics
    
    def analyze_single_record(self, record_name: str) -> Dict[str, Any]:
        """
        Análisis completo de un registro ECG individual
        
        Args:
            record_name: Nombre del registro (ej: 'ath_001')
        
        Returns:
            Diccionario con todos los resultados del análisis
        """
        if record_name not in self.ecg_data:
            raise ValueError(f"Registro {record_name} no encontrado")
        
        signal = self.ecg_data[record_name]['signal']
        
        # 1. Filtrado digital
        filtered_signal = self.apply_digital_filtering(signal, 'bandpass')
        
        # 2. Detección de picos R
        r_peaks = self.detect_r_peaks(filtered_signal)
        
        # 3. Cálculo de intervalos RR y HRV
        if len(r_peaks) > 1:
            rr_intervals = np.diff(r_peaks) * (1000 / self.fs)  # Convertir a ms
            hrv_metrics = self.calculate_hrv_metrics(rr_intervals)
        else:
            rr_intervals = np.array([])
            hrv_metrics = {'sdnn': 0, 'rmssd': 0, 'mean_hr': 0, 'n_beats': 0}
        
        # 4. Análisis FFT
        fft_results = self.perform_fft_analysis(filtered_signal)
        
        # 5. Métricas estadísticas
        statistical_metrics = self.calculate_statistical_metrics(filtered_signal)
        
        # 6. Análisis de correlación entre derivaciones
        correlation_matrix = np.corrcoef(filtered_signal.T)
        
        return {
            'record_name': record_name,
            'raw_signal': signal,
            'filtered_signal': filtered_signal,
            'r_peaks': r_peaks,
            'rr_intervals': rr_intervals,
            'hrv_metrics': hrv_metrics,
            'fft_results': fft_results,
            'statistical_metrics': statistical_metrics,
            'correlation_matrix': correlation_matrix,
            'metadata': self.metadata[record_name]
        }
    
    def analyze_all_records(self) -> Dict[str, Any]:
        """
        Análisis completo de todos los registros ECG
        
        Returns:
            Diccionario con resultados de todos los análisis
        """
        print("Iniciando análisis completo de todos los registros...")
        
        all_results = {}
        summary_stats = {
            'heart_rates': [],
            'hrv_sdnn': [],
            'hrv_rmssd': [],
            'sl12_diagnoses': [],
            'cardiologist_diagnoses': []
        }
        
        for record_name in self.ecg_data.keys():
            print(f"Analizando {record_name}...")
            
            try:
                results = self.analyze_single_record(record_name)
                all_results[record_name] = results
                
                # Acumular estadísticas para análisis comparativo
                summary_stats['heart_rates'].append(results['hrv_metrics']['mean_hr'])
                summary_stats['hrv_sdnn'].append(results['hrv_metrics']['sdnn'])
                summary_stats['hrv_rmssd'].append(results['hrv_metrics']['rmssd'])
                summary_stats['sl12_diagnoses'].append(results['metadata']['sl12_diagnosis'])
                summary_stats['cardiologist_diagnoses'].append(results['metadata']['cardiologist_diagnosis'])
                
            except Exception as e:
                print(f"Error analizando {record_name}: {e}")
        
        # Estadísticas agregadas
        summary_stats['mean_hr'] = np.mean(summary_stats['heart_rates'])
        summary_stats['std_hr'] = np.std(summary_stats['heart_rates'])
        summary_stats['mean_sdnn'] = np.mean(summary_stats['hrv_sdnn'])
        summary_stats['mean_rmssd'] = np.mean(summary_stats['hrv_rmssd'])
        
        return {
            'individual_results': all_results,
            'summary_statistics': summary_stats,
            'total_records': len(all_results)
        }


def main():
    """
    Función principal para ejecutar el análisis
    """
    # Ruta a los datos
    data_path = "norwegian-endurance-athlete-ecg-database-1.0.0"
    
    # Crear analizador
    analyzer = ECGAnalyzer(data_path)
    
    # Cargar datos
    analyzer.load_all_ecg_data()
    
    # Realizar análisis completo
    results = analyzer.analyze_all_records()
    
    print(f"\nAnálisis completado:")
    print(f"- Total de registros procesados: {results['total_records']}")
    print(f"- Frecuencia cardíaca promedio: {results['summary_statistics']['mean_hr']:.1f} BPM")
    print(f"- HRV SDNN promedio: {results['summary_statistics']['mean_sdnn']:.1f} ms")
    print(f"- HRV RMSSD promedio: {results['summary_statistics']['mean_rmssd']:.1f} ms")
    
    return results


if __name__ == "__main__":
    results = main()
