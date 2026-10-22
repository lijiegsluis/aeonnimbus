# 05 · Esquema del backend

## 1. Situación actual: no hay backend
Los "datos" son dos JSON versionados en git, generados por GitHub Actions. No hay base de datos, ni autenticación, ni usuarios.

### 1.1 `research-feed.json` (forma compatible con rss2json)
```jsonc
{
  "status": "ok",
  "feed": { "url", "title", "link", "author", "description", "image" },
  "items": [{
    "title": "string",
    "pubDate": "YYYY-MM-DD HH:MM:SS",   // UTC
    "link": "url", "guid": "url",
    "author": "string",
    "thumbnail": "string",
    "description": "string",             // extracto
    "content": "html",                   // post completo (pesa ~0,9 MB en total)
    "enclosure": {},
    "categories": ["string"]
  }]
}
```
Fuente: `refresh_feed.py`. Si el RSS no trae items, **conserva el snapshot anterior**.

### 1.2 `market-data.json`
```jsonc
{
  "generated_at": "ISO-8601",
  "flow": {
    "as_of": "ISO-8601",
    "criteria": { /* umbrales: MIN_VOLUME 500, MIN_VOL_OI 2.0, MIN_PREMIUM 250k, EXPIRIES 4 */ },
    "items": [{                      // ~60
      "tk": "TSLA", "type": "call|put",
      "strike": "$375", "expiry": "Oct 23", "exp": "2026-10-23",
      "prem": "$26.8M", "premNum": 26792612,
      "volOI": "3.7×", "vol": 23177, "oi": 6272,
      "bias": "bullish|bearish", "side": "bought|sold",
      "time": "Oct 20 19:59 UTC"
    }]
  },
  "congress": {
    "as_of": "...", "source": "string",
    "items": [{                      // ~150
      "pol": "string", "party": "R|D|I", "state": "OH",
      "tk": "GOOG", "dir": "BUY|SELL", "amt": "$50,001–$100,000",
      "trdate": "Oct 16, 2026", "traded": "YYYY-MM-DD", "disclosed": "YYYY-MM-DD",
      "delay": 3, "sector": "string", "link": "url al PDF oficial"
    }]
  }
}
```
Cada sección se conserva del snapshot previo si su fuente falla.

### 1.3 Almacenamiento en navegador
| Clave | Contenido |
|---|---|
| `theme` | `light` / `dark` |
| `lang` | `en/es/fr/de/it/cn` |
| `CACHE_KEY` (precios) | `{ts, prices}` |
| `an_pitcher_email` | email del usuario de AI Pitcher |

## 2. Backend objetivo **[Propuesto]**
Motor: **Postgres (Supabase)**. Solo para lo que un sitio estático no puede hacer: formularios, leads, límite de uso y track record estructurado. La lectura pública sigue siendo JSON estático generado desde estas tablas.

### 2.1 Autenticación
- **Público (anónimo)**: puede insertar en `contact_requests`, `subscribers`, `pitcher_usage`; no puede leer nada.
- **Admin (LiJie)**: login con magic link de Supabase; único rol con lectura/edición total (`is_admin` en JWT).
- Sin registro de usuarios finales: no hay cuentas.

### 2.2 Tablas

#### `contact_requests`
| Columna | Tipo | Notas |
|---|---|---|
| id | uuid PK | `gen_random_uuid()` |
| created_at | timestamptz | default `now()` |
| name | text NOT NULL | |
| email | text NOT NULL | validar formato |
| kind | text | `services` \| `access` \| `recruiting` \| `other` |
| message | text | máx. 4000 |
| lang | text | idioma de la UI |
| status | text | `new` \| `replied` \| `closed`, default `new` |
| source_page | text | p. ej. `pitcher`, `services` |
| ip_hash | text | hash, nunca IP en claro |

#### `subscribers`
| Columna | Tipo | Notas |
|---|---|---|
| id | uuid PK | |
| email | text UNIQUE NOT NULL | |
| created_at | timestamptz | |
| utm_source / utm_medium / utm_campaign | text | atribución |
| confirmed_at | timestamptz | doble opt-in |
| unsubscribed_at | timestamptz | |

#### `pitcher_usage`
| Columna | Tipo | Notas |
|---|---|---|
| id | bigserial PK | |
| created_at | timestamptz | |
| email | text NULL | |
| ip_hash | text NOT NULL | para rate limit |
| ticker | text | |
| model | text | modelo que respondió |
| tokens_in / tokens_out | int | control de coste |
| ok | boolean | |

Índice: `(ip_hash, created_at)`. Regla: máx. N informes/día por `ip_hash`.

#### `calls` (track record)
| Columna | Tipo | Notas |
|---|---|---|
| id | uuid PK | |
| published_at | timestamptz NOT NULL | **inmutable** (trigger que impide UPDATE) |
| post_guid | text NULL | FK lógica a `research-feed` |
| ticker | text NOT NULL | |
| direction | text | `long` \| `short` |
| entry_price | numeric NOT NULL | |
| target_price | numeric | |
| stop_price | numeric | |
| horizon_days | int | |
| thesis_url | text | |
| status | text | `open` \| `hit` \| `stopped` \| `expired` |
| closed_at | timestamptz | |
| exit_price | numeric | |

#### `call_marks`
| Columna | Tipo | Notas |
|---|---|---|
| call_id | uuid FK → calls.id | |
| as_of | date | PK compuesta `(call_id, as_of)` |
| price | numeric | |
| return_pct | numeric | calculado |

#### `strategies` y `strategy_stats`
`strategies(id, slug UNIQUE, name, asset_class, dashboard_url, report_url)` y `strategy_stats(strategy_id FK, year int, return_pct, max_dd_pct, sharpe, PK(strategy_id, year))`. Alimentan el heatmap anual de Track Record (hoy escrito a mano en HTML).

### 2.3 Relaciones
```
calls 1───* call_marks
strategies 1───* strategy_stats
contact_requests, subscribers, pitcher_usage → independientes (sin FK)
```

### 2.4 Seguridad (RLS)
- RLS activado en todas las tablas.
- Políticas: `INSERT` para rol `anon` en `contact_requests`, `subscribers`, `pitcher_usage`; `SELECT` solo `is_admin`.
- `calls`, `call_marks`, `strategies*`: lectura pública (`SELECT` anon), escritura solo admin.
- Datos personales (email, mensaje): retención 24 meses, endpoint de borrado bajo petición (RGPD).

### 2.5 Endpoints (Cloudflare Worker / Vercel Function)
| Método y ruta | Función |
|---|---|
| `POST /api/contact` | Valida (honeypot + Turnstile), inserta en `contact_requests`, notifica por email |
| `POST /api/subscribe` | Inserta en `subscribers`, envía confirmación |
| `POST /api/pitcher` | Comprueba rate limit, llama a Gemini con la clave del servidor, registra uso |
| `GET /api/quote?symbol=` | Proxy de Finnhub/FMP con caché de 60 s |

### 2.6 Generación de JSON públicos
Un workflow nocturno exporta `calls`, `call_marks` y `strategy_stats` a `data/track.json` para que la web siga siendo 100 % estática en lectura.
