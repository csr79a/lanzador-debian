# Lanzador Debian

Una sola interfaz para configurar **Debian Testing** y **Debian Sid**, con las
acciones de cada distribución separadas.

> **Estado: Fase 1 (esqueleto).** Este repositorio se está construyendo por
> fases. La documentación completa (`MANUAL.md`) llegará en la fase de
> documentación.

## Qué es

Panel gráfico (PyQt6) tipo centro de aplicaciones: barra lateral con buscador y
secciones, tarjetas de acciones con estado, y una consola integrada donde se
responden las preguntas y la contraseña de `sudo`.

El lanzador **no duplica** la lógica de instalación: clona o actualiza el
repositorio de cada acción (`git pull --ff-only`) y ejecuta su script tal cual.

## Estado por fases

- **Fase 1 — Esqueleto (actual):** motor unificado partiendo de la base de
  Testing, con `requiere_sudo` portado de Sid y `apt_update` conservado. Rutas
  de datos y `.desktop` ya usan `lanzador-debian`. De momento carga las acciones
  de Testing desde `proyectos.json`.
- Fase 2 — Configuración externa (`config/comunes.json`, `testing.json`, `sid.json`).
- Fase 3 — Selector Testing/Sid y detección de la distribución.
- Fase 4 — Datos, `.desktop` e instalador unificados.
- Fase 5 — Pruebas reales y checklist de paridad.
- Fase 6 — Documentación unificada.

## Requisitos

- Debian Testing o Debian Sid.
- `python3-pyqt6` y `git`.
- `sudo` configurado para tu usuario.
- `konsole` (opcional; solo para scripts con menús o modo terminal).

## Uso

```bash
sudo apt install python3-pyqt6 git
git clone https://github.com/csr79a/lanzador-debian.git ~/lanzador-debian
cd ~/lanzador-debian
bash instalar-lanzador.sh
```

O directamente:

```bash
python3 ~/lanzador-debian/lanzador.py
```

El lanzador se inicia como **usuario normal** y se niega a arrancar como root.
