# Flux76.com — live zetten via GitHub Pages (Flux76HQ)

De site is een statische pagina (`index.html` + wat assets), dus GitHub Pages is perfect. Twee delen: (A) repo + Pages aanzetten, (B) je domein `flux76.com` koppelen.

---

## A. Repo aanmaken en Pages aanzetten

1. Maak in je organisatie **Flux76HQ** een nieuwe **publieke** repo met exact deze naam:
   ```
   flux76hq.github.io
   ```
   *(Een repo met de naam `<org>.github.io` wordt automatisch de hoofdsite van de org — ideaal voor je apex-domein.)*

2. Zet **alle bestanden uit de map `website/`** in de **root** van die repo:
   ```
   index.html
   favicon.svg
   og-image.png
   CNAME          ← bevat al: flux76.com
   .nojekyll
   ```
   Slepen via de webinterface (Add file → Upload files) kan, of via git:
   ```bash
   git clone https://github.com/Flux76HQ/flux76hq.github.io
   cd flux76hq.github.io
   # kopieer de inhoud van website/ hierin
   git add .
   git commit -m "Flux76.com launch"
   git push
   ```

3. Ga naar **Settings → Pages**.
   - **Source:** "Deploy from a branch" → branch **main** → map **/(root)** → Save.
   - Na ~1 minuut staat je site live op `https://flux76hq.github.io`.

---

## B. Je domein flux76.com koppelen

### B1. In GitHub (Pages-instellingen)
- **Settings → Pages → Custom domain:** typ `flux76.com` → Save.
  *(Het `CNAME`-bestand staat er al; GitHub pikt dit op.)*
- Aanrader: verifieer je domein op org-niveau (**Org Settings → Pages → Verified domains**) om domain-takeover te voorkomen.

### B2. Bij je domeinregistrar (DNS)
Zorg dat oude records/forwarding voor flux76.com eerst **weg** zijn. Maak dan:

**Apex (`flux76.com`) — 4 A-records:**
```
185.199.108.153
185.199.109.153
185.199.110.153
185.199.111.153
```
*(Optioneel, voor IPv6, ook 4 AAAA-records:)*
```
2606:50c0:8000::153
2606:50c0:8001::153
2606:50c0:8002::153
2606:50c0:8003::153
```

**www (`www.flux76.com`) — 1 CNAME-record:**
```
www  →  flux76hq.github.io
```
GitHub maakt automatisch de redirect tussen `flux76.com` en `www.flux76.com`.

### B3. HTTPS aanzetten
- Terug in **Settings → Pages**: vink **"Enforce HTTPS"** aan zodra die optie beschikbaar is (kan even duren tot het certificaat is uitgegeven).

---

## Even geduld & controle
- DNS-wijzigingen kunnen tot **24 uur** duren om overal door te werken (meestal sneller).
- Test in een incognitovenster: `https://flux76.com` en `https://www.flux76.com` moeten allebei je site tonen, met een geldig slotje.
- Controle via terminal: `dig flux76.com +noall +answer -t A` → moet de vier GitHub-IP's teruggeven.

---

## Nog aanpassen in de site (optioneel)
- **App Store-links** toevoegen zodra je apps live zijn (nu wijzen de knoppen naar de projecten/GitHub).
- **Bluesky/Discord-links** invullen in de footer (nu placeholders).
- `flux76.app` later als aparte app-landingssite opzetten (eigen repo + dat domein), of laten doorverwijzen naar `flux76.com/#projects` voorlopig.
