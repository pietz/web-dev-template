This is the current state of my tech stack for building web applications. It's revolves around Python, simplicity and development speed.
## Backend: Python

Python is still the king in the data and AI space. While JavaScript is also great for building web apps, it's often limited in terms of functionality in data processing, calculation speed and machine learning. We use Python 3.12 with all its latest language features.
### Web Server: FastAPI

The core of the backend is based on FastAPI. It strikes a solid middle ground between the dinosaur Flask and new kids on the block like LiteStar. Django has the batteries included type of approach, but I like to keep things light and simple.

The server will go in the `app.py` file and new routers can be created for authentication or other groupable functions. Environment variables will be stored in a `.env` file.
```
pip install fastapi==0.114.2
```
### Configuration: Pydantic Settings

Pydantic Settings allows for easy and powerful management of environment variables and configuration. Since Pydantic v2 it has to be installed separately.
```
pip install pydantic-settings==2.5.2
```
It's good practice to store the settings in `config.py` and import the `settings` variable elsewhere. It will automatically load the `.env` file as well.
```python
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_url: str
	database_url: str
	session_key: str
	github_client_id: str
	github_client_secret: str

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
```
### Database: SQLite

SQLite is often only recommended for prototypes or small applications but with the current progress of cloud compute you can push it very far today even for larger applications. Hosting it is super simple by including the file in the storage of the application. It fits right into the simplicity and development speed focus of my tech stack.
### ORM: SQLModel & Pydantic

As an ORM I like to use SQLModel built by the same people as FastAPI is uses similar tech revolving around Pydantic. It's convenient and yet explicit. It will be instantiated in the `lifespan` functionality of the FastAPI server and based on Pydantic models that are defined in the `models.py` module.
```
pip install sqlmodel==0.0.22
```
### Authentication: Authlib with GitHub

With Authlib it's easy to integrate social providers like GitHub or Google. It's also battle tested and has stood the test of time. The logic including the necessary endpoints will go in a module called `auth.py`.

When building tools or services for developers my first choice is using GitHub as a authentication provider. For wide consumer focussed products the choice might be different.
```
pip install authlib==1.3.2
```
### Templating: JinjaX

JinjaX is an extension to the Jinja templating engine that introduces a component-based approach, making it easier to manage and maintain complex templates in Python web applications. This approach encapsulates HTML, CSS, and JavaScript within individual components, which can be reused across different parts of a project, leading to a cleaner and more modular codebase.

JinjaX replaces Jinja on the implementation side while being fully backwards compatible. It just adds new syntax on top that can be used. What Jinja refers to as "templates", JinjaX calls "components".
```
pip install jinjax==0.46
```
#### Initialization

Like in Jinja, we need to initialize our component catalog and point it to the right directory.
```python
from jinjax.catalog import Catalog
catalog = Catalog()
catalog.add_folder("components")
```
This will point JinjaX to the `components` folder in which we store .jinja files. I usually like to have the following folders:

- **components**: Small reusable and parametrized blocks
- **pages**: Full pages that make use of components
#### Rendering

Rendering a component in JinjaX is straightforward.
```python
return catalog.render("Layout", title="Hello World")
```
This tells JinjaX we want to return the "Layout.jinja" component file and provide the `title` variable with a string. JinjaX components need to start with capital letters.
#### Defining Components

JinjaX components are just Jinja templates with a header. If no variables are used in the component, the header is optional.
```html
{#def title, include_footer=True #}

<header>
	<h1>{{ title }}</h1>
</header>

{{ content }}

{% if include_footer %}
<footer>
	copyright 2024
</footer>
{% endif %}
```
This is equivalent to doing this in Jinja:
```html

<header>
	<h1>{{ title }}</h1>
<header>

{% block content %}
{% endblock %}

{% if include_footer | default(true) %}
<footer>
	copyright 2024
</footer>
{% endif %}
```
- Variables and control statements are used in the same way as in vanilla Jinja
- JinjaX components explicitly declare their arguments at the beginning of the file using a special `{#def ... #}` comment including default values.
- The `{{ content }}` variable has a special meaning in JinjaX, as it will be used as the content for the main slot of the component.
#### Calling Components

When calling components the react-like syntax becomes visible. Continuing the layout example from above we can call the `Layout` component like so:
```html
<Layout title="My title">
	<main>My cool page</main>
</Layout>
```
- The capital letter of the HTML element signals that we want to use a JinjaX component. It needs to be part of the folder that was initialized above.
- Providing a value to the `title` is mandatory, since we didn't provide a default value, but we don't provide the value of `include_footer`, which will render it with the default.
- Everything that goes within the `<Layout>` tags will be shown in the `content` slot of the component.
- Self-closing tags are supported if the `content` slot is unused.
- In contrast to Jinja, string variables should not be wrapped in quotes: This is right: `<Heading text={{ text }} />` while this is false: ``<Heading text="{{ text }}" />``

This syntax replaces all major structural statements in Jinja: `extends`, `block`, `include`, `macro`.
#### Full Example

**Jinja**:
```html
{% extends "layout.html" %}
{% block title %}My title{% endblock %}

{% from "bunch_of_macros.html" import card_macro, another_macro %}

{% block content -%}
<div>
	<h2>Hello {{ mistery or "World?" }}</h2>
	<div>
		{% call card_macro(div="So verbose") %}
			{% for product in products %}
				{{ another_macro(product) }}
			{% endfor %}
		{% endcall %}
	</div>
</div>
{% with items=products %}
	{% include "snippets/pagination.html" %}
{% endwith %}
{%- endblock %}
```
**JinjaX**:
```html
{#def products, msg="World!" #}

<Layout title="My title">
	<div>
		<h2>Hello, {{ msg }}</h2>
		<div>
			<Card div="So clean">
				{% for product in products %}
					<Product product={{ product }} />
				{% endfor %}
			</Card>
		</div>
	</div>
	<Paginator items={{ products }} />
</Layout>
```
All the structural statements are replaced by component calls with attributes and the content slot. It's much easier on the eyes and
## Frontend

JavaScript focused frameworks like react introduce a whole world of complexity. This complexity may be needed for some applications but as a default option, it's overkill in a lot of situations. Going back to where the web came from and extending it with new features is a much simpler approach to build modern apps.
### Interactivity: HTMX

We use HTMX to build interaction into our applications. It's easy to understand, easy to integrate, a small dependency and the improvement in user experience can be huge. Instead of sending JSON data to the frontend, we send HTML partials (JinjaX components) that will be rendered into areas of the DOM where something needs to be replaced.

We should try to use HTMX to it's full extend before writing custom JavaScript code. HTMX has many baked in functionalities that basically everything can be built with its attributes. When it doubt, do it in the backend and ship the partial HTML. That way the application doesn't have to deal with uncommitted state that only exists in the frontend. We simply treat the browser as a viewing device while still benefitting from SPA like partial updates.
```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/htmx/2.0.2/htmx.min.js"></script>
```
### Styling: PicoCSS

PicoCSS is a minimalist, (almost) classless CSS framework that emphasizes semantic HTML. It provides a lightweight solution for responsive web design, working primarily with native HTML elements to reduce reliance on complex class systems.

PicoCSS also features many components that add a bit of syntax on top of native HTML conventions. We should try to use vanilla PicoCSS styling to its full extend before writing custom CSS. In most cases I find it simpler and more pracical to add inline CSS to the HTML elements instead of creating a custom CSS file or section in the head.
```html
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/picocss/2.0.6/pico.min.css" />
```
#### Buttons
```html
<button>Default Button</button>
<button class="secondary">Secondary Button</button>
<button class="contrast">Contrast Button</button>
```
#### Forms
```html
<form>
<input type="text" name="text">
<input type="email" name="email" autocomplete="email">
<input type="number" name="number">
<input type="password" name="password">
<input type="tel" name="tel" autocomplete="tel">
<input type="url" name="url">
<input type="date" name="date">
<input type="datetime-local" name="datetime-local">
<input type="month" name="month">
<input type="time" name="time">
<input type="file">
<input name="switch" type="checkbox" role="switch" aria-invalid="false" /> Turn me on
<button type="submit">Submit</button>
</form>
```
#### Validation
```html
<input
	type="text"
	name="valid"
	value="Valid"
	aria-invalid="false"
>

<input
	type="text"
	name="invalid"
	value="Invalid"
	aria-invalid="true"
>
```
#### Navigation
```html
<nav>
	<ul>
		<li><strong>Acme Corp</strong></li>
	</ul>
	<ul>
		<li><a href="#">About</a></li>
		<li><a href="#">Services</a></li>
		<li><a href="#">Products</a></li>
	</ul>
</nav>
```
#### Cards
```html
<article>
	<header>Card Title</header>
	<p>Card content goes here.</p>
	<footer>Card footer</footer>
</article>
```
#### Accordions
```html
<details>
	<summary>Accordion Title</summary>
	<p>Accordion content goes here.</p>
</details>
```
#### Progress
```html
<progress value="50" max="100"></progress>
```
#### Tooltips
```html
<button data-tooltip="This is a tooltip">Hover me</button>
```
#### Modal
```html
<button onclick="modal.showModal()">Open Modal</button>
<dialog id="modal">
	<article>
		<header>
			<button aria-label="Close" rel="prev" onclick="modal.close()"></button>
			Modal Title
		</header>
		<p>Modal content goes here.</p>
	</article>
</dialog>
```
#### Grid
```html
<div class="grid">
	<div>Grid item 1</div>
	<div>Grid item 2</div>
	<div>Grid item 3</div>
</div>
```
#### Search
```html
<input
	type="search"
	name="search"
	placeholder="Search"
	aria-label="Search"
/>
```
#### Dropdown
```html
<!-- Dropdown -->
<details class="dropdown">
	<summary>Dropdown</summary>
	<ul>
		<li><a href="#">Solid</a></li>
		<li><a href="#">Liquid</a></li>
		<li><a href="#">Gas</a></li>
		<li><a href="#">Plasma</a></li>
	</ul>
</details>

<!-- Form Element -->
<select name="select" aria-label="Select" required>
	<option selected disabled value="">Select</option>
	<option>Solid</option>
	<option>Liquid</option>
	<option>Gas</option>
	<option>Plasma</option>false
</select>
```
#### Loading
```html
<span aria-busy="true">Generating your link...</span>
<button aria-busy="true" aria-label="Please wait…" />
<article aria-busy="true"></article>
```
#### Groups
```html
<form>
	<fieldset role="group">
		<input
			type="email"
			name="email"
			placeholder="Enter your email"
			autocomplete="email"
		/>
		<input type="submit" value="Subscribe" />
	</fieldset>
</form>
```