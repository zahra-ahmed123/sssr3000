# Ansiktsgjenkjenning med Raspberry Pi og PiCamera

Dette prosjektet demonstrerer sanntids ansiktsgjenkjenning ved hjelp av en Raspberry Pi, PiCamera og OpenCV. 
Systemet oppdager ansikter innenfor en viss avstand ved hjelp av en ultrasonisk avstandssensor 
og utfører gjenkjenning basert på forhåndstrente modeller.

## Forutsetninger

- Raspberry Pi med Raspbian OS
- PiCamera
- Python 3.x
- OpenCV
- gpiozero

## Installasjon

1. Klon dette depotet:

    ```bash
    git clone https://github.com/zahra-ahmed123/sssr3000.git
    ```

2. Installer de nødvendige Python-pakkene: --> pass på å ikke ovride me external environment


3. Last ned den forhåndstrente ansiktsgjenkjenningsmodellen `haarcascade_frontalface_default.xml` og plasser den i prosjektmappen.

4. Tren ansiktsgjenkjenningsmodellen med ditt datasett.

## Bruk

1. Koble PiCamera og den ultrasoniske avstandssensoren til din Raspberry Pi.--> Brukte Breadbord 

2. Kjør hoved-Python-skriptet:

    ```bash
    cd AiSecurityCamera
    python main.py
    ```

3. Systemet vil vente på bevegelse innenfor en angitt avstand oppdaget av avstandssensoren.

4. Når bevegelse oppdages, vil PiCamera begynne å fange rammer. Hvis et ansikt oppdages innenfor rammen, vil det bli gjenkjent og merket deretter.

5. For å avslutte programmet, trykk 'q' på tastaturet. Eller  venter sytemet for at bevegelse blir utenfor max avstanden anngitt av avtands sensoren

## Konfigurasjon

Du kan justere parameterne i `params`-diksjonæret innenfor skriptet for å tilpasse visningen av ansiktsgjenkjenningen, som f.eks. skriftstørrelse og boks-farger.

## prolemer/feilhåndtering

- inteallering av openCV ved bruk av pip. Fikk ikke lov på grunn av external managed environment.
- måtte lie virituell environment for pip installeringer.
- Fått problemer senere på prosjekt tiden fordi jeg harre imulitis og numpy installert i verituell environment mens openCV var installert i den externe. 
- Måtte   laste ned openCV på nytt ved hejlp av pip på virituell environment. Dette var veldig tidskrevende

## Krediteringer

Dette prosjektet bruker følgende biblioteker:

- [PiCamera](https://picamera.readthedocs.io/)
- [gpiozero](https://gpiozero.readthedocs.io/)
- [OpenCV](https://opencv.org/)

## Kilder

- [https://github.com/justsaumit/opencv-face-recognition-rpi4/tree/main/face-detection]--> Fra moduler i canvas lagt ut av foreleser- 
- [forelesningsNotater]

## Lisens

Dette prosjektet er lisensiert under MIT Lisensen - se [LICENSE](LICENSE)-filen for detaljer.
