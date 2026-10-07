# Pruebas y checklist de paridad — Lanzador Debian

## 0. Alcance y entorno

- Este repositorio se ha desarrollado y verificado **automáticamente en un
  equipo no-Debian** (CachyOS). Las comprobaciones automáticas validan el
  código, la configuración y la construcción de comandos, pero **no** ejecutan
  los scripts reales.
- Las pruebas que **ejecutan los scripts** deben hacerse en **Debian Testing** y
  **Debian Sid reales**. Están listadas abajo como pendientes (manuales).
- Ninguna acción del sistema se ha ejecutado para estas pruebas. En particular,
  **no se ejecutan** acciones destructivas.

## 1. Comprobaciones automáticas (ya realizadas, sin tocar el sistema)

| Comprobación | Cómo | Resultado |
| --- | --- | --- |
| Esquema de la configuración (campos, `id` únicos, `modo` válido, overrides existentes, orden de secciones) | `python3 tests/verificar-config.py` | OK |
| Paridad 1:1 Testing | `tests/verificar-config.py --antiguo-testing …` | 13/13, sin cambios |
| Paridad 1:1 Sid | `tests/verificar-config.py --antiguo-sid …` | 12/12 + AutoFirma (adición) |
| Comando en modo `auto` | simulado | `bash <script>` |
| `requiere_sudo` | simulado | `sudo env PATH=<shim>… LANZADOR_INTEGRADO=1 bash <script>` |
| `apt_update` | simulado | `sudo apt update` antes del script |
| Modo `gui` | simulado | llama a `_lanzar_gui` (Popen sin terminal) |
| Modo `terminal` (Konsole) | simulado | `konsole -e bash -c …` y 4.º argumento `1`/`0` según `requiere_sudo` |
| Chips de estado | simulado | Cancelado → `off`, Completado → `ok` |
| `entorno()` | directo | shim de whiptail al frente del `PATH`, `LANZADOR_INTEGRADO=1`, `PAGER=cat` |
| Shim de `whiptail` | `bash -n` | sintaxis OK |
| `VistaLog` (ANSI y `\r`) | directo | colores aplicados; `\r` reescribe la línea |
| Instalador en copia limpia | `instalar-lanzador.sh` con `HOME` ficticio | `.desktop` correcto; idempotente; aborta si falta/está corrupta la config |
| Selector, detección y persistencia | offscreen | cambio Testing/Sid en la misma ventana; guardado en QSettings |

## 2. Pruebas manuales en Debian Testing y Debian Sid

### 2.1. Prueba de humo (no modifica el sistema) — en AMBAS distribuciones

1. Instalar: `bash instalar-lanzador.sh`.
2. Comprobar el `.desktop`: `Name=Lanzador Debian`, `Exec` apunta a la copia
   instalada; aparece en el menú.
3. Abrir el lanzador **como usuario normal**. No debe arrancar como root.
4. Comprobar el bloque **DISTRIBUCIÓN**: cambia entre Testing y Sid **sin abrir
   otra ventana**, y al cerrar y reabrir recuerda la última.
5. "Sistema detectado" muestra el sistema; la detección **no bloquea** el cambio.
6. Testing → **13 acciones**; Sid → **13** (con sección *Firma electrónica*).
7. Buscador y filtro por sección funcionan.
8. En una acción `peligroso`, aparece la confirmación; si se cancela, no se
   ejecuta nada.
9. Comprobar que los datos van a `~/.local/share/lanzador-debian/`.

### 2.2. Acciones que modifican el sistema — prueba manual obligatoria

Recomendación: hacerlo en una **máquina virtual o con instantánea** previa.
"Revertir" indica la acción de limpieza/desinstalación equivalente cuando existe.

| # | Distro | Acción | Riesgo | Qué comprobar | Revertir |
| --- | --- | --- | --- | --- | --- |
| 1 | Testing | Corregir repositorios Debian Testing | Medio (APT) | `/etc/apt/sources.list*` en formato deb822; `apt update` sin errores | restaurar fuentes |
| 2 | Testing | Configurar Debian Testing | Alto | paquetes/fuentes/flatpak según el script | Limpiar Debian Testing |
| 3 | Testing | Limpiar Debian Testing | **Destructivo** | qué elimina realmente | reinstalar/instantánea |
| 4 | Testing | Sincronizar repositorios APT | Bajo | `apt update` termina OK | — |
| 5 | Testing | Instalar gaming | Alto | Steam, Heroic, GameMode, MangoHud, ntsync | Limpiar gaming |
| 6 | Testing | Limpiar gaming | **Destructivo** | qué elimina | instantánea |
| 7 | Testing/Sid | Instalar sched-ext | Alto (compila) | kernel con `CONFIG_SCHED_CLASS_EXT=y`; herramientas scx | Desinstalar sched-ext |
| 8 | Testing/Sid | Instalar gestor de sched-ext (GUI) | Medio | requiere sched-ext ya instalado; abre la app | desinstalar GUI |
| 9 | Testing/Sid | Desinstalar sched-ext | **Destructivo** | qué elimina | — |
| 10 | Testing/Sid | Instalar driver NVIDIA | Alto | nvidia-smi; MOK si Secure Boot; reinicio | — |
| 11 | Testing/Sid | Instalar asusctl / ROG Control | Medio | hardware ASUS detectado; servicio asusd | Desinstalar asusctl |
| 12 | Testing/Sid | Desinstalar asusctl / ROG Control | **Destructivo** | qué elimina | — |
| 13 | Testing/Sid | Configurar terminal con Starship | Bajo | `~/.bashrc`/config; abre shell nueva | quitar línea de Starship |
| 14 | Sid | Convertir Debian Testing a Sid | **Muy alto** (`requiere_sudo`) | fuentes a `sid`; `apt update`; reinicio; upgrade | reinstalar/instantánea |
| 15 | Sid | Configurar Debian Sid | Alto | paquetes/flatpak | Limpiar Debian Sid |
| 16 | Sid | Limpiar Debian Sid | **Destructivo** | qué elimina | instantánea |
| 17 | Sid | Instalar gaming | Alto | igual que Testing (repo distinto) | Limpiar gaming |
| 18 | Sid | Limpiar gaming | **Destructivo** | qué elimina | instantánea |
| 19 | Sid | Instalar AutoFirma | Medio (modo `gui`) | abre la app de firma sin terminal; log en `logs/instalar_autofirma_qt.log` | desinstalar AutoFirma |

### 2.3. Acciones compartidas — verificar en **ambas** distribuciones

Antes de darlas por "compartidas", comprobar que se comportan igual en Testing y
Sid (aquí es donde puede haber diferencias reales):

- [ ] Instalar sched-ext
- [ ] Instalar gestor de sched-ext (GUI)
- [ ] Desinstalar sched-ext
- [ ] Instalar driver NVIDIA
- [ ] Instalar asusctl / ROG Control
- [ ] Desinstalar asusctl / ROG Control
- [ ] Configurar terminal con Starship

Si alguna difiere entre distribuciones, **separarla** en `testing.json`/`sid.json`
(una definición por distro) en lugar de dejarla en `comunes.json`.

### 2.4. Pruebas del motor dentro de Debian (no destructivas)

- Preguntas de un script: responder desde el campo inferior.
- Contraseña de `sudo`: el campo pasa a modo oculto.
- `whiptail --yesno/--msgbox/--infobox`: se muestran como preguntas de texto.
- Script con menús/listas: se abre en Konsole.
- **Cancelar**: Ctrl+C y, si no responde, termina en unos segundos.
- Modo `gui`: la app se abre sin terminal y el log queda en `logs/`.

## 3. Checklist de paridad

`[x]` = verificado automáticamente · `[ ]` = pendiente de prueba manual en Debian.

### 3.1. Interfaz y motor

- [x] PyQt6 · barra lateral · buscador · tarjetas · estados
- [x] Ejecución integrada por pseudo-terminal (PTY)
- [x] Modos `auto`, `integrado`, `gui`, `terminal` (construcción de comandos verificada)
- [x] Entrada de contraseña de `sudo` (campo oculto) — lógica verificada
- [x] Shim de `whiptail` (`--yesno`/`--msgbox`/`--infobox`) — sintaxis verificada
- [x] Detección de menús/listas → fallback a Konsole — lógica verificada
- [x] Cancelación escalonada (Ctrl+C → TERM → KILL) — lógica presente
- [x] Logs (modo `gui`)
- [x] `git clone` / `git pull --ff-only` antes de ejecutar
- [x] Ejecución como usuario normal; se niega como root
- [x] `.desktop` + `instalar-lanzador.sh`
- [x] Selector Testing/Sid en una sola ventana
- [x] Detección de la distribución como valor inicial
- [x] Persistencia con QSettings
- [ ] Prueba de humo completa en Debian Testing (sección 2.1)
- [ ] Prueba de humo completa en Debian Sid (sección 2.1)
- [ ] Preguntas/contraseña/whiptail/Konsole/cancelación en un script real (sección 2.4)

### 3.2. Acciones

- [x] Las **13** acciones de Testing presentes y equivalentes (paridad 1:1)
- [x] Las **12** acciones de Sid presentes y equivalentes (paridad 1:1)
- [x] `requiere_sudo` (Convertir Testing → Sid) — comando verificado
- [x] `apt_update` — comando verificado
- [x] AutoFirma en modo `gui`
- [ ] Acción 1–6 de Testing probadas de verdad (tabla 2.2)
- [ ] Acción 14–19 de Sid probadas de verdad (tabla 2.2)
- [ ] Las 7 compartidas probadas de verdad en **ambas** distros (2.3)

## 4. Cómo repetir las comprobaciones automáticas

```bash
cd ~/lanzador-debian
python3 tests/verificar-config.py

# con paridad contra los lanzadores antiguos:
python3 tests/verificar-config.py \
  --antiguo-testing ~/Proyectos/instalador-aplicaciones-debian-testing/proyectos.json \
  --antiguo-sid     ~/Proyectos/lanzador-debian-sid/proyectos.json
```

## 5. Diferencias y notas

1. La detección de distro es una **heurística**: Testing suele reportar
   `trixie/sid` y Sid `sid`; un estable o un derivado devuelven `None` y se abre
   Testing por defecto. La elección manual siempre manda.
2. Las **acciones compartidas** son la única parte que aún puede esconder
   diferencias entre Testing y Sid; hay que probarlas en ambas (2.3).
3. Los scripts reales viven en repos externos (`debian-testing-setup`,
   `debian-sid-setup`, `gaming-*`, etc.); esta fase no los modifica ni ejecuta.
