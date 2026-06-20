document.addEventListener("DOMContentLoaded", function () {
    
    const btnStatic = document.getElementById('btnStatic');
    const btnDynamic = document.getElementById('btnDynamic');
    const codeDisplay = document.getElementById('codeDisplay');
    const resultDisplay = document.getElementById('resultDisplay');

    // CONTENT DATA
    const staticContent = {
        code: `<span style="color:#888">&lt;!-- Static HTML --&gt;</span><br>
               &lt;div&gt;<br>
               &nbsp;&nbsp;&lt;h1&gt;Welcome User&lt;/h1&gt;<br>
               &lt;/div&gt;`,
        result: `<h3>Welcome User</h3>`
    };

    const dynamicContent = {
        code: `<span style="color:#569cd6">@if</span>(User.IsAdmin)<br>
               {<br>
               &nbsp;&nbsp;&lt;h1&gt;Hello Admin!&lt;/h1&gt;<br>
               &nbsp;&nbsp;&lt;button&gt;Edit&lt;/button&gt;<br>
               }`,
        result: `<h3 style="color:#06b6d4">Hello Admin!</h3>
                 <button style="background:#06b6d4;color:white;border:none;padding:5px 10px;border-radius:4px">Edit</button>`
    };

    function setView(isDynamic) {
        if(isDynamic) {
            btnDynamic.classList.add('active');
            btnStatic.classList.remove('active');
            
            codeDisplay.innerHTML = dynamicContent.code;
            resultDisplay.innerHTML = dynamicContent.result;
            resultDisplay.style.border = "2px solid #06b6d4"; // Cyan border for active
        } else {
            btnStatic.classList.add('active');
            btnDynamic.classList.remove('active');
            
            codeDisplay.innerHTML = staticContent.code;
            resultDisplay.innerHTML = staticContent.result;
            resultDisplay.style.border = "1px solid #ddd";
        }
    }

    // Event Listeners
    btnStatic.addEventListener('click', () => setView(false));
    btnDynamic.addEventListener('click', () => setView(true));

    // Init
    setView(false);
});