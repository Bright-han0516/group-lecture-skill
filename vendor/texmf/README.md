# vendor/texmf — rsfs

`rsfs` is required by `mathptmx` for a few arrow/script glyphs under XeLaTeX. Without
it, `\to` and `\rightarrow` fail with:

```
xdvipdfmx:fatal: Unable to find TFM file "rsfs10".
```

This tree contains the unmodified `rsfs` fonts from CTAN:

```
fonts/tfm/public/rsfs/      *.tfm
fonts/type1/public/rsfs/    *.pfb, *.pfm
fonts/afm/public/rsfs/      *.afm
```

`build_topic.sh` sets `TEXMFHOME` to `_模板/texmf` (a copy of this tree) or to
`vendor/texmf` when building the demo, so `kpsewhich rsfs10.tfm` finds it.

## Credit and license

The `rsfs` README (Ralph Smith, UCSD) says:

> You are welcome to use and distribute these files; if you modify them, please
> change the name but give credit to the original author!

The files are included unmodified. Source: CTAN `fonts/rsfs`.

This is not a TeX Live installation; only the `rsfs` files needed by the template
are vendored. All other packages come from the user's TeX distribution.
