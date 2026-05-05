// ====== CSRF Helper ======
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let c of cookies) {
      c = c.trim();
      if (c.startsWith(name + '=')) {
        cookieValue = decodeURIComponent(c.slice(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

const CSRF = getCookie('csrftoken');

function postJSON(url, data) {
  return fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'X-CSRFToken': CSRF },
    body: JSON.stringify(data),
  }).then(r => r.json());
}

function postForm(url, formData) {
  return fetch(url, {
    method: 'POST',
    headers: { 'X-CSRFToken': CSRF },
    body: formData,
  }).then(r => r.json());
}

// ====== Лайк ======
document.addEventListener('click', e => {
  const btn = e.target.closest('.like-btn');
  if (!btn) return;
  e.preventDefault();
  const url = btn.dataset.url;
  fetch(url, { method: 'POST', headers: { 'X-CSRFToken': CSRF } })
    .then(r => r.json())
    .then(data => {
      if (data.liked !== undefined) {
        btn.classList.toggle('liked', data.liked);
        const counter = btn.closest('[data-like-counter]') || document.querySelector('.like-counter');
        if (counter) counter.textContent = data.count;
      } else if (data.detail === 'Учетные данные не были предоставлены.' || data.detail) {
        window.location = '/accounts/login/';
      }
    });
});

// ====== Добавление комментария ======
const commentForm = document.getElementById('comment-form');
if (commentForm) {
  commentForm.addEventListener('submit', e => {
    e.preventDefault();
    const text = commentForm.querySelector('textarea').value.trim();
    if (!text) return;
    const url = commentForm.dataset.url;
    postJSON(url, { text }).then(data => {
      if (data.ok) {
        commentForm.querySelector('textarea').value = '';
        const list = document.getElementById('comments-list');
        const div = document.createElement('div');
        div.className = 'notification-item';
        const avatarHtml = data.comment.avatar
          ? `<img src="${data.comment.avatar}" class="comment-avatar" alt="">`
          : `<div class="comment-avatar-placeholder"><i class="bi bi-person"></i></div>`;
        div.innerHTML = `
          ${avatarHtml}
          <div>
            <strong class="d-block" style="font-size:0.9rem">${data.comment.user}</strong>
            <p class="mb-0" style="font-size:0.9rem;color:var(--text)">${data.comment.text}</p>
            <small class="text-muted-custom">${data.comment.date}</small>
          </div>`;
        list.prepend(div);
        const counter = document.querySelector('.comment-counter');
        if (counter) counter.textContent = parseInt(counter.textContent || 0) + 1;
      }
    });
  });
}

// ====== Отправка сообщения ======
const messageForm = document.getElementById('message-form');
if (messageForm) {
  messageForm.addEventListener('submit', e => {
    e.preventDefault();
    const fd = new FormData(messageForm);
    const url = messageForm.dataset.url;
    postForm(url, fd).then(data => {
      if (data.ok) {
        messageForm.querySelector('textarea').value = '';
        const fileInput = messageForm.querySelector('input[type=file]');
        if (fileInput) fileInput.value = '';
        appendBubble(data.message);
        const chat = document.getElementById('chat-container');
        if (chat) chat.scrollTop = chat.scrollHeight;
      }
    });
  });
}

function appendBubble(msg) {
  const chat = document.getElementById('chat-container');
  if (!chat) return;
  const div = document.createElement('div');
  div.className = 'd-flex ' + (msg.is_mine ? 'justify-content-end' : 'justify-content-start');
  let content = msg.text ? `<span>${escapeHtml(msg.text)}</span>` : '';
  if (msg.image) content += `<br><img src="${msg.image}" style="max-width:200px;border-radius:8px;margin-top:6px">`;
  div.innerHTML = `
    <div class="bubble bubble-${msg.is_mine ? 'mine' : 'other'}">
      ${content}
      <small class="bubble-time">${msg.time}</small>
    </div>`;
  chat.appendChild(div);
  chat.scrollTop = chat.scrollHeight;
}

function escapeHtml(s) {
  return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}

// ====== Счётчик непрочитанных (опрос каждые 10 сек) ======
function pollUnread() {
  fetch('/messages/api/unread/')
    .then(r => r.json())
    .then(d => {
      const badge = document.getElementById('msg-badge');
      if (badge) {
        badge.textContent = d.count || '';
        badge.style.display = d.count ? 'inline' : 'none';
      }
    }).catch(() => {});
}

if (document.getElementById('msg-badge')) {
  pollUnread();
  setInterval(pollUnread, 10000);
}

// ====== Подписка ======
document.addEventListener('click', e => {
  const btn = e.target.closest('.follow-btn');
  if (!btn) return;
  e.preventDefault();
  const url = btn.dataset.url;
  fetch(url, { method: 'POST', headers: { 'X-CSRFToken': CSRF } })
    .then(r => r.json())
    .then(d => {
      if (d.following !== undefined) {
        btn.classList.toggle('btn-accent', d.following);
        btn.classList.toggle('btn-ghost', !d.following);
        btn.innerHTML = d.following
          ? '<i class="bi bi-person-check-fill me-1"></i>Вы подписаны'
          : '<i class="bi bi-person-plus me-1"></i>Подписаться';
        const fc = document.querySelector('.followers-count');
        if (fc) fc.textContent = d.count;
      }
    });
});

// ====== Пометить уведомления прочитанными ======
const markAllBtn = document.getElementById('mark-all-read');
if (markAllBtn) {
  markAllBtn.addEventListener('click', () => {
    fetch('/notifications/read-all/', { method: 'POST', headers: { 'X-CSRFToken': CSRF } })
      .then(r => r.json())
      .then(() => {
        document.querySelectorAll('.notification-item.unread').forEach(el => el.classList.remove('unread'));
        const nb = document.getElementById('notif-badge');
        if (nb) { nb.textContent = ''; nb.style.display = 'none'; }
      });
  });
}

// ====== Выбор координат на карте (профиль) ======
window.initProfileMap = function(lat, lng) {
  const mapEl = document.getElementById('profile-map-picker');
  if (!mapEl) return;
  const initLat = lat || 55.7558;
  const initLng = lng || 37.6173;
  const map = L.map('profile-map-picker').setView([initLat, initLng], lat ? 10 : 5);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
  }).addTo(map);
  let marker = null;
  if (lat && lng) {
    marker = L.marker([lat, lng]).addTo(map);
  }
  map.on('click', e => {
    const { lat, lng } = e.latlng;
    document.getElementById('id_latitude').value = lat.toFixed(6);
    document.getElementById('id_longitude').value = lng.toFixed(6);
    if (marker) marker.setLatLng([lat, lng]);
    else marker = L.marker([lat, lng]).addTo(map);
  });
};

// ====== Карта создателей ======
window.initCreatorsMap = function() {
  const mapEl = document.getElementById('map');
  if (!mapEl) return;
  const map = L.map('map').setView([60, 55], 4);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
  }).addTo(map);

  const typeFilter = document.getElementById('type-filter');

  function loadCreators() {
    const type = typeFilter ? typeFilter.value : '';
    let url = '/map/api/creators/';
    if (type) url += '?type=' + type;
    fetch(url).then(r => r.json()).then(data => {
      map.eachLayer(l => { if (l instanceof L.Marker) map.removeLayer(l); });
      data.creators.forEach(c => {
        const icon = L.divIcon({
          className: '',
          html: `<div style="width:40px;height:40px;border-radius:50%;border:2px solid #F5A623;overflow:hidden;box-shadow:0 2px 10px rgba(0,0,0,0.5)">
                   ${c.avatar ? `<img src="${c.avatar}" style="width:100%;height:100%;object-fit:cover">` : '<div style="width:100%;height:100%;background:#1C1C1C;display:flex;align-items:center;justify-content:center;color:#888">👤</div>'}
                 </div>`,
          iconSize: [40, 40],
          iconAnchor: [20, 20],
        });
        const marker = L.marker([c.lat, c.lng], { icon }).addTo(map);
        marker.bindPopup(`
          <div style="min-width:180px;color:#F0F0F0">
            <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px">
              ${c.avatar ? `<img src="${c.avatar}" style="width:44px;height:44px;border-radius:50%;object-fit:cover">` : ''}
              <div>
                <strong style="display:block">${c.name}</strong>
                <span style="color:#F5A623;font-size:0.8rem">${c.creator_type}</span>
              </div>
            </div>
            <div style="color:#888;font-size:0.8rem;margin-bottom:8px">${c.city}${c.specialization ? ' · ' + c.specialization : ''}</div>
            <a href="${c.url}" style="color:#F5A623;font-size:0.85rem">Открыть профиль →</a>
          </div>
        `);
      });
    });
  }

  loadCreators();
  if (typeFilter) typeFilter.addEventListener('change', loadCreators);
};

// ====== Таблицы администратора (toggle) ======
document.addEventListener('click', e => {
  const btn = e.target.closest('[data-toggle-url]');
  if (!btn) return;
  e.preventDefault();
  const url = btn.dataset.toggleUrl;
  fetch(url, { method: 'POST', headers: { 'X-CSRFToken': CSRF } })
    .then(r => r.json())
    .then(d => {
      const key = Object.keys(d)[0];
      const val = d[key];
      const indicator = btn.closest('tr').querySelector('.toggle-indicator');
      if (indicator) {
        if (val) {
          indicator.innerHTML = '<span class="text-success"><i class="bi bi-check-circle-fill"></i></span>';
        } else {
          indicator.innerHTML = '<span class="text-muted"><i class="bi bi-x-circle"></i></span>';
        }
      }
      btn.textContent = val ? 'Выкл.' : 'Вкл.';
    });
});

// ====== Auto-scroll чата ======
const chatContainer = document.getElementById('chat-container');
if (chatContainer) {
  chatContainer.scrollTop = chatContainer.scrollHeight;
}
