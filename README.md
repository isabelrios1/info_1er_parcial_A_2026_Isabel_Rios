# Angry Birds, Primer Parcial Infografia I

## Descripcion

Este proyecto consiste en un clon basico de Angry Birds usando arcade para la parte visual y pymunk para la simulacion fisica, la base del proyecto ya incluia la estructura principal y durante el desarrollo se completaron las mecanicas faltantes y se agregaron funcionalidades extra.

Ademas de implementar las funciones requeridas del slingshot y las habilidades especiales de los pajaros, tambien se agrego un sistema de niveles basado en puntaje minimo para hacer el juego un poco mas dinamico y darle una progresion entre niveles.

## Funcionalidades implementadas

### Sistema de lanzamiento

Primero se implementaron las funciones faltantes en game_logic.py, las cuales permiten calcular el angulo, la distancia y el impulso necesario para lanzar los pajaros.

El lanzamiento funciona con el comportamiento de una resortera real, entonces el usuario hace click, arrastra el mouse y al soltar el pajaro sale disparado en la direccion opuesta al arrastre.

Ademas se agrego una imagen visual del slingshot para que el lanzamiento se vea mas parecido al juego original, esta imagen aparece unicamente mientras el usuario hace click y arrastra el mouse y su posicion fue ajustada para que la abertura central coincida con el punto desde donde inicia la linea de lanzamiento.

## Pajaros especiales

### YellowBird

Se implemento el YellowBird usando herencia a partir de Bird, este pajaro puede activar una habilidad especial mientras esta en vuelo.

Cuando el usuario hace click izquierdo el pajaro recibe un aumento de impulso en la direccion en la que ya se estaba moviendo y esta habilidad solo puede usarse una vez por pajaro.

### BlueBird

Tambien se implemento BlueBird usando herencia.

Cuando el usuario hace click mientras el pajaro esta en vuelo este se divide en tres pajaros con diferentes angulos, manteniendo la direccion general y la velocidad del movimiento original.

La habilidad solo puede activarse una vez para evitar divisiones infinitas.

## Sistema de niveles

Como funcionalidad extra se agrego un sistema de niveles basado en puntaje.

Cada nivel tiene una cantidad minima de puntos requerida para completarse y al alcanzar esa cantidad aparece una pantalla de nivel completado.

En lugar de pasar automaticamente al siguiente nivel, aparece una imagen de Level Cleared junto con un boton de Next Level que puede presionarse para continuar.

Ademas cada nivel aumenta la dificultad agregando mas columnas y mas cerdos en posiciones distintas.

Nivel 1, pocos objetos y una estructura simple

Nivel 2, mas columnas y mas objetivos

Nivel 3, mayor cantidad de obstaculos y dificultad

## Mejoras agregadas

Tambien se realizaron algunos ajustes adicionales para mejorar la experiencia del juego.

La ventana fue ajustada a un tamaño mas adecuado y se centro automaticamente en la pantalla.

Se agrego un sistema de puntaje que aumenta segun los objetos destruidos.

Los tipos de pajaros van cambiando automaticamente entre Bird normal, YellowBird y BlueBird.

Se corrigieron errores relacionados con clicks repetidos, activacion de poderes y cambio entre niveles.

## Ejecucion

Para ejecutar el proyecto usar,

```bash
uv run main.py