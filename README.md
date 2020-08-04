# OEIS-crawler
A crawler, that finds broken links at the OEIS. Based on https://github.com/buckyroberts/Spider.

Right now only recognises links that throw Error 404.
Becomes increasingly slower over time.

Known bugs: can sometimes fall into infinite recursion, doesn't always work properly if you alter the queue by hand.

broken.txt is the file of all dead links I found so far, crawled.txt is the file of all links I've already checked.
broken.xlsx contains replacements for rotten links alongside with some other useful data. Not finished yet.
