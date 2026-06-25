const endpoint = process.argv[2];
let expression = process.argv.slice(3).join(" ");

if (process.argv[3] === "--file") {
  expression = (await import("node:fs")).readFileSync(process.argv[4], "utf8");
}

if (!endpoint || !expression) {
  console.error("Usage: node antigravity-devtools-eval.mjs <ws-url> <js-expression>");
  process.exit(2);
}

console.error(`Evaluating expression: ${JSON.stringify(expression)}`);

let id = 0;
const pending = new Map();
const ws = new WebSocket(endpoint);

ws.addEventListener("open", () => {
  send("Runtime.enable");
  send("Runtime.evaluate", {
    expression,
    awaitPromise: true,
    returnByValue: true,
  });
});

ws.addEventListener("message", (event) => {
  const message = JSON.parse(event.data);
  if (!message.id) return;
  const resolve = pending.get(message.id);
  if (!resolve) return;
  pending.delete(message.id);
  resolve(message);
});

ws.addEventListener("error", (error) => {
  console.error(error);
  process.exit(1);
});

function send(method, params = {}) {
  const messageId = ++id;
  ws.send(JSON.stringify({ id: messageId, method, params }));
  pending.set(messageId, (response) => {
    if (method !== "Runtime.evaluate") return;
    console.log(JSON.stringify(response.result?.result?.value ?? response, null, 2));
    ws.close();
  });
}
