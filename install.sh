#!/bin/bash

APP_NAME="deepseek-gtk"
ICON_SOURCE="assets/deepseek-icon.png"

INSTALL_BIN="$HOME/.local/bin"
INSTALL_SHARE="$HOME/.local/share/deepseek-gtk"
INSTALL_DESKTOP="$HOME/.local/share/applications"

print_header() {
    echo "=============================================="
    echo "      DeepSeek GTK - Instalador"
    echo "=============================================="
}

print_status() {
    echo -e "[INFO] $1"
}

print_success() {
    echo -e "[OK] $1"
}

print_warning() {
    echo -e "[WARNING] $1"
}

print_error() {
    echo -e "[ERROR] $1"
}

print_header


# Verificacion de dependencias

print_status "Verificando dependencias..."

if ! command -v python3 &> /dev/null; then
    print_error "Python 3 no fue encontrado."
    echo "Por favor, instale Python 3 antes de continuar."
    exit 1
fi
print_success "Python 3 encontrado."

# Verificar PyGObject
python3 -c "import gi" 2>/dev/null
if [ $? -ne 0 ]; then
    print_error "Biblioteca PyGObject (GTK) no encontrada."
    echo "Instale los bindings GTK para Python (ex: python3-gi o python-gobject)."
    exit 1
fi
print_success "PyGObject (GTK) encontrado."

# Verificar gi

python3 -c "from gi.repository import WebKit2" 2>/dev/null
if [ $? -ne 0 ]; then
   print_error "WebKit2 no encontrado. Instale gir1.2-webkit2-4.1"
   exit 1
fi

print_success "WebKit2 encontrado."

# Preparar directorios

print_status "Preparando directorios de instalacion..."
mkdir -p "$INSTALL_BIN"
mkdir -p "$INSTALL_SHARE"
mkdir -p "$INSTALL_DESKTOP"


# Instalacion del paquete y ejecutable

print_status "Copiando archivos de aplicacion..."

# Limpiar instalacion anterior para evitar conflictos
rm -rf "$INSTALL_SHARE/deepseek"

# Copia el paquete hacia ~/.local/share/deepseek-gtk/deepseek
if [ -d "deepseek" ]; then
    cp -r deepseek "$INSTALL_SHARE/"
    print_success "Paquete copiado en $INSTALL_SHARE"
else
    print_error "Directorio deepseek no encontrado"
    exit 1
fi

# Instalar el icono

if [ -f "$ICON_SOURCE" ]; then
       cp "$ICON_SOURCE" "$INSTALL_SHARE/deepseek-icon.png"
       print_success "Icono instalado."
   else
       print_warning "Icono no encontrado en $ICON_SOURCE. El acceso directo no tendrá icono."
   fi

# Crear script de lanzamiento en ~/.local/bin/deepseek-gtk
print_status "Creando ejecutable..."
cat > "$INSTALL_BIN/$APP_NAME" <<EOF
#!/bin/bash
export PYTHONPATH="$INSTALL_SHARE"
exec python3 -m deepseek
EOF

chmod +x "$INSTALL_BIN/$APP_NAME"
print_success "Ejecutable instalado en $INSTALL_BIN/$APP_NAME"


# Creacion de atajo

cat > "$INSTALL_DESKTOP/$APP_NAME.desktop" <<FIM
[Desktop Entry]
Name=DeepSeek
Comment=Cliente no oficial para DeepSeek Chat
Exec=$INSTALL_BIN/$APP_NAME
Icon=$INSTALL_SHARE/deepseek-icon.png
Terminal=false
Type=Application
Categories=Network;Chat;
StartupWMClass=deepseek
X-GNOME-SingleWindow=true
FIM

print_success "Atajo creado en $INSTALL_DESKTOP"

# Finalizacion

update-desktop-database "$INSTALL_DESKTOP" 2>/dev/null

echo ""
echo -e "=============================================="
echo -e "      Instalacion concluida con exito!       "
echo -e "=============================================="
echo ""
echo "La aplicacion DeepSeek debe aparecer en el menu de aplicaciones."
echo "Para desinstalar, elimine:"
echo "  - $INSTALL_BIN/$APP_NAME"
echo "  - $INSTALL_SHARE"
echo "  - $INSTALL_DESKTOP/$APP_NAME.desktop"
echo ""


