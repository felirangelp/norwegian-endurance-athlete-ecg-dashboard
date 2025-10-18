#!/bin/bash

# 🚀 Script para conectar proyecto ECG con GitHub
# Ejecutar después de crear el repositorio en GitHub

echo "🔗 Conectando proyecto ECG con GitHub..."
echo ""

# Verificar que estamos en el directorio correcto
if [ ! -f "main.py" ]; then
    echo "❌ Error: No se encontró main.py. Asegúrate de estar en el directorio del proyecto."
    exit 1
fi

# Verificar que Git está inicializado
if [ ! -d ".git" ]; then
    echo "❌ Error: Git no está inicializado. Ejecuta 'git init' primero."
    exit 1
fi

echo "📋 Por favor, proporciona la información de tu repositorio GitHub:"
echo ""

# Solicitar información del usuario
read -p "👤 Tu usuario de GitHub: " github_user
read -p "📁 Nombre del repositorio (recomendado: norwegian-endurance-athlete-ecg-dashboard): " repo_name

# Usar nombre por defecto si no se proporciona
if [ -z "$repo_name" ]; then
    repo_name="norwegian-endurance-athlete-ecg-dashboard"
fi

echo ""
echo "🔗 Configurando repositorio remoto..."
echo "URL: https://github.com/$github_user/$repo_name.git"
echo ""

# Añadir repositorio remoto
git remote add origin "https://github.com/$github_user/$repo_name.git"

if [ $? -eq 0 ]; then
    echo "✅ Repositorio remoto añadido exitosamente"
else
    echo "⚠️  El repositorio remoto ya existe o hubo un error"
fi

echo ""
echo "📤 Subiendo código a GitHub..."

# Subir código
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 ¡Proyecto sincronizado exitosamente con GitHub!"
    echo ""
    echo "📊 Resumen:"
    echo "   • Repositorio: https://github.com/$github_user/$repo_name"
    echo "   • Versión actual: $(cat VERSION)"
    echo "   • Rama principal: main"
    echo ""
    echo "🔗 Enlaces útiles:"
    echo "   • Ver en GitHub: https://github.com/$github_user/$repo_name"
    echo "   • Clonar: git clone https://github.com/$github_user/$repo_name.git"
    echo ""
    echo "📋 Para futuras actualizaciones:"
    echo "   git add ."
    echo "   git commit -m 'Descripción de cambios'"
    echo "   git push origin main"
else
    echo ""
    echo "❌ Error al subir código. Verifica que:"
    echo "   1. El repositorio existe en GitHub"
    echo "   2. Tienes permisos de escritura"
    echo "   3. Tu usuario y contraseña/token son correctos"
    echo ""
    echo "💡 Si usas autenticación por token:"
    echo "   git remote set-url origin https://TU_TOKEN@github.com/$github_user/$repo_name.git"
fi
