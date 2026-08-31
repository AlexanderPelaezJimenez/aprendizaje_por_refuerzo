#!/usr/bin/env python3
"""Verifica que ningún contenido de los SVG se salga de su viewBox.

Regla dura del proyecto: en esta presentación NO puede haber texto recortado
ni superpuesto. Este script cubre el caso "se sale del lienzo", que es el que
se puede comprobar por geometría.

Uso:  python3 estilo/verificar-svg.py [archivo.html ...]
Sale con código 1 si encuentra algo fuera de rango.
"""

import re
import sys
import pathlib
import xml.etree.ElementTree as ET

SVG_NS = "{http://www.w3.org/2000/svg}"

# Ancho medio de carácter, en múltiplos del font-size. Generoso a propósito:
# preferimos un falso positivo a un texto recortado en la proyección.
ANCHO_CARACTER = {
    "rotulo": 0.62,      # Shantell Sans, peso 800
    "rotulo-min": 0.52,  # Caveat, más estrecha
    None: 0.62,
}


def numeros(d):
    """Todos los pares de coordenadas de un atributo `d` de <path>."""
    crudos = [float(n) for n in re.findall(r"-?\d+\.?\d*", d)]
    return crudos


def caja_texto(el):
    """Caja envolvente aproximada de un <text>, respetando text-anchor."""
    texto = "".join(el.itertext())
    tam = float(el.get("font-size", 16))
    clase = el.get("class")
    factor = ANCHO_CARACTER.get(clase, ANCHO_CARACTER[None])

    ancho = len(texto) * tam * factor
    x = float(el.get("x", 0))
    y = float(el.get("y", 0))

    anclaje = el.get("text-anchor", "start")
    if anclaje == "middle":
        x0 = x - ancho / 2
    elif anclaje == "end":
        x0 = x - ancho
    else:
        x0 = x

    # y es la línea base: la altura de mayúscula sube, los descendentes bajan.
    return x0, y - tam * 0.78, x0 + ancho, y + tam * 0.25, repr(texto[:40])


def caja_elemento(el):
    """Devuelve (x0, y0, x1, y1, descripcion) o None si no aporta geometría."""
    etiqueta = el.tag.replace(SVG_NS, "")

    if etiqueta == "text":
        return caja_texto(el)

    if etiqueta == "circle":
        cx, cy = float(el.get("cx", 0)), float(el.get("cy", 0))
        r = float(el.get("r", 0))
        return cx - r, cy - r, cx + r, cy + r, f"<circle {cx},{cy}>"

    if etiqueta in ("rect",):
        x, y = float(el.get("x", 0)), float(el.get("y", 0))
        w, h = float(el.get("width", 0)), float(el.get("height", 0))
        borde = float(el.get("stroke-width", 0)) / 2
        return x - borde, y - borde, x + w + borde, y + h + borde, f"<rect {x},{y}>"

    if etiqueta == "path" and el.get("d"):
        vals = numeros(el.get("d"))
        if len(vals) < 2:
            return None
        xs, ys = vals[0::2], vals[1::2]
        # Los comandos relativos hacen que estos números no sean absolutos;
        # solo comprobamos paths con comandos absolutos.
        if re.search(r"[a-z]", re.sub(r"[a-z]", lambda m: "", el.get("d"))):
            pass
        if re.search(r"[mlcqsthvaz]", el.get("d")):
            return None  # relativo: fuera del alcance de esta comprobación
        borde = float(el.get("stroke-width", 0)) / 2
        return min(xs) - borde, min(ys) - borde, max(xs) + borde, max(ys) + borde, "<path>"

    return None


def revisar(ruta):
    html = pathlib.Path(ruta).read_text()
    fallos = []

    for bruto in re.findall(r"<svg\b.*?</svg>", html, re.S):
        raiz = ET.fromstring(bruto)
        vb = raiz.get("viewBox")
        if not vb:
            fallos.append((ruta, "un <svg> no declara viewBox", ""))
            continue
        _, _, ancho, alto = [float(n) for n in vb.split()]
        etiqueta_svg = (raiz.get("aria-label") or "sin aria-label")[:52]

        for el in raiz.iter():
            if el.tag.endswith("defs") or el.tag.endswith("marker"):
                continue
            caja = caja_elemento(el)
            if not caja:
                continue
            x0, y0, x1, y1, desc = caja
            if x0 < -1 or y0 < -1 or x1 > ancho + 1 or y1 > alto + 1:
                fallos.append((
                    etiqueta_svg,
                    f"{desc} se sale del viewBox {ancho:g}x{alto:g}",
                    f"caja = ({x0:.0f}, {y0:.0f}) → ({x1:.0f}, {y1:.0f})",
                ))

    return fallos


def main():
    rutas = sys.argv[1:] or ["estilo/muestra-estilo.html"]
    total = []
    for ruta in rutas:
        total += revisar(ruta)

    if not total:
        print(f"✓ Sin desbordes. Revisados: {', '.join(rutas)}")
        return 0

    print(f"✗ {len(total)} problema(s):\n")
    for donde, que, detalle in total:
        print(f"  · {donde}\n    {que}\n    {detalle}\n")
    return 1


if __name__ == "__main__":
    sys.exit(main())
