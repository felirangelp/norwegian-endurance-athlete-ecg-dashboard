# 🚀 Script para Sincronizar con GitHub

## Pasos para conectar tu proyecto con GitHub:

### 1. Crear repositorio en GitHub
1. Ve a [GitHub.com](https://github.com) y haz login
2. Haz clic en el botón "+" en la esquina superior derecha
3. Selecciona "New repository"
4. Configuración recomendada:
   - **Repository name**: `norwegian-endurance-athlete-ecg-dashboard`
   - **Description**: `Dashboard interactivo para análisis ECG de atletas de resistencia noruegos usando técnicas de procesamiento de señales biológicas`
   - **Visibility**: Private (recomendado para proyectos académicos)
   - **NO marques**: "Add a README file" (ya tienes uno)
   - **NO marques**: "Add .gitignore" (ya tienes uno)
   - **NO marques**: "Choose a license" (opcional)

### 2. Conectar repositorio local con GitHub
Después de crear el repositorio, ejecuta estos comandos en tu terminal:

```bash
# Navegar al directorio del proyecto
cd "/Users/feliperangel/Javeriana/Mestría IA/Procesamiento de señales biológicas/Proyecto_final/Norwegian Endurance Athlete ECG Database"

# Añadir el repositorio remoto (reemplaza TU_USUARIO con tu usuario de GitHub)
git remote add origin https://github.com/TU_USUARIO/norwegian-endurance-athlete-ecg-dashboard.git

# Subir el código a GitHub
git push -u origin main
```

### 3. Verificar la sincronización
```bash
# Verificar el estado
git status

# Ver los remotos configurados
git remote -v

# Ver el historial de commits
git log --oneline
```

## 📋 Comandos útiles para el futuro:

### Actualizar el repositorio después de cambios:
```bash
# Añadir cambios
git add .

# Hacer commit con mensaje descriptivo
git commit -m "Descripción de los cambios realizados"

# Subir cambios a GitHub
git push origin main
```

### Crear una nueva versión:
```bash
# Actualizar número de versión en VERSION
echo "1.1.0" > VERSION

# Actualizar CHANGELOG.md con los nuevos cambios
# Luego hacer commit y push
git add VERSION CHANGELOG.md
git commit -m "📦 Versión 1.1.0 - [Descripción de cambios]"
git push origin main

# Crear tag para la versión
git tag -a v1.1.0 -m "Versión 1.1.0"
git push origin v1.1.0
```

### Trabajar con ramas (para futuras mejoras):
```bash
# Crear nueva rama para una funcionalidad
git checkout -b feature/nueva-funcionalidad

# Trabajar en la rama, hacer commits
# ...

# Fusionar con main cuando esté listo
git checkout main
git merge feature/nueva-funcionalidad
git push origin main
```

## 🎯 Estado actual del proyecto:
- ✅ Repositorio Git inicializado
- ✅ Commit inicial realizado (Versión 1.0.0)
- ✅ Archivos de control de versiones creados (VERSION, CHANGELOG.md)
- ✅ .gitignore configurado
- ⏳ Pendiente: Conectar con GitHub

## 📁 Archivos incluidos en el repositorio:
- `src/` - Código fuente del proyecto
- `norwegian-endurance-athlete-ecg-database-1.0.0/` - Datos ECG
- `requirements.txt` - Dependencias Python
- `README.md` - Documentación del proyecto
- `CHANGELOG.md` - Historial de cambios
- `VERSION` - Número de versión actual
- `.gitignore` - Archivos a ignorar
- `main.py` - Script principal
- `context.md` - Contexto del proyecto
- `tecnicas.md` - Técnicas del semestre
