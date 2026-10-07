# Lanzador Debian

Una sola interfaz para configurar **Debian Testing** y **Debian Sid**, con las
acciones de cada distribución separadas.

> **Estado: Fase 2 (configuración externa).** Este repositorio se está
> construyendo por fases. La documentación completa (`MANUAL.md`) llegará en la
> fase de documentación.

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
- **Fase 2 — Configuración externa (actual):** las acciones viven en
  `config/comunes.json`, `config/testing.json` y `config/sid.json`. El lanzador
  fusiona comunes + distro (con overrides) y, de momento, carga Testing por
  defecto a la espera del selector.
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

