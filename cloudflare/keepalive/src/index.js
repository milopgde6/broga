async function ping(url) {
  try {
    const res = await fetch(url, { method: "GET", cf: { cacheTtl: 0 } });
    return res.status;
  } catch (err) {
    return `error: ${err}`;
  }
}

export default {
  async scheduled(_controller, env, ctx) {
    ctx.waitUntil(ping(env.TARGET_URL));
  },

  async fetch(_request, env) {
    const status = await ping(env.TARGET_URL);
    return new Response(`keepalive ${env.TARGET_URL} -> ${status}\n`, {
      status: 200,
      headers: { "content-type": "text/plain" },
    });
  },
};
