# -*- coding: utf-8 -*-
"""
Obsah podstránek. Zdroj pravdy pro tools/build_pages.py.

Pravidla, která tu platí:
  - Čísla musí sedět s homepage: 250 mil. Kč proinvestováno, průměrný ROAS 4,3,
    6+ let v oboru, vítěz Sklik výzvy Black Friday 2025. Nikde jinou hodnotu.
  - Žádné ceny. Cenu určuje konzultace, tak je to i ve FAQ.
  - Každá stránka odkazuje na 3 další (pole `related`), aby prolinkování
    mířilo na konkrétní stránky, ne jen na homepage.
  - FAQ otázky se mezi stránkami NEOPAKUJÍ a neopakují ani ty z homepage
    (tools/faq.json), jinak si stránky konkurují navzájem.
"""

SITE = {
    "base": "https://www.pavelvognarek.cz",
    "modified": "2026-09-06",
}

NAV = [
    {"slug": "sprava-google-ads", "href": "/sprava-google-ads/", "label": "Google Ads"},
    {"slug": "sprava-meta-ads", "href": "/sprava-meta-ads/", "label": "Meta Ads"},
    {"slug": "ppc-pro-eshopy", "href": "/ppc-pro-eshopy/", "label": "PPC pro e-shopy"},
    {"slug": "ppc-audit", "href": "/ppc-audit/", "label": "Audit PPC"},
    {"slug": "ppc-specialista-brno", "href": "/ppc-specialista-brno/", "label": "PPC Brno"},
]

PAGES = [
    # ══════════════════════════════════════════════════════════════════════
    {
        "slug": "sprava-google-ads",
        "nav_label": "Správa Google Ads",
        "teaser": "Search, Shopping a Performance Max pro e-shopy a B2B",
        "crumb": "Správa Google Ads",
        "title": "Správa Google Ads pro e-shopy a B2B | Pavel Vognárek",
        "description": "Kompletní správa Google Ads: Search, Shopping, Performance Max, měření v GA4 a produktový feed. 250 mil. Kč v kampaních, průměrný ROAS 4,3. Česko i Slovensko.",
        "service_name": "Správa Google Ads",
        "service_type": "Správa PPC kampaní v Google Ads",
        "area": ["Česká republika", "Slovensko"],
        "h1": "Správa Google Ads pro e-shopy a&nbsp;B2B<br><span>bez černé skříňky</span>",
        "lead": "Správa Google Ads znamená u mě celý cyklus: audit účtu, struktura kampaní, klíčová a negativní klíčová slova, bidding strategie, měření konverzí v GA4 a produktový feed pro Shopping a Performance Max. K tomu měsíční report, ve kterém se dozvíte, co se stalo a proč.",
        "faq_title": "Časté otázky ke správě Google Ads",
        "cta_title": "Pojďme se podívat do vašeho účtu",
        "cta_text": "Úvodní konzultace trvá asi 30 minut a je zdarma. Projdeme aktuální stav účtu, cíle a jestli má spolupráce vůbec smysl.",
        "form_placeholder": "Napište mi, jaký máte měsíční rozpočet v Google Ads a co vás na účtu nejvíc trápí...",
        "related": ["ppc-audit", "ppc-pro-eshopy", "sprava-meta-ads"],
        "sections": [
            {
                "h2": "Co ve správě Google Ads reálně dostanete",
                "html": """
<p>Slovo správa se v nabídkách používá pro hodně různých věcí, od jednou měsíčně zkontrolovaného rozpočtu po každodenní práci s účtem. Aby bylo jasno, tady je konkrétní výčet toho, co dělám.</p>
<h3>Struktura a nastavení kampaní</h3>
<ul>
  <li><strong>Search kampaně:</strong> rozdělení podle záměru, ne podle abecedy. Brand, generické dotazy, konkurence a dlouhý ocas mají každý jinou ekonomiku, takže patří do jiných kampaní s jiným rozpočtem.</li>
  <li><strong>Klíčová a negativní klíčová slova:</strong> pravidelný průchod reálnými vyhledávacími dotazy. Negativa přidávám ve frázové shodě, protože přesná shoda nezablokuje varianty téhož dotazu.</li>
  <li><strong>Shopping a Performance Max:</strong> rozdělení produktů podle marže a obrátky, aby PMax netlačil rozpočet jen do bestsellerů, které by se prodaly tak jako tak.</li>
  <li><strong>Texty reklam a rozšíření:</strong> responzivní reklamy s dost odlišnými nadpisy, aby měl algoritmus co kombinovat, plus rozšíření o odkazy, popisky a ceny.</li>
</ul>
<h3>Měření, bez kterého je optimalizace tipování</h3>
<ul>
  <li>Kontrola konverzí v GA4 a v Google Ads: co je primární konverze, co jen mikrokonverze, a jestli se nesčítá obojí do jednoho čísla.</li>
  <li>Rozdělení metrik podle konverzní akce. CPA počítám na nákup, ne na součet všech konverzí, jinak vychází vždycky lépe, než jaká je realita.</li>
  <li>Hodnota konverze a napojení na skutečné tržby, aby ROAS nebyl jen hezké číslo do reportu.</li>
</ul>
<h3>Průběžná práce a reporting</h3>
<ul>
  <li>Optimalizace rozpočtů mezi kampaněmi podle toho, kde reálně přibývají objednávky.</li>
  <li>Sledování učící fáze u bidding strategií, aby změny rozpočtu neresetovaly to, co se algoritmus naučil.</li>
  <li>Měsíční report s vysvětlením, co se stalo, proč a co bude dál. Ne jen export čísel.</li>
</ul>
""",
            },
            {
                "h2": "Jak spolupráce probíhá",
                "class": "bg-light",
                "html": """
<ol class="steps">
  <li><strong>Úvodní konzultace, asi 30 minut, zdarma</strong>
    <p>Projdeme váš business, cíle a aktuální stav účtu. Na konci víte, jestli má smysl pokračovat, i kdyby odpověď byla ne.</p></li>
  <li><strong>Audit účtu, 1 až 2 týdny</strong>
    <p>Analýza kampaní, měření, produktového feedu a celkové strategie. Výstupem je konkrétní plán s prioritami, ne seznam obecných doporučení.</p></li>
  <li><strong>Nasazení změn</strong>
    <p>Nejdřív se opraví měření, teprve pak kampaně. Optimalizovat na rozbitá data znamená utíkat špatným směrem rychleji.</p></li>
  <li><strong>Průběžná správa a vyhodnocení</strong>
    <p>První poctivé vyhodnocení po čtyřech až šesti týdnech, protože chytré bidding strategie potřebují dva až tři týdny na naučení. Pak měsíční cyklus report a plán.</p></li>
</ol>
<p class="muted">Přístup do účtů zůstává celou dobu váš. Když spolupráce skončí, nic si neodnáším a účet zůstává funkční.</p>
""",
            },
            {
                "h2": "Pro koho to sedí a pro koho ne",
                "html": """
<div class="cards">
  <div class="card">
    <div class="card-num">SEDÍ</div>
    <h3>E-shop, kde Google Ads už běží</h3>
    <p>Máte historii konverzí a rozpočet, ale chybí strategický pohled a propojení s ostatními kanály. Tady je nejrychlejší návratnost práce.</p>
  </div>
  <div class="card">
    <div class="card-num">SEDÍ</div>
    <h3>B2B firma s delším rozhodováním</h3>
    <p>Poptávka nevzniká hned po kliknutí. Řeší se kvalita leadů a měření až do CRM, ne počet konverzí ve formuláři.</p>
  </div>
  <div class="card">
    <div class="card-num">SEDÍ</div>
    <h3>Přechod od agentury</h3>
    <p>Dostáváte reporty, ale ne odpovědi. Začínáme auditem převzatého účtu, ne bouráním všeho, co funguje.</p>
  </div>
  <div class="card">
    <div class="card-num">NESEDÍ</div>
    <h3>Jen rychlá úprava kampaní</h3>
    <p>Pokud hledáte hodinu práce v účtu bez přístupu k datům a bez dialogu o marži, nebudu vám platný.</p>
  </div>
  <div class="card">
    <div class="card-num">NESEDÍ</div>
    <h3>Bez přístupu k měření</h3>
    <p>Když se nedostanu do GA4 ani do dat o objednávkách, nedokážu odlišit dobrý ROAS od dobře vypadajícího ROAS.</p>
  </div>
  <div class="card">
    <div class="card-num">NESEDÍ</div>
    <h3>Garance pozice nebo obratu</h3>
    <p>Nikdo, kdo tomu rozumí, negarantuje konkrétní číslo předem. Garantuju postup a transparentnost, ne výsledek aukce.</p>
  </div>
</div>
""",
            },
            {
                "h2": "Čím se to dá doložit",
                "class": "bg-light",
                "html": """
<p>Přes <strong>250 milionů Kč</strong> proinvestovaných v reklamních kampaních a <strong>průměrný ROAS 4,3</strong> napříč spravovanými účty. Zkušenosti sbírám od menších e-shopů s rozpočty v desítkách tisíc měsíčně po účty s rozpočty v milionech, jako Doppler, Biju.cz, Lomax nebo Fitmin.</p>
<p>Dvě věci si můžete ověřit u zdroje, ne jen na mém webu:</p>
<ul>
  <li><a href="https://blog.seznam.cz/2025/12/sklik-vyzva-nejlepsi-black-friday-strategie-ma-viteze/" target="_blank" rel="noopener">První místo ve Sklik výzvě za nejlepší Black Friday strategii 2025</a> na blogu Seznamu.</li>
  <li><a href="https://www.sklikakademie.cz/cs/pripadove-studie/detail/~/17/" target="_blank" rel="noopener">Případová studie Doppler</a> na Sklik Akademii.</li>
</ul>
<p>Praxi mám z brněnských agentur ROIMARK a In Creative i z přímé spolupráce s klienty. Podrobnosti o značkách najdete <a href="/#reference">v referencích na úvodní stránce</a>.</p>
""",
            },
        ],
        "faq": [
            ("Jak často se v účtu reálně pracuje?",
             "Záleží na velikosti účtu, ale u aktivně spravovaných účtů se do nich dívám několikrát týdně. Nejde o to klikat každý den, jde o to nenechat kampaň jet týden špatným směrem. Denní kontrola dává smysl v období, kdy se něco mění: nová kampaň, nový feed, sezónní špička. V klidném období je důležitější kvalita zásahů než jejich počet."),
            ("Jak pracujete s Performance Max, když do něj není vidět?",
             "PMax je černější skříňka než klasické kampaně, ale ne úplně slepá. Pracuji s rozdělením produktů do asset groups a listing groups podle marže a obrátky, hlídám podíl brandových dotazů, sleduji sestavy podle výkonu a používám vylučování značky tam, kde má smysl. Klíčové je nedat PMaxu celý katalog jedním balíkem, protože pak si vybere to, co by se prodalo i bez reklamy, a vykáže skvělý ROAS bez skutečného přínosu."),
            ("Co když mám malý rozpočet a Google Ads mi zatím nevydělávají?",
             "U malých rozpočtů je nejčastější chyba rozdrobení do příliš mnoha kampaní. Data se pak rozpadnou na tolik částí, že se algoritmus nemá z čeho učit. Řešení bývá zúžení na to, co má nejlepší marži a nejjasnější poptávku, a teprve pak rozšiřování. Někdy je odpověď i to, že Google Ads nejsou v dané fázi ten správný kanál, a řeknu to rovnou."),
            ("Používáte automatické bidding strategie, nebo ruční nabídky?",
             "Skoro vždy automatické, protože ruční nabídky dnes nemají jak konkurovat signálům, které má systém k dispozici. Podmínkou ale je funkční měření a dost konverzí. U účtu, který má pár konverzí měsíčně, automatická strategie jen znásobí šum, takže se tam začíná jinak: sběrem dat a mikrokonverzemi, které dávají smysl."),
            ("Spravujete Google Ads i pro slovenský trh?",
             "Ano. Slovensko obsluhuji online a jazyk není překážka. Kampaně se pro SK ale nedají jen zkopírovat: jiná aukce, jiné ceny za klik, jiné zvyky ve vyhledávání a u e-shopů i jiná měna a lokalizace feedu. Právě proto se tam dá získat výhoda proti konkurenci, která nasadila české kampaně beze změny."),
        ],
    },
    # ══════════════════════════════════════════════════════════════════════
    {
        "slug": "sprava-meta-ads",
        "nav_label": "Správa Meta Ads",
        "teaser": "Facebook a Instagram, kreativa a škálování výkonu",
        "crumb": "Správa Meta Ads",
        "title": "Správa Meta Ads: Facebook a Instagram reklama | Pavel Vognárek",
        "description": "Správa Meta Ads pro e-shopy a B2B: katalogové kampaně, prospecting, obměna kreativy, Conversions API a škálování podle incrementality. Česko i Slovensko.",
        "service_name": "Správa Meta Ads",
        "service_type": "Správa reklamy na Facebooku a Instagramu",
        "area": ["Česká republika", "Slovensko"],
        "h1": "Správa Meta Ads<br><span>Facebook a Instagram jako plnohodnotný kanál</span>",
        "lead": "Meta Ads u mě není přívěsek k Googlu. U e-shopů řeším katalogové a dynamické remarketingové kampaně nad produktovým feedem, prospecting na nová publika a hlavně kreativu, protože právě na ní se výsledek v Metě láme nejvíc. K tomu měření přes Meta Pixel a Conversions API.",
        "faq_title": "Časté otázky ke správě Meta Ads",
        "cta_title": "Zasekl se vám výkon na Metě?",
        "cta_text": "Napište mi, co se děje. Na úvodní konzultaci, asi 30 minut a zdarma, projdeme účet, kreativu a měření a řekneme si, kde je úzké hrdlo.",
        "form_placeholder": "Napište mi, jaký máte měsíční rozpočet na Metě a kde cítíte, že se to zaseklo...",
        "related": ["sprava-google-ads", "ppc-pro-eshopy", "ppc-audit"],
        "sections": [
            {
                "h2": "Co ve správě Meta Ads dostanete",
                "html": """
<h3>Struktura účtu a kampaně</h3>
<ul>
  <li><strong>Katalogové a dynamické remarketingové kampaně</strong> nad produktovým feedem. U e-shopu je to obvykle nejvýkonnější část účtu, protože oslovuje lidi, kteří už produkt viděli.</li>
  <li><strong>Prospecting</strong> na nová publika. Broad targeting s dobrou kreativou dnes většinou poráží úzce nastavené zájmové cílení, ale potřebuje dost konverzí, aby se měl algoritmus z čeho učit.</li>
  <li><strong>Konsolidace sestav</strong> místo dvaceti malých. Rozdrobený účet znamená, že se každá sestava učí zvlášť a žádná se nenaučí nic.</li>
  <li><strong>Lead kampaně pro B2B</strong> včetně formulářů přímo v Metě a jejich napojení dál, aby leady nekončily v exportu, na který se zapomene.</li>
</ul>
<h3>Kreativa, protože ta rozhoduje</h3>
<ul>
  <li>Obměna kreativy v pravidelném cyklu. Únava kreativy je nejčastější důvod, proč kampaň, která měsíc fungovala, najednou zdraží.</li>
  <li>Testování formátů: video, statika, karusel, kolekce. Každý formát mluví k jiné fázi rozhodování.</li>
  <li>Testování úhlů, ne jen barev tlačítka. Jiný benefit, jiná námitka, jiná cílovka. Rozdíly ve výkonu jsou tady řádově větší než u drobných úprav.</li>
</ul>
<h3>Měření, které dnes rozhoduje o výsledku</h3>
<ul>
  <li><strong>Conversions API</strong> vedle pixelu. Bez server-side měření Meta po změnách v prohlížečích a na iOS ztrácí velkou část konverzí a algoritmus se učí z neúplných dat.</li>
  <li>Kontrola deduplikace, aby se jedna objednávka nepočítala dvakrát.</li>
  <li>Porovnání toho, co si Meta připisuje, s tím, co ukazuje váš e-shop. Rozdíl bývá velký a je potřeba ho znát, než se podle něj rozdělí rozpočet.</li>
</ul>
""",
            },
            {
                "h2": "Jak škáluju výkon, když se kampaň zasekne",
                "class": "bg-light",
                "html": """
<p>Zaseknutý výkon má na Metě obvykle jednu ze tří příčin. Postupuju v tomhle pořadí, protože nasypat víc peněz do vyčerpané kreativy jen zdraží stejný výsledek.</p>
<ol class="steps">
  <li><strong>Vyčerpaná kreativa</strong>
    <p>Frekvence roste, CTR klesá, cena za výsledek jde nahoru. Řešení je nová kreativa, ne vyšší rozpočet. Tady se dá zlepšení dosáhnout nejrychleji.</p></li>
  <li><strong>Vyčerpané publikum</strong>
    <p>Kampaň už oslovila prakticky všechny, kdo dávají smysl. Řešení je rozšíření do šířky: nová publika, nové trhy, nové formáty umístění.</p></li>
  <li><strong>Rozbité měření</strong>
    <p>Algoritmus dostává neúplný nebo zdvojený signál a optimalizuje na špatný cíl. Dokud tohle neseděší, každá další změna jen mění, jakým směrem se plýtvá.</p></li>
</ol>
<p>Samotné škálování pak vedu dvěma směry. Do šířky přes nová publika a trhy, do hloubky přes obměnu kreativy a konsolidaci sestav. Rozpočet zvedám postupně, ne skokově, protože velký skok resetuje učící fázi. A každý krok se posuzuje na tom, kolik objednávek reálně přibylo, ne kolik si Meta připsala.</p>
""",
            },
            {
                "h2": "Proč Meta a Google patří k sobě",
                "html": """
<p>Nejčastější drahá chyba, kterou v účtech vidím, není špatné nastavení kampaně. Je to hodnocení kanálů odděleně.</p>
<p>Meta i Google si běžně připisují stejnou objednávku. Když se pak sečtou obraty z obou rozhraní, vyjde víc, než kolik e-shop reálně prodal. Rozpočet se rozdělí podle nafouknutých čísel a peníze tečou tam, kde je lepší atribuce, ne kde je lepší přínos.</p>
<p>Proto vedu Google Ads, Sklik, Meta Ads i zbožové srovnávače jako jednu strategii. Meta typicky vytváří poptávku, Google a srovnávače ji sbírají. Hodnotit sběrač podle stejného metru jako tvůrce poptávky vede k tomu, že se postupně vypne to, co celý systém živí.</p>
<p>Pokud tohle řešíte, začněte <a href="/ppc-audit/">auditem PPC</a>, kde se porovnávají data napříč kanály, nebo se podívejte na <a href="/sprava-google-ads/">správu Google Ads</a>.</p>
""",
            },
        ],
        "faq": [
            ("Kolik kreativ je potřeba měsíčně, aby účet nezdegeneroval?",
             "Univerzální číslo neexistuje, protože záleží na rozpočtu a velikosti publika. Platí ale jednoduché pravidlo: čím rychleji roste frekvence, tím rychleji potřebujete novou kreativu. U menších účtů stačí několik nových konceptů měsíčně, u větších je to průběžný proces. Důležitější než počet je rozmanitost úhlů, protože deset variant téže myšlenky se vyčerpá stejně rychle jako jedna."),
            ("Potřebuju Conversions API, když mi funguje pixel?",
             "Ano, a čím dál víc. Pixel běží v prohlížeči, takže ho blokuje část rozšíření, nastavení soukromí i systémová omezení. Conversions API posílá událost ze serveru, takže dorazí i tam, kde pixel selže. Bez něj se algoritmus učí z neúplného vzorku a vy zároveň v rozhraní vidíte méně konverzí, než kolik jich reálně bylo. Nasazení řeším včetně deduplikace, aby se událost nezapočítala dvakrát."),
            ("Zvládne Meta i B2B, nebo je to jen pro e-shopy?",
             "Zvládne, ale jinak. U B2B nejde o okamžitý nákup, ale o lead a jeho kvalitu. To znamená pracovat s formuláři přímo v Metě nebo na webu, hlídat, jestli leady dávají obchodně smysl, a posílat zpátky signál o kvalitě, ne jen o počtu. Bez toho se algoritmus naučí přivádět nejlevnější leady, což u B2B obvykle znamená ty nejhorší."),
            ("Jak poznám, že mi Meta reálně přidává objednávky?",
             "Podle toho, co se stane s celkovými tržbami, ne podle čísla v rozhraní Mety. Nejjednodušší praktický test je řízené vypnutí nebo výrazné omezení kampaní na definované období a sledování dopadu na celkový obrat a na podíl přímých a brandových vstupů. Není to laboratorně čisté, ale je to nesrovnatelně blíž pravdě než sečíst dva reporty a doufat."),
            ("Řešíte i produkci kreativy, nebo jen nastavení kampaní?",
             "Nastavení, strategii a zadání kreativy dělám. Samotnou produkci videí a grafiky obvykle dodává klientský tým nebo kreativec, se kterým spolupracujeme. Klíčové je, aby zadání vycházelo z dat o tom, co v účtu funguje, ne z pocitu. To zadání připravuju."),
        ],
    },
    # ══════════════════════════════════════════════════════════════════════
    {
        "slug": "ppc-pro-eshopy",
        "nav_label": "PPC pro e-shopy",
        "teaser": "Feedy, srovnávače a propojení kanálů",
        "crumb": "PPC pro e-shopy",
        "title": "PPC pro e-shopy: feedy, srovnávače a ROAS | Pavel Vognárek",
        "description": "PPC pro e-shopy: produktové feedy, Google Shopping, Heureka, Zboží.cz, katalog v Metě a optimalizace na marži místo na obrat. 250 mil. Kč v kampaních, ROAS 4,3.",
        "service_name": "PPC pro e-shopy a správa produktových feedů",
        "service_type": "Výkonnostní marketing pro e-shopy",
        "area": ["Česká republika", "Slovensko"],
        "h1": "PPC pro e-shopy<br><span>od feedu po propojení kanálů</span>",
        "lead": "U e-shopu se výsledek často láme spíš na kvalitě produktového feedu než na nastavení kampaně. Řeším proto obojí: Google Merchant Center, Heureku, Zboží.cz, Favi, Biano a katalog v Metě zároveň s kampaněmi v Google Ads, Skliku a Metě, aby všechny kanály jely z jednoho čistého zdroje dat.",
        "faq_title": "Časté otázky k PPC pro e-shopy",
        "cta_title": "Podíváme se na váš feed a účty",
        "cta_text": "Napište mi, na jaké platformě e-shop běží a kde vám to nesedí. Úvodní konzultace trvá asi 30 minut a je zdarma.",
        "form_placeholder": "Napište mi, na jaké platformě e-shop běží, kolik má produktů a co potřebujete řešit...",
        "related": ["sprava-google-ads", "sprava-meta-ads", "ppc-audit"],
        "sections": [
            {
                "h2": "Feed je základ, kampaň je až druhá",
                "html": """
<p>Produktový feed rozhoduje o tom, na jaké dotazy se produkt vůbec ukáže. Můžete mít perfektně nastavenou Shopping kampaň, ale pokud má produkt název podle interního kódu a chybí mu velikost nebo značka, do relevantních aukcí se prostě nedostane.</p>
<h3>Co ve feedu řeším</h3>
<ul>
  <li><strong>Názvy a popisky produktů</strong> podle toho, co lidé reálně hledají, ne podle toho, jak se produkt jmenuje ve skladovém systému. U produktů bez provozu to bývá jediná změna, která je rozhýbe.</li>
  <li><strong>Chybějící atributy:</strong> GTIN, značka, velikost, barva, materiál, stav. Bez nich Merchant Center část produktů buď zamítne, nebo zařadí špatně.</li>
  <li><strong>Kategorizace</strong> do stromu Google i do kategorií srovnávačů. Špatná kategorie znamená špatnou konkurenci a špatnou cenu za proklik.</li>
  <li><strong>Vylučování</strong> neprodejných, nedostupných a ztrátových položek, aby se rozpočet neutápěl v tom, co stejně nedorazí do košíku.</li>
  <li><strong>Pravidla v Mergadu</strong> pro úpravy, které nejde nebo se nevyplatí dělat přímo v e-shopu.</li>
</ul>
<h3>Kam feed napojuji</h3>
<ul>
  <li>Google Merchant Center pro Shopping a Performance Max</li>
  <li>Heureka.cz a Heureka.sk, Zboží.cz</li>
  <li>Favi a Biano u nábytku a bydlení</li>
  <li>Katalog v Metě pro dynamický remarketing a Advantage+ kampaně</li>
</ul>
<p>Jeden čistý zdroj dat pro všechny kanály znamená, že oprava se dělá jednou a projeví se všude.</p>
""",
            },
            {
                "h2": "Optimalizace na marži, ne na obrat",
                "class": "bg-light",
                "html": """
<p>ROAS bez znalosti marže je hezké číslo do reportu. Dva produkty se stejným ROAS mohou mít úplně jiný přínos: u jednoho zůstane po odečtení nákupní ceny, dopravy a vratek slušný zisk, u druhého nezůstane nic.</p>
<p>Proto se v prvním kroku ptám na věci, které se v běžné správě kampaní neřeší:</p>
<ul>
  <li>Jakou marži má která kategorie a které produkty jsou reálně ztrátové po dopravě.</li>
  <li>Jaká je míra vratek. U módy dokáže vratkovost obrátit pořadí nejvýnosnějších kampaní.</li>
  <li>Jaká je hodnota opakovaného nákupu. U spotřebního zboží se vyplatí platit za prvního zákazníka víc, než dovolí jednorázový ROAS.</li>
</ul>
<p>Z toho pak vzniká rozdělení produktů v Shopping a Performance Max kampaních, protože právě tam se rozhoduje, kam poteče většina rozpočtu.</p>
""",
            },
            {
                "h2": "Kanály, které u e-shopu dávají smysl",
                "html": """
<div class="cards">
  <div class="card">
    <div class="card-num">01</div>
    <h3>Google Ads</h3>
    <p>Search, Shopping a Performance Max. Sbírá existující poptávku a u většiny e-shopů tvoří páteř výkonu. <a href="/sprava-google-ads/">Více o správě Google Ads</a>.</p>
  </div>
  <div class="card">
    <div class="card-num">02</div>
    <h3>Sklik</h3>
    <p>Jiná aukce a jiné publikum než Google. Často se vyplatí i tam, kde je Google už nasycený. Vítěz Sklik výzvy Black Friday 2025.</p>
  </div>
  <div class="card">
    <div class="card-num">03</div>
    <h3>Meta Ads</h3>
    <p>Vytváří poptávku a drží remarketing nad katalogem. <a href="/sprava-meta-ads/">Více o správě Meta Ads</a>.</p>
  </div>
  <div class="card">
    <div class="card-num">04</div>
    <h3>Zbožové srovnávače</h3>
    <p>Heureka, Zboží.cz, Favi, Biano. Vysoký nákupní záměr, ale výkon stojí a padá na kvalitě feedu a na ceně.</p>
  </div>
</div>
<p style="margin-top:22px">Všechny čtyři vedu jako jednu strategii. Bez toho se stane, že si dva kanály přiznávají stejnou objednávku a rozpočet se rozděluje podle nafouknutých čísel.</p>
""",
            },
        ],
        "faq": [
            ("Mám produkty, které nemají skoro žádné zobrazení. Čím to je?",
             "Typicky názvem. Pokud se produkt jmenuje podle interního kódu nebo příliš obecně, nespáruje se s tím, co lidé hledají, a do aukcí se nedostane. Druhá častá příčina jsou chybějící atributy, hlavně GTIN a značka, kvůli kterým Merchant Center produkt zařadí špatně. Řeším to tak, že se podívám na reálné vyhledávací dotazy, které k dané kategorii chodí, a podle nich přepíšu názvy na vzorku produktů. Pokud se vzorek rozhýbe, aplikuje se to plošně."),
            ("Na jaké e-shopové platformě umíte pracovat?",
             "Platforma není překážka, protože pracuji s exportem feedu, ne s administrací e-shopu. Shoptet, WooCommerce, Shopify, Upgates i vlastní řešení mají všechny nějaký XML nebo CSV výstup, a co v něm chybí, se dá doplnit pravidly v Mergadu. Tam, kde jde úprava udělat rovnou v e-shopu, je to lepší, protože se projeví i mimo reklamu."),
            ("Vyplatí se Heureka, když si účtuje provizi z objednávky?",
             "U hodně e-shopů ano, protože přivádí lidi těsně před nákupem. Rozhoduje ale marže a to, jestli soutěžíte hlavně cenou. Pokud jste v kategorii nejdražší a nemáte jiný důvod, proč u vás nakoupit, srovnávač vám ukáže konkurenci a zaplatíte za proklik, který nekonvertuje. Proto se do toho nejdřív dívám na data o marži a teprve pak nastavuji, které kategorie do srovnávače pustit."),
            ("Umíte pracovat s XML feedem pro slovenský trh?",
             "Ano. Pro Slovensko se feed lokalizuje: měna, dostupnost, doprava, texty a napojení na Heureka.sk. Nestačí přepnout jazyk, protože kategorie i zvyky ve vyhledávání se liší. Právě proto tam bývá prostor získat výhodu proti konkurenci, která nasadila český feed beze změny."),
            ("Kolik produktů musí e-shop mít, aby to dávalo smysl?",
             "Neexistuje spodní hranice v počtu produktů, rozhoduje objem poptávky a marže. Viděl jsem dobře fungující účty s několika desítkami produktů i účty s tisíci položkami, kde se rozpočet utápěl v položkách bez poptávky. Důležitější než počet je, jestli má katalog jasné bestsellery, na které jde soustředit rozpočet, a jestli sedí data o dostupnosti."),
        ],
    },
    # ══════════════════════════════════════════════════════════════════════
    {
        "slug": "ppc-audit",
        "nav_label": "Audit PPC",
        "teaser": "Kde se utrácí zbytečně a kde leží potenciál",
        "crumb": "Audit PPC",
        "title": "Audit PPC kampaní a měření | Pavel Vognárek",
        "description": "Audit PPC účtu, měření a produktového feedu s konkrétním plánem na výstupu. Google Ads, Sklik, Meta Ads a srovnávače. Trvá 1 až 2 týdny, konzultace zdarma.",
        "service_name": "Audit PPC kampaní",
        "service_type": "Audit reklamních účtů a měření",
        "area": ["Česká republika", "Slovensko"],
        "h1": "Audit PPC kampaní<br><span>s konkrétním plánem, ne seznamem doporučení</span>",
        "lead": "Audit projde Google Ads, Sklik, Meta Ads, měření v GA4 a produktový feed a odpoví na dvě otázky: kde se utrácí zbytečně a kde leží nevyužitý potenciál. Výstupem je seřazený plán s odhadem dopadu, ne obecný seznam doporučení, který si můžete přečíst v každém blogu.",
        "faq_title": "Časté otázky k auditu PPC",
        "cta_title": "Chcete vědět, co se ve vašem účtu opravdu děje?",
        "cta_text": "Úvodní konzultace trvá asi 30 minut a je zdarma. Řekneme si, co vás trápí, a já odhadnu, jestli má audit u vás smysl.",
        "form_placeholder": "Napište mi, jaké kanály používáte a co vás vede k tomu nechat si udělat audit...",
        "related": ["sprava-google-ads", "sprava-meta-ads", "ppc-pro-eshopy"],
        "sections": [
            {
                "h2": "Co audit prochází",
                "html": """
<h3>Měření jako první, ne jako poslední</h3>
<p>Audit vždycky začíná měřením. Optimalizovat kampaně na rozbitá data znamená utíkat špatným směrem rychleji. Kontroluje se:</p>
<ul>
  <li>Které konverze jsou primární a které jen mikrokonverze, a jestli se obojí nesčítá do jednoho čísla. Když má kampaň v konverzních cílech zapnutý nákup i přidání do košíku zároveň, sloupec Konverze míchá obojí a všechny metriky odvozené od něj jsou zkreslené.</li>
  <li>Jestli hodnota konverze odpovídá skutečným tržbám, nebo se počítá včetně DPH a dopravy tam, kde by neměla.</li>
  <li>Nasazení Conversions API v Metě a deduplikace proti pixelu.</li>
  <li>Rozdíl mezi tím, co si přiznávají reklamní systémy, a tím, co ukazuje e-shop nebo CRM.</li>
</ul>
<h3>Účty a kampaně</h3>
<ul>
  <li>Struktura kampaní podle záměru: brand, generické dotazy, konkurence, dlouhý ocas.</li>
  <li>Reálné vyhledávací dotazy a chybějící negativní klíčová slova.</li>
  <li>Bidding strategie a jestli mají dost konverzních dat, aby fungovaly.</li>
  <li>Rozdělení produktů v Shopping a Performance Max podle marže a obrátky.</li>
  <li>Kreativa v Metě: frekvence, únava, rozmanitost úhlů.</li>
  <li>Překryv kanálů a dvojí přiznávání stejné objednávky.</li>
</ul>
<h3>Produktový feed</h3>
<ul>
  <li>Kvalita a úplnost dat v Merchant Centru, zamítnuté položky a jejich důvody.</li>
  <li>Názvy produktů proti reálným vyhledávacím dotazům.</li>
  <li>Kategorizace a chybějící atributy.</li>
</ul>
""",
            },
            {
                "h2": "Jak audit probíhá",
                "class": "bg-light",
                "html": """
<ol class="steps">
  <li><strong>Úvodní konzultace, asi 30 minut, zdarma</strong>
    <p>Projdeme business, cíle a to, co vás k auditu vede. Občas z toho vyjde, že audit nepotřebujete a stačí jedna konkrétní změna. To vám řeknu rovnou.</p></li>
  <li><strong>Přístupy</strong>
    <p>Potřebuju čtecí přístup do reklamních účtů, do GA4, do Merchant Centra a ideálně data o objednávkách. Bez dat o objednávkách nejde odlišit dobrý ROAS od dobře vypadajícího ROAS.</p></li>
  <li><strong>Analýza, 1 až 2 týdny</strong>
    <p>Průchod účty, měřením a feedem. Nálezy se rovnou třídí podle toho, kolik peněz je v sázce a jak náročná je oprava.</p></li>
  <li><strong>Prezentace a plán</strong>
    <p>Projdeme nálezy spolu, ne mailem s přílohou. Na konci máte seřazený plán: co opravit hned, co ve druhé vlně a čeho se nedotýkat.</p></li>
  <li><strong>Co dál</strong>
    <p>Buď plán nasadím a pokračujeme dlouhodobou správou, nebo ho předáme vašemu týmu či stávající agentuře. Obojí je v pořádku, audit není nástroj, jak si vás přivázat.</p></li>
</ol>
""",
            },
            {
                "h2": "Kdy má audit smysl a kdy je to zbytečný výdaj",
                "html": """
<div class="cards">
  <div class="card">
    <div class="card-num">ANO</div>
    <h3>Utrácíte víc a nerostete</h3>
    <p>Nejjasnější signál. Obvykle za tím stojí měření nebo překryv kanálů, ne špatně napsaná reklama.</p>
  </div>
  <div class="card">
    <div class="card-num">ANO</div>
    <h3>Zvažujete změnu agentury</h3>
    <p>Audit vám dá nezávislý podklad k rozhodnutí a zároveň zadání pro toho, kdo přijde po ní.</p>
  </div>
  <div class="card">
    <div class="card-num">ANO</div>
    <h3>Chystáte větší investici</h3>
    <p>Před zvýšením rozpočtu nebo vstupem na Slovensko se vyplatí vědět, jestli základ unese víc.</p>
  </div>
  <div class="card">
    <div class="card-num">NE</div>
    <h3>Účet běží pár týdnů</h3>
    <p>Není z čeho číst. Chytré bidding strategie se učí dva až tři týdny a poctivé vyhodnocení dává smysl až po čtyřech až šesti.</p>
  </div>
  <div class="card">
    <div class="card-num">NE</div>
    <h3>Rozhodnutí už padlo</h3>
    <p>Pokud audit potřebujete jen jako potvrzení něčeho, co se stejně udělá, je to vyhozený čas i peníze.</p>
  </div>
  <div class="card">
    <div class="card-num">NE</div>
    <h3>Bez přístupu k datům</h3>
    <p>Když se nedostanu do měření a k datům o objednávkách, výstupem bude odhad, ne audit.</p>
  </div>
</div>
""",
            },
        ],
        "faq": [
            ("Jak dlouho audit trvá a co k němu potřebujete?",
             "Samotná analýza trvá jeden až dva týdny podle velikosti účtu. Potřebuju čtecí přístup do reklamních účtů, do GA4, do Google Merchant Centra a pokud jde o e-shop, také data o objednávkách a ideálně o marži. Přístupy stačí čtecí, nic v účtu během auditu neměním."),
            ("Co konkrétně dostanu na konci?",
             "Seřazený seznam nálezů podle toho, kolik peněz je v sázce a jak náročná je oprava, s vysvětlením u každého, proč je to problém a co s tím. K tomu plán rozdělený na to, co udělat hned, co ve druhé vlně a čeho se nedotýkat. Nálezy procházíme spolu na hovoru, ne mailem s přílohou, protože polovina hodnoty auditu je v tom dialogu."),
            ("Musím po auditu pokračovat ve spolupráci?",
             "Ne. Audit je uzavřená služba a klidně skončí předáním plánu vašemu týmu nebo stávající agentuře. Považuju to za normální výsledek, ne za neúspěch. Pokud dává smysl pokračovat správou, řekneme si to, ale není to podmínka a nedělám audit tak, aby k tomu vedl."),
            ("Auditujete i účty, které spravuje jiná agentura?",
             "Ano, a je to dost častý důvod, proč si audit lidé objednávají. Snažím se držet věcný tón: cílem je popsat stav účtu, ne najít viníka. Někdy z auditu vyjde, že agentura odvádí dobrou práci a problém je jinde, například v marži nebo v konkurenci. To je taky užitečný výsledek."),
            ("Řešíte v auditu i konkurenci a ceny?",
             "V rozsahu, který jde poctivě doložit z dostupných dat. To znamená podíl zobrazení, ztracený podíl kvůli rozpočtu a kvůli hodnocení, aukční přehledy a u e-shopů cenové srovnání ve srovnávačích. Nedělám odhady tržeb konkurence z nástrojů třetích stran, protože ta čísla bývají natolik nepřesná, že se podle nich nedá rozhodovat."),
        ],
    },
    # ══════════════════════════════════════════════════════════════════════
    {
        "slug": "ppc-specialista-brno",
        "nav_label": "PPC specialista Brno",
        "teaser": "Osobní spolupráce v Brně a okolí",
        "crumb": "PPC specialista Brno",
        "title": "PPC specialista Brno: Google Ads a Meta Ads | Pavel Vognárek",
        "description": "PPC specialista pro Brno a okolí. Google Ads, Sklik, Meta Ads a zbožové srovnávače pro e-shopy a B2B. Praxe z brněnských agentur ROIMARK a In Creative.",
        "service_name": "PPC specialista a Google Ads konzultant pro Brno",
        "service_type": "Správa PPC kampaní",
        "area": ["Česká republika"],
        "h1": "PPC specialista pro Brno<br><span>a okolí</span>",
        "lead": "Praxi jsem sbíral jako Team Leader PPC v brněnských agenturách ROIMARK a In Creative a dnes spolupracuji s firmami z Brna napřímo. Spravuji Google Ads, Sklik, Meta Ads a zbožové srovnávače. Osobní schůzka v Brně není problém, ale spolupráci vedu z větší části online.",
        "faq_title": "Časté otázky ke spolupráci v Brně",
        "cta_title": "Sejdeme se v Brně, nebo online",
        "cta_text": "Úvodní konzultace trvá asi 30 minut a je zdarma. Můžeme ji vzít přes Google Meet, nebo se potkat osobně v Brně.",
        "form_placeholder": "Napište mi, co řešíte a jestli preferujete osobní schůzku v Brně, nebo online...",
        "related": ["sprava-google-ads", "ppc-audit", "ppc-pro-eshopy"],
        "sections": [
            {
                "h2": "Co pro brněnské firmy dělám",
                "html": """
<p>Sídlím ve Velkých Bílovicích u Břeclavi, což je od Brna asi 45 minut autem. Do Brna jezdím pravidelně a osobní schůzka je normální součást spolupráce, hlavně na začátku, kdy se člověk potřebuje poznat.</p>
<ul>
  <li><strong><a href="/sprava-google-ads/">Správa Google Ads</a> a Sklik:</strong> Search, Shopping a Performance Max pro e-shopy i B2B firmy.</li>
  <li><strong><a href="/sprava-meta-ads/">Správa Meta Ads</a>:</strong> Facebook a Instagram, katalogové kampaně, prospecting a kreativa.</li>
  <li><strong><a href="/ppc-pro-eshopy/">Produktové feedy a srovnávače</a>:</strong> Merchant Center, Heureka, Zboží.cz, Favi, Biano.</li>
  <li><strong><a href="/ppc-audit/">Audit PPC</a>:</strong> nezávislý pohled na účet, měření a feed, včetně situace, kdy zvažujete změnu agentury.</li>
</ul>
<p>Přes 250 milionů Kč proinvestovaných v kampaních a průměrný ROAS 4,3 napříč spravovanými účty. Vítěz Sklik výzvy za nejlepší Black Friday strategii 2025.</p>
""",
            },
            {
                "h2": "Proč konzultant a ne agentura",
                "class": "bg-light",
                "html": """
<p>Brno má agentur dost a řada z nich odvádí dobrou práci. Přesto je pár situací, kdy dává větší smysl jeden člověk.</p>
<ul>
  <li><strong>Mluvíte přímo s tím, kdo v účtu pracuje.</strong> Odpadá vrstva account managementu, která informace předává oběma směry. Zkušenost z agenturní strany mi dovoluje říct, že se tím ztrácí víc, než se čeká.</li>
  <li><strong>Nejste v pořadí za většími klienty.</strong> V agentuře se kapacita přirozeně stěhuje k největším účtům. U konzultanta je dohodnutý rozsah dohodnutý rozsah.</li>
  <li><strong>Kanály neřeší tři různí lidé.</strong> Google, Meta a srovnávače vede jeden člověk, takže se pozná, kdy si dva kanály přiznávají stejnou objednávku.</li>
</ul>
<p>Zároveň je férové říct, kdy je lepší agentura: když potřebujete kreativní produkci, velký objem obsahu, nepřetržité pokrytí a tým, který se zastoupí. Tohle sám nepokryju a nebudu předstírat, že ano.</p>
""",
            },
            {
                "h2": "Odkud jsou moji klienti",
                "html": """
<p>Osobně jsem doma na jižní Moravě: Brno, Břeclav, Velké Bílovice, Hodonín, Mikulov, Znojmo a Kyjov. Online spolupracuji s firmami po celé České republice včetně Prahy a také na Slovensku, kde díky blízkosti jazyka nepotřebujeme tlumočení ani překlady.</p>
<p>Praxi mám z brněnských agentur ROIMARK a In Creative, kde jsem pracoval na značkách jako Biju.cz, Doppler, Vinotrh, Lomax, Izomat a Fitmin. Přehled najdete <a href="/#reference">v referencích</a>.</p>
<p>Pokud jste z Břeclavska nebo z okolí Velkých Bílovic, platí to samé, jen je to blíž. Konkurence v PPC je tam navíc slabší než v Brně, takže dobře nastavené Google Ads a srovnávače dokážou malou firmu dostat před větší.</p>
<h3>Co brněnské firmy řeší nejčastěji</h3>
<p>Z toho, co vidím v účtech, se opakují tři situace. První je e-shop, který má slušný obrat, ale nikdo mu neřekl, kolik z něj reálně zbyde po marži, dopravě a vratkách. Druhá je B2B firma, která měří odeslání formuláře, ale ne to, kolik z těch poptávek skončí obchodem, takže se kampaně optimalizují na počet leadů místo na jejich kvalitu. Třetí je firma, která běží na Googlu i na Metě, ale kanály vyhodnocuje odděleně, takže si obě rozhraní přiznávají stejnou objednávku a rozpočet se dělí podle nafouknutých čísel.</p>
<p>Žádná z těch tří věcí se neopraví lepším textem reklamy. Proto u nových spoluprací začínám <a href="/ppc-audit/">auditem</a>, kde se nejdřív srovná měření a teprve pak se sahá na kampaně.</p>
""",
            },
        ],
        "faq": [
            ("Jak vypadá PPC konkurence v Brně oproti menším městům?",
             "V Brně je konkurence v aukcích znatelně vyšší než na Břeclavsku nebo Hodonínsku, hlavně u služeb a u kategorií, kde působí i pražské firmy. Prakticky to znamená vyšší cenu za proklik a menší prostor pro chyby v měření, protože se rychleji projeví. Na druhou stranu je v Brně větší objem poptávky, takže se dřív nasbírá dost konverzí na to, aby chytré bidding strategie fungovaly. U brněnských účtů proto obvykle věnuju víc času struktuře a negativním klíčovým slovům, aby rozpočet netekl do dotazů, které nikdy nekonvertují."),
            ("Musíme se potkávat osobně, nebo stačí online?",
             "Stačí online a většina spolupráce tak i probíhá, přes Google Meet, sdílené dashboardy a pravidelné reporty. Osobní schůzka v Brně je ale možná kdykoliv a na začátku ji spíš doporučuju, protože se u ní vyjasní věci, které se přes hovor řeší hůř. Rozhodně to není podmínka a nikdy jsem nezažil, že by vzdálenost byla to, co spolupráci zabrzdí."),
            ("Jak rychle se dostanu na řadu?",
             "Beru omezený počet klientů právě proto, aby nevznikala fronta. Konkrétní termín ale závisí na tom, kolik toho zrovna běží, takže nejrychlejší odpověď dostanete, když napíšete. Úvodní konzultaci obvykle zvládnu domluvit v řádu dní, nasazení pak navazuje podle rozsahu auditu."),
            ("Pracoval jste v brněnských agenturách. Není to konflikt zájmů?",
             "Ne, spolupráce s ROIMARKem pokračuje v roli konzultanta a je to na webu uvedené otevřeně. Konflikt by nastal, kdybych vedl dva přímo konkurenční e-shopy ve stejné kategorii, a to nedělám. Pokud by k takové situaci mělo dojít, řeknu to dřív, než začneme."),
            ("Děláte i školení nebo konzultace pro interní tým?",
             "Ano. U firem, které mají vlastního člověka na PPC, dává často větší smysl konzultační režim než plná správa: pravidelné konzultace, revize účtu a nastavení procesů, zatímco denní práci dělá váš tým. Řekneme si to na úvodní konzultaci podle toho, jak je tým silný a co reálně potřebuje."),
        ],
    },
]
