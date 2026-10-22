# 04 · Brief de diseño

## 1. Principios
- **Institucional y sobrio**: sensación de informe de banca privada, no de web fintech de moda.
- **Editorial + datos**: serif para leer, monoespaciada para cifras y etiquetas.
- **Oro como único acento**: el color guía al CTA y a lo importante.
- **Oscuro por defecto**, claro como alternativa de primera clase.

## 2. Paleta (tokens reales del CSS)

### Modo oscuro (`html.dark`, por defecto)
| Token | Valor | Uso |
|---|---|---|
| `--bg` | `#04040A` | Fondo de página |
| `--bg1` | `#08070E` | Fondo de sección |
| `--bg2` | `#0F0E17` | Tarjetas |
| `--bg3` | `#16151F` | Elementos elevados |
| `--ink` | `#F4F0EC` | Texto principal |
| `--ink2` | `#C0BAB4` | Texto secundario |
| `--ink3` | `#7A7570` | Texto terciario / etiquetas |
| `--gold` | `#D49020` | Acento, enlaces, logo |
| `--gold2` | `#EAA830` | Hover del acento |
| `--rule` | `rgba(212,144,32,.15)` | Líneas con acento |
| `--rule2` | `rgba(255,255,255,.07)` | Divisores neutros |

### Modo claro (marca original, `AEONNIMBUS.md`)
Oro `#8B6914` · tinta `#1A1814` · papel `#F5F2EC`.

### Datos / gráficos
| Token | Oscuro | Claro | Uso |
|---|---|---|---|
| `--dv-pos` | `#256abf` | `#2a78d6` | Positivo en heatmaps |
| `--dv-neg` | `#c83f3f` | `#e34948` | Negativo |
| `--dv-mid` | `#383835` | `#f0efec` | Neutro |
| `--su-eq` / `--su-fx` / `--su-tk` | `#3987e5` / `#c98500` / `#199e70` | `#2a78d6` / `#b37400` / `#1baf7a` | Series: renta variable, FX, ticker |
| `--sub-orange` | `#FF8040` | `#FF6719` | Solo para Substack |

> Positivo/negativo **no** dependen solo del color: llevan signo (`+12.3`, `-3.3`) y la intensidad se codifica con `--k`.

## 3. Tipografía
| Rol | Fuente | Token |
|---|---|---|
| Cuerpo / titulares editoriales | **Newsreader** (serif, opsz 6–72) | `--FS` |
| UI, nav, logo | **Inter** 300–600 | `--FD` |
| Cifras, etiquetas, tablas, código | **JetBrains Mono** 300–500 | `--FM` |

- Cuerpo 16 px / interlineado 1,7.
- Logo: Inter 11 px, 700, tracking `.16em`, mayúsculas, color `--gold`.
- Etiquetas pequeñas (chips, botones): mono 9–11 px, mayúsculas, tracking `.08em`.

## 4. Componentes existentes
| Componente | Clase | Notas |
|---|---|---|
| Página | `.pg` / `#pg-*` | Una visible a la vez |
| Barra de nav | `.nlogo`, `.nbtn`, `.nav-cta` | CTA «Subscribe →» destacado |
| Dropdown | `.nav-drop-wrap`, `.nav-dropdown`, `.nav-drop-item` | Etiqueta pequeña + nombre |
| Tarjeta de herramienta | `.tc` > `.tchd` + `.tbody` | Colapsable; pestañas internas |
| Post de research | `.post[data-cat]`, `.pchip`, `.ptt`, `.pex`, `.pmeta` | Chips `ce`, `cm`, `cg`, `cb` |
| Heatmap | `td.hm.pos/.neg/.na` con `--k` | Celda `dk` para intensidad alta |
| Botón idioma/tema | `.dm-btn`, `.lang-item` | Mono 9 px, borde 1 px |
| Progreso | `#progress-bar` | 2 px, oro |
| Subir | `#stt` | 38 × 38 px, cuadrado |

Estilo geométrico: **esquinas rectas**, bordes de 1 px, sin sombras pesadas; separación por líneas `--rule`.

## 5. Especificación por pantalla
| Pantalla | Composición | Énfasis |
|---|---|---|
| Home | Hero con `hero-bg`/`hero-topography`, titular serif grande, 3 bloques de cifras, tools, sectores | Un único CTA primario |
| Research | Filtros por chip + lista de posts en 2 columnas (fecha / contenido) | Legibilidad |
| Track Record | Heatmap anual por par, tablas mono, enlaces a PDF | Transparencia de datos |
| Strategies | Tarjetas con rentabilidad, drawdown, enlace a dashboard | Densidad controlada |
| Tools | Acordeón de 12 tarjetas, inputs mono, gráficos SVG | Resultado visible sin scroll |
| Markets | Tablas con sesgo coloreado + chip bullish/bearish | Escaneo rápido |
| AI Pitcher | Caja de chat, monograma pulsante (`AA`, `TW`), informe en secciones | Sensación de herramienta premium |
| Services/Contact | Formulario simple, expectativas claras | Baja fricción |

## 6. Movimiento
Transiciones de 0,2–0,3 s (tema, hover). Pulso suave en monogramas (`pitcherPulse`). Respetar `prefers-reduced-motion` **[Propuesto]**.

## 7. Accesibilidad **[Propuesto]**
- Contraste: `--ink3` (`#7A7570`) sobre `#04040A` ronda 4,3:1; subirlo para texto < 18 px.
- Etiquetas de 9 px son pequeñas: mínimo 11 px.
- Foco visible en todos los controles; `aria-expanded` en tarjetas de herramientas y dropdown.
- Todos los gráficos SVG con `role="img"` y resumen textual.
- Objetivo táctil ≥ 44 px (el botón `#stt` mide 38).

## 8. Responsive
Rejillas `g4g/g3g` → 2 columnas bajo el primer breakpoint; `sec3` → 1 columna. Sin scroll horizontal (`overflow-x:hidden` en body).
