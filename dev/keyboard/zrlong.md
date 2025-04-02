## Information

1. row

- alphabet
- sheng：声母可以不变。
- yun：对应的韵母。

2. table

- yun：如何单独打出韵母。
- bianma：击键顺序。

## Convert

row 每 8 个为一个 row
下面的意义何在？

```js
{ alphabet: ';' },
```

以:为间隔，右侧为按键 key，左侧为对应韵母 yun。
key -> alphabet uppercase
yun -> table/yun 排序

table
yun：按照首字母放在一个 table
删去 i 开头，没有这样拼音构成的字。

## zrlong

```js
yun:{
    "ā":"l","á":"u","ǎ":"m","à":"i",
    "ē":"r","é":"e","ě":"l","è":"i",
    "ī":"j","í":"b","ǐ":"g","ì":"t",
    "ō":"p","ó":"e","ǒ":"i","ò":"g",
    "ū":"a","ú":"l","ǔ":"m","ù":"h",
    "ǖ":"h","ǘ":"m","ǚ":"h","ǜ":"f",
    "āi":"b","ái":"d","ǎi":"u","ài":"o",
    "ān":"n","án":"k","ǎn":"o","àn":"j",
    "āng":"u","áng":"w","ǎng":"p","àng":"d",
    "āo":"q","áo":"i","ǎo":"x","ào":"v",
    "ēi":"i","éi":"r","ěi":"j","èi":"f",
    "ēn":"e","én":"s","ěn":"o","èn":"o",
    "ēng":"c","éng":"f","ěng":"y","èng":"f",
    "ēr":"q","ér":"k","ěr":"u","èr":"h",
    "īn":"h","ín":"c","ǐn":"x","ìn":"v",
    "īng":"e","íng":"n","ǐng":"w","ìng":"w",
    "ōng":"k","óng":"j","ǒng":"n","òng":"y",
    "ōu":"x","óu":"a","ǒu":"z","òu":"r",
    "ūn":"g","ún":"f","ǔn":"o","ùn":"r",
    "iā":"d","iá":"c","iǎ":"n","ià":"x",
    "iān":"r","ián":"v","iǎn":"p","iàn":"a",
    "iāng":"y","iáng":"i","iǎng":"u","iàng":"e",
    "iāo":"m","iáo":"u","iǎo":"l","iào":"l",
    "iē":"k","ié":"s","iě":"c","iè":"q",
    "iōng":"p","ióng":"k","iǒng":"e",
    "iū":"z","iú":"m","iǔ":"z","iù":"o",
    "uā":"s","uá":"t","uǎ":"g","uà":"g",
    "uāi":"g","uái":"s","uǎi":"p","uài":"f",
    "uān":"d","uán":"o","uǎn":"s","uàn":"c",
    "uāng":"w","uáng":"b","uǎng":"u","uàng":"e",
    "uī":"t","uí":"w","uǐ":"v","uì":"f",
    "uō":"s","uó":"l","uǒ":"l","uò":"p",
    "üē":"u","üé":"i","üě":"o","üè":"d"
}
```

## bianma

```
1: ān án ǎn àn=nkoj
2: āáǎà=lumi
3: āi ái ǎi ài=bduo
4: āng áng ǎng àng=uwpd
5: āo áo ǎo ào=qixv
6: ēéěè=reli
7: ēi éi ěi èi=irjf
8: ēn én ěn èn=esoo
9: ēng éng ěng èng=cfyf
10: ērérěrèr=qkuh
11: īíǐì=jbgt
12: iā iá iǎ ià=dcnx
13: iān ián iǎn iàn=rvpa
14: iāng iáng iǎng iàng=yiue
15: iāo iáo iǎo iào=mull
16: iē ié iě iè=kscq
17: īn ín ǐn ìn=hcxv
18: īng íng ǐng ìng=enww
19: iōng ióng iǒng=pke
20: iū iú iǔ iù=zmzo
21: ōóǒò=peig
22: ōng óng ǒng òng=kjny
23: ōu óu ǒu òu=xazr
24: ūúǔù=almh
25: ǖǘǚǜ=hmsf
26: uā uá uǎ uà=stgg
27: uāi uái uǎi uài=gspf
28: uān uán uǎn uàn=dosc
29: uāng uáng uǎng uàng=wbue
30: üē üé üě üè=uiod
31: uī uí uǐ uì=twvf
32: ūn ún ǔn ùn=gfor
33: uō uó uǒ uò=sllp
```
