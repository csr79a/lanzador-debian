# Lanzador Debian

Una sola aplicación para configurar **Debian Testing** y **Debian Sid**, con las
acciones de cada distribución separadas.

La interfaz es común (tipo centro de aplicaciones): barra lateral con buscador y
secciones, tarjetas de acciones con estado y una consola integrada donde se
responden las preguntas y la contraseña de `sudo`. El lanzador no duplica la
lógica de instalación: clona o actualiza el repositorio de cada acción
(`git pull --ff-only`) y ejecuta su script tal cual.

## Requisitos

- Debian Testing o Debian Sid (o derivado basado en APT).
- `python3`, `python3-pyqt6` y `git`.
- `sudo` configurado para tu usuario.
- `konsole` (opcional; solo para scripts con menús o modo terminal).

```bash
sudo apt install python3 python3-pyqt6 git
```

## Instalación

```bash
git clone https://github.com/csr79a/lanzador-debian.git ~/lanzador-debian
cd ~/lanzador-debian
bash instalar-lanzador.sh
```

El instalador comprueba dependencias, valida la configuración y crea el
`.desktop` `lanzador-debian.desktop` («Lanzador Debian»). Es idempotente.

Después, busca **Lanzador Debian** en el menú o ábrelo con:

```bash
python3 ~/lanzador-debian/lanzador.py
```

Se inicia como **usuario normal** y se niega a arrancar como root.

## Selector Testing / Sid

En la barra lateral, el bloque **DISTRIBUCIÓN** permite elegir **Testing** o
**Sid**. Al cambiar, se recargan las acciones en la misma ventana (no se abre
otro programa).

- **Detección automática:** lee `/etc/debian_version` y `/etc/os-release` para
  fijar la selección inicial. Es solo informativa y **no** bloquea el cambio
  manual. En un equipo no-Debian o Debian estable no detecta nada y se abre
  Testing.
- **Persistencia:** la última distribución elegida se guarda con `QSettings`.
  Precedencia al arrancar: **última guardada > detectada > Testing**.

## Acciones

- **Debian Testing:** 13 acciones (Base, Gaming, Rendimiento, Gráficos NVIDIA,
  Hardware ASUS, Terminal).
- **Debian Sid:** 13 acciones (las de Testing adaptadas a Sid + **Firma
  electrónica → Instalar AutoFirma** en modo `gui`).
- **Compartidas** (definidas una vez en `config/comunes.json`): sched-ext
  (instalar/gestor GUI/desinstalar), NVIDIA, asusctl (instalar/desinstalar) y
  Starship.

El detalle de cada acción, los modos de ejecución, `sudo`, whiptail, logs y la
solución de problemas están en [`MANUAL.md`](MANUAL.md).

## Configuración

Las acciones viven en `config/`, no en el código:

```text
config/
├── comunes.json   # ajustes globales + acciones compartidas Testing/Sid
├── testing.json   # acciones propias de Testing + overrides
└── sid.json       # acciones propias de Sid + overrides
```

Reglas de fusión: `comunes.json` + `<distro>.json` → `overrides` por `id` →
quitar lo de `deshabilitar`. Campos por acción: `id`, `seccion`, `titulo`,
`descripcion`, `repo`, `rama`, `script`, `modo`, `apt_update`, `requiere_sudo`,
`peligroso`.

## Dónde se guardan los datos

Todo el estado va a `~/.local/share/lanzador-debian/`:

- `proyectos/<repo>/`: clones de cada acción.
- `shims/whiptail`: el `whiptail` de texto (se regenera solo).
- `logs/`: salida de las acciones en modo `gui`.

La configuración elegida (Testing/Sid) se guarda en `~/.config/lanzador-debian/`.

## Pruebas

- **Automatizadas:** completadas (esquema de configuración, paridad 1:1 frente a
  los lanzadores antiguos, construcción de comandos por modo, shim, instalador y
  selector). Detalle en [`PRUEBAS.md`](PRUEBAS.md) y en el manual.

  ```bash
  python3 ~/lanzador-debian/tests/verificar-config.py
  ```

- **Reales en Debian Testing y Debian Sid: PENDIENTES.** No se han ejecutado
  todavía. Requieren una máquina Debian real (idealmente VM o instantánea) y
  están documentadas como pendientes en [`PRUEBAS.md`](PRUEBAS.md) §2.

## Documentación

- [`MANUAL.md`](MANUAL.md) — manual completo: instalación, selector, detección,
  persistencia, acciones, modos, sudo, terminal, whiptail, logs, solución de
  problemas y pruebas.
- [`PRUEBAS.md`](PRUEBAS.md) — comprobaciones automáticas, plan de pruebas
  manuales y checklist de paridad.

## Seguridad

El lanzador ejecuta lo que haya en la rama por defecto del repo de cada acción;
los scripts pueden usar `sudo` y modificar el sistema. Protege tu cuenta de
GitHub con verificación en dos pasos y revisa los cambios antes de ejecutarlos.
La contraseña de `sudo` no se guarda ni se registra.
