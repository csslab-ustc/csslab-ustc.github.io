## Usage

Assuming you have already install the  `jemdoc+MathJax`, notice that

in `./jemdoc_files/`, we store `.jemdoc` files and `mysite.conf`

in `./www/`, we store the output `.html` / `.css` / `.js` files and website assets.

Suppose you are currently in `./jemdoc_files/`, we use the following to compile

```
python ../jemdoc -c mysite.conf -o ../www/  *.jemdoc
```

You can also use this for single page generation or all page generation by using `*.jemdoc`.