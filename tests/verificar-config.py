#!/usr/bin/env python3
"""Verifica la configuración y la paridad del Lanzador Debian.

No ejecuta acciones ni toca el sistema: solo lee config/ y, opcionalmente,
compara contra los proyectos.json de los lanzadores antiguos.

Uso:

    python3 tests/verificar-config.py

    # para comprobar la paridad 1:1 contra los repos antiguos:
    python3 tests/verificar-config.py \
        --antiguo-testing /ruta/instalador-aplicaciones-debian-testing/proyectos.json \
        --antiguo-sid     /ruta/lanzador-debian-sid/proyectos.json

Sale con código 0 si todo está correcto y 1 si encuentra algún problema.
"""
import argparse
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))

import lanzador as lz  # noqa: E402  (necesita PyQt6, ya es requisito de la app)

PROBLEMAS = []


def problema(msg):
    PROBLEMAS.append(msg)
    print(f"  [ERROR] {msg}")


def validar_accion(a, donde):
    for campo in ("id", "seccion", "titulo", "repo", "script"):
        if not a.get(campo):
            problema(f"{donde}: falta el campo obligatorio '{campo}' ({a.get('id', '?')})")
    if "id" in a and not isinstance(a["id"], str):
        problema(f"{donde}: 'id' debe ser texto")
    if a.get("modo") is not None and a["modo"] not in lz.MODOS:
        problema(f"{donde}: modo inválido '{a['modo']}' ({a.get('id')})")
    for campo in ("apt_update", "requiere_sudo", "peligroso"):
        if campo in a and not isinstance(a[campo], bool):
            problema(f"{donde}: '{campo}' debe ser booleano ({a.get('id')})")


def normalizar(a):
    return (a["repo"], a["script"], a.get("modo", "auto"),
            bool(a.get("peligroso")), bool(a.get("apt_update")),
            bool(a.get("requiere_sudo")))


def comparar_paridad(nombre, antiguo_path, distro):
    print(f"\n== Paridad {nombre} contra {antiguo_path}")
    antiguo = json.loads(Path(antiguo_path).read_text(encoding="utf-8"))["acciones"]
    nuevo = lz.cargar_acciones(distro)
    idx_a = {(a["seccion"], a["titulo"]): normalizar(a) for a in antiguo}
    idx_n = {(a["seccion"], a["titulo"]): normalizar(a) for a in nuevo}

    faltan = [k for k in idx_a if k not in idx_n]
    extra = [k for k in idx_n if k not in idx_a]
    distintas = [(k, idx_a[k], idx_n[k]) for k in idx_a if k in idx_n and idx_a[k] != idx_n[k]]

    print(f"  antiguo: {len(antiguo)} | nuevo: {len(nuevo)}")
    if faltan:
        problema(f"paridad {nombre}: faltan acciones {faltan}")
    else:
        print("  [OK] ninguna acción antigua falta")
    if distintas:
        for k, o, n in distintas:
            problema(f"paridad {nombre}: '{k[1]}' cambia de {o} a {n}")
    else:
        print("  [OK] todos los campos coinciden")
    if extra:
        print(f"  [NOTA] acciones añadidas: {[k[1] for k in extra]}")
    else:
        print("  [OK] sin acciones añadidas")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--antiguo-testing")
    ap.add_argument("--antiguo-sid")
    args = ap.parse_args()

    print("== Esquema de configuración")
    comunes = lz._leer_json(lz.CONFIG_DIR / "comunes.json")
    if not comunes.get("carpeta_proyectos"):
        problema("comunes.json: falta 'carpeta_proyectos'")

    ids_vistos = set()
    for a in comunes.get("acciones", []):
        validar_accion(a, "comunes.json")
        if a.get("id") in ids_vistos:
            problema(f"comunes.json: 'id' duplicado '{a.get('id')}'")
        ids_vistos.add(a.get("id"))

    for distro in ("testing", "sid"):
        propia = lz._leer_json(lz.CONFIG_DIR / f"{distro}.json")
        for campo in ("nombre", "acciones"):
            if campo not in propia:
                problema(f"{distro}.json: falta '{campo}'")
        ids_d = set()
        for a in propia.get("acciones", []):
            validar_accion(a, f"{distro}.json")
            if a.get("id") in ids_d:
                problema(f"{distro}.json: 'id' duplicado '{a.get('id')}'")
            ids_d.add(a.get("id"))
        # overrides deben apuntar a acciones existentes
        acciones_finales = {a["id"] for a in lz.cargar_acciones(distro)}
        for aid in propia.get("overrides", {}):
            if aid not in acciones_finales:
                problema(f"{distro}.json: override a 'id' inexistente '{aid}'")
        secciones_usadas = []
        for a in lz.cargar_acciones(distro):
            if a["seccion"] not in secciones_usadas:
                secciones_usadas.append(a["seccion"])
        faltan_orden = [s for s in secciones_usadas if s not in propia.get("orden_secciones", [])]
        if faltan_orden:
            print(f"  [NOTA] {distro}: secciones fuera de orden_secciones: {faltan_orden}")

    if not PROBLEMAS:
        print("  [OK] esquema, ids, overrides y orden correctos")

    print("\n== Acciones por distribución")
    for distro in ("testing", "sid"):
        acciones = lz.cargar_acciones(distro)
        print(f"  {distro}: {len(acciones)} acciones")

    if args.antiguo_testing:
        comparar_paridad("TESTING", args.antiguo_testing, "testing")
    if args.antiguo_sid:
        comparar_paridad("SID", args.antiguo_sid, "sid")

    print()
    if PROBLEMAS:
        print(f"RESULTADO: {len(PROBLEMAS)} PROBLEMA(S)")
        return 1
    print("RESULTADO: TODO CORRECTO")
    return 0


if __name__ == "__main__":
    sys.exit(main())
