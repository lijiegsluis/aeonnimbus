# 06 · Plan de implementación

Secuencia de construcción, de lo urgente a lo opcional. Cada paso es un PR pequeño con criterio de "hecho" comprobable. Pasos 0–2 son los de mayor valor/menor riesgo.

## Fase 0 · Seguridad (inmediato, antes de cualquier otra cosa)
**0.1 Rotar claves expuestas**
- Revocar y regenerar las claves de Finnhub, FMP y Gemini que están en `index.html` (líneas ~14616, ~14826, ~18827).
- *Hecho cuando*: las claves antiguas devuelven 401/403.

**0.2 Proxy serverless**
- Crear Worker con secretos: `/api/quote`, `/api/profile`, `/api/pitcher`.
- Sustituir los `fetch` directos de `index.html` por rutas `/api/*`.
- Añadir CORS restringido a `https://aeonnimbus.com`.
- *Hecho cuando*: `grep -iE "finnhub.*token=|apikey=|atob\('" index.html` sin resultados.

**0.3 Escaneo de secretos**
- Activar GitHub secret scanning + push protection; añadir `gitleaks` en CI.

## Fase 1 · Base de calidad (sin cambiar el aspecto)
**1.1** Comprobar fin de línea (`file index.html`); documentar en `AEONNIMBUS.md`; corregir que mencione Vercel y la ruta `D:/` (hoy deploy es GitHub Pages).
**1.2** Añadir `package.json` con ESLint, Prettier, Vitest, Playwright.
**1.3** Extraer funciones puras (Black-Scholes, Monte Carlo, bonos, DCF, sizing) a `js/finance.js` y escribir tests con valores de referencia.
**1.4** Workflow `ci.yml`: lint + tests + humo Playwright (carga cada `#pg-*` sin errores de consola).
- *Hecho cuando*: CI verde en PR.

## Fase 2 · Separar el monolito
**2.1** Extraer CSS a `css/main.css` (mismas variables y reglas).
**2.2** Extraer JS por módulos: `nav.js`, `i18n.js`, `research.js`, `markets.js`, `tools/*.js`, `pitcher.js`.
**2.3** Mantener un único `index.html` ligero con `<script defer>`; verificar paridad visual con capturas de Playwright antes/después.
**2.4** Versionar assets (`?v=hash`) y activar caché larga.
- *Hecho cuando*: `index.html` < 150 KB y sin regresión visual.

## Fase 3 · Rutas e SEO
**3.1** Router con `history.pushState`: `/research`, `/track`, `/tools`, `/markets`, `/pitcher`, `/services`, `/about`, `/contact`.
**3.2** Generar páginas HTML por ruta (copias con `<title>`/meta propios) para indexación y `404.html` como fallback SPA en GitHub Pages.
**3.3** Actualizar `sitemap.xml` con todas las rutas.
**3.4** Disclaimer financiero común en el pie de cada página.
- *Hecho cuando*: cada ruta carga directamente y aparece con título propio en Lighthouse SEO ≥ 95.

## Fase 4 · Backend de captación
**4.1** Crear proyecto Supabase; aplicar el esquema del doc 05 (`contact_requests`, `subscribers`, `pitcher_usage`) con migraciones SQL versionadas en `db/migrations/`.
**4.2** Activar RLS y políticas; probar con rol `anon`.
**4.3** Endpoints `POST /api/contact` y `/api/subscribe` con honeypot + Turnstile.
**4.4** Sustituir el `mailto:` por formulario con estados: enviando / éxito / error.
**4.5** Rate limit en `/api/pitcher` y registro de uso.
- *Hecho cuando*: un envío de prueba aparece en la tabla y llega el aviso por email.

## Fase 5 · Track record automatizado
**5.1** Tablas `calls`, `call_marks`, `strategies`, `strategy_stats`; trigger de inmutabilidad en `calls`.
**5.2** Script Python (en `.github/scripts/`) que actualiza `call_marks` diariamente con precios de cierre.
**5.3** Exportar `data/track.json` en workflow nocturno; reescribir la página Track Record y los heatmaps para leer de ahí (hoy son HTML escrito a mano).
- *Hecho cuando*: añadir un call en la tabla lo muestra en la web tras el siguiente workflow, sin tocar HTML.

## Fase 6 · Datos y rendimiento
**6.1** Publicar `research-feed-light.json` (sin `content`) para la lista; cargar el contenido completo solo bajo demanda.
**6.2** Añadir retries/backoff a los scripts de refresco y alerta (issue automático) si una fuente falla N veces seguidas.
**6.3** Vídeos con `preload="none"` y póster; revisar peso de imágenes.
**6.4** CSP estricta una vez eliminadas las claves y proxies públicos.

## Fase 7 · Pulido y accesibilidad
- Contraste de `--ink3`, tamaños mínimos de 11 px, foco visible, `aria-expanded`, `prefers-reduced-motion`.
- Traducciones completas de los 6 idiomas (auditar claves `data-i18n` sin traducir).
- Página individual por post de research.

## Orden de ejecución recomendado
`0.1 → 0.2 → 0.3 → 1.x → 2.x → 3.x → 4.x → 5.x → 6.x → 7`

## Reglas para el agente que implemente
1. Un PR por subpaso; no mezclar fases.
2. Antes de empujar: `git pull --rebase` (los bots hacen commits en `main`).
3. Ejecutar lint + tests + humo antes de cada push.
4. Nunca pegar claves en código, commits ni logs.
5. No tocar `market-data.json` ni `research-feed.json` a mano: los regeneran los workflows.
6. Conservar la estética (doc 04) salvo que el paso diga lo contrario.
