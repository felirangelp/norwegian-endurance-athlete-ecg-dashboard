# 🤖 Instrucciones para Cursor AI - Dashboards en GitHub Pages

## 🎯 Prompt Completo para Nuevos Proyectos

Copia y pega este prompt completo cuando quieras crear un nuevo dashboard:

```
Necesito crear un dashboard interactivo con Plotly que se publique correctamente en GitHub Pages. 

REQUISITOS CRÍTICOS:
1. Crear dashboard HTML interactivo con Plotly
2. Configurar GitHub Pages sin errores 404
3. Asegurar que todos los archivos HTML se suban correctamente
4. Evitar el problema común de archivos ignorados por Git

CONFIGURACIÓN .GITIGNORE OBLIGATORIA:
- NO ignorar archivos HTML del dashboard
- Comentar cualquier regla que ignore *.html o dashboard.html
- Solo ignorar archivos temporales y de desarrollo
- Verificar que dashboard.html esté en el repositorio

ARCHIVOS NECESARIOS:
- dashboard.html (dashboard principal con Plotly)
- index.html (página de entrada profesional)
- .gitignore (configurado correctamente)
- README.md (con instrucciones de uso)

VERIFICACIÓN POST-CREACIÓN:
- Confirmar que git ls-files | grep html muestra todos los archivos HTML
- Verificar que git check-ignore dashboard.html no muestra nada
- Probar que GitHub Pages funciona sin error 404
- Documentar el proceso para futuros proyectos

ESTRUCTURA RECOMENDADA:
proyecto/
├── index.html          # Página principal
├── dashboard.html      # Dashboard principal
├── assets/            # Recursos estáticos
├── src/               # Código fuente
├── README.md          # Documentación
├── .gitignore         # Configurado correctamente
└── requirements.txt   # Dependencias

PROCESO COMPLETO:
1. Crear estructura del proyecto
2. Configurar .gitignore correctamente
3. Crear archivos HTML del dashboard
4. Configurar Git y GitHub
5. Habilitar GitHub Pages
6. Verificar funcionamiento
7. Documentar proceso

IMPORTANTE: El error 404 más común es que dashboard.html esté en .gitignore. 
Asegurar que esto NO suceda es crítico para el éxito del proyecto.
```

## 🔧 Comandos de Verificación para Cursor

Incluye estos comandos en tu proceso de verificación:

```bash
# Verificar que los archivos HTML están en el repositorio
git ls-files | grep html

# Verificar que NO están siendo ignorados
git check-ignore dashboard.html index.html

# Verificar estado de Git
git status

# Verificar contenido de .gitignore
cat .gitignore | grep -E "(html|dashboard)"
```

## 📋 Checklist para Cursor AI

### ✅ **Configuración Inicial:**
- [ ] Crear .gitignore sin ignorar archivos HTML
- [ ] Crear estructura de directorios
- [ ] Configurar archivos HTML del dashboard
- [ ] Inicializar repositorio Git

### ✅ **Verificación Pre-Commit:**
- [ ] `git ls-files | grep html` muestra todos los archivos HTML
- [ ] `git check-ignore dashboard.html` no muestra nada
- [ ] Archivos HTML no están en .gitignore
- [ ] Estructura del proyecto es correcta

### ✅ **Configuración GitHub:**
- [ ] Repositorio creado en GitHub
- [ ] Archivos subidos correctamente
- [ ] GitHub Pages habilitado
- [ ] URLs funcionan sin error 404

### ✅ **Documentación:**
- [ ] README.md con instrucciones
- [ ] Comentarios en código
- [ ] Guía de solución de problemas
- [ ] Proceso documentado para futuros proyectos

## 🚨 Errores Comunes a Evitar

### ❌ **Error 1: Archivos HTML en .gitignore**
```bash
# INCORRECTO en .gitignore:
dashboard.html
*.html

# CORRECTO en .gitignore:
# dashboard.html  # Comentado
# *.html          # Comentado
```

### ❌ **Error 2: No verificar archivos en repositorio**
```bash
# SIEMPRE verificar:
git ls-files | grep html
# Debe mostrar: dashboard.html, index.html
```

### ❌ **Error 3: No probar GitHub Pages**
```bash
# SIEMPRE probar:
# 1. Página principal carga
# 2. Dashboard se abre sin 404
# 3. Visualizaciones funcionan
```

## 🎯 Template de .gitignore Correcto

```bash
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
```

## 📊 Template de index.html

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

## 🎓 Resumen para Cursor AI

**PROBLEMA MÁS COMÚN:** Error 404 en GitHub Pages porque `dashboard.html` está en `.gitignore`

**SOLUCIÓN:** Comentar reglas de `.gitignore` que ignoren archivos HTML del dashboard

**VERIFICACIÓN:** `git ls-files | grep html` debe mostrar todos los archivos HTML

**RESULTADO:** Dashboard funciona correctamente en GitHub Pages sin errores 404
