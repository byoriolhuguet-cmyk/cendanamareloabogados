// Formulario de contacto: función serverless de Vercel.
// Envía la consulta por correo mediante Resend (https://resend.com).
// Variables de entorno en Vercel (Settings > Environment Variables):
//   RESEND_API_KEY  clave de la API de Resend (obligatoria para enviar)
//   CONTACT_TO      destino (por defecto despacho@cendanamareloabogados.com)
//   CONTACT_FROM    remitente verificado en Resend (por defecto "Web Cendán & Amarelo <onboarding@resend.dev>")
// Sin RESEND_API_KEY responde 503 y la web abre el correo del usuario como alternativa.

const clean = (v, max) => String(v || '').replace(/[\r\n]+/g, ' ').trim().slice(0, max);
const esc = (s) => s.replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

export default async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).json({ ok: false });
  const key = process.env.RESEND_API_KEY;
  if (!key) return res.status(503).json({ ok: false, error: 'not-configured' });

  const b = typeof req.body === 'string' ? JSON.parse(req.body || '{}') : (req.body || {});
  if (b.web) return res.status(200).json({ ok: true });            // trampa anti-spam
  const nombre = clean(b.nombre, 120), telefono = clean(b.telefono, 40), email = clean(b.email, 160);
  const area = clean(b.area, 80), mensaje = String(b.mensaje || '').trim().slice(0, 4000);
  if (!nombre || telefono.replace(/\D/g, '').length < 9 || !mensaje || !b.privacidad) {
    return res.status(400).json({ ok: false, error: 'invalid' });
  }

  const html = `<h2>Nueva consulta desde la web</h2>
<p><b>Nombre:</b> ${esc(nombre)}<br><b>Teléfono:</b> ${esc(telefono)}<br><b>Email:</b> ${esc(email || '-')}<br><b>Área:</b> ${esc(area || '-')}<br>
<b>Acepta comunicaciones:</b> ${b.comunicaciones ? 'sí' : 'no'}</p><p>${esc(mensaje).replace(/\n/g, '<br>')}</p>`;
  const r = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: { Authorization: `Bearer ${key}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({
      from: process.env.CONTACT_FROM || 'Web Cendán & Amarelo <onboarding@resend.dev>',
      to: [process.env.CONTACT_TO || 'despacho@cendanamareloabogados.com'],
      reply_to: email || undefined,
      subject: `Consulta web: ${nombre}${area ? ` (${area})` : ''}`,
      html,
    }),
  });
  return r.ok ? res.status(200).json({ ok: true }) : res.status(502).json({ ok: false });
}
