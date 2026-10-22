# 01 · PRD — Aeon Nimbus Research

> Documento de requisitos de producto. Describe el producto **tal como existe hoy** (derivado del código del repo) y lo que debe construirse a continuación. Lo marcado **[Propuesto]** no existe todavía.

## 1. Resumen

**Aeon Nimbus Research** (aeonnimbus.com) es el sitio institucional de LiJie Guo, analista independiente de macro y renta variable. Combina cuatro cosas en un solo sitio:

1. **Investigación**: artículos publicados en Substack, mostrados como feed.
2. **Prueba de resultados (track record)**: calls publicados *antes* del resultado, estrategias sistemáticas con dashboards y PDFs.
3. **Herramientas gratuitas**: calculadoras y trackers de mercado que demuestran capacidad cuantitativa.
4. **Captación**: suscripción a Substack, solicitud de servicios/acceso, contacto.

Lema de marca: *"Spanish-born, Chinese. Global markets & technology. Investing since 18."*

## 2. Problema y propuesta de valor

- El lector institucional (family offices, fondos pequeños, reclutadores, inversores privados serios) no se fía de "gurús": necesita **evidencia verificable** de que el analista acierta.
- Propuesta: *"The market misprices"* — tesis argumentadas + calls fechados + herramientas abiertas (código en GitHub con CI) + track record publicado.

## 3. Usuarios objetivo

| Persona | Qué busca | Acción deseada |
|---|---|---|
| Inversor / family office | Tesis y calls con track record | Suscribirse, pedir servicios |
| Reclutador / empleador | CV, formación (emlyon, Polimi, Bayes), proyectos | Contactar, descargar CV |
| Quant / developer | Herramientas y repos open source | Usar tools, visitar GitHub |
| Lector de Substack | Ver más contexto | Volver al sitio, suscribirse |

## 4. Funcionalidades (estado actual)

### 4.1 Páginas (SPA de una sola página, `sp(id)`)
| ID | Página | Contenido |
|---|---|---|
| `home` | Inicio | Hero, "12 Systematic Strategies", "Pre-Outcome Investment Calls", "Six Analyst Tools — Free", sectores bajo cobertura, ticker de mercado |
| `research` | Research | Lista de posts con filtro por categoría (equity, macro, geo, central-bank), cargada de `research-feed.json` |
| `track` | Track Record | Calls pre-resultado, heatmaps de rentabilidad anual por par FX, enlaces a informes |
| `strats` | Systematic Strategies | Estrategias cuantitativas; dashboards y PDFs en `/reports` |
| `portfolios` | Fund Lab | Asset Allocation Dynamic Fund (cartera modelo) |
| `tools` | Open Source Tools | 12 tarjetas de herramientas (ver 4.2) |
| `markets` | Markets | Flujo de opciones inusual y operaciones del Congreso (`market-data.json`) |
| `pitcher` | AI Pitcher | Chat que genera un informe de equity research de 14 secciones con Gemini |
| `services` | Services | Oferta de servicios y solicitud de acceso completo |
| `about` | About | Formación, investigación actual, disponibilidad, cómo se construye una tesis |
| `contact` | Contact | Contacto |

### 4.2 Herramientas (`#tc-*`)
`quant` (Black-Scholes, Monte Carlo, bonos, volatilidad) · `dcf` · `sotp` · `corr` (matriz de correlación) · `size` (position sizing) · `port` (portfolio construction) · `idea` (idea screener) · `analyst` · `earnings` · `heatmap` · `congress` · `tradewar`.
Exportan a Excel con SheetJS (`exportBSExcel()`, `exportMCExcel()`, `exportBondExcel()`, `exportDCFExcel()`).

### 4.3 Transversales
- Tema claro/oscuro (`html.dark` / `html.light`, persistido en `localStorage`).
- Multi-idioma: EN, ES, FR, DE, IT, CN (`setLang`, atributos `data-i18n`).
- SEO: JSON-LD, Open Graph, `sitemap.xml`, `robots.txt` (abierto a crawlers de IA).
- Barra de progreso, botón "scroll to top".
- Suite de producto separada en `/products` (app React compilada): "Intelligence Suite" con vídeos demo.

### 4.4 Automatización de datos
- `refresh-feed.yml`: cada 6 h baja el RSS de Substack → `research-feed.json`.
- `refresh-market-data.yml`: laborables 16:41 y 21:41 UTC → `market-data.json` (opciones inusuales vía yfinance + STOCK Act de la Cámara).
- Ambos hacen commit automático si hay cambios.

## 5. Fuera de alcance (hoy)
Cuentas de usuario, pagos, comentarios, ejecución de órdenes, asesoramiento personalizado.

## 6. Requisitos nuevos **[Propuesto]**

| # | Requisito | Prioridad |
|---|---|---|
| R1 | Mover claves de API (Finnhub, FMP, Gemini) fuera del cliente a un proxy serverless | **P0** |
| R2 | Formulario real de contacto / solicitud de acceso con almacenamiento (hoy solo `mailto:`) | P1 |
| R3 | Rutas reales por página (URLs indexables: `/research`, `/tools`…) en vez de un solo `index.html` de 1,2 MB | P1 |
| R4 | Track record automatizado: tabla de calls con fecha, precio de entrada, resultado actual | P1 |
| R5 | Suscripción con captura de email propia (además de Substack) | P2 |
| R6 | Página por post de investigación | P2 |
| R7 | Límite de uso y registro en AI Pitcher | P1 |
| R8 | Disclaimer legal visible por página (no es asesoramiento financiero) | P0 |

## 7. Métricas de éxito
- Suscriptores Substack atribuidos al sitio (UTM).
- Solicitudes de contacto/servicios por mes.
- Usos de herramientas (eventos) y exportaciones a Excel.
- Lighthouse ≥ 90 en rendimiento móvil (hoy dudoso por el HTML de 1,2 MB).
- 0 claves expuestas en el repo.

## 8. Riesgos
- **Legal/regulatorio**: contenido financiero sin disclaimer homogéneo; track record debe ser verificable y no engañoso.
- **Claves en el cliente** (ver TRD §6).
- **Mantenibilidad**: monolito de ~19 000 líneas.
- **Fuentes de datos frágiles**: yfinance y scraping de disclosures pueden romperse sin aviso.
