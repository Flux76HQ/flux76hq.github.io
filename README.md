# Flux76.com

De website van Flux76, een app- en webstudio uit Nederland. Statische site op GitHub Pages
(`main`, map `/`), in het Engels op [flux76.com](https://flux76.com/) en in het Nederlands op
[flux76.com/nl/](https://flux76.com/nl/), met een privacyverklaring (`/privacy/`, `/nl/privacy/`) en
voorwaarden (`/terms/`, `/nl/voorwaarden/`).

*The Flux76 company website: a static site on GitHub Pages, in English at `/` and Dutch at `/nl/`.*

## Hoe het in elkaar zit

| Pad | Wat |
|---|---|
| `src/index.template.html` | De homepage, voor beide talen |
| `src/legal.template.html` | De privacyverklaring en de voorwaarden, voor beide talen |
| `src/partials/` | Wat alle pagina's delen: kop, navigatie, voettekst; ingevoegd met `{{> naam}}` |
| `src/content/en.json`, `nl.json` | Alle korte tekst, per taal |
| `src/legal/<taal>/privacy.html`, `terms.html` | De tekst van de juridische pagina's, als HTML |
| `scripts/build.py` | Maakt alle pagina's uit template + tekst; de lijst staat in `PAGES` |
| `scripts/check.py` | Controles (zie hieronder) |
| `assets/css/tokens.css` | De Flux76-merktokens, overgenomen uit `App-Guidance/shared/branding/flux76/` |
| `assets/css/site.css`, `assets/js/site.js` | Stijl en gedrag van de site |
| `assets/fonts/` | Zelf gehoste lettertypen met licenties: Archivo (één variabel bestand voor koppen en tekst) en JetBrains Mono |
| `assets/img/` | Screenshots als WebP |

`index.html`, `nl/index.html` en de juridische pagina's (`privacy/`, `terms/`, `nl/privacy/`,
`nl/voorwaarden/`) zijn **gegenereerd en staan toch in de repo**: GitHub Pages
serveert de repo zoals hij is, dus er is geen deploy-stap die ze voor ons kan bouwen. Bewerk ze
niet met de hand.

## Een tekst aanpassen

1. Pas de waarde aan in `src/content/en.json` **en** `src/content/nl.json`.
2. `python3 scripts/build.py`
3. `python3 scripts/check.py`
4. Commit de bron en de gegenereerde pagina's samen.

## De privacyverklaring of voorwaarden aanpassen

1. Pas `src/legal/nl/<document>.html` **en** `src/legal/en/<document>.html` aan.
2. Zet in `scripts/build.py` de datum `updated` van dat document (`PRIVACY` of `TERMS`) op vandaag; die
   staat bovenaan de pagina als "Laatst bijgewerkt".
3. Zet `lastmod` in `sitemap.xml` voor beide talen op dezelfde datum.
4. Bouw, controleer en commit zoals hierboven.

Verandert de site zelf iets aan wat hij verwerkt (analytics, een formulier, een ingesloten dienst van
een andere partij, een nieuwe hoster), werk dan in dezelfde wijziging de privacyverklaring bij.

Alleen Python 3 is nodig; er zijn geen dependencies.

## Lokaal bekijken

```bash
python3 -m http.server 8000
```

Open daarna `http://localhost:8000/` en `http://localhost:8000/nl/`. De pagina's gebruiken paden
vanaf de root (`/assets/...`), dus open ze via de server en niet als los bestand.

## Controles

`python3 scripts/check.py` draait ook bij elke pull request (`.github/workflows/check.yml`) en
faalt als:

- de gecommitte pagina's niet overeenkomen met de bron;
- een sleutel in één taal ontbreekt, leeg is, niet gebruikt wordt, of in beide talen dezelfde
  waarde heeft (onvertaald), tenzij hij in `SAME_IN_BOTH` staat;
- een pagina niet in `sitemap.xml` staat, of andersom;
- een link naar een anker of lokaal bestand nergens uitkomt;
- een pagina iets laadt van een andere host. Lettertypen, beelden, scripts en stijlen staan
  allemaal in deze repo, zodat een bezoek geen derde partij raakt.

## Publiceren

Mergen naar `main` zet de site live. DNS en Pages-instellingen staan in [`DEPLOY.md`](DEPLOY.md).

## Merk en beeld

- Kleuren, lettertypen en het logo volgen `App-Guidance/shared/branding/flux76/brand.md`. Verwijs
  naar de tokens in `tokens.css`; zet geen losse merkkleuren in `site.css`. Het lichte kleurenschema
  is met `color-mix()` uit die tokens afgeleid. De site volgt het schema van het apparaat, tot de
  bezoeker met de knop in de navigatie zelf licht of donker kiest; die keuze wordt in de browser onthouden.
- De DiscVault-beelden komen uit `Flux76HQ/discvault.eu` (`media-source/screenshots/`,
  `screenshots-light/` en, voor de telefoon, `screenshots-iphone/`): de democollectie met verzonnen films en gegenereerde hoezen. Gebruik
  geen screenshots met echte filmhoezen.
- Elk themabeeld bestaat in `-light-` en `-dark-` en in twee breedtes; houd die namen aan bij
  vervangen, dan hoeft de template niet mee te veranderen.
