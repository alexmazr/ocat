let code = document.getElementById('code');
let out = document.getElementById('compile-out');

async function compile ()
{
    out.innerHTML +=  "<p>" + await eel.compile (code.innerText)() + "</p>";
}

function color (e)
{
    console.log (e);
}

let timeout = null;

code.addEventListener('keyup', function (e) {
    clearTimeout (timeout);
    timeout = setTimeout(function () {
        color (e);
    }, 500);
});