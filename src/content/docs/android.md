---
title: Android
description: Estado de Eclipse en Android.
---

:::caution[Sin probar en dispositivo]
Eclipse **compila contra las librerías de Android** (Among Us 2026.9.29), pero todavía no se ha ejecutado en un teléfono.
:::

## Qué está hecho

- El repositorio incluye una comprobación en CI que compila el mod con `AmongUs.GameLibs.Android`.
- Los assets se empaquetan en dos bundles: `eclipse-assets-win.bundle` (PC) y `eclipse-assets-android.bundle` (Android).

## Qué falta

- Probarlo en un dispositivo real.
- Las versiones públicas de Starlight no cargan mods sin aprobar: hace falta que una build sea aprobada por el staff de All Of Us o entrar en el programa de beta testers de Starlight.

## Cómo compilar para Android

```bash
dotnet build src/Eclipse/Eclipse.csproj -c Release -p:AmongUsPlatform=Android
```

Esto sirve para detectar código que usa métodos que no existen en Android; el DLL resultante es el mismo.
