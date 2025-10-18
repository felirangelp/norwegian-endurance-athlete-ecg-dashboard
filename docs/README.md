# 📚 Documentación del Proyecto - Norwegian Endurance Athlete ECG Database

## 🎯 Índice de Documentación

Esta carpeta contiene toda la documentación técnica y de proceso del proyecto de análisis ECG de atletas de resistencia noruegos.

### 📊 **Documentación Principal del Proyecto**

- **`context.md`** - Contexto del proyecto y descripción de los datos
- **`tecnicas.md`** - Técnicas de procesamiento de señales biológicas aplicadas
- **`README.md`** - Documentación principal del proyecto (en raíz)

### 🔧 **Documentación Técnica**

- **`GUIA_DASHBOARD_GITHUB_PAGES.md`** - Guía completa para publicar dashboards en GitHub Pages
- **`INSTRUCCIONES_CURSOR_AI.md`** - Instrucciones específicas para Cursor AI
- **`RESUMEN_SOLUCION_404.md`** - Resumen del problema 404 y su solución

### 🚀 **Documentación de GitHub**

- **`GITHUB_SETUP.md`** - Instrucciones para configurar GitHub
- **`GITHUB_PAGES.md`** - Guía para configurar GitHub Pages
- **`GITHUB_PAGES_STATUS.md`** - Estado actual de GitHub Pages
- **`ENABLE_PAGES.md`** - Instrucciones para habilitar GitHub Pages

### 📋 **Archivos de Configuración**

- **`CHANGELOG.md`** - Historial de cambios del proyecto
- **`VERSION`** - Versión actual del proyecto
- **`project.json`** - Metadatos del proyecto
- **`.gitignore`** - Configuración de archivos ignorados por Git

## 🎓 **Uso de la Documentación**

### **Para Futuros Proyectos de Dashboard:**

1. **Lee `GUIA_DASHBOARD_GITHUB_PAGES.md`** - Guía completa paso a paso
2. **Usa `INSTRUCCIONES_CURSOR_AI.md`** - Prompt específico para Cursor AI
3. **Consulta `RESUMEN_SOLUCION_404.md`** - Referencia rápida del problema más común

### **Para Configurar GitHub:**

1. **Sigue `GITHUB_SETUP.md`** - Configuración inicial del repositorio
2. **Usa `GITHUB_PAGES.md`** - Configuración de GitHub Pages
3. **Consulta `ENABLE_PAGES.md`** - Si tienes problemas con GitHub Pages

### **Para Entender el Proyecto:**

1. **Lee `context.md`** - Contexto y descripción de los datos
2. **Revisa `tecnicas.md`** - Técnicas implementadas
3. **Consulta `README.md`** - Documentación principal

## 🚨 **Problemas Comunes y Soluciones**

### **Error 404 en GitHub Pages:**
- **Causa:** Archivos HTML en `.gitignore`
- **Solución:** Ver `RESUMEN_SOLUCION_404.md`
- **Prevención:** Usar `INSTRUCCIONES_CURSOR_AI.md`

### **Dashboard no se actualiza:**
- **Causa:** Archivos no subidos al repositorio
- **Solución:** Verificar `git ls-files | grep html`
- **Prevención:** Seguir checklist en `GUIA_DASHBOARD_GITHUB_PAGES.md`

### **GitHub Pages no funciona:**
- **Causa:** GitHub Pages no habilitado
- **Solución:** Seguir `ENABLE_PAGES.md`
- **Prevención:** Verificar configuración en `GITHUB_PAGES.md`

## 📊 **Estructura del Proyecto**

```
proyecto/
├── docs/                           # 📚 Documentación completa
│   ├── GUIA_DASHBOARD_GITHUB_PAGES.md
│   ├── INSTRUCCIONES_CURSOR_AI.md
│   ├── RESUMEN_SOLUCION_404.md
│   ├── GITHUB_SETUP.md
│   ├── GITHUB_PAGES.md
│   ├── GITHUB_PAGES_STATUS.md
│   └── ENABLE_PAGES.md
├── src/                            # 🔧 Código fuente
│   ├── ecg_processor.py
│   ├── dashboard_generator.py
│   └── statistical_analysis.py
├── norwegian-endurance-athlete-ecg-database-1.0.0/  # 📊 Datos
├── index.html                      # 🏠 Página principal
├── dashboard.html                  # 📊 Dashboard interactivo
├── README.md                       # 📖 Documentación principal
├── context.md                      # 📋 Contexto del proyecto
├── tecnicas.md                     # 🔬 Técnicas implementadas
├── requirements.txt                # 📦 Dependencias
├── main.py                         # 🚀 Script principal
└── .gitignore                      # 🚫 Archivos ignorados
```

## 🎯 **Comandos de Verificación Rápida**

```bash
# Verificar que el dashboard funciona
git ls-files | grep html
git check-ignore dashboard.html

# Verificar estado de GitHub Pages
git status
git log --oneline -5

# Verificar archivos de documentación
ls docs/
```

## 📞 **Soporte y Contacto**

- **Proyecto:** Norwegian Endurance Athlete ECG Database
- **Autores:** Felipe Rangel, Nicolás Torres, Jorge
- **Institución:** Pontificia Universidad Javeriana
- **Curso:** Procesamiento de Señales Biológicas
- **Semestre:** 2025-1

---

**Última actualización:** Octubre 2025  
**Versión:** 1.1.0  
**Estado:** ✅ Completamente funcional
