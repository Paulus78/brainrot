# Bongo-Produktion — Learnings aus Pilot 001 und Plan für die nächste Story

Stand: 2026-09-28

## Ziel dieses Dokuments

Dieses Dokument hält fest, was aus den bisherigen Bongo-Versuchen tatsächlich funktioniert hat, was trotz bestandener technischer Qualitätskontrolle noch nicht überzeugend ist und welche Regeln für das nächste Video gelten. Es ersetzt keine Rohdateien oder Einzel-QC, sondern bildet die kreative Entscheidungsgrundlage für Episode 002.

## Ehrliches Urteil über Pilot 001 V2

V2 ist gegenüber V1 deutlich verständlicher: Der kaputte Ventilator wird gezeigt, er und die Banane gelangen sichtbar in den Eimer, der Eimer wird geschüttelt, der reparierte Ventilator kommt heraus und läuft anschließend. Die Objekt- und Figurenmerkmale sind wesentlich stabiler.

Trotzdem ist das Video noch nicht veröffentlichungsreif. Die Geschichte ist nur dann sicher verständlich, wenn man sehr aufmerksam zusieht. Der Rhythmus wirkt eher wie eine Reihe einzeln erzeugter Tests als wie eine zusammenhängende kleine Szene. Die Inszenierung ist zu statisch, der Einstieg zeigt den Defekt nicht auffällig oder lustig genug, das Schütteln des Eimers wirkt künstlich, der Humor baut sich nicht organisch auf und die Stimme wechselt bei „perfecto“ hörbar in eine unpassend hohe Lage.

## Was funktioniert hat

- Die feste Bongo-Referenz schützt die wichtigsten Erkennungsmerkmale: braunes Fell, große Ohren, asymmetrische Augen, blauer Ring, einzelner Zahn, Banane auf dem Kopf und genau eine linke blaue Sandale.
- Ein klarer Objektzustand pro Keyframe verbessert die Kontinuität deutlich.
- Die Aufteilung in überprüfbare Zustände hat Teleportation und unerklärte Objektwechsel reduziert.
- Kurze Prompts mit einer dominanten Aktion sind für Flow/Veo stabiler als viele gleichzeitige Bewegungen.
- Die akzeptierten Wiederholungen von Shot 1 und Shot 2 zeigen, dass gezielte Korrekturen wirksamer sind als das unveränderte Neugenerieren desselben Prompts.
- Drei ausdrücklich getrennte Bewegungen mit Rückkehr zur Mitte waren technisch zählbarer als ein allgemein formuliertes „dreimal schütteln“; überzeugend oder körperlich glaubwürdig wurde die Bewegung dadurch noch nicht.
- Das Sichern aller Prompts, Rohversuche, Ablehnungsgründe und akzeptierten Dateien in GitHub macht das Projekt reproduzierbar.

## Was noch nicht funktioniert

### 1. Zu viele Informationen in zwölf Sekunden

Der Film versucht in zwölf Sekunden gleichzeitig Folgendes zu erzählen: kaputten Ventilator erkennen, Knopf drücken, Ventilator aufnehmen, vollständig in den Eimer legen, Banane einwerfen, dreimal schütteln, Reparatur enthüllen, Stillstand zeigen, Ventilator starten, Luftwirkung zeigen und fünf gesprochene Beats unterbringen. Die Handlung ist formal vollständig, aber kognitiv überladen.

Konsequenz: Die nächste Episode erhält weniger Handlungsschritte oder etwa 15 Sekunden Laufzeit. Jeder wichtige Zustand bekommt mindestens einen deutlich lesbaren Moment.

### 2. Fünf statische Mini-Clips erzeugen keinen natürlichen Fluss

Die Vorgabe „statische Kamera, harte Schnitte, eine Aktion pro Shot“ half zunächst bei der Kontrolle, wurde aber zu streng angewendet. Dadurch sieht jede Szene wie ein neuer Anlauf aus. Blickrichtung, Körperenergie und räumlicher Impuls werden nicht natürlich über die Schnitte weitergeführt.

Konsequenz: Die nächste Episode nutzt drei bis vier längere erzählerische Einheiten, Bewegungsanschlüsse zwischen den Schnitten und mindestens einen bewusst dynamischen Payoff-Shot. Die Kamera darf sich leicht und motiviert bewegen, wenn dadurch die Aktion besser lesbar wird.

### 3. Das Schütteln des Eimers wirkt nicht überzeugend

Die drei Bewegungen sind zwar grundsätzlich zählbar, sehen aber nicht nach einem schweren Eimer mit Inhalt aus. Die seitliche Bewegung wirkt mechanisch und körperlich nicht glaubwürdig; Bongo und Eimer scheinen zu wackeln, statt dass Bongo sichtbar Kraft überträgt. Der wiederholte identische Bildaufbau macht die Passage zusätzlich langweiliger, obwohl sie nur wenige Sekunden dauert.

Konsequenz: Das handgehaltene Drei-Schüttel-Ritual wird nicht wiederverwendet. Der Eimer steht künftig fest und schwer auf dem Boden oder einer stabilen Werkbank. Bongo gibt ihm drei klar getrennte Klopfer: klein, mittel, stark. Erst nach einer kurzen Stille beginnt der Eimer selbstständig zu rumpeln. Dadurch entstehen Gewicht, Antizipation und Eskalation, ohne komplizierte Arm-, Griff- und Eimerbewegungen gleichzeitig generieren zu müssen.

### 4. Der Einstieg besitzt noch keinen starken Scroll-Stopper

Der Ventilator ist erkennbar defekt, aber sein Defekt ist nicht übertrieben oder komisch genug. Ein leicht hängendes Blatt und ein stiller Knopf funktionieren als technische Erklärung, nicht als sofortiger Brainrot-Hook. In einem Kurzvideo muss im ersten Bild bereits etwas schiefgehen.

Ein stärkerer Ventilator-Einstieg hätte beispielsweise direkt mitten in der Panne begonnen: Der Ventilator hustet einmal, ein loses Blatt schießt heraus und bleibt in Bongos Kopfbanane stecken, während der Motor mit einem traurigen Quietschen absackt. Bongo friert mit nach hinten geblasenen Ohren ein. Damit wären Defekt, Figur und komische Übertreibung innerhalb einer Sekunde verständlich gewesen.

Konsequenz: Künftige Videos beginnen nicht mit einer neutralen Aufbauaufnahme. Innerhalb der ersten 0,8 Sekunden muss eine auffällige Panne, ein absurdes Missgeschick oder eine unmögliche Überraschung passieren. Diese Aktion muss auch als stummes erstes GIF-Fragment funktionieren.

### 5. Der Schnitt beschleunigt die ohnehin kurzen Clips zu stark

Die fünf akzeptierten Quellen wurden für den finalen Zwölf-Sekunden-Schnitt ungefähr mit folgenden Faktoren beschleunigt:

| Shot | Beschleunigung |
| --- | ---: |
| Kaputter Ventilator | 1,21× |
| Ventilator und Banane in den Eimer | 1,48× |
| Drei Schüttelbewegungen | 1,22× |
| Reparierter Ventilator kommt heraus | 1,60× |
| Funktionierender Ventilator / Schluss | 1,78× |

Gerade Reveal und Schluss verlieren dadurch Gewicht. Der Zuschauer bekommt kaum Zeit, den neuen Ventilator zu erkennen, bevor bereits die nächste Pointe folgt.

Konsequenz: In Zukunft maximal etwa 1,15× Geschwindigkeitsänderung für Dialog- oder Storyshots. Wenn ein Clip zu lang ist, wird die Handlung neu inszeniert oder neu erzeugt, statt sie aggressiv zu komprimieren.

### 6. Die Stimme ist nicht wirklich über alle Shots verriegelt

Obwohl in Flow dieselbe benutzerdefinierte Stimme ausgewählt wurde, wurde die Sprachperformance pro Videoclip neu erzeugt. Das sichert keine identische Tonlage, Resonanz oder Sprechweise. Die Regieanweisung „delighted wonder“ bei „OOOOOO… perfecto“ förderte zusätzlich einen hohen, beinahe anderen Charakterklang. Die spätere Zeitkompression bewahrte technisch die Tonhöhe, verdichtete aber die Sprachmelodie und verstärkte den künstlichen Eindruck.

Konsequenz: Veo erzeugt künftig nicht mehr den finalen Dialog pro Shot. Zuerst wird der visuelle Schnitt mit temporärem Ton gebaut. Danach entsteht die gesamte Bongo-Stimme in einer einzigen zusammenhängenden Session mit derselben Stimme und klarer Tonhöhenbegrenzung. Diese Masteraufnahme wird geschnitten, aber nicht pro Szene neu synthetisiert. Falls vorläufig doch Flow-Dialog nötig ist, gilt: „same warm mid-low register throughout; never raise pitch for surprise; surprise comes from timing and breath, not pitch“.

### 7. Technische PASS-Werte reichen nicht für kreative Freigabe

Auflösung, Laufzeit, Pegel, Objektkontinuität und fehlende Schwarzbilder können korrekt sein, während der Film trotzdem langweilig oder schwer verständlich bleibt. Die bisherige Qualitätskontrolle gewichtete technische Kriterien zu stark.

Konsequenz: Jede künftige Freigabe benötigt zusätzlich drei menschliche Gates:

1. **Stummfilmtest:** Ist die Ursache-Wirkung ohne Sprache beim ersten Ansehen verständlich?
2. **Audiovergleich:** Klingt Bongo in allen Zeilen wie exakt dieselbe Figur?
3. **Unterhaltungstest:** Gibt es innerhalb der ersten zwei Sekunden einen Hook, danach eine Eskalation und am Ende ein Bild, das man erneut sehen möchte?

## Neue Produktionsregeln

- Erst Storybeat und Stummfilm-Animatic freigeben, dann Credits für Video ausgeben.
- Innerhalb der ersten 0,8 Sekunden muss ein starker visueller Scroll-Stopper passieren; keine neutrale Einleitung.
- Pro Episode höchstens vier Hauptbeats und höchstens drei kurze Bongo-Zeilen.
- Nicht mehr als ein neuer wichtiger Gedanke innerhalb von ungefähr zwei Sekunden.
- Bewegungen über Schnitte hinweg anschließen: gleiche Richtung, passende Handposition und klarer Vorher-/Nachher-Zustand.
- Den gefüllten Eimer nicht mehr in Bongos Händen hin- und herschütteln. Er bleibt als schwerer, stabiler Anker stehen; Energie entsteht durch Klopfer und anschließendes Eigenleben.
- Reaktionen nicht nur über Dialog erzählen; Augen, Ohren, Körperhaltung, Timing und Geräusche tragen die Pointe.
- Der wichtigste visuelle Gag erhält mindestens 1,5 Sekunden ungestörte Lesbarkeit.
- Kein fertiger Dialog direkt aus einzeln generierten Videoclips.
- Eine einzige Voice-Masteraufnahme pro Episode; keine wechselnde Sprechlage zwischen Shots.
- Stimme: warm, leicht nasal, kleine natürliche Rauheit, mitteltief, organische Atempausen, trocken statt schrill.
- Musik und Geräusche bauen Energie auf, ohne die Handlung zu verdecken.
- Eine finale Version wird erst als PASS markiert, wenn sie einmal ohne Ton und einmal nur als Audio geprüft wurde.
- Nach jedem belastbaren Schritt: kritisch prüfen, Entscheidung dokumentieren, committen und nach `main` auf GitHub pushen.

## Empfohlene neue Story: „Bongo Popcorno“

Diese Geschichte behält Bongo, den gelben Eimer und die absurde Bananenlogik, vermeidet aber eine komplizierte Reparatur. Sie hat einen sofort verständlichen Wunsch, eine einfache Ursache-Wirkung-Kette, eine stärkere Eskalation und einen visuellen Schlussgag.

### Kernidee

Bongo ist hungrig und besitzt nur ein einzelnes, übergroßes goldenes Maiskorn, das auch auf einem Handybildschirm klar lesbar bleibt. Beim Versuch, es zu essen, prallt es mit einem lauten „PING“ von seinem einzelnen Vorderzahn ab und landet im gelben Eimer. Bongo wirft eine Banane hinterher. Nach drei Klopfern beginnt der fest stehende Eimer selbst zu rumpeln und spuckt eine riesige Fontäne bananenförmigen Popcorns aus. Bongo wird darin begraben, taucht zufrieden wieder auf und sagt trocken: „Bongo snacko.“

### Warum diese Idee stärker ist

- Der Wunsch „hungrig / nur ein Korn“ ist sofort verständlich.
- Der Zahn-PING ist bereits im ersten Moment eine sichtbare Panne und ein akustischer Scroll-Stopper.
- Es müssen keine technischen Details eines kaputten Geräts erklärt werden.
- Korn und Banane sind visuell klar unterscheidbar.
- Das Ergebnis ist eine deutliche Vergrößerung und damit ohne Dialog lesbar.
- Die Popcornfontäne erzeugt Bewegung, Überraschung und ein starkes Thumbnail-Bild.
- Der Schluss kann nahtlos zum Anfang zurückführen und erhöht den Loop- und Rewatch-Wert.

## Beat Sheet für 15 Sekunden

### Beat 1 — Hook: Zahn-PING, 0,0–3,0 Sekunden

Das erste Bild beginnt bereits mitten in der Aktion: Bongo versucht gierig, genau ein übergroßes goldenes Maiskorn zu beißen. Nach spätestens 0,8 Sekunden prallt es mit einem übertrieben klaren „PING“ von seinem einzelnen, fest sitzenden Vorderzahn ab. Der Zahn bleibt unverändert. Das Korn fliegt in einer gut verfolgbaren Bahn nach unten und landet im bekannten leeren gelben Smiley-Eimer. Bongo erstarrt kurz mit aufgerichteten Ohren und schaut dem Korn verwundert hinterher. Kein erklärender Satz nötig.

Ziel: Der erste komische Unfall stoppt den Scroll innerhalb von 0,8 Sekunden; Hunger, genau ein Korn und dessen Landung im Eimer sind ohne Sprache verständlich.

### Beat 2 — Klare Zutaten, 3,0–7,0 Sekunden

Der Bewegungsanschluss folgt dem bereits in den Eimer gefallenen Korn. In einer zusammenhängenden mittleren Einstellung schaut Bongo hinein, hat eine absurde Idee und wirft genau eine ganze Banane hinterher. Die Banane überquert sichtbar den Rand und verschwindet vollständig. Er grinst: „Bucketo.“

Ziel: Korn und Banane sind als zwei getrennte Zutaten vollständig nachvollziehbar, ohne einen versteckten Objektwechsel.

### Beat 3 — Spannung statt hektischer Wiederholung, 7,0–10,5 Sekunden

Bongo stellt beide Füße fest auf den Boden; der Eimer bleibt vollständig abgestellt und bewegt sich zunächst nicht. Bongo gibt dem Eimer mit einer Pfote drei rhythmische Klopfer: klein, mittel, stark. Seine Pfote löst sich nach jedem Kontakt klar vom Eimer. Nach dem dritten Schlag bleibt er abrupt still. Eine kurze halbe Sekunde passiert gar nichts. Dann beginnt ausschließlich der Eimer von selbst zu rumpeln; Bongo weicht misstrauisch einen Schritt zurück. Bongo hebt den Eimer zu keinem Zeitpunkt an und schüttelt ihn nicht.

Ziel: Erwartung und komödiantische Pause entstehen, bevor der Payoff beginnt.

### Beat 4 — Großer Payoff und Loop, 10,5–15,0 Sekunden

Eine gewaltige Fontäne gelben, bananenförmigen Popcorns schießt aus dem Eimer und begräbt Bongo bis auf Kopf und Ohren. Die Kamera darf leicht zurückfahren, damit die Eskalation Platz bekommt. Bongo taucht auf, nimmt ein Stück, kostet es und sagt in derselben mitteltiefen Stimme trocken: „Bongo snacko.“ Ein einzelnes Maiskorn fällt am Schluss wieder neben den Eimer und schafft die Möglichkeit für einen sauberen Loop.

Ziel: Das finale Bild bleibt mindestens 1,5 Sekunden lesbar und trägt die Pointe auch ohne Sprache.

## Geplanter visueller Rhythmus

| Abschnitt | Bildgefühl | Schnittprinzip |
| --- | --- | --- |
| Hook | nah, sofort verständlich | schneller Einstieg, aber kein hektischer Folgeschnitt |
| Zutaten | ruhige mittlere Einstellung | kontinuierliche sichtbare Aktion |
| Ritual | zunehmende Energie | Rhythmus durch Bewegung und Ton, nicht durch viele Schnitte |
| Payoff | weit genug für die Fontäne | leichte motivierte Kamerafahrt, längerer Schluss-Hold |

## Audio- und Voice-Plan

1. Visuelle Clips zunächst ohne finalen Dialog erzeugen.
2. Rohschnitt mit Geräuschen und temporärer Sprachspur erstellen.
3. Alle endgültigen Zeilen als eine einzige Bongo-Performance aufnehmen oder generieren:
   - „Bucketo.“ — selbstsicher, knapp, mitteltief.
   - „Bongo snacko.“ — trocken, zufrieden, exakt gleiche Tonlage.
4. Keine Regieanweisung wie „high-pitched excitement“, „delighted squeal“ oder langes „OOOOOO“ verwenden.
5. Die Stimme zuerst komplett solo anhören und erst nach bestandener Identitätsprüfung in den Videoschnitt legen.
6. Geräusche: sofortiges klares Zahn-PING, hörbare Kornlandung, weicher Bananen-Plopp, drei steigende Eimerklopfer, kurze Stille, wachsendes Rumpeln, große Popcornfontäne, trockener letzter Knusperton.

## Neue Erkenntnisse aus den Bewegungsprototypen von Episode 002

### Kleine Objekttransfers bleiben trotz gesperrter Endbilder unzuverlässig

Vier Veo-Versuche mit dem Maiskorn führten zu verlangsamtem Fall, Morphing, Wiederauftauchen oder Duplikaten. Der einzelne Transfer wurde erst eindeutig, als Zahnkontakt, Randzustand und leerer Eimer als kontrollierte Zustände mit festem Timing zusammengeschnitten wurden. Die Banane war wegen ihrer Größe besser verfolgbar, hinterließ aber im Rohclip einen sichtbaren Stielrest. Daraus folgt: brauchbare KI-Bewegung darf übernommen werden, ein fehlerhafter Endzustand jedoch nicht.

### „Genau dreimal“ im Prompt garantiert keine drei sichtbaren Kontakte

Beim ersten Klopfversuch winkte Bongo mit der Pfote, während der Eimer abhob und mehrfach hüpfte. Der Text war eindeutig, die generierte Körpermechanik trotzdem falsch. Zählbare Wiederholung wird deshalb nicht mehr nur sprachlich verlangt, sondern aus einem klar getrennten Bereitschafts- und Kontaktzustand aufgebaut. Die Kontaktphasen müssen durch vollständig freie Pfotenpositionen getrennt sein.

### Kontrolle allein genügt nicht: harte Zustandswechsel können wieder langweilig wirken

Der erste kontrollierte Klopfschnitt bestand zwar die Zähl- und Bodenprüfung, sah durch harte Sprünge jedoch mechanisch aus. Weiche Überblendkurven zwischen exakt denselben Zuständen lieferten mehr Fluss, ohne die Objektkontinuität aufzugeben. Die drei Kontaktpulse wurden bewusst länger statt schneller: klein, mittel, stark.

### Eine korrekte Aktion braucht eine sichtbare emotionale Folge

Die zweite kontrollierte Version hatte drei Klopfer, Pause und Rumpeln, aber Bongo reagierte nicht. Sie war logisch korrekt und trotzdem flach. Erst das verzögerte Zurückweichen, die eingezogenen Pfoten und die geweiteten Augen machen klar, dass der Eimer nun selbstständig lebt. Für jeden übernatürlichen Objektbeat gilt daher: Reaktion erst nach dem Auslöser, aber sichtbar genug, um dessen Bedeutung zu verstärken.

### Aktueller belastbarer Stand

- Zahn-PING-Hook: bestanden als kontrollierter Hybrid.
- Banane in den Eimer: bestanden als Kombination aus verifizierter Veo-Bewegung und sauberem Endzustand.
- Drei Klopfer plus Eigenrütteln: bestanden als Hybrid V3; Eimer bleibt durchgehend am Boden.
- Finale Popcornfontäne: bestanden als Hybrid V2 mit eindeutigem Eimerursprung, kurzer Eskalation und mehr als 3,5 Sekunden Schlussbild.

Diese Ergebnisse bestätigen die Produktionsregel: generative Bewegung wird nur dort eingesetzt, wo sie nach Einzelbildprüfung physisch und erzählerisch besteht. Kritische Objektübergänge, exakte Wiederholungszahlen und Bodenhaftung werden deterministisch abgesichert.

Der erste vollständige Bildschnitt bestätigt außerdem, dass das 15-Sekunden-Ziel ohne hektische Beschleunigung erreichbar ist. Die vier bestandenen Einheiten ergeben 14,959 Sekunden, wenn ausschließlich die langen Ergebnis-Holds von Hook und Bananenbeat gekürzt werden. Ritual und Payoff bleiben vollständig. In der stummen Übersicht ist die gesamte Ursache-Wirkung-Kette beim ersten Durchlauf nachvollziehbar; der visuell größte Gag erhält die längste ununterbrochene Lesbarkeit.

## Produktionsplan für Episode 002

### Phase A — Story und Lesbarkeit

- Drei bis vier Storyboard-Keyframes erstellen.
- Zustände von Bongo, Eimer, Korn und Banane in einer kleinen Continuity-Tabelle festhalten.
- Einen 15-Sekunden-Stummfilm-Animatic bauen.
- Nur fortfahren, wenn eine Erstansicht ohne Erklärung verständlich ist.

### Phase B — Bewegungsprototypen

- Zuerst Zahn-PING-Hook, Zutaten-Shot und Payoff-Shot testen, weil dort das größte Generationsrisiko liegt.
- Pro Test nur eine klar definierte Bewegung bewerten.
- Fehlversuche sofort mit sichtbarem Ablehnungsgrund dokumentieren.
- Keine weiteren Shots erzeugen, solange Ursache oder Payoff nicht lesbar sind.

### Phase C — Schnitt und Stimme

- Drei bis vier längere Shots mit Bewegungsanschlüssen montieren.
- Keine Storyaufnahme stärker als ungefähr 1,15× beschleunigen.
- Rohschnitt stumm und anschließend nur als Audio prüfen.
- Eine einzelne Voice-Masteraufnahme erzeugen und in den fertigen Bildschnitt einpassen.
- Erst danach Geräusche und gegebenenfalls eine sehr reduzierte musikalische Textur ergänzen.

### Phase D — finale Qualitätsprüfung

- Erster-Blick-Stummfilmtest.
- Stimmenvergleich beider Zeilen.
- Frame-Prüfung von blauem Augenring, Zahn, Kopfbanane und linker Sandale.
- Prüfung auf zusätzliche Körner, Bananen, Eimer oder dupliziertes Popcorn vor dem Payoff.
- Mindestens 1,5 Sekunden klarer Schluss-Hold.
- Technische Prüfung von Laufzeit, Format, Lautheit und Schwarzbildern.
- Dokumentation, Commit und Push auf GitHub.

## Freigabekriterien für die nächste Version

Episode 002 ist erst fertig, wenn alle folgenden Fragen mit Ja beantwortet werden:

- Versteht man ohne Ton: kleines Korn plus Banane gehen hinein, sehr viel Bananenpopcorn kommt heraus?
- Passiert innerhalb der ersten 0,8 Sekunden ein klarer, lustiger Scroll-Stopper?
- Fühlt sich die Szene wie ein zusammenhängender Moment und nicht wie mehrere Testclips an?
- Bleibt Bongo in jedem Shot dieselbe Figur?
- Klingt jede gesprochene Zeile eindeutig nach derselben Stimme?
- Gibt es eine erkennbare Steigerung von ruhig zu gespannt zu chaotisch?
- Bleibt der Eimer während des Rituals sichtbar schwer und stabil, ohne das alte künstliche Hin-und-her-Schütteln?
- Bleibt der visuelle Payoff lange genug stehen, um ihn zu erfassen?
- Ist der Schluss lustig oder überraschend genug, dass ein erneutes Ansehen reizvoll ist?

## Nächster konkreter Schritt

Der Bildschnitt ist bestanden. Als nächstes folgt die einmalig erzeugte Voice-Masteraufnahme für „Bucketo.“ und „Bongo snacko.“. Beide Zeilen müssen in derselben mitteltiefen, warmen, trockenen Stimme innerhalb einer Session entstehen. Anschließend wird zuerst nur die Sprachspur auf Identität und Natürlichkeit geprüft und erst danach mit dem Bildschnitt verbunden.
