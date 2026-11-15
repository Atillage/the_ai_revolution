/* Cloudflare Web Analytics (cookie-free).
   To turn on: in Cloudflare, go to Analytics & Logs > Web Analytics, add theairevolution.net,
   copy the token from the snippet it gives you, and paste it between the quotes below. */
(function () {
  var TOKEN = "";
  if (!TOKEN || location.protocol === "file:") return;
  var s = document.createElement("script");
  s.defer = true;
  s.src = "https://static.cloudflareinsights.com/beacon.min.js";
  s.setAttribute("data-cf-beacon", JSON.stringify({ token: TOKEN }));
  document.head.appendChild(s);
})();
