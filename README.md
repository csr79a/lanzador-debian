# Lanzador Debian

Una sola interfaz para configurar **Debian Testing** y **Debian Sid**, con las
acciones de cada distribución separadas.

> **Estado: Fase 4 (datos, `.desktop` e instalador unificados).** Este
> repositorio se está construyendo por fases. La documentación completa
> (`MANUAL.md`) llegará en la fase de documentación.

## Qué es

Panel gráfico (PyQt6) tipo centro de aplicaciones: barra lateral con buscador y
secciones, tarjetas de acciones con estado, y una consola integrada donde se
responden las preguntas y la contraseña de `sudo`.

El lanzador **no duplica** la lógica de instalación: clona o actualiza el
repositorio de cada acción (`git pull --ff-only`) y ejecuta su script tal cual.

## Estado por fases

- **Fase 1 — Esqueleto:** motor unificado partiendo de la base de Testing, con
  `requiere_sudo` portado de Sid y `apt_update` conservado. Rutas de datos y
  `.desktop` ya usan `lanzador-debian`.
- **Fase 2 — Configuración externa:** las acciones viven en
  `config/comunes.json`, `config/testing.json` y `config/sid.json`. El lanzador
  fusiona comunes + distro (con overrides).
- **Fase 3 — Selector Testing/Sid:** la misma ventana permite elegir Testing o
  Sid; al cambiar se recargan las acciones sin abrir otro programa. La elección
  se recuerda con `QSettings` y la detección del sistema solo fija el valor
  inicial.
- **Fase 4 — Datos, `.desktop` e instalador unificados (actual):** todo el
  estado va a `~/.local/share/lanzador-debian/`; `instalar-lanzador.sh` valida
  dependencias, archivos y JSON, y crea el `.desktop` «Lanzador Debian».
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

## Configuración

Las acciones no están en el código: viven en `config/`.

```text
config/
├── comunes.json   # ajustes globales + acciones compartidas Testing/Sid
├── testing.json   # acciones propias de Testing + overrides
└── sid.json       # acciones propias de Sid + overrides
```

Reglas de fusión: `comunes.json` + `<distro>.json` → `overrides` por `id` →
quitar lo listado en `deshabilitar`. El resultado se ordena según
`orden_secciones` y, dentro de cada sección, por orden de aparición.

Campos por acción: `id`, `seccion`, `titulo`, `descripcion`, `repo`, `rama`,
`script`, `modo` (`auto`/`integrado`/`gui`/`terminal`), `apt_update`,
`requiere_sudo`, `peligroso`.

## Distribución

En la barra lateral, el bloque **DISTRIBUCIÓN** permite elegir **Testing** o
**Sid**; al cambiar se recargan las acciones en la misma ventana. La última
elección se guarda con `QSettings` (precedencia: última guardada > detectada >
Testing). La detección del sistema (`/etc/debian_version`, `/etc/os-release`)
solo decide la selección inicial y **no** impide cambiar manualmente.

## Dónde se guardan los datos

Todo el estado va a `~/.local/share/lanzador-debian/`:

- `proyectos/<repo>/`: cada acción clona ahí su repositorio.
- `shims/whiptail`: el `whiptail` de texto (se regenera solo).
- `logs/`: salida de las acciones en modo `gui`.

