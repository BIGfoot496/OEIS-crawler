# OEIS-crawler
A crawler that finds broken links at the OEIS. Based on https://github.com/buckyroberts/Spider.

Right now only recognises links that throw Error 404, because only with those I could be absolutely sure that they are actually broken, and not just don't like web-spiders, or my laptop, or me...
Becomes increasingly slower over time. 
To solve the slowing down I limit the number of links it can hold in the queue to 20000 links.

Known bugs: can sometimes fall into infinite recursion if you alter the queue by hand (usually it's fine though).

broken.txt is the file of all dead links I found so far, crawled.txt is the file of all links I've already checked.
broken.xlsx contains replacements for rotten links alongside with some other useful data.
These ones are probably really outdated, I last looked at them in 2020 lol
