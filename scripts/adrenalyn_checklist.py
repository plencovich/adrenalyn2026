from __future__ import annotations

import json
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal, TypeAlias


CardPosition: TypeAlias = Literal[
    "goalkeeper",
    "defender",
    "midfielder",
    "forward",
    "fan_favourite",
    "icon",
]


@dataclass(frozen=True)
class Card:
    number: int
    group: str
    name: str
    position: CardPosition | None

    def as_json(self) -> dict[str, Any]:
        return {
            "number": self.number,
            "name": self.name,
            "position": self.position,
        }


ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT_DIR / "data" / "figuritas.json"

COLLECTION = {
    "name": "FIFA World Cup 2026 Adrenalyn XL",
    "publisher": "Panini",
    "total_cards": 620,
    "numbering": "global",
}

POSITION_BY_CODE: dict[str, CardPosition | None] = {
    "": None,
    "GK": "goalkeeper",
    "DF": "defender",
    "MF": "midfielder",
    "FW": "forward",
    "FF": "fan_favourite",
    "IC": "icon",
}

RANGES: list[tuple[str, int, int]] = [
    ("GOLDEN_BALLERS", 1, 9),
    ("ALG", 10, 21),
    ("ARG", 22, 33),
    ("AUS", 34, 45),
    ("AUT", 46, 57),
    ("BEL", 58, 69),
    ("BRA", 70, 81),
    ("CAN", 82, 93),
    ("CPV", 94, 105),
    ("COL", 106, 117),
    ("CRO", 118, 129),
    ("CUW", 130, 141),
    ("ECU", 142, 153),
    ("EGY", 154, 165),
    ("ENG", 166, 177),
    ("FRA", 178, 189),
    ("GER", 190, 201),
    ("GHA", 202, 213),
    ("HAI", 214, 225),
    ("IRN", 226, 237),
    ("CIV", 238, 249),
    ("JPN", 250, 261),
    ("JOR", 262, 273),
    ("KOR", 274, 285),
    ("MEX", 286, 297),
    ("MAR", 298, 309),
    ("NED", 310, 321),
    ("NZL", 322, 333),
    ("NOR", 334, 345),
    ("PAN", 346, 357),
    ("PAR", 358, 369),
    ("POR", 370, 381),
    ("QAT", 382, 393),
    ("KSA", 394, 405),
    ("SCO", 406, 417),
    ("SEN", 418, 429),
    ("RSA", 430, 441),
    ("ESP", 442, 453),
    ("SUI", 454, 465),
    ("TUN", 466, 477),
    ("USA", 478, 489),
    ("URU", 490, 501),
    ("UZB", 502, 513),
    ("CONTENDERS", 514, 519),
    ("DEN", 520, 524),
    ("ITA", 525, 529),
    ("JAM", 530, 534),
    ("POL", 535, 539),
    ("SWE", 540, 544),
    ("TUR", 545, 549),
    ("TOP_KEEPERS", 550, 558),
    ("DEFENSIVE_ROCKS", 559, 567),
    ("MIDFIELD_MAESTROS", 568, 585),
    ("GOAL_MACHINES", 586, 607),
    ("MASTER_ROOKIES", 608, 620),
]

SPECIAL_KEYS = {
    "GOLDEN_BALLERS",
    "CONTENDERS",
    "TOP_KEEPERS",
    "DEFENSIVE_ROCKS",
    "MIDFIELD_MAESTROS",
    "GOAL_MACHINES",
    "MASTER_ROOKIES",
}
GROUP_ORDER = [group for group, _, _ in RANGES]
COUNTRY_KEYS = set(GROUP_ORDER) - SPECIAL_KEYS
RANGE_BY_GROUP = {group: (start, end) for group, start, end in RANGES}
GROUP_BY_NUMBER = {
    number: group
    for group, start, end in RANGES
    for number in range(start, end + 1)
}
ALLOWED_POSITIONS = {value for value in POSITION_BY_CODE.values() if value is not None}

# Source transcribed from fifa-wc-tcg-26_checklist-pdf-international-lr.pdf.
# The PDF is image-based; this is the reviewed structured source used at build time.
# The visible PDF also lists 621-630, but this stage is intentionally constrained to
# the user-requested official ranges 1-620.
SOURCE_ROWS = """
1;GOLDEN_BALLERS;MESSI (ARG);FW
2;GOLDEN_BALLERS;VINÍCIUS JÚNIOR (BRA);FW
3;GOLDEN_BALLERS;SALAH (EGY);FW
4;GOLDEN_BALLERS;KANE (ENG);FW
5;GOLDEN_BALLERS;MBAPPÉ (FRA);FW
6;GOLDEN_BALLERS;SON (KOR);FW
7;GOLDEN_BALLERS;HAALAND (NOR);FW
8;GOLDEN_BALLERS;RONALDO (POR);FW
9;GOLDEN_BALLERS;YAMAL (ESP);FW
10;ALG;RAYAN AÏT-NOURI;FF
11;ALG;TEAM CREST;
12;ALG;RIYAD MAHREZ;IC
13;ALG;ALEXIS GUENDOUZ;GK
14;ALG;RAMY BENSEBAINI;DF
15;ALG;YOUCEF ATAL;DF
16;ALG;AÏSSA MANDI;DF
17;ALG;NABIL BENTALEB;MF
18;ALG;SAÏD BENRAHMA;FW
19;ALG;AMINE GOUIRI;FW
20;ALG;MOHAMED AMOURA;FW
21;ALG;BAGHDAD BOUNEDJAH;FW
22;ARG;JULIÁN ÁLVAREZ;FF
23;ARG;TEAM CREST;
24;ARG;LIONEL MESSI;IC
25;ARG;EMILIANO MARTÍNEZ;GK
26;ARG;NAHUEL MOLINA;DF
27;ARG;CRISTIAN ROMERO;DF
28;ARG;NICOLÁS OTAMENDI;DF
29;ARG;ENZO FERNÁNDEZ;MF
30;ARG;ALEXIS MAC ALLISTER;MF
31;ARG;RODRIGO DE PAUL;MF
32;ARG;GIULIANO SIMEONE;FW
33;ARG;LAUTARO MARTÍNEZ;FW
34;AUS;HARRY SOUTTAR;FF
35;AUS;TEAM CREST;
36;AUS;MATHEW RYAN;IC
37;AUS;ALESSANDRO CIRCATI;DF
38;AUS;JORDAN BOS;DF
39;AUS;LEWIS MILLER;DF
40;AUS;MILOS DEGENEK;DF
41;AUS;JACKSON IRVINE;MF
42;AUS;RILEY MCGREE;MF
43;AUS;AIDEN O'NEILL;MF
44;AUS;CONNOR METCALFE;MF
45;AUS;CRAIG GOODWIN;FW
46;AUT;MARKO ARNAUTOVIĆ;FF
47;AUT;TEAM CREST;
48;AUT;DAVID ALABA;IC
49;AUT;ALEXANDER SCHLAGER;GK
50;AUT;KEVIN DANSO;DF
51;AUT;PHILIPP LIENHART;DF
52;AUT;KONRAD LAIMER;MF
53;AUT;NICOLAS SEIWALD;MF
54;AUT;MARCEL SABITZER;MF
55;AUT;FLORIAN GRILLITSCH;MF
56;AUT;CHRISTOPH BAUMGARTNER;FW
57;AUT;MICHAEL GREGORITSCH;FW
58;BEL;YOURI TIELEMANS;FF
59;BEL;TEAM CREST;
60;BEL;KEVIN DE BRUYNE;IC
61;BEL;THIBAUT COURTOIS;GK
62;BEL;ARTHUR THEATE;DF
63;BEL;TIMOTHY CASTAGNE;DF
64;BEL;MAXIM DE CUYPER;DF
65;BEL;AMADOU ONANA;MF
66;BEL;JÉRÉMY DOKU;FW
67;BEL;CHARLES DE KETELAERE;FW
68;BEL;LEANDRO TROSSARD;FW
69;BEL;ROMELU LUKAKU;FW
70;BRA;MARQUINHOS;FF
71;BRA;TEAM CREST;
72;BRA;VINÍCIUS JÚNIOR;IC
73;BRA;ALISSON;GK
74;BRA;DANILO;DF
75;BRA;ÉDER MILITÃO;DF
76;BRA;GABRIEL MAGALHÃES;DF
77;BRA;CASEMIRO;MF
78;BRA;BRUNO GUIMARÃES;MF
79;BRA;RODRYGO;FW
80;BRA;MATHEUS CUNHA;FW
81;BRA;RAPHINHA;FW
82;CAN;JONATHAN DAVID;FF
83;CAN;TEAM CREST;
84;CAN;ALPHONSO DAVIES;IC
85;CAN;DAYNE ST. CLAIR;GK
86;CAN;RICHIE LARYEA;DF
87;CAN;DEREK CORNELIUS;DF
88;CAN;STEPHEN EUSTÁQUIO;MF
89;CAN;ISMAËL KONÉ;MF
90;CAN;JONATHAN OSORIO;MF
91;CAN;JACOB SHAFFELBURG;FW
92;CAN;TAJON BUCHANAN;FW
93;CAN;CYLE LARIN;FW
94;CPV;VOZINHA;FF
95;CPV;TEAM CREST;
96;CPV;RYAN MENDES;IC
97;CPV;LOGAN COSTA;DF
98;CPV;PICO;DF
99;CPV;STEVEN MOREIRA;DF
100;CPV;JOÃO PAULO;MF
101;CPV;KEVIN PINA;MF
102;CPV;JAMIRO MONTEIRO;MF
103;CPV;YANNICK SEMEDO;MF
104;CPV;JOVANE CABRAL;FW
105;CPV;DAILON LIVRAMENTO;FW
106;COL;LUIS DÍAZ;FF
107;COL;TEAM CREST;
108;COL;JAMES RODRÍGUEZ;IC
109;COL;CAMILO VARGAS;GK
110;COL;DAVINSON SÁNCHEZ;DF
111;COL;YERRY MINA;DF
112;COL;DANIEL MUÑOZ;DF
113;COL;JEFFERSON LERMA;MF
114;COL;RICHARD RÍOS;MF
115;COL;JUAN FERNANDO QUINTERO;MF
116;COL;JHON ARIAS;FW
117;COL;LUIS SUÁREZ;FW
118;CRO;IVAN PERIŠIĆ;FF
119;CRO;TEAM CREST;
120;CRO;LUKA MODRIĆ;IC
121;CRO;DOMINIK LIVAKOVIĆ;GK
122;CRO;DUJE ĆALETA-CAR;DF
123;CRO;JOŠKO GVARDIOL;DF
124;CRO;JOSIP STANIŠIĆ;DF
125;CRO;MATEO KOVAČIĆ;MF
126;CRO;LOVRO MAJER;MF
127;CRO;MARIO PAŠALIĆ;MF
128;CRO;ANTE BUDIMIR;FW
129;CRO;ANDREJ KRAMARIĆ;FW
130;CUW;JURRIËN GAARI;FF
131;CUW;TEAM CREST;
132;CUW;LEANDRO BACUNA;IC
133;CUW;ELOY ROOM;GK
134;CUW;SHEREL FLORANUS;DF
135;CUW;ROSHON VAN EIJMA;DF
136;CUW;ARMANDO OBISPO;DF
137;CUW;LIVANO COMENENCIA;MF
138;CUW;JUNINHO BACUNA;MF
139;CUW;KENJI GORRÉ;FW
140;CUW;SONTJE HANSEN;FW
141;CUW;JEARL MARGARITHA;FW
142;ECU;MOISÉS CAICEDO;FF
143;ECU;TEAM CREST;
144;ECU;ENNER VALENCIA;IC
145;ECU;HERNÁN GALÍNDEZ;GK
146;ECU;PIERO HINCAPIÉ;DF
147;ECU;PERVIS ESTUPIÑÁN;DF
148;ECU;WILLIAN PACHO;DF
149;ECU;ÁNGELO PRECIADO;DF
150;ECU;JOEL ORDÓÑEZ;DF
151;ECU;ALAN FRANCO;MF
152;ECU;GONZALO PLATA;FW
153;ECU;KEVIN RODRÍGUEZ;FW
154;EGY;OMAR MARMOUSH;FF
155;EGY;TEAM CREST;
156;EGY;MOHAMED SALAH;IC
157;EGY;MOHAMED EL SHENAWY;GK
158;EGY;MOHAMED HANY;DF
159;EGY;MOHAMED ABDELMONEM;DF
160;EGY;RAMY RABIA;DF
161;EGY;MARWAN ATTIA;MF
162;EGY;ZIZO;MF
163;EGY;HAMDY FATHY;MF
164;EGY;MOSTAFA MOHAMED;FW
165;EGY;TRÉZÉGUET;FW
166;ENG;JUDE BELLINGHAM;FF
167;ENG;TEAM CREST;
168;ENG;HARRY KANE;IC
169;ENG;JORDAN PICKFORD;GK
170;ENG;REECE JAMES;DF
171;ENG;JOHN STONES;DF
172;ENG;DECLAN RICE;MF
173;ENG;JORDAN HENDERSON;MF
174;ENG;PHIL FODEN;MF
175;ENG;BUKAYO SAKA;FW
176;ENG;COLE PALMER;FW
177;ENG;MARCUS RASHFORD;FW
178;FRA;OUSMANE DEMBÉLÉ;FF
179;FRA;TEAM CREST;
180;FRA;KYLIAN MBAPPÉ;IC
181;FRA;MIKE MAIGNAN;GK
182;FRA;WILLIAM SALIBA;DF
183;FRA;JULES KOUNDÉ;DF
184;FRA;THÉO HERNÁNDEZ;DF
185;FRA;AURÉLIEN TCHOUAMÉNI;MF
186;FRA;EDUARDO CAMAVINGA;MF
187;FRA;BRADLEY BARCOLA;FW
188;FRA;MARCUS THURAM;FW
189;FRA;RANDAL KOLO MUANI;FW
190;GER;JAMAL MUSIALA;FF
191;GER;TEAM CREST;
192;GER;JOSHUA KIMMICH;IC
193;GER;MARC-ANDRÉ TER STEGEN;GK
194;GER;ANTONIO RÜDIGER;DF
195;GER;JONATHAN TAH;DF
196;GER;FELIX NMECHA;MF
197;GER;LEON GORETZKA;MF
198;GER;FLORIAN WIRTZ;MF
199;GER;SERGE GNABRY;MF
200;GER;KAI HAVERTZ;FW
201;GER;LEROY SANÉ;FW
202;GHA;THOMAS PARTEY;FF
203;GHA;TEAM CREST;
204;GHA;MOHAMMED KUDUS;IC
205;GHA;LAWRENCE ATI ZIGI;GK
206;GHA;ALIDU SEIDU;DF
207;GHA;ALEXANDER DJIKU;DF
208;GHA;GIDEON MENSAH;DF
209;GHA;CALEB YIRENKYI;DF
210;GHA;ABDUL ISSAHAKU FATAWU;MF
211;GHA;KAMALDEEN SULEMANA;FW
212;GHA;JORDAN AYEW;FW
213;GHA;ANTOINE SEMENYO;FW
214;HAI;FRANTZDY PIERROT;FF
215;HAI;TEAM CREST;
216;HAI;DUCKENS NAZON;IC
217;HAI;JOHNY PLACIDE;GK
218;HAI;RICARDO ADÉ;DF
219;HAI;CARLENS ARCUS;DF
220;HAI;HANNES DELCROIX;DF
221;HAI;LEVERTON PIERRE;MF
222;HAI;DANLEY JEAN JACQUES;MF
223;HAI;JEAN-RICNER BELLEGARDE;MF
224;HAI;RUBEN PROVIDENCE;FW
225;HAI;DON DEEDSON LOUICIUS;FW
226;IRN;MEHDI TAREMI;FF
227;IRN;TEAM CREST;
228;IRN;SARDAR AZMOUN;IC
229;IRN;ALIREZA BEIRANVAND;GK
230;IRN;SHOJA KHALILZADEH;DF
231;IRN;MILAD MOHAMMADI;DF
232;IRN;RAMIN REZAEIAN;DF
233;IRN;HOSSEIN KANAANI;DF
234;IRN;SAEID EZATOLAHI;MF
235;IRN;SAMAN GHODDOS;MF
236;IRN;MOHAMMAD MOHEBI;MF
237;IRN;ALIREZA JAHANBAKHSH;FW
238;CIV;FRANCK KESSIÉ;FF
239;CIV;TEAM CREST;
240;CIV;SÉBASTIEN HALLER;IC
241;CIV;YAHIA FOFANA;GK
242;CIV;GHISLAIN KONAN;DF
243;CIV;ODILON KOSSOUNOU;DF
244;CIV;EVAN N'DICKA;DF
245;CIV;WILFRIED SINGO;DF
246;CIV;IBRAHIM SANGARÉ;MF
247;CIV;NICOLAS PÉPÉ;FW
248;CIV;SIMON ADINGRA;FW
249;CIV;OUMAR DIAKITÉ;FW
250;JPN;TAKUMI MINAMINO;FF
251;JPN;TEAM CREST;
252;JPN;TAKEFUSA KUBO;IC
253;JPN;ZION SUZUKI;GK
254;JPN;TSUYOSHI WATANABE;DF
255;JPN;KAISHU SANO;MF
256;JPN;AO TANAKA;MF
257;JPN;DAICHI KAMADA;MF
258;JPN;RITSU DOAN;MF
259;JPN;KEITO NAKAMURA;MF
260;JPN;SHUTO MACHINO;FW
261;JPN;AYASE UEDA;FW
262;JOR;YAZAN AL-NAIMAT;FF
263;JOR;TEAM CREST;
264;JOR;MUSA AL-TAAMARI;IC
265;JOR;YAZEED ABULAILA;GK
266;JOR;MOHAMMAD ABUHASHISH;DF
267;JOR;YAZAN AL-ARAB;DF
268;JOR;ABDALLAH NASIB;DF
269;JOR;IBRAHIM SAADEH;MF
270;JOR;NIZAR AL-RASHDAN;MF
271;JOR;NOOR AL-RAWABDEH;MF
272;JOR;MAHMOUD AL-MARDI;FW
273;JOR;ALI OLWAN;FW
274;KOR;MINJAE KIM;FF
275;KOR;TEAM CREST;
276;KOR;HEUNGMIN SON;IC
277;KOR;HYEONWOO JO;GK
278;KOR;YOUNGWOO SEOL;DF
279;KOR;YUMIN CHO;DF
280;KOR;TAESEOK LEE;DF
281;KOR;INBEOM HWANG;MF
282;KOR;JAESUNG LEE;MF
283;KOR;KANGIN LEE;MF
284;KOR;HYEONGYU OH;FW
285;KOR;HEECHAN HWANG;FW
286;MEX;EDSON ÁLVAREZ;FF
287;MEX;TEAM CREST;
288;MEX;RAÚL JIMÉNEZ;IC
289;MEX;LUIS MALAGÓN;GK
290;MEX;ISRAEL REYES;DF
291;MEX;JOHAN VÁSQUEZ;DF
292;MEX;CÉSAR MONTES;DF
293;MEX;JESÚS GALLARDO;DF
294;MEX;CARLOS RODRÍGUEZ;MF
295;MEX;ORBELÍN PINEDA;MF
296;MEX;HIRVING LOZANO;FW
297;MEX;SANTIAGO GIMÉNEZ;FW
298;MAR;YOUSSEF EN-NESYRI;FF
299;MAR;TEAM CREST;
300;MAR;ACHRAF HAKIMI;IC
301;MAR;YASSINE BOUNOU;GK
302;MAR;NOUSSAIR MAZRAOUI;DF
303;MAR;NAYEF AGUERD;DF
304;MAR;SOFYAN AMRABAT;MF
305;MAR;ELIESSE BEN SEGHIR;MF
306;MAR;ISMAEL SAIBARI;MF
307;MAR;BRAHIM DÍAZ;FW
308;MAR;ABDE EZZALZOULI;FW
309;MAR;AYOUB EL KAABI;FW
310;NED;MEMPHIS DEPAY;FF
311;NED;TEAM CREST;
312;NED;VIRGIL VAN DIJK;IC
313;NED;BART VERBRUGGEN;GK
314;NED;NATHAN AKÉ;DF
315;NED;JEREMIE FRIMPONG;DF
316;NED;DENZEL DUMFRIES;DF
317;NED;TIJJANI REIJNDERS;MF
318;NED;RYAN GRAVENBERCH;MF
319;NED;CODY GAKPO;FW
320;NED;DONYELL MALEN;FW
321;NED;WOUT WEGHORST;FW
322;NZL;MARKO STAMENIC;FF
323;NZL;TEAM CREST;
324;NZL;CHRIS WOOD;IC
325;NZL;MAX CROCOMBE;GK
326;NZL;MICHAEL BOXALL;DF
327;NZL;LIBERATO CACACE;DF
328;NZL;TIM PAYNE;DF
329;NZL;FINN SURMAN;DF
330;NZL;JOE BELL;MF
331;NZL;SARPREET SINGH;MF
332;NZL;MATT GARBETT;MF
333;NZL;ELIJAH JUST;FW
334;NOR;MARTIN ØDEGAARD;FF
335;NOR;TEAM CREST;
336;NOR;ERLING HAALAND;IC
337;NOR;ØRJAN NYLAND;GK
338;NOR;JULIAN RYERSON;DF
339;NOR;KRISTOFFER VASSBAKK AJER;DF
340;NOR;DAVID MØLLER WOLFE;DF
341;NOR;SANDER BERGE;MF
342;NOR;PATRICK BERG;MF
343;NOR;ANTONIO NUSA;FW
344;NOR;OSCAR BOBB;FW
345;NOR;ALEXANDER SØRLOTH;FW
346;PAN;MICHAEL AMIR MURILLO;FF
347;PAN;TEAM CREST;
348;PAN;ANÍBAL GODOY;IC
349;PAN;ORLANDO MOSQUERA;GK
350;PAN;ANDRÉS ANDRADE;DF
351;PAN;FIDEL ESCOBAR;DF
352;PAN;CRISTIAN MARTÍNEZ;MF
353;PAN;ADALBERTO CARRASQUILLA;MF
354;PAN;ÉDGAR BÁRCENAS;MF
355;PAN;JOSÉ FAJARDO;FW
356;PAN;ISMAEL DÍAZ;FW
357;PAN;JOSÉ LUIS RODRÍGUEZ;FW
358;PAR;GUSTAVO GÓMEZ;FF
359;PAR;TEAM CREST;
360;PAR;MIGUEL ALMIRÓN;IC
361;PAR;ROBERTO FERNÁNDEZ;GK
362;PAR;JUAN JOSÉ CÁCERES;DF
363;PAR;OMAR ALDERETE;DF
364;PAR;JÚNIOR ALONSO;DF
365;PAR;ANDRÉS CUBAS;MF
366;PAR;MATHÍAS VILLASANTI;MF
367;PAR;JULIO ENCISO;MF
368;PAR;RAMÓN SOSA;FW
369;PAR;ANTONIO SANABRIA;FW
370;POR;VITINHA;FF
371;POR;TEAM CREST;
372;POR;CRISTIANO RONALDO;IC
373;POR;DIOGO COSTA;GK
374;POR;RÚBEN DIAS;DF
375;POR;NUNO MENDES;DF
376;POR;BERNARDO SILVA;MF
377;POR;BRUNO FERNANDES;MF
378;POR;RÚBEN NEVES;MF
379;POR;FRANCISCO CONCEIÇÃO;FW
380;POR;PEDRO NETO;FW
381;POR;RAFAEL LEÃO;FW
382;QAT;ALMOEZ ALI;FF
383;QAT;TEAM CREST;
384;QAT;HASAN AL-HAYDOS;IC
385;QAT;MESHAAL BARSHAM;GK
386;QAT;BOUALEM KHOUKHI;DF
387;QAT;LUCAS MENDES;DF
388;QAT;PEDRO MIGUEL;DF
389;QAT;HOMAM AL-AMIN;DF
390;QAT;AHMED FATHI;MF
391;QAT;EDMILSON JUNIOR;FW
392;QAT;AHMED AL-GANEHI;FW
393;QAT;AKRAM HASSAN AFIF;FW
394;KSA;FERAS ALBRIKAN;FF
395;KSA;TEAM CREST;
396;KSA;SALEM ALDAWSARI;IC
397;KSA;NAWAF ALAQIDI;GK
398;KSA;HASSAN ALTAMBAKTI;DF
399;KSA;JEHAD THIKRI;DF
400;KSA;SAUD ABDULHAMID;DF
401;KSA;NASSER ALDAWSARI;MF
402;KSA;ABDULLAH ALKHAIBARI;MF
403;KSA;MUSAB ALJUWAYR;MF
404;KSA;SALEH ABUALSHAMAT;MF
405;KSA;SALEH ALSHEHRI;FW
406;SCO;SCOTT MCTOMINAY;FF
407;SCO;TEAM CREST;
408;SCO;ANDREW ROBERTSON;IC
409;SCO;ANGUS GUNN;GK
410;SCO;KIERAN TIERNEY;DF
411;SCO;GRANT HANLEY;DF
412;SCO;BILLY GILMOUR;MF
413;SCO;LEWIS FERGUSON;MF
414;SCO;RYAN CHRISTIE;MF
415;SCO;JOHN MCGINN;MF
416;SCO;BEN GANNON-DOAK;FW
417;SCO;CHÉ ADAMS;FW
418;SEN;KALIDOU KOULIBALY;FF
419;SEN;TEAM CREST;
420;SEN;SADIO MANÉ;IC
421;SEN;ÉDOUARD MENDY;GK
422;SEN;MOUSSA NIAKHATÉ;DF
423;SEN;EL HADJI MALICK DIOUF;DF
424;SEN;IDRISSA GANA GUEYE;MF
425;SEN;PAPE MATAR SARR;MF
426;SEN;ILIMAN NDIAYE;MF
427;SEN;KRÉPIN DIATTA;FW
428;SEN;ISMAÏLA SARR;FW
429;SEN;NICOLAS JACKSON;FW
430;RSA;LYLE FOSTER;FF
431;RSA;TEAM CREST;
432;RSA;RONWEN WILLIAMS;IC
433;RSA;SIYABONGA NGEZANA;DF
434;RSA;AUBREY MODIBA;DF
435;RSA;MBEKEZELI MBOKAZI;DF
436;RSA;KHULISO MUDAU;DF
437;RSA;TEBOHO MOKOENA;MF
438;RSA;VAYA SITHOLE;MF
439;RSA;THEMBA ZWANE;MF
440;RSA;OSWIN APPOLLIS;FW
441;RSA;IQRAAM RAYNERS;FW
442;ESP;LAMINE YAMAL;FF
443;ESP;TEAM CREST;
444;ESP;RODRI;IC
445;ESP;UNAI SIMÓN;GK
446;ESP;ROBIN LE NORMAND;DF
447;ESP;DEAN HUIJSEN;DF
448;ESP;MARC CUCURELLA;DF
449;ESP;MARTÍN ZUBIMENDI;MF
450;ESP;PEDRI;MF
451;ESP;FABIÁN RUIZ;MF
452;ESP;NICO WILLIAMS;FW
453;ESP;MIKEL OYARZABAL;FW
454;SUI;MANUEL AKANJI;FF
455;SUI;TEAM CREST;
456;SUI;GRANIT XHAKA;IC
457;SUI;GREGOR KOBEL;GK
458;SUI;NICO ELVEDI;DF
459;SUI;RICARDO RODRÍGUEZ;DF
460;SUI;SILVAN WIDMER;DF
461;SUI;DENIS ZAKARIA;MF
462;SUI;REMO FREULER;MF
463;SUI;BREEL EMBOLO;FW
464;SUI;RUBÉN VARGAS;FW
465;SUI;DAN NDOYE;FW
466;TUN;FERJANI SASSI;FF
467;TUN;TEAM CREST;
468;TUN;ELLYES SKHIRI;IC
469;TUN;AYMEN DAHMEN;GK
470;TUN;MONTASSAR TALBI;DF
471;TUN;YASSINE MERIAH;DF
472;TUN;ALI ABDI;DF
473;TUN;AÏSSA LAÏDOUNI;MF
474;TUN;HANNIBAL MEJBRI;MF
475;TUN;NAÏM SLITI;FW
476;TUN;ELIAS ACHOURI;FW
477;TUN;HAZEM MASTOURI;FW
478;USA;WESTON MCKENNIE;FF
479;USA;TEAM CREST;
480;USA;CHRISTIAN PULISIC;IC
481;USA;MATT FREESE;GK
482;USA;CHRIS RICHARDS;DF
483;USA;TIM REAM;DF
484;USA;ANTONEE ROBINSON;DF
485;USA;TANNER TESSMANN;MF
486;USA;TYLER ADAMS;MF
487;USA;TIMOTHY WEAH;FW
488;USA;MALIK TILLMAN;FW
489;USA;FOLARIN BALOGUN;FW
490;URU;JOSÉ MARÍA GIMÉNEZ;FF
491;URU;TEAM CREST;
492;URU;FEDERICO VALVERDE;IC
493;URU;SERGIO ROCHET;GK
494;URU;RONALD ARAÚJO;DF
495;URU;SEBASTIÁN CÁCERES;DF
496;URU;MATHÍAS OLIVERA;DF
497;URU;NAHITAN NÁNDEZ;DF
498;URU;RODRIGO BENTANCUR;MF
499;URU;MANUEL UGARTE;MF
500;URU;FACUNDO PELLISTRI;FW
501;URU;DARWIN NÚÑEZ;FW
502;UZB;ABDUKODIR KHUSANOV;FF
503;UZB;TEAM CREST;
504;UZB;ELDOR SHOMURODOV;IC
505;UZB;UTKIR YUSUPOV;GK
506;UZB;FARRUKH SAYFIEV;DF
507;UZB;SHERZOD NASRULLAEV;DF
508;UZB;HUSNIDDIN ALIQULOV;DF
509;UZB;RUSTAM ASHURMATOV;DF
510;UZB;KHOJIAKBAR ALIJONOV;MF
511;UZB;ODILJON HAMROBEKOV;MF
512;UZB;OTABEK SHUKUROV;MF
513;UZB;ABBOSBEK FAYZULLAEV;FW
514;CONTENDERS;ITA - NIR/WAL - BIH;
515;CONTENDERS;UKR - SWE/POL - ALB;
516;CONTENDERS;TUR - ROU/SVK - KOS;
517;CONTENDERS;DEN - MKD/CZE - IRL;
518;CONTENDERS;NCL - JAM/COD;
519;CONTENDERS;SUR - BOL/IRQ;
520;DEN;HJULMAND (DEN);MF
521;DEN;HØJBJERG (DEN);MF
522;DEN;ERIKSEN (DEN);MF
523;DEN;DAMSGAARD (DEN);MF
524;DEN;HØJLUND (DEN);FW
525;ITA;DONNARUMMA (ITA);GK
526;ITA;BASTONI (ITA);DF
527;ITA;TONALI (ITA);MF
528;ITA;BARELLA (ITA);MF
529;ITA;KEAN (ITA);FW
530;JAM;BLAKE (JAM);GK
531;JAM;PINNOCK (JAM);DF
532;JAM;GRAY (JAM);FW
533;JAM;BAILEY (JAM);FW
534;JAM;NICHOLSON (JAM);FW
535;POL;CASH (POL);DF
536;POL;KIWIOR (POL);DF
537;POL;ZIELIŃSKI (POL);MF
538;POL;SZYMAŃSKI (POL);MF
539;POL;LEWANDOWSKI (POL);FW
540;SWE;HIEN (SWE);DF
541;SWE;KULUSEVSKI (SWE);MF
542;SWE;ELANGA (SWE);FW
543;SWE;GYÖKERES (SWE);FW
544;SWE;ISAK (SWE);FW
545;TUR;SÖYÜNCÜ (TUR);DF
546;TUR;ÇALHANOĞLU (TUR);MF
547;TUR;GÜLER (TUR);MF
548;TUR;YILDIZ (TUR);FW
549;TUR;AKTÜRKOĞLU (TUR);FW
550;TOP_KEEPERS;MARTÍNEZ (ARG);GK
551;TOP_KEEPERS;COURTOIS (BEL);GK
552;TOP_KEEPERS;ALISSON (BRA);GK
553;TOP_KEEPERS;MAIGNAN (FRA);GK
554;TOP_KEEPERS;SUZUKI (JPN);GK
555;TOP_KEEPERS;BOUNOU (MAR);GK
556;TOP_KEEPERS;DIOGO COSTA (POR);GK
557;TOP_KEEPERS;SIMÓN (ESP);GK
558;TOP_KEEPERS;KOBEL (SUI);GK
559;DEFENSIVE_ROCKS;ÉDER MILITÃO (BRA);DF
560;DEFENSIVE_ROCKS;DAVIES (CAN);DF
561;DEFENSIVE_ROCKS;SALIBA (FRA);DF
562;DEFENSIVE_ROCKS;RÜDIGER (GER);DF
563;DEFENSIVE_ROCKS;KIM (KOR);DF
564;DEFENSIVE_ROCKS;HAKIMI (MAR);DF
565;DEFENSIVE_ROCKS;VAN DIJK (NED);DF
566;DEFENSIVE_ROCKS;NUNO MENDES (POR);DF
567;DEFENSIVE_ROCKS;HUIJSEN (ESP);DF
568;MIDFIELD_MAESTROS;FERNÁNDEZ (ARG);MF
569;MIDFIELD_MAESTROS;DE BRUYNE (BEL);MF
570;MIDFIELD_MAESTROS;CASEMIRO (BRA);MF
571;MIDFIELD_MAESTROS;MODRIĆ (CRO);MF
572;MIDFIELD_MAESTROS;CAICEDO (ECU);MF
573;MIDFIELD_MAESTROS;BELLINGHAM (ENG);MF
574;MIDFIELD_MAESTROS;TCHOUAMÉNI (FRA);MF
575;MIDFIELD_MAESTROS;WIRTZ (GER);MF
576;MIDFIELD_MAESTROS;AMRABAT (MAR);MF
577;MIDFIELD_MAESTROS;REIJNDERS (NED);MF
578;MIDFIELD_MAESTROS;ØDEGAARD (NOR);MF
579;MIDFIELD_MAESTROS;VITINHA (POR);MF
580;MIDFIELD_MAESTROS;MCTOMINAY (SCO);MF
581;MIDFIELD_MAESTROS;RODRI (ESP);MF
582;MIDFIELD_MAESTROS;PEDRI (ESP);MF
583;MIDFIELD_MAESTROS;XHAKA (SUI);MF
584;MIDFIELD_MAESTROS;ADAMS (USA);MF
585;MIDFIELD_MAESTROS;VALVERDE (URU);MF
586;GOAL_MACHINES;ÁLVAREZ (ARG);FW
587;GOAL_MACHINES;LUKAKU (BEL);FW
588;GOAL_MACHINES;RAPHINHA (BRA);FW
589;GOAL_MACHINES;DAVID (CAN);FW
590;GOAL_MACHINES;DÍAZ (COL);FW
591;GOAL_MACHINES;KRAMARIĆ (CRO);FW
592;GOAL_MACHINES;VALENCIA (ECU);FW
593;GOAL_MACHINES;MARMOUSH (EGY);FW
594;GOAL_MACHINES;RASHFORD (ENG);FW
595;GOAL_MACHINES;KOLO MUANI (FRA);FW
596;GOAL_MACHINES;HAVERTZ (GER);FW
597;GOAL_MACHINES;HALLER (CIV);FW
598;GOAL_MACHINES;JIMÉNEZ (MEX);FW
599;GOAL_MACHINES;EN-NESYRI (MAR);FW
600;GOAL_MACHINES;GAKPO (NED);FW
601;GOAL_MACHINES;WOOD (NZL);FW
602;GOAL_MACHINES;SØRLOTH (NOR);FW
603;GOAL_MACHINES;JACKSON (SEN);FW
604;GOAL_MACHINES;OYARZABAL (ESP);FW
605;GOAL_MACHINES;EMBOLO (SUI);FW
606;GOAL_MACHINES;PULISIC (USA);FW
607;GOAL_MACHINES;NÚÑEZ (URU);FW
608;MASTER_ROOKIES;PAZ (ARG);MF
609;MASTER_ROOKIES;MASTANTUONO (ARG);FW
610;MASTER_ROOKIES;DEBAST (BEL);DF
611;MASTER_ROOKIES;WESLEY (BRA);DF
612;MASTER_ROOKIES;ESTÊVÃO (BRA);FW
613;MASTER_ROOKIES;SUČIĆ (CRO);MF
614;MASTER_ROOKIES;PÁEZ (ECU);MF
615;MASTER_ROOKIES;ROGERS (ENG);MF
616;MASTER_ROOKIES;DOUÉ (FRA);FW
617;MASTER_ROOKIES;BARCOLA (FRA);FW
618;MASTER_ROOKIES;WOLTEMADE (GER);FW
619;MASTER_ROOKIES;SIMONS (NED);FW
620;MASTER_ROOKIES;SCHJELDERUP (NOR);MF
""".strip()


def parse_source_rows(source: str = SOURCE_ROWS) -> list[Card]:
    cards: list[Card] = []
    for line_number, line in enumerate(source.splitlines(), start=1):
        parts = line.split(";")
        if len(parts) != 4:
            raise ValueError(f"Invalid source line {line_number}: {line!r}")

        raw_number, group, name, code = parts
        if code not in POSITION_BY_CODE:
            raise ValueError(f"Invalid position code {code!r} on source line {line_number}")

        cards.append(
            Card(
                number=int(raw_number),
                group=group,
                name=name,
                position=POSITION_BY_CODE[code],
            )
        )

    return cards


def build_checklist(cards: list[Card] | None = None) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[Card]] = {group: [] for group in GROUP_ORDER}
    for card in cards or parse_source_rows():
        grouped.setdefault(card.group, []).append(card)

    return {
        group: [card.as_json() for card in sorted(grouped[group], key=lambda item: item.number)]
        for group in GROUP_ORDER
    }


def empty_inventory() -> dict[str, list[dict[str, Any]]]:
    return {group: [] for group in GROUP_ORDER}


def empty_stock() -> dict[str, list[dict[str, Any]]]:
    return {group: [] for group in GROUP_ORDER}


def build_document() -> dict[str, Any]:
    document = {
        "collection": COLLECTION,
        "checklist": build_checklist(),
        "stock": empty_stock(),
    }
    return with_derived_inventory(document)


def load_document(path: Path = DATA_FILE) -> dict[str, Any]:
    with path.open(encoding="utf-8") as file:
        data = json.load(file)
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return data


def card_lookup(document: dict[str, Any]) -> dict[int, tuple[str, dict[str, Any]]]:
    lookup: dict[int, tuple[str, dict[str, Any]]] = {}
    for group, cards in document.get("checklist", {}).items():
        for card in cards:
            lookup[card["number"]] = (group, card)
    return lookup


def checklist_numbers_by_group(document: dict[str, Any]) -> dict[str, set[int]]:
    grouped: dict[str, set[int]] = {group: set() for group in GROUP_ORDER}
    for group, cards in document.get("checklist", {}).items():
        if not isinstance(cards, list):
            continue
        grouped.setdefault(group, set()).update(
            card.get("number") for card in cards if isinstance(card.get("number"), int)
        )
    return grouped


def stock_quantities(document: dict[str, Any]) -> dict[int, int]:
    quantities: dict[int, int] = {}
    stock = document.get("stock", {})
    if not isinstance(stock, dict):
        return quantities

    for cards in stock.values():
        if not isinstance(cards, list):
            continue
        for card in cards:
            if not isinstance(card, dict):
                continue
            number = card.get("number")
            quantity = card.get("quantity")
            if isinstance(number, int) and isinstance(quantity, int):
                quantities[number] = quantity

    return quantities


def derive_inventory(document: dict[str, Any]) -> tuple[dict[str, list[dict[str, Any]]], dict[str, list[dict[str, Any]]]]:
    lookup = card_lookup(document)
    by_group = checklist_numbers_by_group(document)
    quantities = stock_quantities(document)
    repetidas = empty_inventory()
    faltantes = empty_inventory()

    for group in GROUP_ORDER:
        for number in sorted(by_group.get(group, set())):
            card = lookup[number][1]
            quantity = quantities.get(number, 0)
            if quantity <= 0:
                faltantes[group].append(card.copy())
            elif quantity > 1:
                repetidas[group].extend(card.copy() for _ in range(quantity - 1))

    return repetidas, faltantes


def with_derived_inventory(document: dict[str, Any]) -> dict[str, Any]:
    document = dict(document)
    repetidas, faltantes = derive_inventory(document)
    document["repetidas"] = repetidas
    document["faltantes"] = faltantes
    return document


def resolve_card(document: dict[str, Any], number: int) -> dict[str, Any]:
    lookup = card_lookup(document)
    try:
        return lookup[number][1]
    except KeyError as exc:
        raise KeyError(f"Card number {number} does not exist in checklist") from exc


def cards_for_group(document: dict[str, Any], group: str) -> list[dict[str, Any]]:
    try:
        cards = document["checklist"][group]
    except KeyError as exc:
        raise KeyError(f"Group {group!r} does not exist in checklist") from exc
    if not isinstance(cards, list):
        raise ValueError(f"Checklist group {group!r} must be a list")
    return cards


def validate_document(document: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    if document.get("collection") != COLLECTION:
        errors.append("collection metadata does not match FIFA World Cup 2026 Adrenalyn XL")

    checklist = document.get("checklist")
    if not isinstance(checklist, dict):
        return ["checklist must be an object"]

    checklist_keys = set(checklist)
    expected_keys = set(GROUP_ORDER)
    unknown_keys = checklist_keys - expected_keys
    missing_keys = expected_keys - checklist_keys
    if unknown_keys:
        errors.append(f"checklist has unknown groups: {sorted(unknown_keys)}")
    if missing_keys:
        errors.append(f"checklist is missing groups: {sorted(missing_keys)}")

    all_cards: list[tuple[str, dict[str, Any]]] = []
    for group in GROUP_ORDER:
        cards = checklist.get(group)
        if not isinstance(cards, list):
            errors.append(f"checklist group {group} must be a list")
            continue
        all_cards.extend((group, card) for card in cards if isinstance(card, dict))
        if len(cards) != sum(1 for expected in GROUP_BY_NUMBER.values() if expected == group):
            errors.append(f"checklist group {group} has {len(cards)} cards")

    numbers = [card.get("number") for _, card in all_cards]
    int_numbers = [number for number in numbers if isinstance(number, int)]
    if len(all_cards) != COLLECTION["total_cards"]:
        errors.append(f"checklist has {len(all_cards)} cards, expected {COLLECTION['total_cards']}")
    if int_numbers != list(range(1, COLLECTION["total_cards"] + 1)):
        missing = sorted(set(range(1, COLLECTION["total_cards"] + 1)) - set(int_numbers))
        duplicates = sorted(number for number, count in Counter(int_numbers).items() if count > 1)
        if missing:
            errors.append(f"checklist is missing numbers: {missing}")
        if duplicates:
            errors.append(f"checklist has duplicate numbers: {duplicates}")
        if not missing and not duplicates:
            errors.append("checklist numbers are not in deterministic 1-620 order")

    for group, card in all_cards:
        number = card.get("number")
        name = card.get("name")
        position = card.get("position")

        if not isinstance(number, int):
            errors.append(f"{group} has card with non-integer number: {card!r}")
            continue
        expected_group = GROUP_BY_NUMBER.get(number)
        if expected_group != group:
            errors.append(f"card {number} is in {group}, expected {expected_group}")
        if not isinstance(name, str) or not name.strip():
            errors.append(f"card {number} has an empty or invalid name")
        if position is not None and position not in ALLOWED_POSITIONS:
            errors.append(f"card {number} has invalid position {position!r}")

    errors.extend(_validate_stock(document))
    errors.extend(_validate_derived_inventory(document))
    errors.extend(_validate_inventory(document, "repetidas"))
    errors.extend(_validate_inventory(document, "faltantes"))
    errors.extend(_validate_inventory_overlap(document))
    return errors


def _validate_stock(document: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    stock = document.get("stock")
    if not isinstance(stock, dict):
        return ["stock must be an object"]

    lookup = card_lookup(document)
    seen: set[int] = set()
    for group, cards in stock.items():
        if group not in GROUP_ORDER:
            errors.append(f"stock has unknown group {group!r}")
            continue
        if not isinstance(cards, list):
            errors.append(f"stock.{group} must be a list")
            continue

        for card in cards:
            if not isinstance(card, dict):
                errors.append(f"stock.{group} contains a non-object card")
                continue
            number = card.get("number")
            quantity = card.get("quantity")
            if not isinstance(number, int) or number not in lookup:
                errors.append(f"stock.{group} contains unknown card number {number!r}")
                continue
            expected_group, _ = lookup[number]
            if expected_group != group:
                errors.append(f"stock.{group} contains card {number} from {expected_group}")
            if number in seen:
                errors.append(f"stock contains duplicate card {number}")
            seen.add(number)
            if not isinstance(quantity, int) or quantity < 1:
                errors.append(f"stock.{group} card {number} must have quantity >= 1")

    return errors


def _validate_derived_inventory(document: dict[str, Any]) -> list[str]:
    expected_repetidas, expected_faltantes = derive_inventory(document)
    errors: list[str] = []
    if document.get("repetidas") != expected_repetidas:
        errors.append("repetidas must be derived from stock")
    if document.get("faltantes") != expected_faltantes:
        errors.append("faltantes must be derived from stock")
    return errors


def _validate_inventory(document: dict[str, Any], section: str) -> list[str]:
    errors: list[str] = []
    inventory = document.get(section)
    if not isinstance(inventory, dict):
        return [f"{section} must be an object"]

    lookup = card_lookup(document)
    seen_missing: set[int] = set()
    for group, cards in inventory.items():
        if group not in GROUP_ORDER:
            errors.append(f"{section} has unknown group {group!r}")
            continue
        if not isinstance(cards, list):
            errors.append(f"{section}.{group} must be a list")
            continue

        for card in cards:
            if not isinstance(card, dict):
                errors.append(f"{section}.{group} contains a non-object card")
                continue
            number = card.get("number")
            if not isinstance(number, int) or number not in lookup:
                errors.append(f"{section}.{group} contains unknown card number {number!r}")
                continue
            expected_group, expected_card = lookup[number]
            if expected_group != group:
                errors.append(f"{section}.{group} contains card {number} from {expected_group}")
            if card.get("name") != expected_card.get("name"):
                errors.append(f"{section}.{group} card {number} name differs from checklist")
            if card.get("position") != expected_card.get("position"):
                errors.append(f"{section}.{group} card {number} position differs from checklist")
            if section == "faltantes":
                if number in seen_missing:
                    errors.append(f"faltantes contains duplicate card {number}")
                seen_missing.add(number)

    return errors


def _validate_inventory_overlap(document: dict[str, Any]) -> list[str]:
    repeated = _inventory_numbers(document.get("repetidas", {}))
    missing = _inventory_numbers(document.get("faltantes", {}))
    overlap = sorted(repeated & missing)
    if overlap:
        return [f"cards cannot be both repetidas and faltantes: {overlap}"]
    return []


def _inventory_numbers(inventory: Any) -> set[int]:
    numbers: set[int] = set()
    if not isinstance(inventory, dict):
        return numbers
    for cards in inventory.values():
        if not isinstance(cards, list):
            continue
        numbers.update(card.get("number") for card in cards if isinstance(card, dict))
    return {number for number in numbers if isinstance(number, int)}
