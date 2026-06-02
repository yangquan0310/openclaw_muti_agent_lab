#!/usr/bin/env node
// 走完整设备身份认证 → 拿到 admin scope → 创建测试卡
import { randomUUID, generateKeyPairSync, createSign, createHash, webcrypto } from "node:crypto";
import { subtle } from "node:crypto";

const TOKEN = process.env.OPENCLAW_GATEWAY_TOKEN;
const GATEWAY_URL = "ws://127.0.0.1:18098";
if (!TOKEN) { console.error("OPENCLAW_GATEWAY_TOKEN not set"); process.exit(1); }

const ws = new WebSocket(GATEWAY_URL);
const pending = new Map();
let seq = 0;

function send(method, params) {
  const id = `req-${++seq}`;
  return new Promise((resolve, reject) => {
    pending.set(id, { resolve, reject, method });
    ws.send(JSON.stringify({ type: "req", id, method, params }));
  });
}
function withTimeout(p, ms, label) {
  return Promise.race([p, new Promise((_, r) => setTimeout(() => r(new Error(`timeout: ${label}`)), ms))]);
}

// Ed25519 设备身份 (Web Crypto 风格)
async function genDeviceIdentity() {
  const { publicKey, privateKey } = await subtle.generateKey({ name: "Ed25519" }, true, ["sign", "verify"]);
  const pubRaw = await subtle.exportKey("raw", publicKey);
  const privJwk = await subtle.exportKey("jwk", privateKey);
  const pubB64 = Buffer.from(pubRaw).toString("base64").replaceAll("+", "-").replaceAll("/", "_").replace(/=+$/, "");
  const deviceId = createHash("sha256").update(Buffer.from(pubRaw)).digest("hex");
  return { deviceId, publicKey: pubB64, privateKeyJwk: privJwk };
}
async function signPayload(privJwk, payload) {
  const privateKey = await subtle.importKey("jwk", privJwk, { name: "Ed25519" }, false, ["sign"]);
  const sig = await subtle.sign("Ed25519", privateKey, new TextEncoder().encode(payload));
  return Buffer.from(sig).toString("base64").replaceAll("+", "-").replaceAll("/", "_").replace(/=+$/, "");
}
function buildDeviceSigPayload({ deviceId, clientId, clientMode, role, scopes, signedAtMs, token, nonce }) {
  const v = ["v2", deviceId, clientId, clientMode, role, scopes.join(","), String(signedAtMs), token, nonce].join("|");
  return v;
}

let connectNonce = null;
let identity = null;

ws.addEventListener("message", async (ev) => {
  const msg = JSON.parse(ev.data);
  if (msg.type === "event") {
    if (msg.event === "connect.challenge") {
      connectNonce = msg.payload?.nonce || null;
      console.log("[challenge] nonce:", connectNonce?.slice(0, 16) + "...");
      identity = await genDeviceIdentity();
      const signedAtMs = Date.now();
      const scopes = ["operator.admin", "operator.read", "operator.write", "operator.approvals", "operator.pairing"];
      const sigPayload = buildDeviceSigPayload({
        deviceId: identity.deviceId,
        clientId: "cli",
        clientMode: "cli",
        role: "operator",
        scopes,
        signedAtMs,
        token: TOKEN,
        nonce: connectNonce,
      });
      const signature = await signPayload(identity.privateKeyJwk, sigPayload);
      const device = { id: identity.deviceId, publicKey: identity.publicKey, signature, signedAt: signedAtMs, nonce: connectNonce };
      try {
        const hello = await withTimeout(send("connect", {
          minProtocol: 4, maxProtocol: 4,
          client: { id: "cli", version: "smoke-test", platform: "node", mode: "cli" },
          role: "operator", scopes,
          device, caps: ["tool-events"],
          auth: { token: TOKEN },
        }), 10000, "connect");
        console.log("[hello] auth.scopes:", JSON.stringify(hello?.auth?.scopes));
        if (!hello?.auth?.scopes?.includes("operator.admin")) {
          console.log("[!] scopes 不含 admin，设备可能未配对");
        }
      } catch (e) {
        console.log("[connect err]", e.message, JSON.stringify(e.details || {}));
        process.exit(1);
      }
    }
    return;
  }
  if (msg.type === "res") {
    const handler = pending.get(msg.id);
    if (handler) {
      pending.delete(msg.id);
      if (msg.ok) handler.resolve(msg.payload);
      else handler.reject(Object.assign(new Error(msg.error?.message || "rpc error"), { code: msg.error?.code, details: msg.error?.details }));
    }
  }
});
ws.addEventListener("close", (ev) => console.log(`[ws] close code=${ev.code}`));

async function main() {
  await new Promise((r) => ws.addEventListener("open", r, { once: true }));
  // 等 connect 流程
  await new Promise((r) => setTimeout(r, 1500));

  console.log("\n=== 1. 建卡 ===");
  let created;
  try {
    created = await withTimeout(send("workboard.cards.create", {
      title: "🧪 烟测卡 - Workboard 全流程验证",
      notes: "这是大管家创建的第一张测试卡，用于验证：建卡 → 列卡 → 认领 → 评论 → 续约 → 释放 → 归档 全链路。",
      status: "todo", priority: "normal",
      labels: ["smoke-test", "workboard", "steward"],
      agentId: "steward",
    }), 10000, "cards.create");
  } catch (e) {
    console.log("[create err]", e.message, JSON.stringify(e.details || {}, null, 2));
    if (e.code === "AUTH_TOKEN_MISMATCH" || /pairing/i.test(e.message)) {
      console.log("\n[!] 需要先在 Dashboard 里批准设备配对");
      console.log("    请打开 http://10.0.0.9:18098/estqvr/ 同意配对请求");
    }
    ws.close();
    process.exit(1);
  }
  const cardId = created.card.id;
  console.log(`✅ 创建成功: ${cardId}`);
  console.log(`   标题: ${created.card.title}`);

  console.log("\n=== 2. 列卡 ===");
  const list = await withTimeout(send("workboard.cards.list", {}), 10000, "cards.list");
  const found = list.cards.find((c) => c.id === cardId);
  console.log(`✅ 总卡片数: ${list.cards.length}, 测试卡存在: ${found ? "✅" : "❌"}`);

  console.log("\n=== 3. 认领 ===");
  const claimed = await withTimeout(send("workboard.cards.claim", { id: cardId, ownerId: "steward", ttlSeconds: 120 }), 10000, "cards.claim");
  const claimToken = claimed.token;
  console.log(`✅ 认领: ownerId=${claimed.card?.metadata?.claim?.ownerId}, ttl=${claimed.card?.metadata?.claim?.expiresAt ? Math.round((claimed.card.metadata.claim.expiresAt - Date.now())/1000)+"s" : "?"}`);

  console.log("\n=== 4. 评论 ===");
  await withTimeout(send("workboard.cards.comment", { id: cardId, body: "👋 烟测评论：建卡后已认领" }), 10000, "cards.comment");
  console.log(`✅ 评论成功`);

  console.log("\n=== 5. 续约 ===");
  const beat = await withTimeout(send("workboard.cards.heartbeat", { id: cardId, ownerId: "steward", token: claimToken, note: "烟测心跳 #1" }), 10000, "cards.heartbeat");
  console.log(`✅ 续约: status=${beat.status}, lastHeartbeatAt=${beat.metadata?.claim?.lastHeartbeatAt ? new Date(beat.metadata.claim.lastHeartbeatAt).toISOString() : "?"}`);

  console.log("\n=== 6. 释放 ===");
  const released = await withTimeout(send("workboard.cards.release", { id: cardId, ownerId: "steward", token: claimToken, status: "done" }), 10000, "cards.release");
  console.log(`✅ 释放: 新状态=${released.status}, claim=${released.metadata?.claim ? "仍存在" : "已清空"}`);

  console.log("\n=== 7. 归档（跳过，保留供查看）===");
  console.log(`⏭️  卡片保留在 status=done 状态供 Dashboard 查看`);

  console.log("\n=== 🎉 烟测全链路通过 ===");
  console.log(`卡片 ID: ${cardId}`);
  console.log(`Dashboard: http://10.0.0.9:18098/estqvr/  →  Workboard`);
  ws.close();
  process.exit(0);
}

main().catch((e) => { console.error("❌ 烟测失败:", e.message); process.exit(1); });
