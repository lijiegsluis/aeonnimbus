# 03 · Flujo de la app

## 1. Mapa de navegación

```
Nav superior
├─ Home                      sp('home')
├─ Research                  sp('research')
├─ Track Record              sp('track')
├─ Fund Lab ▾ (dropdown)
│   ├─ Asset Allocation Dynamic Fund  → sp('portfolios') + showPortFund()
│   ├─ Systematic Strategies          → sp('strats')
│   └─ Open Source Tools              → sp('tools')
├─ Markets                   sp('markets')
├─ AI Pitcher  (badge dorado) sp('pitcher')
├─ Services / About / Contact
├─ [EN ▾] idioma · [tema] claro/oscuro
└─ CTA «Subscribe →» (Substack) · GitHub ↗ · LinkedIn ↗
```
Todo vive en `index.html`; `sp(id)` pone `display:block` en `#pg-<id>` y oculta las demás.

## 2. Fases del recorrido del usuario

| Fase | Pantalla | Qué ve | Salida natural |
|---|---|---|---|
| Descubrir | Home | Propuesta de valor, métricas, ticker | Research / Track / Tools |
| Evaluar | Research → Track Record | Tesis + prueba de aciertos | Subscribe o Services |
| Probar | Tools / Markets / AI Pitcher | Uso gratuito | Exportar Excel, GitHub, Services |
| Convertir | Services / Contact | Solicitud de acceso | Email / formulario |
| Retener | Substack | Newsletter | Vuelta al sitio |

## 3. Comportamiento por interacción

### Navegación y estado
| Acción | Resultado |
|---|---|
| Clic en ítem de nav | `sp(id)`: muestra la página, cierra menús, sube al inicio, actualiza barra de progreso |
| Scroll > umbral | Aparece `#stt` (scroll to top); la barra superior de 2 px avanza |
| Botón tema | Alterna `html.dark`/`html.light`; guarda `theme` en `localStorage`; se restaura al cargar |
| Selector de idioma | `setLang(x)`: sustituye textos `data-i18n`, actualiza etiqueta (`EN/ES/FR/DE/IT/CN`), guarda `lang` |
| Dropdown Fund Lab | Hover/clic abre; elegir cierra y navega |

### Research
1. Al abrir: `fetch('research-feed.json',{cache:'no-cache'})`.
2. Si falla → rss2json → allorigins → corsproxy (cadena de respaldo).
3. Filtro por categoría (`equity`, `macro`, `geo`, `central-bank`) oculta/mustra `.post[data-cat]`.
4. «Read →» abre el post en Substack en pestaña nueva.

### Markets
1. Carga `market-data.json` (`flow`, `congress`, `generated_at`).
2. Muestra `as_of`; filas de opciones con sesgo *bullish/bearish*, prima, vol/OI.
3. Congreso: político, partido, ticker, compra/venta, rango, retraso de divulgación, enlace al PDF oficial.

### Herramientas (patrón común)
1. Clic en cabecera `.tchd` → despliega `.tbody`.
2. Rellenar inputs (con valores por defecto si están vacíos: p. ej. S=100, K=100, T=0,5).
3. Botón calcular → resultado + gráfico SVG; los botones «Export Excel» **aparecen solo tras calcular**.
4. `vt('tool','panel')` cambia pestañas internas (BS / MC / Bond / Vol).
5. Exportar → SheetJS genera `.xlsx` en el navegador.

### AI Pitcher
1. Usuario escribe ticker (+ peers y contexto opcionales).
2. Se guarda `an_pitcher_email` en `localStorage` si se pide.
3. `_callGemini` prueba `gemini-2.5-flash` → `2.5-pro` → `2.0-flash`; el primero que responda OK gana.
4. Render del informe de 14 secciones; si todos fallan → mensaje de error.
5. **[Propuesto]** pasar por proxy con límite de uso por IP/email.

### Contacto / servicios
- Hoy: botón construye `mailto:` y lo abre en el cliente de correo.
- **[Propuesto]** formulario → endpoint → tabla `contact_requests` → confirmación en pantalla.

### Suite `/products`
Landing React con vídeos demo (`aeon-explainer`, `tool-*`) y `select.html` para elegir producto.

## 4. Estados y casos límite
| Caso | Comportamiento esperado |
|---|---|
| JSON de datos no carga | Mostrar último dato en caché (`localStorage` con `CACHE_KEY`) y aviso «datos de hh:mm» |
| API de cotizaciones sin respuesta | Dejar «—» y reintentar en 60 s (intervalo existente) |
| Entrada numérica vacía/negativa | Usar valor por defecto o mensaje inline |
| `localStorage` bloqueado | Funcionar sin persistencia (todo en `try/catch`) |
| URL directa a una sección | **Hoy no soportado** (sin router); Propuesto: hash o rutas reales |
| Móvil | Menú colapsado, rejillas `g3g/g4g` pasan a 2 columnas, `sec3` a 1 |
