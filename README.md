# Aprendizaje por Refuerzo

Presentación web para la exposición de Ingeniería de Sistemas Autoadaptables
(Universidad EAFIT). La página **es** el material: se proyecta y se navega
durante la charla con ← → / espacio / swipe.

27 láminas en tres momentos:

1. **Qué es el Aprendizaje por Refuerzo** — partiendo del Aprendizaje
   Supervisado y No Supervisado, y del bucle entre agente y entorno.
2. **Cómo funciona** — Markov, procesos de decisión de Markov, retorno y
   descuento, Bellman, programación dinámica, Monte Carlo, TD, Q-learning y
   exploración frente a explotación.
3. **Ejemplo cotidiano** — cómo aprende un perro, y qué sale mal al entrenarlo.

## Estructura

    presentacion/    La presentación. Abrir index.html en el navegador.
      construir.py     Genera un archivo autocontenido para publicar
      verificar.py     Comprueba que ningún texto se salga de los SVG
    estilo/          Muestra de estilo aprobada, congelada como referencia

HTML, CSS y JavaScript sin dependencias ni build. Lo único externo son las
fuentes de Google Fonts.
