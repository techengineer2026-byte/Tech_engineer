document.addEventListener("DOMContentLoaded", function () {
    AOS.init({ duration: 800 });

    const codeDisplay = document.getElementById('codeDisplay');
    const visualDisplay = document.getElementById('visualDisplay');
    const fileName = document.getElementById('fileName');
    const tabs = document.querySelectorAll('.tab-btn');

    // Content Data
    const data = {
        front: {
            file: "style.css / index.html",
            code: `<span style="color:#ec4899">.btn</span> {<br>
  background: <span style="color:#fbbf24">gold</span>;<br>
  color: white;<br>
  padding: 10px;<br>
}<br>
&lt;button class="btn"&gt;Click Me&lt;/button&gt;`,
            visual: `<button class="demo-btn">Click Me</button>`
        },
        back: {
            file: "server.js",
            code: `<span style="color:#06b6d4">app.get</span>('/api/user', (req, res) => {<br>
  <span style="color:#fbbf24">const</span> user = db.find(req.id);<br>
  res.json({ name: "John", role: "Admin" });<br>
});`,
            visual: `<div class="demo-api">{ "name": "John", "role": "Admin" }</div>`
        },
        full: {
            file: "App.js",
            code: `<span style="color:#ec4899">fetch</span>('/api/user')<br>
  .then(res => res.json())<br>
  .then(data => {<br>
    <span style="color:#06b6d4">render</span>(&lt;h1&gt;Hello {data.name}&lt;/h1&gt;);<br>
  });`,
            visual: `<div class="demo-full"><h3>Hello John</h3><p>Role: Admin</p></div>`
        }
    };

    window.switchLab = function (type) {
        // UI Tabs
        tabs.forEach(t => t.classList.remove('active'));
        event.currentTarget.classList.add('active');

        // Update Content with Animation
        codeDisplay.style.opacity = '0';
        visualDisplay.style.opacity = '0';

        setTimeout(() => {
            fileName.innerText = data[type].file;
            codeDisplay.innerHTML = data[type].code;
            visualDisplay.innerHTML = data[type].visual;

            codeDisplay.style.opacity = '1';
            visualDisplay.style.opacity = '1';
        }, 200);
    }

    // Init
    switchLab('front');
});