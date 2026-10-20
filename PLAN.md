# Plan y estado de la wiki

Wiki de [Eclipse](https://github.com/soyFault/Eclipse) con [Starlight](https://starlight.astro.build) (Astro), publicada en GitHub Pages: <https://soyfault.github.io/eclipse-wiki/>.

**Última actualización:** 20-oct-2026 · Leyenda: ✅ hecho · 🟡 hecho, provisional · ❌ pendiente

## Decisiones

- Sin Wiki.js: Starlight genera HTML estático y despliega directo a Pages.
- El contenido es el de **soyFault/Eclipse** (no EclipseDev): hoy 7 roles y 1 modificador.
- Solo español por ahora. La home es un **mockup** a propósito (solo 5 botones) para estilizar después.
- Footer en todo el sitio con el aviso de Among Us / Innersloth (`src/components/Footer.astro`).

## Estado

| Área | Estado | Notas |
|---|---|---|
| Proyecto Starlight + `base: /eclipse-wiki` | ✅ | `astro.config.mjs` |
| Despliegue a Pages (`.github/workflows/deploy.yml`) | 🟡 | Escrito, **sin ejecutar**: falta activar Pages (ver abajo) |
| Home con botones (Instalación, Roles, Modificadores, DevLog, Android) | 🟡 | Mockup sin estilo propio |
| Footer con disclaimer de Among Us | ✅ | Español + inglés original; sale también en la home y la 404 |
| Instalación | 🟡 | Versiones tomadas de `build/AmongUs.props`; **sin enlace de descarga** (no hay release) |
| Roles (7) | ✅ | Generados desde el código con `scripts/gen_roles.py` |
| Modificadores (1) | 🟡 | Solo Escudo de Chamán, escrito a mano |
| DevLog | 🟡 | Resumen del historial de git, a mano |
| Android | 🟡 | Solo lo verificado: compila contra librerías Android; sin prueba en dispositivo |
| Imágenes / iconos de roles | ❌ | Ninguna página tiene arte todavía |
| Estilo propio (colores, logo, tipografía) | ❌ | Tema por defecto de Starlight |
| Inglés | ❌ | El mod tiene textos en inglés; la wiki no |

## Roles documentados

| Rol | Nombre en inglés | Alineación | Página |
|---|---|---|---|
| Sensorial | Aurial | Tripulante Investigativo | ✅ |
| Investigador | Investigator | Tripulante Investigativo | ✅ |
| Místico | Mystic | Tripulante Investigativo | ✅ |
| Soplón | Snitch | Tripulante Investigativo | ✅ |
| Sheriff | Sheriff | Tripulante Asesino | ✅ |
| Oficial | Officer | Tripulante Asesino | ✅ |
| Chamán | Shaman (`Medic` en el código) | Tripulante Protector | ✅ |

## Cómo actualizar

```bash
npm install
python3 scripts/gen_roles.py /ruta/a/soyFault/Eclipse   # regenera src/content/docs/roles/*
npm run dev                                              # http://localhost:4321/eclipse-wiki/
```

`gen_roles.py` lee los roles, los ajustes (rangos y valores por defecto) y `es_419.xml` del mod, y **sobrescribe** las páginas de roles. Para cambiar un texto de rol, cámbialo en el mod (o ajusta el script); no edites esas páginas a mano.

## Activar GitHub Pages (una sola vez)

*Settings → Pages → Build and deployment → Source: **GitHub Actions***. Después, cada push a `main` publica la wiki.

## Pendiente / siguiente

1. ❌ Activar Pages y comprobar el primer despliegue.
2. ❌ Añadir roles y modificadores a medida que entren en el mod (re-ejecutar el script).
3. ❌ Enlace de descarga en Instalación cuando haya release.
4. ❌ Estilizar la home y el tema (el mockup es la base).
5. ❌ Probar en Android y actualizar esa página.
6. ❌ Automatizar DevLog (hoy es manual).
