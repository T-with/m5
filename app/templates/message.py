<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <title>Messages</title>
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <style>
        :root {
            --border: #e2e8f0;
            --bg: #f8fafc;
            --bg-panel: #ffffff;
            --primary: #2563eb;
            --primary-soft: #dbeafe;
            --text: #0f172a;
            --text-muted: #64748b;
            --danger: #b91c1c;
        }

        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            background: var(--bg);
            color: var(--text);
        }

        .page {
            max-width: 1200px;
            margin: 0 auto;
            padding: 16px;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            gap: 12px;
        }

        header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 12px;
        }

        header h1 {
            margin: 0;
            font-size: 1.5rem;
        }

        header .user-info {
            font-size: 0.875rem;
            color: var(--text-muted);
            text-align: right;
        }

        .user-info span.role {
            font-weight: 600;
            text-transform: capitalize;
        }

        .user-info span.id {
            font-family: monospace;
        }

        .layout {
            flex: 1;
            display: grid;
            grid-template-columns: 320px minmax(0, 1fr);
            gap: 12px;
            min-height: 480px;
        }

        @media (max-width: 800px) {
            .layout {
                grid-template-columns: 1fr;
                grid-template-rows: auto auto;
            }
        }

        .panel {
            background: var(--bg-panel);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 12px;
            display: flex;
            flex-direction: column;
            gap: 8px;
        }

        .panel-title {
            font-size: 0.95rem;
            font-weight: 600;
            margin-bottom: 4px;
        }

        .muted {
            color: var(--text-muted);
            font-size: 0.875rem;
        }

        .danger {
            color: var(--danger);
        }

        /* Left panel: search + conversations */

        .search-box {
            display: flex;
            flex-direction: column;
            gap: 4px;
            margin-bottom: 8px;
        }

        .search-box input {
            width: 100%;
            padding: 6px 8px;
            border-radius: 6px;
            border: 1px solid var(--border);
            font-size: 0.9rem;
        }

        .search-results {
            max-height: 150px;
            overflow-y: auto;
            border-radius: 6px;
            border: 1px solid transparent;
        }

        .search-results.has-items {
            border-color: var(--border);
        }

        .search-item {
            padding: 6px 8px;
            font-size: 0.875rem;
            cursor: pointer;
            display: flex;
            flex-direction: column;
            gap: 2px;
        }

        .search-item:hover {
            background: var(--primary-soft);
        }

        .search-item-main {
            display: flex;
            justify-content: space-between;
            gap: 8px;
        }

        .search-item-role {
            font-size: 0.75rem;
            text-transform: capitalize;
            color: var(--text-muted);
        }

        .search-item-email {
            font-size: 0.8rem;
            color: var(--text-muted);
        }

        .conversations-list {
            flex: 1;
            border-radius: 6px;
            border: 1px solid var(--border);
            overflow-y: auto;
        }

        .conversation-item {
            padding: 8px 10px;
            cursor: pointer;
            border-bottom: 1px solid var(--border);
            display: flex;
            flex-direction: column;
            gap: 2px;
        }

        .conversation-item:last-child {
            border-bottom: none;
        }

        .conversation-item.active {
            background: var(--primary-soft);
        }

        .conversation-name {
            font-size: 0.9rem;
            font-weight: 500;
        }

        .conversation-meta {
            display: flex;
            justify-content: space-between;
            gap: 8px;
            font-size: 0.75rem;
            color: var(--text-muted);
        }

        .conversation-last {
            font-size: 0.8rem;
            color: var(--text-muted);
            margin-top: 2px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        /* Right panel: messages */

        .messages-container {
            flex: 1;
            display: flex;
            flex-direction: column;
            border-radius: 6px;
            border: 1px solid var(--border);
            overflow: hidden;
        }

        .messages-header {
            padding: 8px 10px;
            border-bottom: 1px solid var(--border);
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 8px;
            font-size: 0.9rem;
        }

        .messages-header .name {
            font-weight: 600;
        }

        .messages-header .role {
            font-size: 0.8rem;
            color: var(--text-muted);
            text-transform: capitalize;
        }

        .messages-header .id {
            font-size: 0.8rem;
            color: var(--text-muted);
            font-family: monospace;
        }

        .messages-list {
            flex: 1;
            padding: 10px;
            overflow-y: auto;
            background: #f1f5f9;
        }

        .message-row {
            display: flex;
            margin-bottom: 8px;
        }

        .message-row.me {
            justify-content: flex-end;
        }

        .message-bubble {
            max-width: 70%;
            padding: 6px 8px;
            border-radius: 10px;
            font-size: 0.875rem;
            line-height: 1.3;
            background: #ffffff;
            border: 1px solid var(--border);
        }

        .message-row.me .message-bubble {
            background: var(--primary);
            color: #ffffff;
            border-color: var(--primary);
        }

        .message-meta {
            margin-top: 2px;
            font-size: 0.7rem;
            color: var(--text-muted);
            text-align: right;
        }

        .messages-empty {
            flex: 1;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            padding: 24px;
            font-size: 0.9rem;
            color: var(--text-muted);
        }

        .composer {
            border-top: 1px solid var(--border);
            padding: 8px;
            background: var(--bg-panel);
            display: flex;
            gap: 8px;
        }

        .composer textarea {
            flex: 1;
            resize: none;
            min-height: 40px;
            max-height: 120px;
            padding: 6px 8px;
            border-radius: 6px;
            border: 1px solid var(--border);
            font-size: 0.9rem;
        }

        .composer button {
            padding: 6px 12px;
            border-radius: 6px;
            border: none;
            background: var(--primary);
            color: #ffffff;
            font-size: 0.9rem;
            cursor: pointer;
            white-space: nowrap;
        }

        .composer button:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }

        .badge {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            padding: 2px 6px;
            border-radius: 999px;
            border: 1px solid var(--border);
            font-size: 0.7rem;
            color: var(--text-muted);
            background: #f8fafc;
        }

        .badge.me {
            border-color: var(--primary-soft);
            background: var(--primary-soft);
            color: var(--primary);
        }
    </style>
</head>
<body>
<div class="page">
    <header>
        <h1>Messages</h1>
        <div class="user-info" id="current-user-info">
            <!-- Filled by JS -->
        </div>
    </header>

    <div id="auth-warning" class="muted danger" style="display:none;">
        You are not signed in. Messaging requires a logged-in job seeker or evaluator.
        Please sign in from the main application and open this page with your user context.
    </div>

    <div class="layout">
        <!-- LEFT PANEL -->
        <section class="panel" id="left-panel">
            <div class="panel-title">Search users</div>
            <div class="search-box">
                <input
                    id="user-search-input"
                    type="text"
                    placeholder="Search by name or email..."
                    autocomplete="off"
                />
                <div class="muted" style="font-size:0.8rem;">
                    Search job seekers and evaluators to start a conversation.
                </div>
            </div>
            <div id="search-results" class="search-results"></div>

            <div class="panel-title" style="margin-top:8px;">Your conversations</div>
            <div class="conversations-list" id="conversations-list">
                <!-- Conversations injected by JS -->
            </div>
        </section>

        <!-- RIGHT PANEL -->
        <section class="panel">
            <div class="panel-title">Conversation</div>
            <div class="messages-container" id="messages-container">
                <div class="messages-empty" id="messages-empty">
                    Select a conversation on the left, or search for a user to start a new one.
                </div>

                <div class="messages-header" id="messages-header" style="display:none;">
                    <div>
                        <div class="name" id="conv-other-name"></div>
                        <div class="role" id="conv-other-role"></div>
                    </div>
                    <div class="id" id="conv-other-id"></div>
                </div>
                <div class="messages-list" id="messages-list" style="display:none;"></div>

                <div class="composer" id="composer" style="display:none;">
                    <textarea id="message-input" placeholder="Type your message..."></textarea>
                    <button id="send-button" type="button">Send</button>
                </div>
            </div>
        </section>
    </div>
</div>

<!-- Backend can still fill these data attributes; JS also falls back to query params and localStorage -->
<div
    id="messages-app"
    data-user-role="{{ user_role }}"
    data-user-id="{{ user_id }}"
    style="display:none;">
</div>

<script>
    (function () {
        const appRoot = document.getElementById("messages-app");

        function getQueryParam(name) {
            const params = new URLSearchParams(window.location.search);
            return params.get(name);
        }

        // 1. Try backend-injected data attributes
        let currentUserRole = appRoot?.dataset.userRole || "";
        let currentUserIdStr = appRoot?.dataset.userId || "";
        let currentUserName = "";
        let currentUserEmail = "";

        // 2. Fallback to query params (?user_role=...&user_id=...)
        if (!currentUserRole) {
            const qRole = getQueryParam("user_role");
            if (qRole) currentUserRole = qRole;
        }
        if (!currentUserIdStr) {
            const qId = getQueryParam("user_id");
            if (qId) currentUserIdStr = qId;
        }

        // 3. Fallback to localStorage (evaluator or job seeker)
        if (!currentUserRole || !currentUserIdStr) {
            try {
                const lsEvaluatorId    = window.localStorage.getItem("evaluatorId");
                const lsEvaluatorName  = window.localStorage.getItem("evaluatorName");
                const lsEvaluatorEmail = window.localStorage.getItem("evaluatorEmail");

                const lsJobSeekerId    = window.localStorage.getItem("jobSeekerId");
                const lsJobSeekerName  = window.localStorage.getItem("jobSeekerName");
                const lsJobSeekerEmail = window.localStorage.getItem("jobSeekerEmail");

                if (!currentUserIdStr && lsEvaluatorId) {
                    currentUserRole  = "evaluator";
                    currentUserIdStr = lsEvaluatorId;
                    currentUserName  = lsEvaluatorName || "";
                    currentUserEmail = lsEvaluatorEmail || "";
                } else if (!currentUserIdStr && lsJobSeekerId) {
                    currentUserRole  = "job_seeker";
                    currentUserIdStr = lsJobSeekerId;
                    currentUserName  = lsJobSeekerName || "";
                    currentUserEmail = lsJobSeekerEmail || "";
                }
            } catch (e) {
                console.warn("localStorage not accessible", e);
            }
        }

        const currentUserId = currentUserIdStr ? parseInt(currentUserIdStr, 10) : NaN;

        const authWarningEl = document.getElementById("auth-warning");
        const userInfoEl = document.getElementById("current-user-info");

        const searchInput = document.getElementById("user-search-input");
        const searchResultsEl = document.getElementById("search-results");

        const conversationsListEl = document.getElementById("conversations-list");

        const messagesEmptyEl = document.getElementById("messages-empty");
        const messagesHeaderEl = document.getElementById("messages-header");
        const messagesListEl = document.getElementById("messages-list");
        const composerEl = document.getElementById("composer");
        const messageInputEl = document.getElementById("message-input");
        const sendButtonEl = document.getElementById("send-button");

        let selectedConversationId = null;
        let selectedOther = null; // { role, id, name, email }
        const conversationsMeta = {}; // convId -> { other_role, other_id, other_name }

        let searchTimeout = null;

        // ---- helpers ----
        function isAuthenticated() {
            return !!currentUserRole && !Number.isNaN(currentUserId);
        }

        function formatRole(role) {
            if (role === "job_seeker") return "Job seeker";
            if (role === "evaluator") return "Evaluator";
            return role || "Unknown";
        }

        function shortTime(isoString) {
            if (!isoString) return "";
            const d = new Date(isoString);
            if (Number.isNaN(d.getTime())) return isoString;
            return d.toLocaleString();
        }

        function escapeHtml(str) {
            return String(str || "")
                .replace(/&/g, "&amp;")
                .replace(/</g, "&lt;")
                .replace(/>/g, "&gt;");
        }

        function buildConversationId(roleA, idA, roleB, idB) {
            const items = [
                { role: roleA, id: idA },
                { role: roleB, id: idB },
            ];
            items.sort((a, b) => {
                if (a.role < b.role) return -1;
                if (a.role > b.role) return 1;
                return a.id - b.id;
            });
            return `${items[0].role}:${items[0].id}|${items[1].role}:${items[1].id}`;
        }

        async function apiGet(path) {
            const res = await fetch(path, { credentials: "include" });
            if (!res.ok) {
                throw new Error("GET " + path + " failed: " + res.status);
            }
            return res.json();
        }

        async function apiPost(path, body) {
            const res = await fetch(path, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                credentials: "include",
                body: JSON.stringify(body),
            });
            if (!res.ok) {
                const text = await res.text();
                throw new Error("POST " + path + " failed: " + res.status + " " + text);
            }
            return res.json();
        }

        // ---- initial auth UI ----
        if (isAuthenticated()) {
            const namePart = currentUserName
                ? `<div>${escapeHtml(currentUserName)}</div>`
                : "";
            const emailPart = currentUserEmail
                ? `<div>${escapeHtml(currentUserEmail)}</div>`
                : "";

            userInfoEl.innerHTML = `
                ${namePart}
                <div>
                    Signed in as <span class="role">${escapeHtml(formatRole(currentUserRole))}</span>
                </div>
                ${emailPart}
                <div>ID: <span class="id">${escapeHtml(String(currentUserId))}</span></div>
            `;
            authWarningEl.style.display = "none";
        } else {
            userInfoEl.innerHTML = `<span class="danger">Not signed in</span>`;
            authWarningEl.style.display = "block";
            // Disable inputs so user can’t use messaging without context
            searchInput.disabled = true;
            messageInputEl.disabled = true;
            sendButtonEl.disabled = true;
        }

        // ---- conversations ----
        async function loadConversations() {
            if (!isAuthenticated()) return;
            conversationsListEl.innerHTML = `<div class="muted" style="padding:8px;">Loading conversations...</div>`;
            try {
                const data = await apiGet(
                    `/api/messages/conversations?user_role=${encodeURIComponent(
                        currentUserRole
                    )}&user_id=${encodeURIComponent(currentUserId)}`
                );

                conversationsListEl.innerHTML = "";
                Object.keys(conversationsMeta).forEach((k) => delete conversationsMeta[k]);

                if (!data || data.length === 0) {
                    conversationsListEl.innerHTML =
                        `<div class="muted" style="padding:8px;">No conversations yet.</div>`;
                    return;
                }

                data.forEach((c) => {
                    conversationsMeta[c.conversation_id] = {
                        other_role: c.other_party_role,
                        other_id: c.other_party_id,
                        other_name: c.other_party_name,
                    };

                    const item = document.createElement("div");
                    item.className = "conversation-item";
                    item.dataset.conversationId = c.conversation_id;

                    if (c.conversation_id === selectedConversationId) {
                        item.classList.add("active");
                    }

                    const name = escapeHtml(c.other_party_name || "(no name)");
                    const lastMsg = escapeHtml(c.last_message || "");
                    const time = shortTime(c.last_message_time);
                    const roleLabel = formatRole(c.other_party_role);

                    item.innerHTML = `
                        <div class="conversation-name">${name}</div>
                        <div class="conversation-meta">
                            <span>${escapeHtml(roleLabel)}</span>
                            <span>${escapeHtml(time)}</span>
                        </div>
                        <div class="conversation-last">${lastMsg}</div>
                    `;

                    item.addEventListener("click", () => {
                        selectConversationFromList(c.conversation_id);
                    });

                    conversationsListEl.appendChild(item);
                });
            } catch (err) {
                console.error(err);
                conversationsListEl.innerHTML =
                    `<div class="muted danger" style="padding:8px;">Failed to load conversations.</div>`;
            }
        }

        function highlightActiveConversation() {
            const items = conversationsListEl.querySelectorAll(".conversation-item");
            items.forEach((el) => {
                if (el.dataset.conversationId === selectedConversationId) {
                    el.classList.add("active");
                } else {
                    el.classList.remove("active");
                }
            });
        }

        async function selectConversationFromList(conversationId) {
            selectedConversationId = conversationId;
            const meta = conversationsMeta[conversationId] || null;

            if (meta) {
                selectedOther = {
                    role: meta.other_role,
                    id: meta.other_id,
                    name: meta.other_name,
                };
            } else {
                selectedOther = null;
            }

            highlightActiveConversation();
            await loadMessages(conversationId);
        }

        // ---- messages ----
        async function loadMessages(conversationId) {
            if (!isAuthenticated()) return;

            messagesEmptyEl.style.display = "none";
            messagesHeaderEl.style.display = "flex";
            messagesListEl.style.display = "block";
            composerEl.style.display = "flex";

            messagesListEl.innerHTML = `<div class="muted">Loading messages...</div>`;

            try {
                const data = await apiGet(
                    `/api/messages/conversations/${encodeURIComponent(conversationId)}`
                );

                const other = selectedOther;
                if (other) {
                    document.getElementById("conv-other-name").textContent =
                        other.name || "(no name)";
                    document.getElementById("conv-other-role").textContent =
                        formatRole(other.role);
                    document.getElementById("conv-other-id").textContent =
                        `ID: ${other.id}`;
                } else if (data && data.length > 0) {
                    // Derive from first message as fallback
                    const first = data[0];
                    const isSenderMe =
                        first.sender_role === currentUserRole &&
                        first.sender_id === currentUserId;
                    const otherRole = isSenderMe ? first.receiver_role : first.sender_role;
                    const otherId = isSenderMe ? first.receiver_id : first.sender_id;
                    const otherName = isSenderMe
                        ? first.receiver_name
                        : first.sender_name;

                    selectedOther = {
                        role: otherRole,
                        id: otherId,
                        name: otherName,
                    };
                    document.getElementById("conv-other-name").textContent =
                        otherName || "(no name)";
                    document.getElementById("conv-other-role").textContent =
                        formatRole(otherRole);
                    document.getElementById("conv-other-id").textContent =
                        `ID: ${otherId}`;
                } else {
                    document.getElementById("conv-other-name").textContent =
                        selectedOther?.name || "(no name)";
                    document.getElementById("conv-other-role").textContent =
                        selectedOther ? formatRole(selectedOther.role) : "";
                    document.getElementById("conv-other-id").textContent =
                        selectedOther ? `ID: ${selectedOther.id}` : "";
                }

                if (!data || data.length === 0) {
                    messagesListEl.innerHTML =
                        `<div class="muted">No messages yet. Say hi!</div>`;
                    return;
                }

                messagesListEl.innerHTML = "";
                data.forEach((m) => {
                    const me =
                        m.sender_role === currentUserRole &&
                        m.sender_id === currentUserId;
                    const row = document.createElement("div");
                    row.className = "message-row" + (me ? " me" : "");

                    const bubble = document.createElement("div");
                    bubble.className = "message-bubble";

                    const content = document.createElement("div");
                    content.textContent = m.content || "";

                    const meta = document.createElement("div");
                    meta.className = "message-meta";
                    const badgeClass = me ? "badge me" : "badge";
                    const whoLabel = me ? "You" : "Them";

                    meta.innerHTML = `
                        <span class="${badgeClass}">${whoLabel}</span>
                        &nbsp;·&nbsp;
                        <span>${escapeHtml(shortTime(m.created_at))}</span>
                    `;

                    bubble.appendChild(content);
                    bubble.appendChild(meta);
                    row.appendChild(bubble);
                    messagesListEl.appendChild(row);
                });

                // Scroll to bottom
                messagesListEl.scrollTop = messagesListEl.scrollHeight;
            } catch (err) {
                console.error(err);
                messagesListEl.innerHTML =
                    `<div class="muted danger">Failed to load messages.</div>`;
            }
        }

        // ---- start conversation from a search result ----
        function clearSearchResults() {
            searchResultsEl.innerHTML = "";
            searchResultsEl.classList.remove("has-items");
        }

        async function performSearch(term) {
            if (!isAuthenticated()) return;
            const q = term.trim().toLowerCase();
            if (!q) {
                clearSearchResults();
                return;
            }

            searchResultsEl.innerHTML = `<div class="muted" style="padding:4px 8px;">Searching...</div>`;
            searchResultsEl.classList.add("has-items");

            try {
                // Use existing APIs: freelancers (job seekers) + evaluators
                const [freelancers, evaluators] = await Promise.all([
                    apiGet("/api/freelancers").catch(err => {
                        console.error("Failed to load freelancers for search:", err);
                        return [];
                    }),
                    apiGet("/api/evaluators").catch(err => {
                        console.warn("Evaluators search endpoint not available:", err);
                        return [];
                    })
                ]);

                const results = [];

                // Job seekers
                (freelancers || []).forEach(f => {
                    const name = (f.name || "").toLowerCase();
                    const email = (f.email || "").toLowerCase();
                    if (name.includes(q) || email.includes(q)) {
                        results.push({
                            id: f.id,
                            role: "job_seeker",
                            name: f.name,
                            email: f.email
                        });
                    }
                });

                // Evaluators (don’t include yourself)
                (evaluators || []).forEach(e => {
                    const name = (e.name || "").toLowerCase();
                    const email = (e.email || "").toLowerCase();
                    if (
                        (name.includes(q) || email.includes(q)) &&
                        !(currentUserRole === "evaluator" && e.id === currentUserId)
                    ) {
                        results.push({
                            id: e.id,
                            role: "evaluator",
                            name: e.name,
                            email: e.email
                        });
                    }
                });

                if (results.length === 0) {
                    searchResultsEl.innerHTML =
                        `<div class="muted" style="padding:4px 8px;">No users found.</div>`;
                    return;
                }

                searchResultsEl.innerHTML = "";
                results.forEach(u => {
                    const item = document.createElement("div");
                    item.className = "search-item";

                    const name = escapeHtml(u.name || "(no name)");
                    const email = escapeHtml(u.email || "");
                    const roleLabel = formatRole(u.role);

                    item.innerHTML = `
                        <div class="search-item-main">
                            <span>${name}</span>
                            <span class="search-item-role">${escapeHtml(roleLabel)}</span>
                        </div>
                        <div class="search-item-email">${email}</div>
                    `;

                    item.addEventListener("click", () => {
                        handleStartConversationFromSearch(u);
                        clearSearchResults();
                        searchInput.value = "";
                    });

                    searchResultsEl.appendChild(item);
                });
            } catch (err) {
                console.error("Search error:", err);
                searchResultsEl.innerHTML =
                    `<div class="muted danger" style="padding:4px 8px;">Search failed. Please try again.</div>`;
            }
        }

        async function handleStartConversationFromSearch(user) {
            if (!isAuthenticated()) return;
            if (!user || !user.role || user.id == null) return;

            const convId = buildConversationId(
                currentUserRole,
                currentUserId,
                user.role,
                user.id
            );

            selectedConversationId = convId;
            selectedOther = {
                role: user.role,
                id: user.id,
                name: user.name || "(no name)",
                email: user.email || ""
            };

            if (!conversationsMeta[convId]) {
                conversationsMeta[convId] = {
                    other_role: user.role,
                    other_id: user.id,
                    other_name: user.name || "(no name)"
                };
            }

            highlightActiveConversation();
            await loadMessages(convId);
        }

        // ---- sending ----
        async function handleSend() {
            if (!isAuthenticated() || !selectedOther || !selectedConversationId) return;
            const text = messageInputEl.value.trim();
            if (!text) return;

            sendButtonEl.disabled = true;

            try {
                await apiPost("/api/messages", {
                    sender_role: currentUserRole,
                    sender_id: currentUserId,
                    receiver_role: selectedOther.role,
                    receiver_id: selectedOther.id,
                    content: text,
                });

                messageInputEl.value = "";
                await loadMessages(selectedConversationId);
                await loadConversations();
            } catch (err) {
                console.error(err);
                alert("Failed to send message.");
            } finally {
                sendButtonEl.disabled = false;
            }
        }

        sendButtonEl.addEventListener("click", handleSend);
        messageInputEl.addEventListener("keydown", (e) => {
            if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                handleSend();
            }
        });

        // ---- search input listener ----
        searchInput.addEventListener("input", (e) => {
            const term = e.target.value;
            if (searchTimeout) {
                clearTimeout(searchTimeout);
            }
            if (!term.trim()) {
                clearSearchResults();
                return;
            }
            searchTimeout = setTimeout(() => performSearch(term), 250);
        });

        // ---- auto-open conversation from URL (freelancer_id) ----
        function getFreelancerIdFromUrl() {
            const params = new URLSearchParams(window.location.search);
            return params.get("freelancer_id");
        }

        async function openConversationForFreelancerIfProvided() {
            const fidStr = getFreelancerIdFromUrl();
            if (!fidStr) return;
            const fid = parseInt(fidStr, 10);
            if (Number.isNaN(fid)) return;
            if (!isAuthenticated()) return;

            try {
                const freelancer = await apiGet(`/api/freelancers/${fid}`);
                const user = {
                    id: freelancer.id,
                    role: "job_seeker",
                    name: freelancer.name,
                    email: freelancer.email,
                };
                await handleStartConversationFromSearch(user);
            } catch (err) {
                console.error("Failed to pre-open freelancer conversation", err);
                const user = {
                    id: fid,
                    role: "job_seeker",
                    name: `Job Seeker #${fid}`,
                    email: "",
                };
                await handleStartConversationFromSearch(user);
            }
        }

        // ---- initial load ----
        if (isAuthenticated()) {
            loadConversations().then(openConversationForFreelancerIfProvided);
        }
    })();
</script>
</body>
</html>

