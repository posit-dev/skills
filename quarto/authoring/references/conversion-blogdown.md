# Converting blogdown to Quarto

Guide for converting blogdown (Hugo-based) sites to Quarto websites or blogs.

## Overview

Key differences:

1. Configuration: `config.toml` or `config.yaml` → `_quarto.yml`
2. Content: Hugo templates → Quarto layouts
3. Shortcodes: Hugo → Quarto shortcodes
4. Themes: Hugo themes → Quarto themes

## Quick Start

### 1. Create Quarto Config

Replace `config.toml` or `config.yaml` with `_quarto.yml`:

```yaml
project:
  type: website

website:
  title: "My Site"
  navbar:
    left:
      - href: index.qmd
        text: Home
      - href: about.qmd
        text: About
      - href: blog.qmd
        text: Blog

format:
  html:
    theme: cosmo
```

### 2. Rename Files

```bash
for f in content/**/*.Rmd; do
  mv "$f" "${f%.Rmd}.qmd"
done
```

### 3. Update Front Matter

#### Blogdown

```yaml
title: "Post Title"
author: "Author"
date: "2024-01-15"
slug: "post-slug"
categories: ["R"]
tags: ["data"]
```

#### Quarto

```yaml
title: "Post Title"
author: "Author"
date: 2024-01-15
categories:
  - R
  - data
```

## Project Structure

### blogdown

```txt
config.toml (or config.yaml)
content/
  _index.md
  about.md
  post/
    2024-01-01-first/
      index.Rmd
static/
  images/
themes/
  hugo-theme/
public/
```

### Quarto

```txt
_quarto.yml
index.qmd
about.qmd
posts/
  first-post/
    index.qmd
images/
_site/
```

## Configuration Mapping

### Basic Site Config

#### Blogdown (`config.toml`)

```toml
baseURL = "https://example.com/"
title = "My Site"
theme = "hugo-theme"

[params]
  description = "Site description"
  author = "Author Name"

[[menu.main]]
  name = "Home"
  url = "/"
  weight = 1

[[menu.main]]
  name = "About"
  url = "/about/"
  weight = 2

[[menu.main]]
  name = "Blog"
  url = "/post/"
  weight = 3
```

#### Blogdown (`config.yaml`)

```yaml
baseURL: "https://example.com/"
title: "My Site"
theme: "hugo-theme"

params:
  description: "Site description"
  author: "Author Name"

menu:
  main:
    - name: "Home"
      url: "/"
      weight: 1
    - name: "About"
      url: "/about/"
      weight: 2
    - name: "Blog"
      url: "/post/"
      weight: 3
```

#### Quarto (`_quarto.yml`)

```yaml
project:
  type: website
  output-dir: _site

website:
  title: "My Site"
  description: "Site description"
  site-url: https://example.com/
  navbar:
    left:
      - href: index.qmd
        text: Home
      - href: about.qmd
        text: About
      - href: blog.qmd
        text: Blog

format:
  html:
    theme: cosmo

author: "Author Name"
```

### Navigation

#### Blogdown (`config.toml`)

```toml
[[menu.main]]
  name = "Blog"
  url = "/post/"

[[menu.main]]
  name = "About"
  url = "/about/"
```

#### Blogdown (`config.yaml`)

```yaml
menu:
  main:
    - name: "Blog"
      url: "/post/"
    - name: "About"
      url: "/about/"
```

#### Quarto

```yaml
website:
  navbar:
    left:
      - text: "Blog"
        href: blog.qmd
      - text: "About"
        href: about.qmd
    right:
      - icon: github
        href: https://github.com/username
```

## Blog Setup

### Listing Page

Create `blog.qmd`:

```yaml
title: "Blog"
listing:
  contents: posts
  type: default
  sort: "date desc"
  categories: true
  feed: true
```

### Post Structure

```txt
posts/
  2024-01-15-first-post/
    index.qmd
    images/
      figure1.png
  2024-01-20-second-post/
    index.qmd
```

### Post Front Matter

```yaml
title: "Post Title"
description: "Brief description for listing"
author: "Author Name"
date: 2024-01-15
categories:
  - R
  - Tutorial
image: images/preview.png
draft: false
```

## Hugo Shortcodes

### Figure

#### Hugo

````markdown
{{</* figure src="image.png" caption="Caption" */>}}
````

#### Quarto

````markdown
![Caption](image.png)
````

### Tweet

#### Hugo

````markdown
{{</* tweet user="username" id="1234567890" */>}}
````

#### Quarto (with extension)

````markdown
{{< tweet username 1234567890 >}}
````

Install extension: `quarto add sellorm/quarto-social-embeds`

### YouTube

#### Hugo

````markdown
{{</* youtube VIDEO_ID */>}}
```

#### Quarto

````markdown
{{< video https://www.youtube.com/embed/VIDEO_ID >}}
````

### Gist

#### Hugo

````markdown
{{</* gist user gist_id */>}}
````

### Highlight

#### Hugo

````markdown
{{</* highlight r */>}}
code here
{{</* /highlight */>}}
```

#### Quarto

````markdown
```{.r}
code here
```
````

or

````markdown
```r
code here
```
````

### Ref/Relref

#### Hugo

````markdown
[Link]({{</* ref "other-post.md" */>}})
````

#### Quarto

````markdown
[Link](other-post.qmd)
````

## Taxonomies

### blogdown Categories and Tags

```yaml
categories: ["R", "Data Science"]
tags: ["ggplot2", "visualization"]
```

### Quarto Categories

```yaml
categories:
  - R
  - Data Science
  - ggplot2
  - visualization
```

Enable category listing:

```yaml
# In blog.qmd
listing:
  contents: posts
  categories: true
```

## Static Files

### blogdown

Static files in `static/` are copied to site root.

### Quarto

Put files in project root or use `resources`:

```yaml
# _quarto.yml
project:
  resources:
    - images/
    - files/
```

## Themes and Styling

### blogdown

Uses Hugo themes from `themes/` directory.

### Quarto

Use built-in themes or custom SCSS:

```yaml
format:
  html:
    theme:
      - cosmo
      - custom.scss
```

### Custom SCSS

```scss
// custom.scss
$body-bg: #ffffff;
$body-color: #333333;
$link-color: #0066cc;

// Custom rules
.quarto-title {
  font-size: 2.5rem;
}
```

## RSS Feed

### blogdown

Hugo generates RSS automatically.

### Quarto

Enable in listing:

- `blog.qmd`

  ````markdown
  ---
  listing:
    feed: true
  ---
  ````

Or in `_quarto.yml`:

```yaml
website:
  site-url: https://example.com

listing:
  feed:
    title: "My Blog"
    description: "Blog description"
```

## Comments

### blogdown (Disqus)

In `config.toml`:

```toml
disqusShortname = "mysite"
```

Or in `config.yaml`:

```yaml
disqusShortname: "mysite"
```

### Quarto

In `_quarto.yml`:

```yaml
website:
  comments:
    giscus:
      repo: username/repo
      category: "Comments"
```

Or per-post:

```yaml
comments:
  giscus:
    repo: username/repo
```

## Syntax Highlighting

### blogdown

Configured in Hugo config or theme.

### Quarto

```yaml
format:
  html:
    highlight-style: github
    code-line-numbers: true
    code-fold: true
```

## Draft Posts

### blogdown

```yaml
draft: true
```

### Quarto

Same syntax:

```yaml
draft: true
```

Render drafts with:

```bash
quarto render --profile drafts
```

With profile config:

```yaml
# _quarto-drafts.yml
execute:
  echo: true

website:
  drafts: true
```

## Step-by-Step Conversion

### 1. Create `_quarto.yml`

Start with basic configuration.

### 2. Convert Navigation

Map Hugo menu to Quarto navbar.

### 3. Create Listing Page

Create `blog.qmd` with listing configuration.

### 4. Migrate Posts

For each post:

1. Rename `.Rmd` to `.qmd`.
2. Update front matter.
3. Convert Hugo shortcodes.
4. Update internal links.

### 5. Migrate Static Files

Move files from `static/` to project root.

### 6. Update Styling

Apply Quarto theme or convert custom CSS.

### 7. Test Locally

```bash
quarto preview
```

### 8. Update Deployment

Update build command from Hugo to Quarto.

## Deployment

### Netlify

```yaml
# netlify.toml
[build]
  command = "quarto render"
  publish = "_site"
```

### GitHub Pages

```yaml
# .github/workflows/publish.yml
name: Publish

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: quarto-dev/quarto-actions/setup@v2
      - run: quarto render
      - uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./_site
```

## Common Issues

### Missing Shortcodes

Install Quarto extensions for missing functionality.

### Broken Internal Links

Update `.md` and `.Rmd` extensions to `.qmd`.

### Theme Differences

Quarto themes differ from Hugo themes; expect visual changes.

### Build Errors

Check for Hugo-specific template syntax in content files.

## Resources

- [Quarto Websites](https://quarto.org/docs/websites/)
- [Quarto Blogs](https://quarto.org/docs/websites/website-blog.html)
- [Quarto Themes](https://quarto.org/docs/output-formats/html-themes.html)
