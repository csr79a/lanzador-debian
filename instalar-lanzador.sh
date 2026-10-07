#!/usr/bin/env bash
# Instala la entrada de menú de «Lanzador Debian».
#
# Reproducible desde una copia limpia del repositorio: solo usa archivos que
# están dentro de la propia copia (no depende de rutas externas). Comprueba
# dependencias y que la configuración sea válida. Idempotente: se puede
# ejecutar varias veces; solo reescribe el .desktop.
set -euo pipefail

if [[ $EUID -eq 0 ]]; then
    echo "No ejecutes este script como root; usa tu usuario normal." >&2
    exit 1
fi

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 1) Archivos necesarios dentro de la copia del repositorio
faltan_archivos=()
for archivo in "$DIR/lanzador.py" \
               "$DIR/config/comunes.json" \
               "$DIR/config/testing.json" \
               "$DIR/config/sid.json"; do
    [[ -f "$archivo" ]] || faltan_archivos+=("$archivo")
done
if ((${#faltan_archivos[@]})); then
    echo "ERROR: faltan archivos requeridos:" >&2
    printf '  - %s\n' "${faltan_archivos[@]}" >&2
    echo "Ejecuta este instalador desde una copia completa del repositorio." >&2
    exit 1
fi

# 2) Dependencias
faltan=()
command -v python3 >/dev/null 2>&1 || faltan+=("python3")
command -v git >/dev/null 2>&1 || faltan+=("git")
python3 -c 'import PyQt6.QtWidgets' >/dev/null 2>&1 || faltan+=("python3-pyqt6")
if ((${#faltan[@]})); then
    echo "Faltan paquetes: ${faltan[*]}"
    echo "Instálalos con: sudo apt install ${faltan[*]}"
    exit 1
fi

# 3) La configuración debe ser JSON válido
for cfg in comunes testing sid; do
    if ! python3 -c 'import json, sys; json.load(open(sys.argv[1], encoding="utf-8"))' \
            "$DIR/config/$cfg.json" 2>/dev/null; then
        echo "ERROR: config/$cfg.json no es un JSON válido." >&2
        exit 1
    fi
done

# 4) Terminal para los scripts con menús o modo terminal (opcional)
if ! command -v konsole >/dev/null 2>&1 \
   && ! command -v x-terminal-emulator >/dev/null 2>&1; then
    echo "AVISO: no se encontró konsole ni x-terminal-emulator. Las acciones que necesiten menús/listas o modo terminal no podrán abrirse."
fi

# 5) Entrada de menú
APPS="${XDG_DATA_HOME:-$HOME/.local/share}/applications"
mkdir -p "$APPS"
cat > "$APPS/lanzador-debian.desktop" <<EOF
[Desktop Entry]
Type=Application
Version=1.0
Name=Lanzador Debian
Comment=Reúne los scripts de configuración de Debian Testing y Debian Sid en una sola ventana
Exec=python3 "$DIR/lanzador.py"
Icon=preferences-system
Terminal=false
Categories=System;
Keywords=debian;testing;sid;configuracion;
EOF
chmod 644 "$APPS/lanzador-debian.desktop"

command -v update-desktop-database >/dev/null 2>&1 \
    && update-desktop-database "$APPS" || true

echo "Instalado: $APPS/lanzador-debian.desktop"
echo "Busca «Lanzador Debian» en el menú de aplicaciones."
echo "O ábrelo ahora con: python3 \"$DIR/lanzador.py\""
