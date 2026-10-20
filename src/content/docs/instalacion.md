---
title: Instalación
description: Cómo instalar Eclipse en PC.
---

:::caution[Mod en desarrollo]
Eclipse todavía no tiene una versión publicada. Esta página describe los requisitos y el proceso previsto; las descargas se añadirán cuando existan.
:::

## Requisitos

| Componente | Versión |
|---|---|
| Among Us | 2026.9.29 |
| BepInEx (IL2CPP) | 6.0.0-be.735 |
| Reactor | 2.5.0-ci.371 |
| Mira API | 0.6.0 |

Eclipse depende de **Reactor** y de **Mira API**: sin ellos no carga.

## Instalar en PC

1. Instala BepInEx IL2CPP en la carpeta de Among Us y abre el juego una vez para que cree sus carpetas.
2. Copia `Reactor.dll`, `MiraAPI.dll` y `Eclipse.dll` en `BepInEx/plugins/`.
3. Abre el juego. En el lobby deben aparecer los ajustes de Eclipse (el menú «Jugadores» y la configuración de cada rol).

## Idiomas

Los textos del mod están en inglés y en español latino.

## Compilarlo tú mismo

Necesitas el SDK de .NET 10 y Git.

```bash
git clone --recurse-submodules https://github.com/soyFault/Eclipse
cd Eclipse
dotnet build Eclipse.sln -c Release
```

El código está en [github.com/soyFault/Eclipse](https://github.com/soyFault/Eclipse) bajo licencia GPLv3.

## Android

Mira la página de [Android](/eclipse-wiki/android/).
