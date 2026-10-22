# 02 · TRD — Requisitos técnicos

> Decisiones técnicas para que un agente (o persona) construya sin adivinar. "Hoy" = verificado en el repo. **[Propuesto]** = decisión recomendada.

## 1. Stack actual

| Capa | Tecnología |
|---|---|
| Frontend principal | HTML/CSS/JS vanilla en **un solo `index.html`** (~1,2 MB, ~19 000 líneas, ~210 funciones). Sin build. |
| Suite `/products` | App React + Vite **compilada** (solo bundles en `products/assets/`; el código fuente no está en este repo) |
| Hosting | GitHub Pages (`CNAME` → `aeonnimbus.com`) con `404.html`. *(AEONNIMBUS.md menciona Vercel; está desactualizado)* |
| Datos | JSON estáticos en la raíz, regenerados por GitHub Actions |
| Pipelines | Python 3.12: `yfinance`, `pypdf`, `requests`; stdlib para RSS |
| CI/CD | GitHub Actions (`refresh-feed`, `refresh-market-data`) con `contents: write` |
| Librerías CDN | SheetJS 0.18.5 (`cdnjs`), Google Fonts |
| Fuentes tipográficas | Newsreader, Inter, JetBrains Mono (y Space Mono en alguna sección) |

## 2. APIs externas

| Servicio | Uso | Dónde |
|---|---|---|
| Substack RSS (`aeonnimbus.substack.com/feed`) | Feed de research | `refresh_feed.py`; fallback en cliente: rss2json, allorigins, corsproxy.io |
| Finnhub | Cotizaciones en vivo (ticker, tools) | cliente, `fetch` directo |
| Financial Modeling Prep | Perfil, histórico S&P 500 | cliente |
| Google Gemini (`gemini-2.5-flash` → `2.5-pro` → `2.0-flash`) | AI Pitcher | cliente |
| yfinance | Cadenas de opciones | `refresh_market_data.py` |
| House Clerk (STOCK Act, ZIP/XML + PDFs) | Operaciones del Congreso | `refresh_market_data.py` |
| GitHub (badges de CI de 6 repos `aeon-*`) | Credibilidad de tools | `<img>` en la página |

## 3. Arquitectura

```
Substack RSS ─┐                       ┌─> research-feed.json ─┐
yfinance      ├─> GitHub Actions ─────┤                       ├─> index.html (fetch, no-cache)
House Clerk  ─┘   (cron + commit)     └─> market-data.json  ──┘
                                                │
Finnhub / FMP / Gemini  <── fetch directo desde el navegador (claves expuestas)
```

Navegación: `sp(id)` muestra `#pg-<id>` y oculta el resto. Sin router, sin historial por página.

## 4. Decisiones **[Propuesto]**

| Decisión | Recomendación | Motivo |
|---|---|---|
| Mantener estático | **Sí**, no pasar a framework pesado todavía | Coste cero, SEO simple, bajo mantenimiento |
| Proxy para APIs con clave | **Cloudflare Workers** (o Vercel Functions) | Esconde claves, permite rate limit y caché |
| Base de datos | **Supabase (Postgres)** solo para formularios/leads/uso de Pitcher | Ver doc 05 |
| Partir el monolito | Extraer `css/`, `js/<modulo>.js` y plantillas por página sin cambiar de stack; después valorar Vite | Reducir 1,2 MB, cachear, testear |
| Routing | `history.pushState` + `404.html` fallback, o páginas HTML reales generadas | URLs indexables |
| Tests | Vitest para funciones puras (Black-Scholes, DCF, sizing); Playwright para humo | Hoy no hay tests en este repo |
| Lint | ESLint + Prettier + `python -m ruff` para scripts | Consistencia |

## 5. Entorno y convenciones
- Respeta el estilo existente: variables CSS en `:root`/`html.dark`, nombres cortos (`.tc`, `.tchd`, `.tbody`, `.pg`).
- **Edición**: `AEONNIMBUS.md` indica fin de línea CRLF y usar Python `str.replace`. Comprobar con `file index.html` antes de editar; si ya es LF, la restricción no aplica.
- Commits automáticos de bots en `main` (`chore: refresh …`): hacer `git pull --rebase` antes de empujar.
- Los workflows usan `concurrency` para no solaparse.

## 6. Seguridad (hallazgos del repo)

| Severidad | Hallazgo | Acción |
|---|---|---|
| **Alta** | Claves de **Finnhub**, **FMP** y **Gemini** hardcodeadas en `index.html` (la de Gemini ofuscada en base64, lo que no la protege) | **Rotar las tres** y moverlas a un proxy. Considerar el historial de git comprometido |
| Media | `GPTBot`, `anthropic-ai`, `CCBot` permitidos en `robots.txt` | Decisión de negocio consciente |
| Media | Proxies CORS públicos (allorigins, corsproxy.io) como fallback | Eliminar al existir `research-feed.json` fiable |
| Baja | `mailto:` como único canal de contacto | Sustituir por formulario con anti-spam |
| Baja | Falta CSP | Añadir `<meta http-equiv="Content-Security-Policy">` tras mover claves |

## 7. Rendimiento
- `index.html` 1,2 MB sin dividir; `research-feed.json` 0,9 MB (incluye `content` completo de cada post) → publicar versión ligera (sin `content`) para la lista.
- Vídeos de `products/videos` (~25 MB en total): `preload="none"` y poster.
- Imágenes en WebP ya existentes: mantener.

## 8. Criterios de aceptación técnica
- Ninguna clave secreta en el árbol ni en el historial vigente.
- Lighthouse móvil ≥ 90 rendimiento, ≥ 95 SEO/accesibilidad.
- Workflows verdes; una caída de fuente conserva el snapshot anterior (ya implementado: "kept from the previous snapshot").
- Tests de funciones financieras con valores de referencia.
