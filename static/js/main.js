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

  const initLat = Number.isFinite(lat) ? lat : 55.7558;
  const initLng = Number.isFinite(lng) ? lng : 37.6173;
  const zoom = lat && lng ? 10 : 5;
  const marker = `pm2rdm1`;
  const mapUrl = `https://static-maps.yandex.ru/1.x/?lang=ru_RU&l=map&size=650,300&ll=${initLng.toFixed(6)},${initLat.toFixed(6)}&z=${zoom}&pt=${initLng.toFixed(6)},${initLat.toFixed(6)},${marker}`;

  mapEl.innerHTML = `<img src="${mapUrl}" alt="Яндекс карта профиля" style="width:100%;display:block;border-radius:12px;border:1px solid var(--border);background:var(--bg2)">`;
};

// ====== Карта создателей ======
window.initCreatorsMap = function() {
  const mapEl = document.getElementById('map');
  if (!mapEl) return;

  const typeFilter = document.getElementById('type-filter');
  const fallbackCenter = { lat: 55.751244, lng: 37.618423 };

  function buildMapUrl(creators) {
    const center = creators.length
      ? creators.reduce((acc, creator) => ({
          lat: acc.lat + Number(creator.lat || 0),
          lng: acc.lng + Number(creator.lng || 0),
        }), { lat: 0, lng: 0 })
      : fallbackCenter;

    if (creators.length) {
      center.lat /= creators.length;
      center.lng /= creators.length;
    }

    const zoom = creators.length > 6 ? 3 : creators.length > 3 ? 4 : 5;
    const points = creators.map((creator, index) => {
      const markerType = `pm2rdm${(index % 9) + 1}`;
      return `${Number(creator.lng).toFixed(6)},${Number(creator.lat).toFixed(6)},${markerType}`;
    }).join('~');

    const baseUrl = 'https://static-maps.yandex.ru/1.x/?lang=ru_RU&l=map&size=650,450';
    const ll = `&ll=${center.lng.toFixed(6)},${center.lat.toFixed(6)}`;
    const z = `&z=${zoom}`;
    const pt = points ? `&pt=${points}` : '';
    return `${baseUrl}${ll}${z}${pt}`;
  }

  function renderMap(creators) {
    const mapUrl = buildMapUrl(creators);
    mapEl.innerHTML = `<img src="${mapUrl}" alt="Яндекс карта специалистов" style="width:100%;display:block;border-radius:var(--radius);border:1px solid var(--border);background:var(--bg2)">`;
  }

  function loadCreators() {
    const type = typeFilter ? typeFilter.value : '';
    let url = '/map/api/creators/';
    if (type) url += '?type=' + type;

    fetch(url)
      .then(r => r.json())
      .then(data => {
        renderMap(Array.isArray(data.creators) ? data.creators : []);
      })
      .catch(() => {
        mapEl.innerHTML = '<div class="card p-4 text-center" style="border:1px solid var(--border)">Карта временно недоступна</div>';
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
