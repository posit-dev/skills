# pkgdown configuration basics

pkgdown configuration usually lives in `_pkgdown.yml`.

## `url` is critical

Set a stable site URL:

- GitHub Pages: `https://<org>.github.io/<repo>/`
- Custom domain: your canonical URL

This affects generated links, metadata, and canonical URLs.

If you change `url` after publishing, you can end up with stale links and SEO/canonical URL confusion.

## Common sections

- `template`: site theme and template options
- `navbar`: top navigation
- `reference`: curated reference index and ordering
- `articles`: group and order articles

Common additional sections:

- `home`: what appears on the home page
- `development`: toggles for development features and warnings

Start minimal and add structure when needed.

## Bootstrap 5

pkgdown 2.x uses Bootstrap 5 if you opt in explicitly:

```yaml
template:
	bootstrap: 5
```

If you have a heavily customized site, test this carefully.

## Minimal example

```yaml
url: https://org.github.io/repo/

template:
	bootstrap: 5

navbar:
	structure:
		left:  [reference, articles, news]
		right: [github]
```
