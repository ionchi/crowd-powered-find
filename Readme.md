# CrowdFind
Dato un numero (grande) di oggetti, una proprietà booleana P e un numero K, 
servirsi dell'aiuto umano per trovare K elementi che soddisfano P. 

Trovare un algoritmo che ottimizzi:
* il costo = numero totale di domande fatte
* il tempo = numero di fasi di crowdsourcing, con domande su uno o più oggetti, fatte in ogni fase

### Algoritmo UncOptCost

##### **Dati**
* O = insieme di oggetti
* K = numero di oggetti desiderati 
* S = strategia (Majority, Rectangular, Threshold, etc...)
* P(*) = Varie probabilità necessarie per i calcoli

##### **Risultato**
* L (inizializzato vuoto) = insieme oggetti desiderati, di dimensione K
* U (inizializzato uguale a O) = insieme iniziale

##### **Algoritmo**
1) Precalcolare Y (il costo previsto per trovare un nuovo elemento che 
soddisfi il predicato partendo da I) per ogni elemento ed in funzione della strategia S, attraverso la formula:
    <pre>
    Y(n1,n2) = PR1*N1+PR2*(Y(0,0)+N2)
    </pre>
    
    dove: 
    
    - n1 = numero di YES per l'oggetto I
    - n2 = numero di NO per l'oggetto I
    - PR1 = probabilità che l'oggetto I diventi un oggetto 1 (appartenente all'insieme L)
    - N1 = numero di domande affinché I diventi un oggetto 1
    - PR2 = probabilità affinché I diventi peggio che cercare un altro oggetto
    - N2 = numero di domande affiché il costo di I sia maggiore di Y(0,0) [che è il costo iniziale
    di ogni elemento]

2) finché la dimensione dell'insieme L < K
    * considerare un insieme O' appartenente a U tale che la dim(O')=(K-dim(L))
    * CQ <- {} // inizializzare l'insieme delle domande
    * per ogni oggetto I appartenente a O'
        * sia n+ il numero minore di YES necessari affinché Y(R(I))=0
        * sia n- il numero minore di NO necessari affinché Y(R(I))=Y(0,0)
        * aggiungere min(n+,n-) domande sull'oggetto I all'insieme CQ
        (questo garantisce che in ogni fase vengano fatte un numero ottimo di domande)
    * richiedere in parallelo le domande dell'insieme CQ a un servizio di crowdsourcing
    * in base alle risposte, aggiornare R(I) per ogni elemento I
    * per ogni I appartenente a CQ 
        * se S(R(I))=1 // cioé se in base alla strategia si può considerare I un oggetto 1
            * rimuovere I da U e aggiungerlo a L
        * se S(R(I))=0 // cioé se in base alla strategia si può considerare I un oggetto 0
            * rimuovere I da U