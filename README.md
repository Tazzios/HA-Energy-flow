# Energy Flow

**Proof of concept! *vibe coding* alert 😄**
Vertalingen werken nog niet en de code kan waarschijnlijk nog heel stuk verbeterd worden.
Deze release is om de animo te peilen en om te zien of er ervaren HA ontwikkelaars willen meehelpen.

## Wat doet het?
Deze integratie splitst de energiestromen in huis op in:

* Zon → huis
* Zon → grid
* Zon → batterij
* Grid → batterij
* Batterij → huis
* Batterij → grid

Per minuut wordt het aantal kWh bepaald.
In combinatie met deze integratie [dynamic_energy_cost](https://github.com/martinarva/dynamic_energy_cost?utm_source=chatgpt.com) kun je dit vervolgens omzetten naar euro’s (15min,dag,maand,jaar).

## Waarom?
Bij het berekenen van de opbrengst in euro’s is het vaak persoonlijk (of landelijk bepaald) hoeveel waarde je toekent aan:
* direct verbruikte zonne-energie
* teruggeleverde zonne-energie

Met deze integratie kun je verschillende prijzen koppelen aan de verschillende energiestromen.

## Code
* De code gaat ervan uit dat je **alle** zonnepanelen- en batterij-energy meters toevoegt. Doe je dit niet, dan kunnen er vreemde resultaten ontstaan.
* Zonne-energie wordt altijd eerst in huis gebruikt.

Voorbeeld van de configuratie
<img width="547" height="935" alt="image" src="https://github.com/user-attachments/assets/73d50f59-9a06-4977-897b-3c9befb1892d" />


