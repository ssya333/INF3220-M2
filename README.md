# cheapGPT

![tests](https://github.com/OWNER/REPO/actions/workflows/tests.yml/badge.svg)

## 1. Qué es cheapGPT
cheapGPT es el chat de servicio al cliente más barato del mercado: usa un LLM gratuito,
tiene tres humores (todos poco profesionales) y un sistema de reclamos que, con mucha suerte,
alguien lee. No lo deben construir desde cero, sino que lo reciben funcionando y lo deben dejar mejor de lo que lo
encontraron.

## 2. Setup

**Antes de la clase**, cada integrante necesita:

- Una cuenta de GitHub.
- Git y Python 3.10 o superior instalados (`git --version` y `python3 --version` para
  revisar).
- Poder hacer push a GitHub desde su computador. Si nunca lo han hecho, pruébenlo antes.
  Si al hacer `git push` les pide contraseña y falla con `Password authentication is not
  supported`, inicien sesión con GitHub en VS Code o GitHub Desktop, o instalen
  [GitHub CLI](https://cli.github.com) y corran `gh auth login`.

1. **Crear el repo del grupo**: un integrante hace clic en "Use this template" en este
   repo y crea el repo del grupo. Después agrega como colaboradores (Settings →
   Collaborators) a los otros dos integrantes y al usuario **`ssya333`** (equipo docente),
   que es quien revisa el repo. El badge de arriba dice `OWNER/REPO`
   porque es un placeholder: reemplacen esas dos palabras, en la línea 3 de este mismo
   `README.md`, por el usuario/organización y el nombre de su repo (por ejemplo,
   `mi-usuario/cheapgpt`) y comiteen el cambio para que el badge muestre el estado real
   de sus tests. Háganlo directo en GitHub (ícono del lápiz sobre el `README.md`) **antes**
   de que los demás clonen el repo.
2. **Clonar y preparar el entorno**:
   ```bash
   git clone <url-del-repo-del-grupo>
   cd <nombre-del-repo-del-grupo>
   python3 -m venv venv       # en Windows: python -m venv venv
   source venv/bin/activate   # en Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
   De aquí en adelante, todos los comandos se corren dentro de la carpeta del repo y con
   el entorno activado (van a ver `(venv)` al inicio de la línea de la terminal).
3. **Revisar que git sepa quiénes son** (cada integrante):
   ```bash
   git config --global user.email
   ```
   Si no muestra nada, o muestra un email que no está en su cuenta de GitHub,
   configúrenlo:
   ```bash
   git config --global user.name "Tu Nombre"
   git config --global user.email "tu-email-de-github@ejemplo.com"
   ```
   GitHub asocia cada commit a una cuenta según este email, no según quién hace el push:
   así se ve quién hizo cada refactoring y quién resolvió cada conflicto.
4. **Configurar la estrategia de pull** (cada integrante, dentro de la carpeta del repo):
   ```bash
   git config pull.rebase false
   ```
   Cuando dos personas pushean en paralelo, git necesita saber cómo combinar los cambios
   al hacer `git pull`; si no se lo dicen, se detiene con el error `fatal: Need to specify
   how to reconcile divergent branches`. Con esta línea, `git pull` siempre hace
   **merge**, que es lo que van a resolver a mano en esta misión. Va sin `--global`, así
   que solo afecta a este repo.
5. **Correr la app**:
   ```bash
   flask --app cheapgpt.app run --port 5050
   ```
   Abran `http://127.0.0.1:5050` y prueben el chat, `/planes`, `/reclamo` y `/excusas`.
6. **Correr los tests**:
   ```bash
   pytest
   ```
7. **API key opcional**: si quieren que el bot use un LLM de verdad (Groq, gratis),
   sigan estos pasos. Sin key, la app funciona igual con un bot falso (`FakeLLMClient`)
   que responde con frases fijas — no hace falta esto para entregar la misión.

   1. Creen una cuenta gratis en [console.groq.com](https://console.groq.com) (no pide
      tarjeta) y generen una API key en **API Keys → Create API Key**.
   2. Copien `.env.example` a `.env`:
      ```bash
      cp .env.example .env       # en Windows: copy .env.example .env
      ```
   3. Peguen su key en `.env`:
      ```
      GROQ_API_KEY=gsk_tu_key_aca
      ```
   4. Reinicien la app (`Ctrl+C` y vuelvan a correr `flask --app cheapgpt.app run --port 5050`) y
      prueben el chat. Si la key es válida, las respuestas ya no van a ser siempre las
      mismas 3 frases del bot falso, sino texto generado por el modelo.
   5. **Nunca comiteen su `.env` ni su key** (ya está en `.gitignore`, pero revisen con
      `git status` antes de cada commit).

## 3. Reglas

- **Prohibido modificar la carpeta `tests/`.** Los tests son el contrato: si tu
  refactoring los rompe, lo hiciste mal.
- Corran `pytest` antes de cada push. Todos los tests tienen que pasar.
- No cambien el comportamiento del código, solo su estructura interna.

## 4. Advertencia: vamos a pushear directo a `main`

En esta misión van a hacer **push directo a `main`, sin pull requests ni revisión**.
Esto **es una mala práctica** y lo hacemos a propósito, con fines pedagógicos:

- Cualquier error de alguien rompe `main` para todo el equipo, al instante.
- Nadie revisa el código antes de que llegue a la rama principal.
- Los conflictos de merge se resuelven sobre la marcha, sin control ni aviso previo.

En la **Misión 3** van a aprender a trabajar con git flow (ramas, pull requests, revisión
de código) para evitar exactamente estos problemas.

## 5. Roles

Cada grupo de 3 se asigna los roles **A**, **B** y **C**. Cada persona hace 2 de los 6
refactorings (uno en la ronda 1, otro en la ronda 2).

## 6. Ronda 1 y ronda 2

**Ronda 1** — orden de push **A → B → C**:

1. Al inicio de la ronda, los tres hacen `git pull`.
2. Trabajan en paralelo en su refactoring.
3. Pushean en el orden indicado: primero A, después B, después C.
4. Si el push es rechazado (`! [rejected] ... (fetch first)`), sigan el tutorial en
   [`docs/merge-conflicts.md`](docs/merge-conflicts.md).

> **Importante:** después del `git pull` del inicio de la ronda, **no vuelvan a hacer
> `git pull` hasta que les toque pushear y su push sea rechazado**. Si hacen pull antes de
> su turno, se saltan el conflicto que tienen que resolver, y eso cuenta como falta al
> protocolo.

**Ronda 2** — orden de push **B → C → A**:

Empieza recién cuando los tres pushes de la ronda 1 están en `main` y el check de
**Actions** está en verde. Mismo procedimiento: `git pull` al inicio, trabajo en paralelo,
push en el orden indicado.

El orden de push es fijo porque es lo que determina **quién se encuentra con el trabajo
de quién**: el que pushea último es siempre el que tiene que combinar su cambio con los
de los dos anteriores.

## 7. Los 6 refactorings

A cada grupo se le asignarán los code smells correspondientes a cada rol y ronda. Cada
refactoring se identifica con un código formado por el rol y la ronda: por ejemplo,
**A1** es el refactoring que hace el rol A en la ronda 1, y **C2** el que hace el rol C en
la ronda 2.

La asignación se entregará en una tabla con el siguiente formato, ordenada según el orden
de push de cada ronda:

| Código | Archivo | Función | Smell | Por qué molesta |
|---|---|---|---|---|
| A1 | `cheapgpt/.../archivo.py` | `nombre_funcion` | Nombre del smell | Explicación breve del problema que genera. |
| B1 | ... | ... | ... | ... |
| C1 | ... | ... | ... | ... |
| B2 | ... | ... | ... | ... |
| C2 | ... | ... | ... | ... |
| A2 | ... | ... | ... | ... |

Para cada uno: identifiquen el smell, entiendan por qué molesta y apliquen el refactoring.
No se entrega la solución: el objetivo es que lo hagan ustedes. Tampoco se entregan
números de línea: busquen las funciones por nombre.

> **Importante:** varios refactorings tocan el mismo archivo o la misma función. Esto es
> intencional: así se generan los conflictos de merge que tendrán que resolver.

## 8. Resolución de conflictos

Cuando un push sea rechazado, van a tener que hacer `git pull` y resolver el conflicto a
mano. Sigan el tutorial paso a paso en [`docs/merge-conflicts.md`](docs/merge-conflicts.md), tiene un ejemplo real sacado de este mismo repo.

Resolver un conflicto **no es elegir un lado**: el resultado tiene que conservar **todos**
los refactorings involucrados, combinados. Si al resolver se descarta el refactoring de un
compañero, ese refactoring se considera no aplicado. Antes de commitear el merge:
no puede quedar ningún marcador (`<<<<<<<`, `=======`, `>>>>>>>`) y `pytest` tiene que pasar.

## 9. GitHub Actions

En la pestaña **Actions** del repo van a ver un workflow (`tests`) que corre `pytest` en
cada `push` y `pull_request`. Un check verde significa que los tests pasan; uno rojo,
que algo se rompió, típicamente, un refactoring que cambió comportamiento o un merge
mal resuelto. Revísenlo después de cada push.

## 10. Entregable

Se evalúa **el repo del grupo**, tal como quedó en `main` a la fecha de entrega: el
código, el historial de commits y los checks de Actions. No hay informe.

1. **Link del repo:** un integrante sube el link del repo del grupo en Canvas, en la
   tarea de la Misión 2.
2. **Acceso:** el usuario `ssya333` tiene que estar agregado como colaborador desde el
   inicio (paso 1 del setup), sea el repo público o privado.
3. **Estado final:** en `main` están los 6 refactorings, sin marcadores de conflicto, y el
   último check de Actions está en verde.
4. **Historial intacto:** se revisa el historial para ver cada refactoring, el orden de
   push y cada resolución de conflicto. No usen `git push --force`, `git rebase` ni
   squash, y no borren ni reescriban commits.
5. **Nada después de la fecha:** se evalúa el último commit de `main` anterior a la fecha
   de entrega (o de atraso, si corresponde).
