# Manual del Lanzador Debian

Una sola aplicación para configurar **Debian Testing** y **Debian Sid**, con las
acciones de cada distribución separadas en su configuración.

---

## 1. Qué hace y qué no hace

El Lanzador Debian es una ventana que agrupa los scripts de configuración del
sistema en tarjetas. Al pulsar **Ejecutar** en una acción:

1. La ventana pasa a la vista de ejecución: panel de registro, campo de respuesta
   y botón **Cancelar**.
2. Clona el proyecto de la acción con `git clone` o lo actualiza con
   `git pull --ff-only`.
3. Si la acción lleva `apt_update: true`, ejecuta `sudo apt update` (sincroniza
   los índices de APT; no actualiza paquetes).
4. Ejecuta el script según el `modo` definido en la configuración.
5. Muestra el resultado (completado, falló con su código o cancelado).

El lanzador **no modifica** los scripts y **no ejecuta nada como root por su
cuenta**: se niega a arrancar como root. Los scripts gestionan sus propios
privilegios; algunos se elevan con `sudo` cuando lo necesitan y otros exigen root
desde el principio (`requiere_sudo`, ver §9).

La interfaz es única; lo que cambia entre Testing y Sid es **las acciones** que
se muestran (ver §7), no el programa.

---

## 2. Requisitos e instalación

### 2.1. Dependencias

- Debian Testing o Debian Sid (o derivado basado en APT).
- `python3` y `python3-pyqt6`.
- `git`.
- `sudo` configurado para tu usuario.
- `konsole` (KDE Plasma): opcional. Solo hace falta si un script usa menús o
  listas, o si una acción usa `modo: terminal`. Si no está, se intenta
  `x-terminal-emulator`.

```bash
sudo apt install python3 python3-pyqt6 git
```

### 2.2. Instalación

```bash
git clone https://github.com/csr79a/lanzador-debian.git ~/lanzador-debian
cd ~/lanzador-debian
bash instalar-lanzador.sh
```

`instalar-lanzador.sh` comprueba las dependencias, valida la configuración y crea
la entrada del menú `~/.local/share/applications/lanzador-debian.desktop`. Es
idempotente (se puede repetir). Después busca **Lanzador Debian** en el menú de
aplicaciones.

### 2.3. Abrirlo directamente

```bash
python3 ~/lanzador-debian/lanzador.py
```

**No lo ejecutes con `sudo`.** Debe correr como usuario normal.

### 2.4. Desinstalación

```bash
# Usuario normal
rm ~/.local/share/applications/lanzador-debian.desktop
rm -rf ~/.local/share/lanzador-debian   # datos, clones y logs del lanzador
rm -rf ~/lanzador-debian                # el repositorio
```

Esto **no** desinstala lo que hayan instalado los scripts; para eso usa las
acciones de limpiar/desinstalar de cada sección.

---

## 3. La ventana

Tiene dos zonas:

- **Barra lateral:** nombre de la app, bloque **DISTRIBUCIÓN**, buscador, lista de
  secciones y una nota con la carpeta de datos.
- **Contenido:** las acciones en tarjetas (rejilla de 2–4 columnas según ancho).
  Cada tarjeta lleva icono, título, descripción, indicador de estado y botón.

El buscador filtra por título y descripción; hacer clic en una sección muestra
solo sus acciones. El indicador de estado va cambiando: **Sin ejecutar**,
**En ejecución…**, **Completado**, **Falló** o **Cancelado**.

---

## 4. Selector de distribución (Testing / Sid)

En la barra lateral, el bloque **DISTRIBUCIÓN** permite elegir:

- **Debian Testing**
- **Debian Sid**

Al cambiar, se recargan las acciones en la **misma ventana** (no se abre otro
programa). Mientras hay un script en ejecución no se puede cambiar de
distribución.

---

## 5. Detección automática

Al arrancar, el lanzador intenta detectar el sistema para fijar una selección
inicial:

- `/etc/debian_version`: `sid` → **Sid**; algo como `trixie/sid` → **Testing**;
  un número (estable) o un sistema no-Debian → sin detección.
- `/etc/os-release`: se lee `PRETTY_NAME` para mostrar «Sistema detectado: …».

La detección es **solo un valor inicial e informativo**: **nunca** bloquea ni
impide cambiar manualmente entre Testing y Sid.

---

## 6. Persistencia de la distribución

La última distribución seleccionada se guarda con **QSettings** (organización y
aplicación `lanzador-debian`). Al volver a abrir el lanzador se muestra la misma
que elegiste.

Precedencia al arrancar:

```text
última guardada  >  detectada  >  Debian Testing
```

Es decir: la detección solo decide la **primera** vez (o hasta que cambies de
distribución).

---

## 7. Acciones disponibles

### 7.1. Debian Testing (13 acciones)

| Sección | Acción | Notas |
| --- | --- | --- |
| Base | Corregir repositorios Debian Testing | fuente `debian-testing-setup` |
| Base | Configurar Debian Testing | |
| Base | Limpiar Debian Testing | peligrosa |
| Base | Sincronizar repositorios APT | ejecuta `repos/apt-update.sh` |
| Gaming | Instalar gaming | `apt_update` |
| Gaming | Limpiar gaming | peligrosa |
| Rendimiento | Instalar sched-ext | `apt_update` |
| Rendimiento | Instalar gestor de sched-ext (GUI) | requiere sched-ext instalado |
| Rendimiento | Desinstalar sched-ext | peligrosa |
| Gráficos NVIDIA | Instalar driver NVIDIA | `apt_update` |
| Hardware ASUS | Instalar asusctl / ROG Control | `apt_update` |
| Hardware ASUS | Desinstalar asusctl / ROG Control | peligrosa |
| Terminal | Configurar terminal con Starship | |

### 7.2. Debian Sid (13 acciones)

| Sección | Acción | Notas |
| --- | --- | --- |
| Base | Convertir Debian Testing a Sid | `requiere_sudo` |
| Base | Configurar Debian Sid | |
| Base | Limpiar Debian Sid | peligrosa |
| Gaming | Instalar gaming | |
| Gaming | Limpiar gaming | peligrosa |
| Rendimiento | Instalar sched-ext | compartida |
| Rendimiento | Instalar gestor de sched-ext (GUI) | compartida |
| Rendimiento | Desinstalar sched-ext | compartida, peligrosa |
| Gráficos NVIDIA | Instalar driver NVIDIA | compartida |
| Hardware ASUS | Instalar asusctl / ROG Control | compartida |
| Hardware ASUS | Desinstalar asusctl / ROG Control | compartida, peligrosa |
| Terminal | Configurar terminal con Starship | compartida |
| Firma electrónica | Instalar AutoFirma | `modo: gui` |

### 7.3. Acciones compartidas

Definidas una sola vez en `config/comunes.json` y usadas por ambas
distribuciones:

- `sched-ext-debian`: Instalar sched-ext · Instalar gestor de sched-ext (GUI) ·
  Desinstalar sched-ext
- `nvidia-debian-setup`: Instalar driver NVIDIA
- `asusctl-rogcontrol-debian`: Instalar asusctl / ROG Control · Desinstalar
- `terminal-starship-setup`: Configurar terminal con Starship

> Estas acciones **deben comprobarse en Testing y en Sid** antes de darlas por
> buenas (ver §15.2). Si alguna difiere entre distribuciones, se separa: una
> definición en `testing.json` y otra en `sid.json`.

---

## 8. Modos de ejecución

Cada acción puede llevar el campo `modo`:

| Modo | Qué hace |
| --- | --- |
| `auto` (por defecto) | Ejecuta el script dentro de la ventana. Si usa menús, listas, campos de texto o `dialog`, lo abre en Konsole. |
| `integrado` | Siempre dentro de la ventana, aunque el script tenga menús. |
| `gui` | Para scripts que abren su propia aplicación: actualiza el proyecto y lanza el script sin terminal. |
| `terminal` | Siempre en Konsole. |

---

## 9. sudo y contraseña

- El lanzador se inicia como **usuario normal** y se niega a correr como root.
- La mayoría de los scripts solicitan `sudo` cuando lo necesitan. La contraseña
  se escribe en el campo inferior y no se muestra mientras se teclea.
- Campo `requiere_sudo: true`: el script se ejecuta con `sudo bash` desde el
  principio (para scripts que exigen root global, como *Convertir Debian Testing
  a Sid*). El `PATH` del shim de whiptail y `LANZADOR_INTEGRADO=1` se conservan.
- La contraseña pasa directamente al terminal del script; el lanzador **no la
  guarda ni la registra**.

---

## 10. Terminal (Konsole)

Algunas acciones necesitan una terminal real:

- Scripts con menús, listas, campos de texto o `dialog` (en modo `auto`).
- Acciones con `modo: terminal`.

Se usa `konsole` y, si no está, `x-terminal-emulator`. Si no hay ninguno, esas
acciones no pueden abrirse y se avisa.

---

## 11. whiptail dentro de la ventana

Mientras un script corre dentro de la ventana, el lanzador pone por delante en el
`PATH` un `whiptail` de texto propio. Convierte:

- `--yesno` en una pregunta `s/n` (Enter elige la opción por defecto;
  `--defaultno` y los botones `--yes-button`/`--no-button` se respetan).
- `--msgbox` en un aviso con «Pulsa Enter para continuar».
- `--infobox` en un mensaje sin pausa.

Los scripts no se modifican: en una terminal normal siguen usando el `whiptail`
real. El lanzador define también `LANZADOR_INTEGRADO=1`. Los cuadros que el
whiptail de texto no sabe convertir (`--menu`, `--checklist`, `--radiolist`,
`--inputbox`, `--passwordbox`, `--gauge`, `--textbox`, `--tailbox`, `--fselect`,
`dialog --`) hacen que el script se abra en Konsole en modo `auto`.

---

## 12. Logs y dónde se guardan los datos

Todo cuelga de `~/.local/share/lanzador-debian/`:

- `proyectos/<repo>/`: cada acción clona aquí su repositorio.
- `shims/whiptail`: el `whiptail` de texto (se regenera solo).
- `logs/`: salida de las acciones en `modo: gui` (un archivo por script).

La configuración elegida (Testing/Sid) se guarda en `~/.config/lanzador-debian/`.

---

## 13. Configuración

Las acciones no están en el código: viven en `config/`.

```text
config/
├── comunes.json   # ajustes globales + acciones compartidas
├── testing.json   # acciones propias de Testing + overrides
└── sid.json       # acciones propias de Sid + overrides
```

**Reglas de fusión:** `comunes.json` + `<distro>.json` → `overrides` por `id` →
quitar lo listado en `deshabilitar`. El resultado se ordena según
`orden_secciones` y, dentro de cada sección, por orden de aparición.

Campos por acción:

| Campo | Obligatorio | Significado |
| --- | --- | --- |
| `id` | Sí | Identificador estable (para overrides) |
| `seccion` | Sí | Categoría (filtro de la barra lateral) |
| `titulo` | Sí | Nombre visible |
| `descripcion` | No | Texto gris |
| `repo` | Sí | URL de clonado |
| `rama` | No | Rama a usar (por defecto, la del repo) |
| `script` | Sí | Ruta del script dentro del repo |
| `modo` | No | `auto`/`integrado`/`gui`/`terminal` |
| `apt_update` | No | `sudo apt update` antes del script |
| `requiere_sudo` | No | Ejecuta el script con `sudo bash` |
| `peligroso` | No | Pide confirmación antes de ejecutar |

Ajuste global en `comunes.json`: `carpeta_proyectos` (dónde se clonan los repos).

**Añadir una acción:** añade una entrada con su `id`, `repo` y `script` a
`testing.json` o `sid.json` (o a `comunes.json` si vale para ambas) y vuelve a
abrir el lanzador. Para cambiar un campo de una acción compartida solo en una
distribución, usa `overrides`.

---

## 14. Solución de problemas

### 14.1. La ventana no se abre
Lánzala desde una terminal para ver el error:
```bash
python3 ~/lanzador-debian/lanzador.py
```
Si dice `No module named 'PyQt6'`, instala `python3-pyqt6`.

### 14.2. «No como root»
La has abierto con `sudo` o como root. Ábrela con tu usuario normal.

### 14.3. «Sin terminal»
Un script necesita Konsole y no hay `konsole` ni `x-terminal-emulator`. Instala
Konsole: `sudo apt install konsole`.

### 14.4. «No se pudo clonar»
Comprueba la conexión y que la URL de `repo` es correcta y pública.

### 14.5. «No existe <script> en <carpeta>»
El repo se descargó pero la ruta de `script` no coincide con su contenido. Revisa
`config/*.json` frente al repo.

### 14.6. Un script parece colgado
Casi siempre espera una respuesta. Mira la última línea del registro: si es una
pregunta, escríbela abajo y pulsa Enter; si pide la contraseña de `sudo`, el campo
pasa a modo oculto. Si no responde, pulsa **Cancelar** (Ctrl+C → TERM → KILL).

### 14.7. La detección no coincide con mi sistema
Pasa en equipos no-Debian o Debian estable: la detección devuelve «desconocido» y
se abre Testing. Cambia manualmente a Sid; se recordará la próxima vez.

### 14.8. Una acción en modo `gui` no abre la aplicación
Si falla en los primeros segundos, la ventana muestra la salida. Revisa el log en
`~/.local/share/lanzador-debian/logs/<script>.log`.

### 14.9. Una copia descargada está rota
Borra solo esa copia; se volverá a clonar al pulsar el botón:
```bash
rm -rf ~/.local/share/lanzador-debian/proyectos/sched-ext-debian
```

### 14.10. Un cuadro de whiptail se ve mal o el script se detiene
Es un tipo de cuadro que el whiptail de texto no convierte y que el lanzador no
detectó (por ejemplo, cargado con `source`). Pon `"modo": "terminal"` en esa
acción.

---

## 15. Pruebas

### 15.1. Pruebas automatizadas (realizadas)

| Comprobación | Resultado |
| --- | --- |
| Esquema de la configuración (campos, `id` únicos, `modo`, overrides, orden) | OK |
| Paridad 1:1 Testing (13/13) | OK |
| Paridad 1:1 Sid (12/12 + AutoFirma) | OK |
| Construcción de comandos (`auto`, `requiere_sudo`, `apt_update`, `gui`, `terminal`) | OK |
| Chips de estado (Cancelado/Completado) | OK |
| `entorno()` (shim al frente, `LANZADOR_INTEGRADO`) | OK |
| Shim de `whiptail` (`bash -n`) | OK |
| `VistaLog` (ANSI y `\r`) | OK |
| Instalador en copia limpia (idempotente, valida config) | OK |
| Selector, detección y persistencia (offscreen) | OK |

Para repetirlas:
```bash
python3 ~/lanzador-debian/tests/verificar-config.py
```

Detalle completo en [`PRUEBAS.md`](PRUEBAS.md).

### 15.2. Pruebas reales en Debian Testing y Sid — **PENDIENTES**

**Todavía no se han ejecutado en Debian Testing ni en Debian Sid.** Las
comprobaciones anteriores son automáticas y no ejecutan los scripts. Queda
pendiente:

- Prueba de humo en Testing y en Sid (arranque, selector, detección,
  persistencia, buscador, confirmación de acciones peligrosas).
- Ejecución real de cada acción que modifica el sistema (recomendado en VM o con
  instantánea previa).
- Verificación de las **7 acciones compartidas** en **ambas** distribuciones.
- Preguntas/contraseña/whiptail/Konsole/cancelación con scripts reales.

La tabla de acciones, riesgos y cómo revertir está en
[`PRUEBAS.md`](PRUEBAS.md) (§2).

---

## 16. Seguridad

- El lanzador ejecuta lo que haya en la rama por defecto del repo de cada acción.
- Los scripts pueden usar `sudo` y modificar el sistema según su función.
- Protege tu cuenta de GitHub con verificación en dos pasos y revisa los cambios
  de un repo antes de ejecutarlo.
- El whiptail de texto solo existe en el `PATH` de los scripts que corren dentro
  de la ventana; no se instala en el sistema.
- La contraseña de `sudo` no se guarda ni se registra.

---

## 17. Estado del proyecto

Las fases de desarrollo (esqueleto, configuración externa, selector, datos e
instalador, pruebas, documentación) están completas. **Las pruebas reales en
Debian Testing y Debian Sid siguen pendientes** (ver §15.2).
