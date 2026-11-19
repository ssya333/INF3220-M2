# Tutorial: resolver un conflicto de merge

Esta guía es para cuando `git push` les rechace el push. El ejemplo es un conflicto real
de este mismo repo: dos integrantes refactorizaron al mismo tiempo la función
`format_reply` (en `cheapgpt/chat/persona.py`).

Los mensajes de git aparecen en inglés porque así los muestra la terminal; debajo de cada
uno se explica qué significa.

## 1. Qué es un conflicto y por qué ocurre

Un conflicto de merge pasa cuando dos personas cambian **las mismas líneas** de un
archivo a partir de la misma versión, y git no puede decidir solo con cuál de los dos
cambios quedarse. No es un error: es git avisando que necesita que una persona decida
cómo combinar ambos cambios.

## 2. El push rechazado

Si un compañero hizo push antes que ustedes, su `git push` va a fallar así:

```
$ git push
To github.com:mi-grupo/cheapgpt.git
 ! [rejected]        main -> main (fetch first)
error: failed to push some refs to 'github.com:mi-grupo/cheapgpt.git'
hint: Updates were rejected because the remote contains work that you do
hint: not have locally.
```

Significa que en GitHub hay commits que ustedes todavía no tienen en su computador. Git
no los deja subir los suyos hasta que traigan esos commits y los combinen con su trabajo.

## 3. Traer los cambios con `git pull`

Para traer los commits del compañero y combinarlos con los suyos, corran
`git pull --no-edit`:

```
$ git pull --no-edit
Auto-merging cheapgpt/chat/persona.py
CONFLICT (content): Merge conflict in cheapgpt/chat/persona.py
Automatic merge failed; fix conflicts and then commit the result.
```

Git trajo los commits de GitHub e intentó combinarlos con los suyos. Pudo combinar
automáticamente todo lo demás, pero en `persona.py` los dos cambiaron las mismas líneas,
así que les pide que resuelvan ese archivo a mano y después hagan commit.

`--no-edit` evita que git abra un editor para escribir el mensaje del merge. Si no
aparece ningún `CONFLICT`, es porque cambiaron partes distintas del código y git juntó
todo solo: corran `pytest` y, si pasa, hagan `git push`. No necesitan seguir con este
tutorial.

## 4. Leer los marcadores

Abran `cheapgpt/chat/persona.py`. Van a ver algo así (recortado):

```python
<<<<<<< HEAD
def _recortar(texto):
    recortado = texto.strip()
    if len(recortado) > 280:
        recortado = recortado[:277] + "..."
    return recortado


def format_reply(d, mood, flg=True):
    if mood == "chistoso":
        tmp = _recortar(d)
        x2 = "😂 " + tmp + "\n\n(Respuesta patrocinada por cheapGPT: barato, pero honesto... a veces)"
        if flg:
            x2 = x2 + "\n— Tu asistente de confianza (confianza baja)"
        return x2
    elif mood == "sarcastico":
        ...
    else:
=======
_ESTILO_POR_HUMOR = {
    "chistoso": ("😂", "(confianza baja)"),
    "sarcastico": ("🙄", "(no te hagas ilusiones)"),
    "dramatico": ("😭", "(entre lagrimas)"),
}


def format_reply(d, mood, flg=True):
    if mood not in _ESTILO_POR_HUMOR:
>>>>>>> 98c2a2c4cb0b431a1f3f507559c4462ebb656c9f
        raise ValueError(f"Humor invalido: {mood}")

    emoji, remate = _ESTILO_POR_HUMOR[mood]
    tmp = d.strip()
    if len(tmp) > 280:
        tmp = tmp[:277] + "..."
    x2 = emoji + " " + tmp + "\n\n(Respuesta patrocinada por cheapGPT: barato, pero honesto... a veces)"
    if flg:
        x2 = x2 + "\n— Tu asistente de confianza " + remate
    return x2
```

- **Desde `<<<<<<< HEAD` hasta `=======`:** su versión, la que ya tenían en un commit en
  su computador. En este ejemplo es el refactoring **C2 (Duplicated Code)**: el recorte a
  280 caracteres estaba repetido en los tres humores y se sacó a una función `_recortar`.
- **Desde `=======` hasta `>>>>>>> 98c2a2c...`:** la versión que llegó con el `pull`, es
  decir, el commit del compañero (el número largo es el identificador de ese commit). En
  este ejemplo es el refactoring **B2 (Repeated Switches)**: la cadena de `if/elif` se
  reemplazó por un diccionario `_ESTILO_POR_HUMOR`.
- **Lo que está después de `>>>>>>>`** no tiene marcadores porque git lo pudo combinar
  solo, pero viene del commit del compañero. Ojo: ahí todavía está el recorte escrito a
  mano (`tmp = d.strip()` y el `if len(tmp) > 280`), sin usar `_recortar`.

En la ronda 2 el orden de push es B → C → A: B ya hizo push, así que C es quien se
encuentra con el conflicto al hacer `git pull`.

## 5. Resolver combinando ambos refactorings

El error más común es "elegir un lado" y borrar el trabajo del otro. Aquí **no hay que
elegir**: el resultado tiene que tener los dos refactorings. Quedarse con el diccionario
de B2 no basta, porque el recorte volvería a estar escrito a mano y se perdería C2. La
solución es mantener el diccionario `_ESTILO_POR_HUMOR` (B2) y usar `_recortar` (C2)
dentro de la nueva versión de `format_reply`:

```python
_ESTILO_POR_HUMOR = {
    "chistoso": ("😂", "(confianza baja)"),
    "sarcastico": ("🙄", "(no te hagas ilusiones)"),
    "dramatico": ("😭", "(entre lagrimas)"),
}


def _recortar(texto):
    recortado = texto.strip()
    if len(recortado) > 280:
        recortado = recortado[:277] + "..."
    return recortado


def format_reply(d, mood, flg=True):
    if mood not in _ESTILO_POR_HUMOR:
        raise ValueError(f"Humor invalido: {mood}")

    emoji, remate = _ESTILO_POR_HUMOR[mood]
    tmp = _recortar(d)
    x2 = emoji + " " + tmp + "\n\n(Respuesta patrocinada por cheapGPT: barato, pero honesto... a veces)"
    if flg:
        x2 = x2 + "\n— Tu asistente de confianza " + remate
    return x2
```

El archivo con marcadores no es Python válido; el resultado de arriba sí lo es y conserva
los dos refactorings. Si les toca un conflicto con tres refactorings sobre la misma función
(por ejemplo, porque llega un tercer cambio), apliquen el mismo criterio: el resultado
tiene que conservar los tres.

## 6. Usar el editor de conflictos de VS Code (opcional)

VS Code detecta los archivos con conflicto y muestra botones sobre cada bloque:
**Accept Current Change** (quedarse con su versión), **Accept Incoming Change** (quedarse
con la del compañero), **Accept Both Changes** (dejar las dos, una debajo de la otra) y
**Compare Changes** (verlas lado a lado). En esta misión, "Accept Current" o "Accept
Incoming" casi nunca bastan, porque el objetivo es combinar ambos cambios, no descartar
uno. Úsenlos como punto de partida y después editen el resultado a mano.

## 7. Revisar, hacer commit y push

```bash
pytest                     # tienen que pasar todos los tests, sin excepción
git add cheapgpt/chat/persona.py
git commit -m "Resuelve conflicto en persona.py"
git push
```

El commit del merge se hace igual que cualquier otro: con `-m` y un mensaje.

No hagan `git commit` hasta que `pytest` pase. Si falla, sigan editando el archivo con
conflicto (o los archivos relacionados) hasta que los tests pasen.

**Después del push, revisen GitHub Actions** (ver la sección "GitHub Actions" del README).
Actions corre los tests en GitHub uno o dos minutos después del push, así que no se puede
revisar antes: por eso antes del push se corre `pytest` en su computador. Esperen a que el
check quede en **verde**. Si queda en rojo, entren a la pestaña **Actions** para ver qué
test falló, arréglenlo, hagan commit y vuelvan a hacer push. La ronda 2 no empieza, y la
misión no está terminada, hasta que el último push esté en verde.

## 8. Errores comunes

- **Dejar los marcadores** (`<<<<<<<`, `=======`, `>>>>>>>`) en el código: el archivo
  deja de ser Python válido y todo se rompe. Antes de hacer commit, corran
  `git diff --check`: si quedó algún marcador, lo muestra.
- **Quedarse con un solo lado y borrar el trabajo del compañero:** el refactoring de la
  otra persona desaparece sin que nadie se dé cuenta, hasta que alguien pregunta por qué
  su cambio no está.
- **No correr los tests antes del push:** un merge mal resuelto rompe `main` para todo el
  equipo, y lo van a ver en rojo en la pestaña **Actions**.
- **Se abrió una pantalla rara en la terminal** al hacer `git pull` o `git commit`: es Vim,
  un editor que git abre para el mensaje del merge. Para salir, aprieten `Esc`, escriban
  `:wq` y den Enter. Para que no pase, usen `git pull --no-edit` y `git commit -m "mensaje"`.
- **Si se pierden a mitad de camino**, pueden cancelar todo y volver a intentarlo con calma:
  ```bash
  git merge --abort
  ```
  Esto deshace el merge y los deja como estaban antes del `git pull`.
