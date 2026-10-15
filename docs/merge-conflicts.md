# Tutorial: resolver un merge conflict

Guía paso a paso para cuando `git push` los rechace. El ejemplo de abajo es un
conflicto real de este mismo repo: dos refactorings de `format_reply`
(`cheapgpt/chat/persona.py`) hechos en paralelo por dos integrantes.

## 1. Qué es un conflicto y por qué ocurre

Un merge conflict pasa cuando dos personas modifican **las mismas líneas** de un
archivo a partir de la misma versión base, y git no puede decidir solo cuál de los
dos cambios "gana". No es un error: es git avisando que necesita que una persona
decida cómo combinar ambos cambios.

## 2. El push rechazado

Si alguien ya pusheó antes que vos, tu `git push` va a fallar así:

```
$ git push
To github.com:tu-grupo/cheapgpt.git
 ! [rejected]        main -> main (fetch first)
error: failed to push some refs to 'github.com:tu-grupo/cheapgpt.git'
hint: Updates were rejected because the remote contains work that you do
hint: not have locally.
```

Esto significa: "el remoto tiene commits que vos no tenés todavía". Falta traerlos.

## 3. `git pull`

```
$ git pull
Auto-merging cheapgpt/chat/persona.py
CONFLICT (content): Merge conflict in cheapgpt/chat/persona.py
Automatic merge failed; fix conflicts and then commit the result.
```

Git trajo los commits del remoto, intentó combinarlos con los tuyos, y avisó que
`persona.py` tiene un conflicto que tenés que resolver a mano.

## 4. Leer los marcadores

Abrí el archivo. Vas a ver algo así (recortado):

```python
def format_reply(d, mood, flg=True):
<<<<<<< HEAD
    if mood == "chistoso":
        tmp = _truncate(d)
        x2 = "😂 " + tmp + "\n\n(Respuesta patrocinada por cheapGPT: barato, pero honesto... a veces)"
        if flg:
            x2 = x2 + "\n— Tu asistente de confianza (confianza baja)"
        return x2
    elif mood == "sarcastico":
        ...
    else:
=======
    if mood not in _MOOD_STYLE:
>>>>>>> 8c1f4e27a9b3d05f6e2c7a1b94d0e3f5a6c8b712
        raise ValueError(f"Humor invalido: {mood}")

    emoji, remate = _MOOD_STYLE[mood]
    tmp = d.strip()
    ...
```

- **`<<<<<<< HEAD`** hasta **`=======`**: tu versión (lo que ya tenías commiteado
  localmente). En este ejemplo, el refactoring **C2 — Extract Function**: se sacó el
  truncado repetido a una función `_truncate`.
- **`=======`** hasta **`>>>>>>> 8c1f4e2...`** (el hash del commit que llegó): la
  versión que trajo el `pull` (el commit del compañero). En este ejemplo, el
  refactoring **B2 — Replace Conditional**: se reemplazó la cadena de `if/elif` por un
  diccionario `_MOOD_STYLE`.

En la ronda 2 el orden es B → C → A: B ya pusheó, así que es C quien se encuentra con
el conflicto al hacer `pull`.

## 5. Resolver combinando ambos refactorings

El error más común es "elegir un lado" y borrar el trabajo del otro. Acá **no hay que
elegir**: hay que aplicar los dos refactorings juntos. El resultado, sin marcadores,
combina la función `_truncate` (C2) con el diccionario `_MOOD_STYLE` (B2):

```python
def _truncate(raw_reply):
    trimmed = raw_reply.strip()
    if len(trimmed) > 280:
        trimmed = trimmed[:277] + "..."
    return trimmed


def format_reply(raw_reply, mood, include_signature=True):
    if mood not in _MOOD_STYLE:
        raise ValueError(f"Humor invalido: {mood}")

    emoji, remate = _MOOD_STYLE[mood]
    trimmed = _truncate(raw_reply)
    result = emoji + " " + trimmed + "\n\n(Respuesta patrocinada por cheapGPT: barato, pero honesto... a veces)"
    if include_signature:
        result = result + "\n— Tu asistente de confianza " + remate
    return result
```

Antes (con marcadores, sin compilar) → después (compila, y conserva ambos
refactorings). Si en tu ronda te toca resolver un conflicto de a tres (por ejemplo
si después llega un tercer refactoring sobre la misma función), aplicá el mismo
criterio: combiná, no seguir eligiendo un solo lado.

## 6. Usar el merge editor de VS Code (opcional)

VS Code detecta los archivos en conflicto y ofrece botones arriba de cada bloque:
"Accept Current", "Accept Incoming", "Accept Both", "Compare Changes". Ojo: "Accept
Current" o "Accept Incoming" solos casi nunca alcanzan en esta misión, porque el
objetivo es combinar ambos cambios, no descartar uno. Usalos como punto de partida y
editá a mano el resultado.

## 7. Verificar, commitear y pushear

```bash
pytest                     # tienen que pasar todos los tests, sin excepción
git add cheapgpt/chat/persona.py
git commit                 # git ya deja armado un mensaje de merge, podés editarlo
git push
```

No hagas `git commit` hasta que `pytest` pase. Si falla, seguís editando el archivo
en conflicto (o los archivos relacionados) hasta que el comportamiento sea correcto.

## 8. Errores comunes

- **Dejar los marcadores** (`<<<<<<<`, `=======`, `>>>>>>>`) en el código commiteado:
  el archivo ya no es Python válido y todo se rompe. Revisá con `git diff --check`
  antes de commitear.
- **Aceptar solo un lado y borrar el trabajo del compañero**: el refactoring de la
  otra persona desaparece silenciosamente. Nadie se entera hasta que alguien pregunta
  por qué su cambio "no está".
- **No correr los tests antes de pushear**: un merge "resuelto" pero roto rompe
  `main` para todo el equipo, y lo van a ver en rojo en la pestaña Actions.
- **Si te perdés a la mitad de la resolución**, podés cancelar todo y volver a
  intentar con calma:
  ```bash
  git merge --abort
  ```
  Esto deshace el merge en curso y te deja como estabas antes del `git pull`.
