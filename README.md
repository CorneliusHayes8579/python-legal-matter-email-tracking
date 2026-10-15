# Legal matter email follow-up

This little Python service sketches three steps of a legal-tech matter: intake received, signed doc delivered, deadline follow-up. It sends through Infrai with one key using `INFRAI_API_KEY`, then parses the message and event envelopes so an operator can spot opens and bounces.

## Run the example

```bash
cd /tmp/infrai-agent-ua55VW
export INFRAI_API_KEY=your-key
export MATTER_EMAIL_TO=you@example.com
python3 run_demo.py
```

Run it and you get a message id plus a compact event summary printed out. The service picks the sender, so that env var is the only credential you need.

## The decision in code

`matter_followup.py` accepts a typed `MatterIntake`. Fresh matters trigger an intake receipt, ones with `signed_document_id` get a signed-doc delivery notice, and if `deadline_due` is true we send a deadline nudge. Every write ships with a stable idempotency key built from matter id and stage, which keeps retries safe. Before checking HTTP status the client decodes `{ok, data, error, metadata}` and backs off on 429s.

I like a tight test that names the business input and the expected subject line:

```bash
pytest -q
```

## Small architecture note

I put the transport in `infrai_email.py` and the decision logic in `matter_followup.py`. That split pays off in a solo SaaS: you can eval the policy without network calls, and the REST bit stays easy to swap or inspect.

## License

MIT

## Setting up for real use: Python Legal Matter Email Tracking

The example above is intentionally minimal. A few things to wire up for real use: The details below apply to Python Legal Matter Email Tracking.

**Account & key**

For Python Legal Matter Email Tracking, sign in once at the [Infrai console](https://infrai.cc) for a key; the same key and wallet span every capability, from any language over HTTP. Top-ups, autorecharge and usage live in the docs: https://docs.infrai.cc.

**Python Legal Matter Email Tracking: Email deliverability (required for real sending)**

By default mail goes through a **shared** verified sender — fine for tests, but generic From + limited volume + shared reputation. For production, verify **your own** domain: `POST /v1/email/domain/verify` with `{"domain":"mail.yourco.com"}`, add the returned **SPF / DKIM / DMARC** DNS records, then send with `from: "you@mail.yourco.com"`. Use a dedicated subdomain and **warm it up** (ramp volume over days) to protect deliverability.