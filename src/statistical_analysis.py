"""
Análisis Estadístico y Conclusiones - Proyecto ECG Atletas
Implementa análisis comparativo y conclusiones sobre los atletas de resistencia
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Any
import matplotlib.pyplot as plt
from scipy import stats
from collections import Counter


class ECGStatisticalAnalyzer:
    """
    Analizador estadístico para conclusiones sobre atletas de resistencia
    """
    
    def __init__(self, analysis_results: Dict[str, Any]):
        self.results = analysis_results
        self.summary_stats = analysis_results['summary_statistics']
        self.individual_results = analysis_results['individual_results']
        
    def analyze_heart_rate_patterns(self) -> Dict[str, Any]:
        """
        Análisis de patrones de frecuencia cardíaca en atletas
        """
        heart_rates = self.summary_stats['heart_rates']
        
        # Estadísticas descriptivas
        hr_stats = {
            'mean': np.mean(heart_rates),
            'std': np.std(heart_rates),
            'median': np.median(heart_rates),
            'min': np.min(heart_rates),
            'max': np.max(heart_rates),
            'q25': np.percentile(heart_rates, 25),
            'q75': np.percentile(heart_rates, 75)
        }
        
        # Clasificación de bradicardia
        bradycardia_count = sum(1 for hr in heart_rates if hr < 60)
        normal_count = sum(1 for hr in heart_rates if 60 <= hr < 100)
        tachycardia_count = sum(1 for hr in heart_rates if hr >= 100)
        
        hr_classification = {
            'bradycardia': bradycardia_count,
            'normal': normal_count,
            'tachycardia': tachycardia_count,
            'bradycardia_percentage': (bradycardia_count / len(heart_rates)) * 100
        }
        
        return {
            'descriptive_stats': hr_stats,
            'classification': hr_classification,
            'raw_data': heart_rates
        }
    
    def analyze_hrv_patterns(self) -> Dict[str, Any]:
        """
        Análisis de patrones de variabilidad de frecuencia cardíaca
        """
        sdnn_values = self.summary_stats['hrv_sdnn']
        rmssd_values = self.summary_stats['hrv_rmssd']
        
        # Estadísticas HRV
        hrv_stats = {
            'sdnn': {
                'mean': np.mean(sdnn_values),
                'std': np.std(sdnn_values),
                'median': np.median(sdnn_values),
                'min': np.min(sdnn_values),
                'max': np.max(sdnn_values)
            },
            'rmssd': {
                'mean': np.mean(rmssd_values),
                'std': np.std(rmssd_values),
                'median': np.median(rmssd_values),
                'min': np.min(rmssd_values),
                'max': np.max(rmssd_values)
            }
        }
        
        # Clasificación de HRV según estándares
        # SDNN > 50ms se considera buena variabilidad
        good_sdnn = sum(1 for sdnn in sdnn_values if sdnn > 50)
        good_rmssd = sum(1 for rmssd in rmssd_values if rmssd > 30)
        
        hrv_classification = {
            'good_sdnn_count': good_sdnn,
            'good_sdnn_percentage': (good_sdnn / len(sdnn_values)) * 100,
            'good_rmssd_count': good_rmssd,
            'good_rmssd_percentage': (good_rmssd / len(rmssd_values)) * 100
        }
        
        return {
            'descriptive_stats': hrv_stats,
            'classification': hrv_classification,
            'raw_data': {
                'sdnn': sdnn_values,
                'rmssd': rmssd_values
            }
        }
    
    def analyze_diagnostic_concordance(self) -> Dict[str, Any]:
        """
        Análisis de concordancia entre diagnósticos SL12 y cardiólogo
        """
        sl12_diagnoses = self.summary_stats['sl12_diagnoses']
        cardiologist_diagnoses = self.summary_stats['cardiologist_diagnoses']
        
        # Contar diagnósticos únicos
        sl12_counts = Counter(sl12_diagnoses)
        cardio_counts = Counter(cardiologist_diagnoses)
        
        # Análisis de concordancia
        concordant_cases = 0
        total_cases = len(sl12_diagnoses)
        
        for i in range(total_cases):
            sl12_diag = sl12_diagnoses[i].lower()
            cardio_diag = cardiologist_diagnoses[i].lower()
            
            # Normalizar diagnósticos para comparación
            if self._normalize_diagnosis(sl12_diag) == self._normalize_diagnosis(cardio_diag):
                concordant_cases += 1
        
        concordance_rate = (concordant_cases / total_cases) * 100
        
        # Análisis de discrepancias
        discrepancies = []
        for i in range(total_cases):
            sl12_diag = sl12_diagnoses[i]
            cardio_diag = cardiologist_diagnoses[i]
            if sl12_diag != cardio_diag:
                discrepancies.append({
                    'record': list(self.individual_results.keys())[i],
                    'sl12': sl12_diag,
                    'cardiologist': cardio_diag
                })
        
        return {
            'concordance_rate': concordance_rate,
            'concordant_cases': concordant_cases,
            'total_cases': total_cases,
            'sl12_distribution': dict(sl12_counts),
            'cardiologist_distribution': dict(cardio_counts),
            'discrepancies': discrepancies
        }
    
    def _normalize_diagnosis(self, diagnosis: str) -> str:
        """
        Normaliza diagnósticos para comparación
        """
        diagnosis = diagnosis.lower()
        
        # Mapeo de términos similares
        if 'normal' in diagnosis or 'sinus' in diagnosis:
            return 'normal'
        elif 'bradycardia' in diagnosis:
            return 'bradycardia'
        elif 'arrhythmia' in diagnosis:
            return 'arrhythmia'
        elif 'borderline' in diagnosis:
            return 'borderline'
        else:
            return diagnosis
    
    def analyze_spectral_characteristics(self) -> Dict[str, Any]:
        """
        Análisis de características espectrales de las señales ECG
        """
        dominant_frequencies = []
        spectral_powers = []
        
        for record_name, record_data in self.individual_results.items():
            fft_results = record_data['fft_results']
            
            for lead_name, lead_data in fft_results.items():
                dominant_freq = lead_data['dominant_freq']
                max_power = np.max(lead_data['magnitude'])
                
                dominant_frequencies.append(dominant_freq)
                spectral_powers.append(max_power)
        
        # Estadísticas espectrales
        spectral_stats = {
            'dominant_freq': {
                'mean': np.mean(dominant_frequencies),
                'std': np.std(dominant_frequencies),
                'median': np.median(dominant_frequencies),
                'range': [np.min(dominant_frequencies), np.max(dominant_frequencies)]
            },
            'spectral_power': {
                'mean': np.mean(spectral_powers),
                'std': np.std(spectral_powers),
                'median': np.median(spectral_powers),
                'range': [np.min(spectral_powers), np.max(spectral_powers)]
            }
        }
        
        return {
            'descriptive_stats': spectral_stats,
            'raw_data': {
                'dominant_frequencies': dominant_frequencies,
                'spectral_powers': spectral_powers
            }
        }
    
    def analyze_correlation_patterns(self) -> Dict[str, Any]:
        """
        Análisis de patrones de correlación entre derivaciones
        """
        correlation_matrices = []
        
        for record_name, record_data in self.individual_results.items():
            corr_matrix = record_data['correlation_matrix']
            correlation_matrices.append(corr_matrix)
        
        # Promedio de matrices de correlación
        mean_correlation = np.mean(correlation_matrices, axis=0)
        
        # Análisis de correlaciones específicas
        leads = ['I', 'II', 'III', 'aVR', 'aVL', 'aVF', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6']
        
        # Correlaciones más altas y más bajas
        correlations = []
        for i in range(len(leads)):
            for j in range(i+1, len(leads)):
                correlations.append({
                    'leads': f"{leads[i]}-{leads[j]}",
                    'correlation': mean_correlation[i, j]
                })
        
        correlations.sort(key=lambda x: abs(x['correlation']), reverse=True)
        
        return {
            'mean_correlation_matrix': mean_correlation,
            'highest_correlations': correlations[:5],
            'lowest_correlations': correlations[-5:],
            'correlation_stats': {
                'mean': np.mean(mean_correlation[np.triu_indices_from(mean_correlation, k=1)]),
                'std': np.std(mean_correlation[np.triu_indices_from(mean_correlation, k=1)]),
                'max': np.max(mean_correlation[np.triu_indices_from(mean_correlation, k=1)]),
                'min': np.min(mean_correlation[np.triu_indices_from(mean_correlation, k=1)])
            }
        }
    
    def generate_comprehensive_conclusions(self) -> Dict[str, Any]:
        """
        Genera conclusiones comprehensivas del análisis
        """
        # Realizar todos los análisis
        hr_analysis = self.analyze_heart_rate_patterns()
        hrv_analysis = self.analyze_hrv_patterns()
        diagnostic_analysis = self.analyze_diagnostic_concordance()
        spectral_analysis = self.analyze_spectral_characteristics()
        correlation_analysis = self.analyze_correlation_patterns()
        
        # Conclusiones principales
        conclusions = {
            'heart_rate_findings': {
                'summary': f"Los atletas muestran una frecuencia cardíaca promedio de {hr_analysis['descriptive_stats']['mean']:.1f} BPM",
                'bradycardia_prevalence': f"{hr_analysis['classification']['bradycardia_percentage']:.1f}% de los atletas presentan bradicardia sinusal",
                'clinical_interpretation': "La bradicardia sinusal es una adaptación fisiológica común en atletas de resistencia"
            },
            'hrv_findings': {
                'summary': f"HRV promedio: SDNN = {hrv_analysis['descriptive_stats']['sdnn']['mean']:.1f}ms, RMSSD = {hrv_analysis['descriptive_stats']['rmssd']['mean']:.1f}ms",
                'good_variability': f"{hrv_analysis['classification']['good_sdnn_percentage']:.1f}% tienen buena variabilidad (SDNN > 50ms)",
                'clinical_interpretation': "La HRV elevada indica buena condición cardiovascular y adaptación al entrenamiento"
            },
            'diagnostic_concordance': {
                'summary': f"Concordancia entre SL12 y cardiólogo: {diagnostic_analysis['concordance_rate']:.1f}%",
                'discrepancies': f"{len(diagnostic_analysis['discrepancies'])} casos con diagnósticos diferentes",
                'clinical_interpretation': "La concordancia moderada sugiere la necesidad de algoritmos especializados para atletas"
            },
            'spectral_findings': {
                'summary': f"Frecuencia dominante promedio: {spectral_analysis['descriptive_stats']['dominant_freq']['mean']:.2f} Hz",
                'power_distribution': f"Potencia espectral promedio: {spectral_analysis['descriptive_stats']['spectral_power']['mean']:.2f}",
                'clinical_interpretation': "Las características espectrales reflejan la actividad eléctrica cardíaca adaptada al entrenamiento"
            },
            'correlation_findings': {
                'summary': f"Correlación promedio entre derivaciones: {correlation_analysis['correlation_stats']['mean']:.3f}",
                'highest_correlation': f"Mayor correlación: {correlation_analysis['highest_correlations'][0]['leads']} ({correlation_analysis['highest_correlations'][0]['correlation']:.3f})",
                'clinical_interpretation': "Los patrones de correlación reflejan la coherencia de la actividad eléctrica cardíaca"
            }
        }
        
        # Implicaciones clínicas
        clinical_implications = {
            'athlete_specific_criteria': "Los criterios estándar de ECG pueden no ser apropiados para atletas de resistencia",
            'algorithm_development': "Se necesitan algoritmos especializados que consideren las adaptaciones cardíacas del entrenamiento",
            'screening_protocols': "Los protocolos de screening deben incluir análisis de HRV y características espectrales",
            'monitoring_recommendations': "El monitoreo continuo puede detectar cambios en la adaptación cardíaca al entrenamiento"
        }
        
        # Limitaciones del estudio
        limitations = {
            'sample_size': "Muestra relativamente pequeña (28 atletas) limita la generalización",
            'single_recording': "Registros de solo 10 segundos pueden no capturar variabilidad completa",
            'no_echocardiography': "Falta de datos ecocardiográficos para confirmar adaptaciones estructurales",
            'cross_sectional': "Diseño transversal no permite evaluar cambios temporales"
        }
        
        return {
            'detailed_analyses': {
                'heart_rate': hr_analysis,
                'hrv': hrv_analysis,
                'diagnostic_concordance': diagnostic_analysis,
                'spectral': spectral_analysis,
                'correlation': correlation_analysis
            },
            'conclusions': conclusions,
            'clinical_implications': clinical_implications,
            'limitations': limitations,
            'recommendations': {
                'future_work': [
                    "Estudios longitudinales para evaluar cambios temporales",
                    "Integración con datos ecocardiográficos",
                    "Desarrollo de algoritmos específicos para atletas",
                    "Análisis de diferentes disciplinas deportivas"
                ],
                'clinical_practice': [
                    "Considerar características específicas de atletas en interpretación ECG",
                    "Incluir análisis de HRV en evaluaciones cardíacas",
                    "Desarrollar protocolos de screening especializados",
                    "Monitoreo continuo de adaptaciones cardíacas"
                ]
            }
        }


def main():
    """
    Función principal para ejecutar el análisis estadístico
    """
    # Importar el procesador ECG
    from ecg_processor import ECGAnalyzer
    
    # Crear analizador y cargar datos
    analyzer = ECGAnalyzer("norwegian-endurance-athlete-ecg-database-1.0.0")
    analyzer.load_all_ecg_data()
    
    # Realizar análisis completo
    results = analyzer.analyze_all_records()
    
    # Crear analizador estadístico
    stat_analyzer = ECGStatisticalAnalyzer(results)
    
    # Generar conclusiones comprehensivas
    conclusions = stat_analyzer.generate_comprehensive_conclusions()
    
    print("\n" + "="*80)
    print("CONCLUSIONES DEL ANÁLISIS ECG - ATLETAS DE RESISTENCIA")
    print("="*80)
    
    print("\n📊 HALLAZGOS PRINCIPALES:")
    print("-" * 40)
    
    print(f"\n💓 FRECUENCIA CARDÍACA:")
    print(f"   • Promedio: {conclusions['conclusions']['heart_rate_findings']['summary']}")
    print(f"   • Bradicardia: {conclusions['conclusions']['heart_rate_findings']['bradycardia_prevalence']}")
    print(f"   • Interpretación: {conclusions['conclusions']['heart_rate_findings']['clinical_interpretation']}")
    
    print(f"\n🔄 VARIABILIDAD DE FRECUENCIA CARDÍACA:")
    print(f"   • {conclusions['conclusions']['hrv_findings']['summary']}")
    print(f"   • Buena variabilidad: {conclusions['conclusions']['hrv_findings']['good_variability']}")
    print(f"   • Interpretación: {conclusions['conclusions']['hrv_findings']['clinical_interpretation']}")
    
    print(f"\n🔍 CONCORDANCIA DIAGNÓSTICA:")
    print(f"   • {conclusions['conclusions']['diagnostic_concordance']['summary']}")
    print(f"   • Discrepancias: {conclusions['conclusions']['diagnostic_concordance']['discrepancies']}")
    print(f"   • Interpretación: {conclusions['conclusions']['diagnostic_concordance']['clinical_interpretation']}")
    
    print(f"\n📈 ANÁLISIS ESPECTRAL:")
    print(f"   • {conclusions['conclusions']['spectral_findings']['summary']}")
    print(f"   • Distribución de potencia: {conclusions['conclusions']['spectral_findings']['power_distribution']}")
    print(f"   • Interpretación: {conclusions['conclusions']['spectral_findings']['clinical_interpretation']}")
    
    print(f"\n🔗 CORRELACIONES:")
    print(f"   • {conclusions['conclusions']['correlation_findings']['summary']}")
    print(f"   • Mayor correlación: {conclusions['conclusions']['correlation_findings']['highest_correlation']}")
    print(f"   • Interpretación: {conclusions['conclusions']['correlation_findings']['clinical_interpretation']}")
    
    print("\n🏥 IMPLICACIONES CLÍNICAS:")
    print("-" * 40)
    for key, implication in conclusions['clinical_implications'].items():
        print(f"   • {implication}")
    
    print("\n⚠️ LIMITACIONES DEL ESTUDIO:")
    print("-" * 40)
    for key, limitation in conclusions['limitations'].items():
        print(f"   • {limitation}")
    
    print("\n📋 RECOMENDACIONES:")
    print("-" * 40)
    print("   Trabajo Futuro:")
    for rec in conclusions['recommendations']['future_work']:
        print(f"   • {rec}")
    
    print("\n   Práctica Clínica:")
    for rec in conclusions['recommendations']['clinical_practice']:
        print(f"   • {rec}")
    
    print("\n" + "="*80)
    
    return conclusions


if __name__ == "__main__":
    conclusions = main()
