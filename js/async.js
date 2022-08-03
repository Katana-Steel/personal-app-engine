/*
    Written for my personal website by Rene Kjellerup
    published under GPLv3 or later and never in minified form.
    see https://www.gnu.org/licenses.html
*/
var page_cache = {};

function async_cached(ele, url)
{
    if (url in page_cache)
    {
        ele.innerHTML = page_cache[url];
        return true;
    }
    return false;
}

function async_load_content(div, url)
{
    const frame = document.getElementById(div);
    if(frame === null){
        console.error( new Error('element '+div+' not found on page'));
        return;
    }
    if (async_cached(frame, url)) {
        return;
    }
    fetch(url)
        .then((resp) => {
            if(!resp.ok)
                throw new Error('could not get '+url+' from server');
            return resp.text();
        })
        .then((page) => {
            page_cache[url] = page;
            frame.innerHTML = page;
        })
        .catch((err) => console.error(err));
}

function ajax_loadContent(div, url) {
    async_load_content(div, url);
}
