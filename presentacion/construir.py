#!/usr/bin/env python3
"""Genera la versión publicable de la presentación.

`index.html` enlaza `sistema.css` para poder trabajar en local con el estilo
separado. Al publicar hace falta un único archivo autocontenido, así que este
script incrusta el CSS y quita el envoltorio <html>/<head> que el visor de
Artifacts añade por su cuenta.

Uso:  python3 presentacion/construir.py [destino.html]
"""

import re
import sys
import pathlib

AQUI = pathlib.Path(__file__).resolve().parent


def construir():
    html = (AQUI / "index.html").read_text()
    css = (AQUI / "sistema.css").read_text()

    # 1. El <link> local se sustituye por el CSS incrustado.
    enlace = '<link rel="stylesheet" href="sistema.css">'
    if enlace not in html:
        raise SystemExit("No encuentro el <link> a sistema.css en index.html")
    html = html.replace(enlace, "<style>\n" + css + "\n</style>")

    # 2. Fuera el envoltorio: el visor lo pone él.
    for patron in (r"<!doctype html>\s*", r'<html lang="es">\s*', r"<head>\s*",
                   r'<meta charset="utf-8">\s*', r'<meta name="viewport"[^>]*>\s*',
                   r"\s*</head>\s*", r"\s*<body>\s*",
                   r"\s*</body>\s*", r"\s*</html>\s*"):
        html = re.sub(patron, "\n", html, flags=re.I)

    return html.strip() + "\n"


if __name__ == "__main__":
    destino = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else AQUI / "publicable.html")
    contenido = construir()
    destino.write_text(contenido)
    print(f"✓ {destino}  ({len(contenido):,} bytes)")
