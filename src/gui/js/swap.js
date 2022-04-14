codePage = ''
decodePage = '<div class="scrollable decode"><p>Decode Output</p></div>'
simulatePage = '<div class="scrollable simulate"><p>Simulator</p></div>'
currentPage = 'code'

                


function swapWindow (target)
{
    let content = document.getElementById ('content');
    let leftButton = document.getElementById ('left-button');
    if (currentPage === 'code') codePage = content.innerHTML;
    else if (currentPage === 'decode') decodePage = content.innerHTML;
    else if (currentPage === 'simulate') simulatePage = content.innerHTML;

    currentPage = target;
    if (target === 'code') content.innerHTML = codePage;
    else if (target === 'decode') content.innerHTML = decodePage;
    else if (target === 'simulate') content.innerHTML = simulatePage;

    if (target !== 'code') {
        leftButton.innerHTML = "<p>Code</p>"
        leftButton.onclick =  function () { swapWindow ("code") }
    } else {
        leftButton.innerHTML = "<p>Compile</p>"
        leftButton.onclick = function () { compile () }
    }
}