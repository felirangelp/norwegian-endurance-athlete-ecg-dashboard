# 📊 Guía Completa: Publicación de Dashboards en GitHub Pages

## 🎯 Resumen Ejecutivo

Esta guía documenta el proceso completo para publicar dashboards interactivos en GitHub Pages, incluyendo la solución al problema común del error 404 que ocurre cuando los archivos HTML están en `.gitignore`.

## 🚨 Problema Común: Error 404 en GitHub Pages

### ❌ **Síntomas:**
- Dashboard funciona localmente pero muestra "404 File not found" en GitHub Pages
- Página principal carga pero el dashboard específico no
- Error: "The site configured at this address does not contain the requested file"

### 🔍 **Causa Raíz:**
El archivo del dashboard (ej: `dashboard.html`) está siendo ignorado por Git debido a reglas en `.gitignore`, por lo que nunca se sube al repositorio.

### ✅ **Solución:**
1. Verificar qué archivos están siendo ignorados
2. Comentar o modificar las reglas de `.gitignore`
3. Agregar los archivos necesarios al repositorio
4. Hacer commit y push

---

## 📋 Instrucciones para Cursor AI

### 🎯 **Prompt Inicial para Nuevos Proyectos:**

```
Necesito crear un dashboard interactivo con Plotly que se publique en GitHub Pages. 

REQUISITOS:
1. Crear un dashboard HTML interactivo con Plotly
2. Configurar GitHub Pages para publicación
3. Asegurar que todos los archivos HTML se suban correctamente
4. Evitar errores 404 comunes

ARCHIVOS NECESARIOS:
- dashboard.html (dashboard principal)
- index.html (página de entrada)
- .gitignore (configurado correctamente)
- README.md (con instrucciones)

CONFIGURACIÓN .GITIGNORE:
- NO ignorar archivos HTML del dashboard
- Ignorar solo archivos temporales y de desarrollo
- Comentar reglas que puedan causar problemas

VERIFICACIÓN:
- Confirmar que todos los archivos HTML están en el repositorio
- Probar que GitHub Pages funciona correctamente
- Documentar el proceso para futuros proyectos
```

---

## 🔧 Proceso Paso a Paso

### **Paso 1: Configuración Inicial del Proyecto**

```bash
# Crear directorio del proyecto
mkdir mi-dashboard-proyecto
cd mi-dashboard-proyecto

# Inicializar Git
git init

# Crear estructura básica
mkdir src
mkdir docs
```

### **Paso 2: Configuración Correcta de .gitignore**

```bash
# Crear .gitignore con configuración correcta
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
pip-wheel-metadata/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual Environment
venv/
env/
ENV/
env.bak/
venv.bak/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Jupyter Notebook
.ipynb_checkpoints

# Generated files - IMPORTANTE: NO ignorar archivos HTML del dashboard
# dashboard.html  # Comentado para permitir que se suba a GitHub Pages
# *.html          # NO ignorar archivos HTML
*.log

# Temporary files
*.tmp
*.temp

# Data files (opcional)
# data/
# *.csv
# *.json
EOF
```

### **Paso 3: Crear Archivos del Dashboard**

#### **dashboard.html (Dashboard Principal)**
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mi Dashboard Interactivo</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 20px;
            background: #f5f5f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            padding: 20px;
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 2px solid #e0e0e0;
        }
        .chart-container {
            margin: 20px 0;
            padding: 20px;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Mi Dashboard Interactivo</h1>
            <p>Visualizaciones interactivas con Plotly</p>
        </div>
        
        <div class="chart-container">
            <div id="grafico1"></div>
        </div>
        
        <div class="chart-container">
            <div id="grafico2"></div>
        </div>
    </div>

    <script>
        // Ejemplo de gráfico con Plotly
        var trace1 = {
            x: [1, 2, 3, 4, 5],
            y: [1, 4, 9, 16, 25],
            type: 'scatter',
            mode: 'lines+markers',
            name: 'Datos de Ejemplo'
        };

        var data = [trace1];
        var layout = {
            title: 'Gráfico de Ejemplo',
            xaxis: { title: 'Eje X' },
            yaxis: { title: 'Eje Y' }
        };

        Plotly.newPlot('grafico1', data, layout);

        // Segundo gráfico
        var trace2 = {
            labels: ['A', 'B', 'C', 'D'],
            values: [20, 30, 25, 25],
            type: 'pie'
        };

        var data2 = [trace2];
        var layout2 = {
            title: 'Gráfico de Pastel'
        };

        Plotly.newPlot('grafico2', data2, layout2);
    </script>
</body>
</html>
```

#### **index.html (Página de Entrada)**
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mi Dashboard - Página Principal</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            padding: 40px 20px;
            text-align: center;
        }
        .header {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            padding: 40px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }
        .header h1 {
            color: #2c3e50;
            font-size: 2.5em;
            margin: 0 0 20px 0;
        }
        .header p {
            color: #7f8c8d;
            font-size: 1.2em;
            margin: 0 0 30px 0;
        }
        .dashboard-button {
            display: inline-block;
            padding: 20px 40px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-decoration: none;
            border-radius: 12px;
            font-size: 1.2em;
            font-weight: bold;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }
        .dashboard-button:hover {
            transform: translateY(-3px);
            box-shadow: 0 6px 20px rgba(0,0,0,0.3);
        }
        .features {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }
        .feature {
            background: rgba(255, 255, 255, 0.9);
            padding: 20px;
            border-radius: 10px;
            border-left: 4px solid #667eea;
        }
        .feature h3 {
            margin: 0 0 10px 0;
            color: #2c3e50;
        }
        .feature p {
            margin: 0;
            color: #666;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Mi Dashboard Interactivo</h1>
            <p>Visualizaciones interactivas con Plotly</p>
            
            <a href="./dashboard.html" class="dashboard-button">
                🚀 Abrir Dashboard Completo
            </a>
        </div>
        
        <div class="features">
            <div class="feature">
                <h3>📈 Gráficos Interactivos</h3>
                <p>Visualizaciones dinámicas con Plotly</p>
            </div>
            <div class="feature">
                <h3>📊 Análisis de Datos</h3>
                <p>Procesamiento y análisis completo</p>
            </div>
            <div class="feature">
                <h3>🎯 Técnicas Avanzadas</h3>
                <p>Implementación de métodos especializados</p>
            </div>
        </div>
    </div>
</body>
</html>
```

### **Paso 4: Configuración de Git y GitHub**

```bash
# Agregar archivos al repositorio
git add .

# Verificar que los archivos HTML están incluidos
git status

# Hacer commit inicial
git commit -m "🎉 Dashboard inicial con Plotly

✨ Características:
- Dashboard interactivo con Plotly
- Página principal profesional
- Configuración correcta de .gitignore
- Listo para GitHub Pages

📊 Archivos incluidos:
- dashboard.html (dashboard principal)
- index.html (página de entrada)
- README.md (documentación)
- .gitignore (configurado correctamente)"

# Crear repositorio en GitHub (usar GitHub CLI o interfaz web)
gh repo create mi-dashboard-proyecto --public --description "Dashboard interactivo con Plotly"

# Agregar remote y hacer push
git remote add origin https://github.com/tu-usuario/mi-dashboard-proyecto.git
git branch -M main
git push -u origin main
```

### **Paso 5: Configuración de GitHub Pages**

1. **Ir a la configuración del repositorio:**
   - Ve a `https://github.com/tu-usuario/mi-dashboard-proyecto/settings/pages`

2. **Configurar GitHub Pages:**
   - **Source**: "Deploy from a branch"
   - **Branch**: "main"
   - **Folder**: "/ (root)"
   - **Save**

3. **Esperar el despliegue:**
   - GitHub tardará 2-5 minutos en procesar
   - Verás un mensaje verde cuando esté listo

### **Paso 6: Verificación y Testing**

```bash
# Verificar que todos los archivos están en el repositorio
git ls-files | grep html

# Debería mostrar:
# dashboard.html
# index.html

# Verificar que no hay archivos ignorados incorrectamente
git check-ignore dashboard.html index.html
# No debería mostrar nada (archivos no ignorados)
```

---

## 🚨 Checklist de Verificación

### ✅ **Antes de Publicar:**
- [ ] Archivos HTML NO están en `.gitignore`
- [ ] `dashboard.html` está en el repositorio (`git ls-files | grep html`)
- [ ] `index.html` está en el repositorio
- [ ] GitHub Pages está habilitado
- [ ] Repositorio es público o tienes GitHub Pro

### ✅ **Después de Publicar:**
- [ ] Página principal carga correctamente
- [ ] Dashboard se abre sin error 404
- [ ] Visualizaciones de Plotly funcionan
- [ ] Enlaces internos funcionan
- [ ] Responsive design funciona en móvil

---

## 🔧 Comandos de Diagnóstico

### **Verificar archivos ignorados:**
```bash
git check-ignore dashboard.html index.html
```

### **Ver archivos en el repositorio:**
```bash
git ls-files | grep html
```

### **Ver estado de Git:**
```bash
git status
```

### **Ver contenido de .gitignore:**
```bash
cat .gitignore
```

---

## 📚 Casos de Uso Comunes

### **Caso 1: Dashboard con Datos Generados**
```bash
# Generar dashboard.html dinámicamente
python generate_dashboard.py

# Asegurar que se suba al repositorio
git add dashboard.html
git commit -m "Actualizar dashboard con nuevos datos"
git push
```

### **Caso 2: Múltiples Dashboards**
```bash
# Estructura recomendada:
# index.html (página principal)
# dashboard1.html (dashboard específico 1)
# dashboard2.html (dashboard específico 2)
# assets/ (CSS, JS, imágenes)

# .gitignore debe permitir todos los HTML:
# *.html  # NO ignorar archivos HTML
```

### **Caso 3: Dashboard con Datos Sensibles**
```bash
# Para datos sensibles, usar variables de entorno
# o archivos de configuración separados
# que SÍ estén en .gitignore

# .gitignore:
# config.json
# secrets.env
# data/sensitive/
```

---

## 🎯 Mejores Prácticas

### **1. Estructura de Archivos:**
```
proyecto/
├── index.html          # Página principal
├── dashboard.html      # Dashboard principal
├── assets/            # Recursos estáticos
│   ├── css/
│   ├── js/
│   └── images/
├── src/               # Código fuente
├── docs/              # Documentación
├── README.md          # Documentación del proyecto
├── .gitignore         # Configurado correctamente
└── requirements.txt   # Dependencias Python
```

### **2. Configuración de .gitignore:**
```bash
# ✅ CORRECTO - Permitir archivos HTML del dashboard
# dashboard.html  # Comentado
# *.html          # Comentado

# ❌ INCORRECTO - Ignorar archivos HTML
dashboard.html
*.html
```

### **3. Commits Descriptivos:**
```bash
git commit -m "📊 Actualizar dashboard con nuevos datos

✨ Cambios:
- Agregar nueva visualización de tendencias
- Actualizar métricas de rendimiento
- Mejorar responsive design

🔧 Técnicas:
- FFT para análisis espectral
- Detección de picos mejorada
- Normalización de señales"
```

---

## 🆘 Solución de Problemas

### **Problema: Error 404 en Dashboard**
```bash
# Diagnóstico:
git ls-files | grep html

# Si no aparece dashboard.html:
# 1. Verificar .gitignore
cat .gitignore | grep html

# 2. Comentar reglas problemáticas
# dashboard.html  # Comentado

# 3. Agregar archivo
git add dashboard.html
git commit -m "Agregar dashboard.html al repositorio"
git push
```

### **Problema: Dashboard no se actualiza**
```bash
# Verificar que el archivo se subió
git log --oneline -5

# Forzar actualización
git add dashboard.html
git commit -m "Actualizar dashboard"
git push
```

### **Problema: GitHub Pages no funciona**
1. Verificar que el repositorio es público
2. Verificar configuración en Settings > Pages
3. Esperar 5-10 minutos para el despliegue
4. Verificar que index.html existe en la raíz

---

## 📖 Recursos Adicionales

- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [Plotly JavaScript Documentation](https://plotly.com/javascript/)
- [Git .gitignore Patterns](https://git-scm.com/docs/gitignore)

---

## 🎓 Conclusión

Esta guía documenta el proceso completo para evitar el error 404 más común en GitHub Pages: archivos HTML ignorados por Git. Siguiendo estos pasos, cualquier dashboard interactivo se publicará correctamente sin problemas.

**Recordatorio clave:** Los archivos HTML del dashboard NO deben estar en `.gitignore` para que GitHub Pages pueda servirlos correctamente.
