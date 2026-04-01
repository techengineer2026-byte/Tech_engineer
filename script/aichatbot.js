const WEBHOOK_URL = 'https://codingmerijan.app.n8n.cloud/webhook/TEAgent';

let currentSessionId = '';
let selectedCategory = '';
let userName = '';
let chatOpen = false;
let queryCount = 0;
// ======================== TOGGLE ========================
function toggleChat() {
    chatOpen = !chatOpen;
    const win = document.getElementById('chatWindow');
    const btn = document.getElementById('chatToggle');
    const badge = document.getElementById('chatBadge');

    if (chatOpen) {
        win.classList.add('open');
        btn.classList.add('active');
        badge.style.display = 'none';
    } else {
        win.classList.remove('open');
        btn.classList.remove('active');
    }
}

// ======================== CHIPS ========================
function loadChips(category) {
    const c = document.getElementById('quickActions');
    if (category === 'training') {
        c.innerHTML = `
                <span class="chip" onclick="quickAsk('What courses do you offer?')">📚 Courses</span>
                <span class="chip" onclick="quickAsk('Tell me about fees')">💰 Fees</span>
                <span class="chip" onclick="quickAsk('Do you give certificates?')">📜 Certificate</span>
                <span class="chip" onclick="quickAsk('Placement support?')">💼 Placement</span>
            `;
    } else {
        c.innerHTML = `
                <span class="chip" onclick="quickAsk('What IT services do you provide?')">🛠️ Services</span>
                <span class="chip" onclick="quickAsk('Tell me about pricing')">💰 Pricing</span>
                <span class="chip" onclick="quickAsk('How can AI help my business?')">🤖 AI Solutions</span>
                <span class="chip" onclick="quickAsk('Do you build custom software?')">💻 Custom Dev</span>
            `;
    }
}

// ======================== SUBMIT LEAD ========================
async function submitLead() {
    const name = document.getElementById('userName').value.trim();
    const email = document.getElementById('userEmail').value.trim();
    const phone = document.getElementById('userPhone').value.trim();
    const category = document.getElementById('userCategory').value;

    selectedCategory = category;
    userName = name;

    if (!name || !email || !phone) { shakeButton(); return; }

    const btn = document.getElementById('btnStart');
    btn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span> Connecting...';
    btn.disabled = true;

    currentSessionId = crypto.randomUUID();
    globalPhone = phone;
    globalEmail = email;

    const payload = {
        Name: name,
        Phone: phone,
        Email: email,
        category: category,
        isFirstMessage: true,
        QueryCount: 0,
        query: "Hi",
        SessionId: currentSessionId
    };

    console.log('Sending LEAD:', payload);

    try {
        const response = await fetch(WEBHOOK_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (response.ok) {
            document.getElementById('leadForm').style.display = 'none';
            document.getElementById('chatInterface').style.display = 'flex';

            const label = category === 'training'
                ? 'AI & IT Training'
                : 'IT Services & Automation';

            addMessage('ai', `Hi ${name}! 👋 Welcome to Tech Engineer. I'm here to help you with <strong>${label}</strong>. What would you like to know?`);
            loadChips(category);
        } else {
            alert('Server error. Try again.');
            btn.innerHTML = '<i class="bi bi-chat-dots me-2"></i> Start Chatting';
            btn.disabled = false;
        }
    } catch (error) {
        console.error('Failed:', error);
        alert('Could not connect.');
        btn.innerHTML = '<i class="bi bi-chat-dots me-2"></i> Start Chatting';
        btn.disabled = false;
    }
}

// ======================== SEND MESSAGE ========================

async function sendMessage() {
    const input = document.getElementById('chatInput');
    const text = input.value.trim();
    if (!text) return;

    addMessage('user', text);
    input.value = '';

    const btn = document.getElementById('btnSend');
    btn.disabled = true;
    showTyping();

    queryCount++;

    try {
        const response = await fetch(WEBHOOK_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                SessionId: currentSessionId,
                category: selectedCategory,
                isFirstMessage: false,
                QueryCount: queryCount,
                query: text
            })
        });
        removeTyping();

        const rawText = await response.text();
        console.log('n8n raw response:', rawText);
        console.log('Response status:', response.status);

        let reply = '';


        try {
            const data = JSON.parse(rawText);

            if (typeof data === 'string') {
                reply = data;
            } else if (Array.isArray(data)) {
                const f = data[0] || {};
                reply = f.output
                    || f.reply
                    || f.text
                    || f.response
                    || f.message
                    || f.answer
                    || f.result
                    || JSON.stringify(f);
            } else if (typeof data === 'object') {
                reply = data.output
                    || data.reply
                    || data.text
                    || data.response
                    || data.message
                    || data.answer
                    || data.result
                    || JSON.stringify(data);
            }
        } catch (e) {
            reply = rawText;
        }

        addMessage('ai', reply);

    } catch (error) {
        removeTyping();
        console.error('Chat error:', error);
        addMessage('ai', 'Connection lost. Please try again.');
    }

    btn.disabled = false;
    input.focus();
}

// ======================== HELPERS ========================
function quickAsk(q) {
    document.getElementById('chatInput').value = q;
    sendMessage();
    document.getElementById('quickActions').style.display = 'none';
}

function addMessage(type, text) {
    const c = document.getElementById('chatMessages');
    const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    c.insertAdjacentHTML('beforeend', `
            <div class="msg ${type}">
                <div class="msg-avatar"><i class="bi bi-${type === 'ai' ? 'robot' : 'person-fill'}"></i></div>
                <div>
                    <div class="bubble">${text}</div>
                    <span class="msg-time">${time}</span>
                </div>
            </div>
        `);
    c.scrollTop = c.scrollHeight;
}

function showTyping() {
    const c = document.getElementById('chatMessages');
    c.insertAdjacentHTML('beforeend', `
            <div class="msg ai" id="typingMsg">
                <div class="msg-avatar"><i class="bi bi-robot"></i></div>
                <div class="bubble">
                    <div class="typing-indicator"><span></span><span></span><span></span></div>
                </div>
            </div>
        `);
    c.scrollTop = c.scrollHeight;
}

function removeTyping() {
    const el = document.getElementById('typingMsg');
    if (el) el.remove();
}

function shakeButton() {
    const btn = document.getElementById('btnStart');
    btn.style.animation = 'none';
    btn.offsetHeight;
    btn.style.animation = 'shake 0.5s ease';
    ['userName', 'userEmail', 'userPhone'].forEach(id => {
        const f = document.getElementById(id);
        if (!f.value.trim()) {
            f.style.borderColor = 'var(--secondary)';
            f.style.boxShadow = '0 0 12px rgba(255,101,132,0.3)';
            setTimeout(() => { f.style.borderColor = ''; f.style.boxShadow = ''; }, 2000);
        }
    });
}

const s = document.createElement('style');
s.textContent = `@keyframes shake{0%,100%{transform:translateX(0)}20%{transform:translateX(-8px)}40%{transform:translateX(8px)}60%{transform:translateX(-5px)}80%{transform:translateX(5px)}}`;
document.head.appendChild(s);

console.log('Chatbot ready. Webhook:', WEBHOOK_URL);